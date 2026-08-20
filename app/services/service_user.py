from app.schemas.dto import RegisterDTO, LoginDTO, TokenPair
from app.schemas.token import TokenData
from app.services.security import password_hashing, verify_password
from fastapi.concurrency import run_in_threadpool
from app.repository import Repository
from app.services.security import generate_access_token, verify_token, generate_refresh_token, hash_refresh_token
from app.services.exception import UserAlreadyExistsEmailError, UserNotFound
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, repository : Repository):
        self.repository = repository

    async def get_user_by_email(self, email):
        user = await self.repository.user_exists_email(email=email)
        if not user:
            raise UserNotFound
        return user

    async def registration(self, user_dto : RegisterDTO):
        password_hash = await run_in_threadpool(
                        password_hashing, user_dto.password
                        )
        refresh_token = generate_refresh_token()
        hash_refresh = await run_in_threadpool(
                        hash_refresh_token, refresh_token
                        )
        user = user_dto.model_dump()
        user.pop('password')
        user['hash_password'] = password_hash
        user['refresh_token'] = hash_refresh
       
        
        async with self.repository.session.begin():
            user_from_db = await self.repository.add_user_for_db(user)
            if not user_from_db:
                raise UserAlreadyExistsEmailError
        user_data = RegisterDTO.model_validate(user_from_db)
        access_token = generate_access_token( data={"sub" : str(user_data.id)})
        return {'data' : user_data,
                'access_token' : access_token,
                'refresh_token': refresh_token}
        



    async def login(self, user_dto : LoginDTO) -> TokenPair | False:
        result = await self.repository.get_user(user_dto.email)
        if not result:
            return False
        

        verify = await run_in_threadpool(verify_password, result.hash_password, user_dto.password)

        if not verify:
            return False
        
        access_token = generate_access_token( data={"sub" : str(result.id)})
        refresh_token = generate_refresh_token()
        hash_refresh = await run_in_threadpool(hash_refresh_token, refresh_token)
        await self.repository.update_token(hash_refresh, result.id)
        await self.repository.commit()
        
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token
                )

    async def verify_user(self, token : str) -> int:
        user_id = verify_token(token)
        if not user_id:
            raise UserNotFound
        user_exists = await self.repository.user_exists_id(id=int(user_id))
        if not user_exists:
            raise UserNotFound
        return user_id
       
    async def refresh(self, token : str) -> TokenPair | None:
        refresh_hash = await run_in_threadpool(hash_refresh_token, token)
        try:
            async with self.repository.session.begin():

                user_id = await self.repository.user_refresh(refresh_hash)
                if user_id:
                    new_access_token = generate_access_token( data={"sub" : user_id})
                    new_refresh_token = generate_refresh_token()
                    new_refresh_hash = await run_in_threadpool(hash_refresh_token, new_refresh_token)
                    await self.repository.update_token(new_refresh_hash, user_id)
                    return TokenPair(access_token=new_access_token,
                                    refresh_token=new_refresh_token)
                
        except Exception:
            logger.exception("Ошибка при обновление refresh_token пользователя")
        return None
    
    async def delete_refresh(self, token : str) -> bool:
        id_user = await run_in_threadpool(verify_token, token)
        status = await self.repository.delete_refresh_db(id_user)
        return status
