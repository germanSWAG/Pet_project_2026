from pydantic import BaseModel, ConfigDict

class Product(BaseModel):
    name : str 
    description : str 
    price : float 
    img_url : str 

    model_config = ConfigDict(from_attributes=True)
