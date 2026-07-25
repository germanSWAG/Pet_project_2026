from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    name : str 
    description : str 
    price : float 
    id : int | None = None
    img_url : str 

    model_config = ConfigDict(from_attributes=True)
