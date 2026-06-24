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
        decode_token = await run_in_threadpool(verify_token, token)
        id = decode_token.get("sub")
        if not id:
            return None
        
        is_active = await self.repository.user_exists_id(id=id)
        if is_active:
            user = TokenData(id_user=decode_token.get("sub")
                    )
            
            return user
        
        return None
       
    async def refresh(self, token : str) -> str:
        refresh_hash = await run_in_threadpool(hash_refresh_token, token)
        id_user = await self.refresh(refresh_hash)
        if refresh_hash == id_user:
            access_token = await run_in_threadpool(generate_access_token, data={"sub" : id_user})
            refresh_token = await run_in_threadpool(generate_refresh_token)
            
            return TokenPair(access_token=access_token,
                             refresh_token=refresh_token)


      

    

        

