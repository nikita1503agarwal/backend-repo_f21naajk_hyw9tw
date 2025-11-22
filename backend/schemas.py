from pydantic import BaseModel, Field, HttpUrl
from typing import Optional

# Each Pydantic model maps to a MongoDB collection: class name lowercased

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., ge=0)
    image: Optional[HttpUrl] = None
    category: Optional[str] = Field(None, max_length=60)
    in_stock: bool = True

class Subscriber(BaseModel):
    email: str

class Message(BaseModel):
    name: str
    email: str
    message: str = Field(..., max_length=2000)
