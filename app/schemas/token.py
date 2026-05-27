from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token : str 
    token_type : str | None = None


class TokenData(BaseModel):
    id_user: str | None = None
    email : str | None = None
    model_config = ConfigDict(from_attributes=True)