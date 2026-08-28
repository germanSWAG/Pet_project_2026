from fastapi import APIRouter, Depends, HTTPException, Response, Request
from app.services.dependencies import get_auth_service
from app.schemas.user import UserAdd, UserOut
from app.schemas.dto import LoginDTO
from app.services.service_user import AuthService
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated



router = APIRouter(prefix="/users", tags=["User services"])

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/users/login")



async def get_current_user(
        token : Annotated[str, Depends(oauth2_schema)],
        auth_service : AuthService = Depends(get_auth_service)
        ):
    user_id = await auth_service.verify_user(token=token)
    return user_id


@router.post("/register", response_model=UserOut)
async def registration(response : Response, user: UserAdd, auth : AuthService = Depends(get_auth_service)):
    result = await auth.registration(user)
    response.set_cookie(
         key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age= 60 * 60 * 24 * 30
    )
    return UserOut.model_validate(result['data'])

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
async def profile(user_id : Annotated[int, Depends(get_current_user)], auth_service : AuthService = Depends(get_auth_service)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    user_data = await auth_service.get_user_profile(user_id)
    return {"data" : user_data}



@router.post("/token")
async def update_tokens(response : Response, request : Request, auth : AuthService = Depends(get_auth_service)):
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
async def logout(response : Response, user_id : Annotated[int, Depends(get_current_user)], auth : AuthService = Depends(get_auth_service)):
    response.delete_cookie("refresh_token")
    await auth.delete_refresh(user_id)
    return {"Status" : "Пользователь вышел из записи"}



