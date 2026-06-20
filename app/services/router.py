from fastapi import APIRouter, Depends, HTTPException
from app.services.dependencies import get_auth_service, get_repository
from app.schemas.user import UserAdd, UserGet
from app.schemas.dto import RegisterDTO, LoginDTO, ItemsDTO
from app.schemas.token import Token
from app.services.service_user import AuthService
from app.repository import Repository
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated



router = APIRouter(prefix="/services", tags=["Работа с эндпоинтами"])

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/services/login")

@router.post("/register")
async def registration(user: UserAdd, auth : AuthService = Depends(get_auth_service)):
    user_dto = RegisterDTO(username=user.username, email=user.email, hash_password=user.hash_password)
    result = await auth.registration(user_dto=user_dto)
    if not result:
        raise HTTPException(status_code=409, detail="Такой пользователь уже есть!")
    return result

@router.post("/login")
async def login(auth : AuthService = Depends(get_auth_service), 
                form_data : OAuth2PasswordRequestForm = Depends()):
    user_dto = LoginDTO(email=form_data.username, hash_password=form_data.password)
    result = await auth.login(user_dto=user_dto)
    if not result:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль!")
    return {"access_token" : result,
            "token_type" : "bearer"}


@router.get("/profile")
async def profile(token : Annotated[str,Depends(oauth2_schema)], auth : AuthService = Depends(get_auth_service)):
    result = await auth.verify_user(token)
    if not result:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    return result.model_dump()



@router.post("/items")
async def items(items : ItemsDTO, db : Repository = Depends(get_repository)):
    
    
    