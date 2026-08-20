from fastapi import APIRouter, Depends, HTTPException, Response, Request, Query
from app.services.dependencies import get_auth_service, get_repository, get_products_service
from app.schemas.user import UserAdd
from app.schemas.product import Product
from app.schemas.dto import RegisterDTO, LoginDTO, TokenPair, ProductBasketDTO
from app.services.service_user import AuthService
from app.services.service_products import Products
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.exception import UserAlreadyExistsEmailError
from typing import Annotated



router = APIRouter(prefix="/services", tags=["Работа с эндпоинтами"])

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/services/login")


async def verify_jwt_token(token : Annotated[str, Depends(oauth2_schema)], auth_service : AuthService = Depends(get_auth_service)):
    user_id_by_token = await auth_service.verify_user(token=token)
    if not user_id_by_token:
        raise 
    return user_id_by_token

@router.post("/register")
async def registration(user: UserAdd, auth : AuthService = Depends(get_auth_service)):
    user = auth.get_user_by_email(user.email)
    if user:
        raise HTTPException(status_code=409, detail="Пользователь с таким email уже существует")
    user_dto = RegisterDTO(username=user.username, email=user.email, password=user.password)
    result = await auth.registration(user_dto=user_dto)
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
    user_id = await verify_jwt_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован")
    return {"user_id" : user_id}



    
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



@router.post("/add_product")
async def add_product(token : Annotated[str, Depends(oauth2_schema)], product : Product, auth_service : AuthService = Depends(get_auth_service), product_service : Products = Depends(get_products_service)):

    result = await product_service.add_product(product)
    if not result:
        raise HTTPException(status_code=400, detail='Ошибка при добавление')
    return {
        "status_code" : 200,
        "Data" : result
    }


@router.get("/get_product")
async def get_product(id_product : int, service_products : Products = Depends(get_products_service)):
    result = await service_products.get_product(id_product)
    if not result:
        raise HTTPException(status_code=404, detail="Такого продукта не существует")
    return result


@router.get("/get_products")
async def get_all_product(page : int = 1, page_size : int = 20, service_products : Products = Depends(get_products_service)):
    result = await service_products.get_all_products(page, page_size)
    return {"data" : 
            result}

@router.post("/basket")
async def cart_user(token : Annotated[str, Depends(oauth2_schema)], product: ProductBasketDTO, auth_service : AuthService = Depends(get_auth_service), service_products: Products = Depends(get_products_service)):
    user_is_verify = auth_service.verify_user(auth_service)
    result = await service_products.add_product_for_basket(product)
    # data = result.model_dump()
    return {'data' : [result]}
