from fastapi import APIRouter, Depends, Query
from app.services.dependencies import get_admin_panel, get_products_service, get_auth_service
from app.services.routers.users import get_current_user
from app.services.admin_service import AdminPanel
from app.schemas.dto import RecordsUsers, RecordDataSchema
from app.schemas.product import Product
from app.services.service_products import Products
from typing import Annotated



async def verify_admin(user_id : Annotated[int, Depends(get_current_user)], admin_panel : AdminPanel = Depends(get_admin_panel)):
    status = await admin_panel.verify_admin(user_id)
    return status


router = APIRouter(prefix="/admin", tags=["Admin dashboard"],
                   dependencies=[Depends(verify_admin)])



@router.get("/all_users", response_model=RecordDataSchema)
async def all_users(page : int = Query(default=1, ge=1, description="Номер страницы"), 
                    page_size : int = Query(default=20, ge=1, le=100, description="Размер страницы"), 
                    admin_panel : AdminPanel = Depends(get_admin_panel)):
    result = await admin_panel.get_all_users(page, page_size)
    return result



@router.post("/add_product")
async def add_product(product : Product, product_service : Products = Depends(get_products_service)):
    result = await product_service.add_product_service(product)
    return result


@router.get("/get_user", response_model=RecordsUsers)
async def get_user_admin(user_id : int, admin_panel : AdminPanel = Depends(get_admin_panel)):
    user = await admin_panel.get_user_admin_service(user_id)
    return user