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
async def update_tokens(response : Response,request : Request, auth : AuthService = Depends(get_auth_service)):
    refresh_token = request.cookies.get("refresh_token")
    if refresh_token is None:
        raise HTTPException(
            status_code=401,
            detail="Недействительный или истекший refresh токен"
        )
    tokens = await auth.refresh(refresh_token)
    if not tokens:
        raise HTTPException(status_code=401, detail="Не найден refresh токен")
    
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
    

@router.post("/logout")
async def logout(response : Response, token : Annotated[str, Depends(oauth2_schema)], auth : AuthService = Depends(get_auth_service)):
    response.delete_cookie("refresh_token")
    status = await auth.delete_refresh(token)
    if not status:
        raise HTTPException(status_code=400, detail="Ошибка при выполнение выхода")
    
    return {"Status" : "Пользователь вышел из записи"}


