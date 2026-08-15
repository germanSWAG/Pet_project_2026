from app.schemas.dto import RegisterDTO, LoginDTO, TokenPair
from app.schemas.token import TokenData
from app.services.security import password_hashing, verify_password
from fastapi.concurrency import run_in_threadpool
from app.repository import Repository
from app.services.security import generate_access_token, verify_token, generate_refresh_token, hash_refresh_token
from sqlalchemy.exc import IntegrityError
from app.services.exception import UserAlreadyExistsEmailError
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, repository : Repository):
        self.repository = repository


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
       
        try:
            async with self.repository.session.begin():
                user_data = await self.repository.add_user_for_db(user)
        except IntegrityError as e:
                if "users_email_key" in str(e.orig):
                    logger.warning(f"Ошибка при регистрации пользователя {user_dto.email}")
                    raise UserAlreadyExistsEmailError(email=user_dto.email)
                logger.exception(f"Неизвестная ошибка целостности базы данных")
                raise e
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
