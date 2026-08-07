from pydantic import BaseModel, EmailStr, HttpUrl, ConfigDict

class RegisterDTO(BaseModel):
    username : str
    email : EmailStr
    password : str


class LoginDTO(BaseModel):
    email : EmailStr
    password : str


class TokenPair(BaseModel):
    access_token : str
    refresh_token : str

class ProductDTO(BaseModel):
    name : str 
    description : str 
    price : float
    img_url : str 

    model_config = ConfigDict(from_attributes=True)

class ProductBasketDTO(BaseModel):
    user_id : int 
    product_id : int 
    quantity : int

    model_config = ConfigDict(from_attributes=True)