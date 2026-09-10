from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    owner_id: int

    model_config = {
        "from_attributes": True
    }
class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
