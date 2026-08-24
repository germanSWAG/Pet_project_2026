from app.schemas.dto import LoginDTO, TokenPair, CreatUserDTO, UserOutDTO, InternalDTO
from app.schemas.token import TokenData
from app.services.security import password_hashing, verify_password
from fastapi.concurrency import run_in_threadpool
from app.repository import Repository
from app.services.security import generate_access_token, verify_token, generate_refresh_token, hashing_token
from app.services.exception import UserAlreadyExistsEmailError, UserNotFound, UserNotFoundPassword, TokenError
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

    async def registration(self, user_dto : CreatUserDTO):
        hash_password = await run_in_threadpool(
                        password_hashing, user_dto.password
                        )
        refresh_token = generate_refresh_token()
        hash_refresh_token = hashing_token(refresh_token)
                        
        internal_dto = InternalDTO(
            **user_dto.model_dump(exclude={"password"}),
            hash_password=hash_password,
            hash_refresh_token=hash_refresh_token
        )
        user_from_db = await self.repository.create_user_for_db(internal_dto.model_dump())

        user_data = UserOutDTO.model_validate(user_from_db)
        access_token = generate_access_token( data={"sub" : str(user_data.id)})
        return {'data' : user_data,
                'refresh_token' : refresh_token,
                'access_token' : access_token}
        

    async def login(self, user_dto : LoginDTO) -> TokenPair | False:
        result = await self.repository.get_user_by_email(user_dto.email)
        if not result:
            raise UserNotFound
            
        await run_in_threadpool(verify_password, result.hash_password, user_dto.password)
            
        access_token = generate_access_token( data={"sub" : str(result.id)})
        refresh_token = generate_refresh_token()
        hash_refresh_token = hashing_token(refresh_token)
        await self.repository.update_token(hash_refresh_token, result.id)
            
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
        refresh_hash = hashing_token(token)
        user_id = await self.repository.user_refresh(refresh_hash)
        if user_id:
            new_access_token = generate_access_token( data={"sub" : user_id})
            new_refresh_token = generate_refresh_token()
            new_refresh_hash = hashing_token(new_refresh_token)
            await self.repository.update_token(new_refresh_hash, user_id)
            await self.repository.session.commit()
            return TokenPair(access_token=new_access_token,
                                    refresh_token=new_refresh_token)
    async def get_user_profile(self, user_id : int):
        user = await self.repository.get_user_by_id(user_id)
        return UserOutDTO.model_validate(user)
                
    
    async def delete_refresh(self, user_id : int) -> None:
        await self.repository.delete_refresh_db(user_id)
        await self.repository.session.commit()
          
