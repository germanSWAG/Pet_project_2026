from pydantic import BaseModel, HttpUrl


class CarsData(BaseModel):
    brand : str
    model : str 
    year : int
    price : int
    city : str
    href : HttpUrl

class CarsListData(BaseModel):
    data : list[CarsData]
