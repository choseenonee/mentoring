from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["Laptop"])
    price: float = Field(gt=0, examples=[999.99])
    in_stock: bool = True


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: float | None = Field(default=None, gt=0)
    in_stock: bool | None = None


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

    class Config:
        from_attributes = True  # позволяет отдавать ORM-объекты напрямую
