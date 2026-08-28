from pydantic import BaseModel, EmailStr, ConfigDict, Field

class CreatUserDTO(BaseModel):
    username : str
    email : EmailStr
    password : str
    username_telegram : str | None

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
    product_id : int 
    quantity : int = Field(gt=0, description="Число должно быть больше 0")

    model_config = ConfigDict(from_attributes=True)


class RecordsUsers(BaseModel):
    id : int
    username : str
    email : EmailStr
    is_active : bool
    is_admin : bool
    username_telegram : str | None = None
    
    model_config = ConfigDict(from_attributes=True)

class RecordDataSchema(BaseModel):
    total : int
    users : list[RecordsUsers]


