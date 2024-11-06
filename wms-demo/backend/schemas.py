# schemas.py

from pydantic import BaseModel
from typing import Optional
from typing import List

class OrderItemCreate(BaseModel):
    product_id: str
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]

class StockAdjustment(BaseModel):
    quantity: int
    container_code: Optional[str] = None