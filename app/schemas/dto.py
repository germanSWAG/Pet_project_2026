from pydantic import BaseModel, EmailStr, HttpUrl, ConfigDict, UUID4

class CreatUserDTO(BaseModel):
    username : str
    email : EmailStr
    password : str
    username_telegram : str = None

class InternalDTO(BaseModel):
    username : str
    email : EmailStr
    hash_password : str
    is_active : bool = True
    hash_refresh_token : str
    username_telegram : str = None



   

class UserOutDTO(BaseModel):
    id : int
    username : str
    email : EmailStr
    model_config = ConfigDict(from_attributes=True)


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