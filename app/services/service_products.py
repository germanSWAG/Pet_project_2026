from app.repository import Repository
from app.schemas.dto import ProductDTO, ProductBasketDTO


class Products():
    def __init__(self, repository : Repository):
        self.repository = repository

    

    async def get_product(self, id : int):
        product = await self.repository.get_product_db(id)
        return ProductDTO.model_validate(product)
    
    async def get_all_products(self, page : int, page_size: int):
        offset = (page - 1) * page_size
        products = await self.repository.get_all_products_db(offset, page_size)
        if not products:
            return None
        return products

    async def add_product_for_basket(self, product : ProductBasketDTO):
        result = await self.repository.add_basket(
                user_id= product.user_id,
                product_id= product.product_id,
                count= product.quantity)
        
        if result is None:
            return None
        return ProductBasketDTO.model_validate(result)


    async def add_product_service(self, product : ProductDTO):
        result = await self.repository.add_product_db(product.model_dump())
        return result
    