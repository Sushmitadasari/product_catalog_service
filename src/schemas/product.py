from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from src.schemas.category import CategoryResponse

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    sku: str

class ProductCreate(ProductBase):
    category_ids: List[UUID] = []

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    sku: Optional[str] = None
    category_ids: Optional[List[UUID]] = None

class ProductResponse(ProductBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    categories: List[CategoryResponse] = []

    model_config = ConfigDict(from_attributes=True)
