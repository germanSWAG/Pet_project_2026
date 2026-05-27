from app.schemas.dto import RegisterDTO, LoginDTO
from app.schemas.user import UserOut
from app.schemas.token import TokenData
from app.services.security import hash_password, verify_password
from fastapi.concurrency import run_in_threadpool
from app.repository import Repository
from app.services.security import create_token, verify_token


class AuthService:
    def __init__(self, repository : Repository):
        self.repository = repository


    async def registration(self, user_dto : RegisterDTO):
        hashed_password = await run_in_threadpool(hash_password, user_dto.hash_password)
        result = await self.repository.check_user(user_dto.email)
        if result:
            return None
        user_dict = user_dto.model_dump()
        user_dict["hash_password"] = hashed_password
        return await self.repository.add_user(user_dict)



    async def login(self, user_dto : LoginDTO) -> str | None:
        result = await self.repository.get_user(user_dto.email)
        if not result:
            return None
        

        verify = await run_in_threadpool(verify_password, result.hash_password, user_dto.hash_password)

        if not verify:
            return None 
        
        token = await run_in_threadpool(create_token, data={"sub" : str(result.id), 
                                          "email" : result.email})
        return token
        
    async def verify_user(self, token : str) -> TokenData | None:
        decode_token = await run_in_threadpool(verify_token, token)
        user_email = decode_token.get("email")
        if not user_email:
            return None
        
        is_active = await self.repository.check_user(user_email)
        if is_active:
            user = TokenData(id_user=decode_token.get("sub"), 
                            email=decode_token.get("email"))
            return user
        print("ошибка")
        return None
       
        


    

        

