from fastapi import APIRouter, Depends, HTTPException, Response, Request, Query
from app.services.dependencies import get_auth_service, get_repository, get_products_service
from app.schemas.user import UserAdd
from app.schemas.product import Product
from app.schemas.dto import LoginDTO, TokenPair, ProductBasketDTO
from app.services.routers.users import oauth2_schema
from app.services.service_user import AuthService
from app.services.service_products import Products
from app.services.routers.admin import verify_admin
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.services.exception import UserAlreadyExistsEmailError
from typing import Annotated



router = APIRouter(prefix="/products", tags=["Рroducts service"])






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
    user_is_verify = await auth_service.verify_user(token)
    result = await service_products.add_product_for_basket(product)
    return {'data' : [result]}
