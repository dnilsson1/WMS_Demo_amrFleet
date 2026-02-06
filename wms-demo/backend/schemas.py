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

class PickOrderRequest(BaseModel):
    destination_name: str


class PointUpdate(BaseModel):
    position: Optional[str] = None
    wms_name: Optional[str] = None