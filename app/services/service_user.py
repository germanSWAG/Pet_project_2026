from app.schemas.dto import RegisterDTO, LoginDTO, TokenPair
from app.schemas.token import TokenData
from app.services.security import hash_password, verify_password
from fastapi.concurrency import run_in_threadpool
from app.repository import Repository
from app.services.security import generate_access_token, verify_token, generate_refresh_token, hash_refresh_token


class AuthService:
    def __init__(self, repository : Repository):
        self.repository = repository


    async def registration(self, user_dto : RegisterDTO):
        result = await self.repository.user_exists_email(user_dto.email)
        
        if result:
            return None
        
        password_hash = await run_in_threadpool(hash_password, user_dto.password)
        return await self.repository.add_user({"username" : user_dto.username,
                                               "email" : user_dto.email,
                                               "hash_password" : password_hash})



    async def login(self, user_dto : LoginDTO) -> TokenPair | False:
        result = await self.repository.get_user(user_dto.email)
        if not result:
            return False
        

        verify = await run_in_threadpool(verify_password, result.hash_password, user_dto.password)

        if not verify:
            return False
        
        access_token = await run_in_threadpool(generate_access_token, data={"sub" : str(result.id)})
        refresh_token = await run_in_threadpool(generate_refresh_token)
        hash_refresh = await run_in_threadpool(hash_refresh_token, refresh_token)
        await self.repository.add_token(hash_refresh, result.id)
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token
                )

    async def verify_user(self, token : str) -> TokenData | None:
        user_id = await run_in_threadpool(verify_token, token)
        
        if not user_id:
            return None
        
        is_active = await self.repository.user_exists_id(id=int(user_id))
        if is_active:
            user = TokenData(id_user=user_id
                    )
            
            return user
        
        return None
       
    async def refresh(self, token : str) -> TokenPair | None:
        refresh_hash = await run_in_threadpool(hash_refresh_token, token)
        user_id = await self.repository.user_refresh(refresh_hash)
        if user_id:
            access_token = await run_in_threadpool(generate_access_token, data={"sub" : user_id})
            refresh_token = await run_in_threadpool(generate_refresh_token)
            new_refresh_hash = await run_in_threadpool(hash_refresh_token, refresh_token)
            await self.repository.add_token(new_refresh_hash, user_id)
            return TokenPair(access_token=access_token,
                             refresh_token=refresh_token)
        return None
    
    async def delete_refresh(self, token : str) -> bool:
        id_user = await run_in_threadpool(verify_token, token)
        status = await self.repository.delete_refresh_db(id_user)
        return status
