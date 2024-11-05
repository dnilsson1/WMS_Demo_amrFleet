from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum
from datetime import datetime

class IPConfig(BaseModel):
    ip: str
    port: str

class ContainerType(str, Enum):
    RACK = "RACK"
    BIN = "BIN"
    BUCKET = "BUCKET"

class EmptyStatus(str, Enum):
    EMPTY = "EMPTY"
    FULL = "FULL"

class Product(BaseModel):
    id: str
    name: str
    sku: str
    description: Optional[str] = None
    unit: str = "pcs"  # pieces, kg, liters, etc.
    minimum_stock: int = 0
    current_stock: int = 0

class InventoryMovement(BaseModel):
    product_id: str
    quantity: int
    container_code: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.now)
    movement_type: str  # "in" or "out"
    reference: Optional[str] = None  # order_id or other reference

class Container(BaseModel):
    containerCode: str
    containerType: Optional[ContainerType] = None
    position: str
    emptyStatus: EmptyStatus = EmptyStatus.EMPTY
    contents: Dict[str, int] = {}  # product_id -> quantity

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    picked_quantity: int = 0

class Order(BaseModel):
    orderId: str
    items: List[OrderItem]
    status: str = "pending"  # pending, picking, completed
    assignedContainer: Optional[str] = None