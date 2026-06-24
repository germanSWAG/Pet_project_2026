from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.services.dependencies import get_auth_service, get_repository
from app.schemas.user import UserAdd
from app.schemas.dto import RegisterDTO, LoginDTO, ItemsDTO, TokenPair
from app.services.service_user import AuthService
from app.repository import Repository
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated



router = APIRouter(prefix="/services", tags=["Работа с эндпоинтами"])

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/services/login")

@router.post("/register")
async def registration(user: UserAdd, auth : AuthService = Depends(get_auth_service)):
    user_dto = RegisterDTO(username=user.username, email=user.email, password=user.password)
    result = await auth.registration(user_dto=user_dto)
    if not result:
        raise HTTPException(status_code=409, detail="Такой пользователь уже есть!")
    return result

@router.post("/login")
async def login(response : Response, auth : AuthService = Depends(get_auth_service), 
                form_data : OAuth2PasswordRequestForm = Depends()):
    
    user_dto = LoginDTO(email=form_data.username, password=form_data.password)
    tokens = await auth.login(user_dto=user_dto)

    if not tokens:

        raise HTTPException(status_code=401, detail="Неверный логин или пароль!")
    
    response.set_cookie(
    key="refresh_token",
    value=tokens.refresh_token,
    httponly=True,
    secure=False,
    samesite="lax",
    max_age= 60 * 60 * 24 * 30
    )

    return {"access_token" : tokens.access_token,
            "token_type" : "bearer"}


@router.get("/profile")
async def profile(token : Annotated[str, Depends(oauth2_schema)], auth : AuthService = Depends(get_auth_service)):
    result = await auth.verify_user(token)
    if not result:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    return result.model_dump()


@router.post("/items")
async def items(items : ItemsDTO, db : Repository = Depends(get_repository)):
    pass
    
    
@router.get("/refresh")
async def get_token_refresh(request : Request, auth : AuthService = Depends(get_auth_service)):
    refresh_token = await request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="У пользователя нет токена")
    
    pass