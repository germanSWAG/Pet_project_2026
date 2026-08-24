from fastapi import APIRouter, Depends, HTTPException
from app.services.dependencies import get_admin_panel, get_products_service
from app.services.routers.users import get_current_user
from app.services.admin_service import AdminPanel
from app.schemas.product import Product
from app.services.service_products import Products
from typing import Annotated



async def verify_admin(user_id : Annotated[int, Depends(get_current_user)], admin_panel : AdminPanel = Depends(get_admin_panel)):
    status = await admin_panel.verify_admin(user_id)
    return status


router = APIRouter(prefix="/admin", tags=["Admin dashboard"],
                   dependencies=[Depends(verify_admin)])



@router.get("/all_users")
async def all_users(admin_panel : AdminPanel = Depends(get_admin_panel)):
    result = await admin_panel.get_all_users()
    return result



@router.post("/add_product")
async def add_product(product : Product, product_service : Products = Depends(get_products_service)):
    result = await product_service.add_product_service(product)
    return {
        "status_code" : 200,
        "Data" : result
    }