from fastapi import APIRouter, Depends, HTTPException, Response, Request, Query
from app.services.dependencies import get_auth_service, get_repository, get_products_service
from app.schemas.user import UserAdd
from app.schemas.product import Product
from app.schemas.dto import LoginDTO, TokenPair, ProductBasketDTO
from app.services.routers.users import oauth2_schema
from app.services.service_user import AuthService
from app.services.service_products import Products
from app.services.routers.admin import verify_admin
from app.services.routers.users import get_current_user
from typing import Annotated



router = APIRouter(prefix="/products", tags=["Рroducts service"])






@router.get("/get_product")
async def get_product(id_product : int, service_products : Products = Depends(get_products_service)):
    result = await service_products.get_product(id_product)
    return result


@router.get("/get_all_products")
async def get_all_product(page : int = 1, page_size : int = 20, service_products : Products = Depends(get_products_service)):
    result = await service_products.get_all_products_service(page, page_size)
    return {"data" : 
            result}

@router.post("/add_basket")
async def cart_user(user_id : Annotated[int, Depends(get_current_user)], product: ProductBasketDTO, service_products: Products = Depends(get_products_service)):
    result = await service_products.add_product_for_basket(product, user_id=user_id,)
    return {'data' : [result]}
