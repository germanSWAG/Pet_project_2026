from app.repository import Repository
from app.schemas.dto import ProductDTO, ProductBasketDTO
from app.services.exception import ProductNotFound


class Products():
    def __init__(self, repository : Repository):
        self.repository = repository

    

    async def get_product(self, id : int):
        product = await self.repository.get_product_db(id)
        return ProductDTO.model_validate(product)
    
    async def get_all_products_service(self, page : int, page_size: int):
        offset = (page - 1) * page_size
        products = await self.repository.get_all_products_db(offset=offset, page_size=page_size)
        if not products:
            raise ProductNotFound
        return products

    async def add_product_for_basket(self, product : ProductBasketDTO, user_id : int):
        result = await self.repository.add_basket(
                user_id= user_id,
                product_id= product.product_id,
                count= product.quantity)
        
        if result is None:
            return None
        return ProductBasketDTO.model_validate(result)


    async def add_product_service(self, product : ProductDTO) -> dict:
        result = await self.repository.add_product_db(product.model_dump())
        return result
    