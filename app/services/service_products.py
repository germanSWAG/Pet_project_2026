from app.repository import Repository
from app.schemas.dto import ProductDTO


class Products():
    def __init__(self, repository : Repository):
        self.repository = repository

    
    async def add_product(self, product : ProductDTO):
        product_data = product.model_dump()
        result = await self.repository.add_product_db(product_data)
        if not result:
            return None
        
        return result

    async def get_product(self, id : int):
        product = await self.repository.get_product_db(id)
        return ProductDTO.model_validate(product)
    
    async def get_all_products(self, page : int, page_size: int):
        products = await self.repository.get_all_products_db()
        if not products:
            return None
        return products
        

    