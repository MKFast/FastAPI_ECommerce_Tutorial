from pydantic.main import BaseModel


class Product(BaseModel):

    title: str
    description: str
    price: int

    class Config:
        orm_mode=True
