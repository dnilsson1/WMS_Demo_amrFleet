# models.py

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict, TYPE_CHECKING
from enum import Enum
from datetime import datetime
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import JSON

if TYPE_CHECKING:
    from typing import TYPE_CHECKING

class IPConfig(SQLModel, table=True):
    ip: str = Field(primary_key=True)
    port: str

class ContainerType(str, Enum):
    RACK = "Rack"
    BRACKET = "Bracket"


class EmptyStatus(str, Enum):
    EMPTY = "EMPTY"
    FULL = "FULL"

class SKUCounter(SQLModel, table=True):
    id: int = Field(default=1, primary_key=True)
    last_sku: int = Field(default=1000)
class Product(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    sku: Optional[str] = Field(default=None, index=True, unique=True)
    description: Optional[str] = None
    unit: Optional[str] = "pcs"
    minimum_stock: int = 0
    current_stock: int = 0

    # Relationship to OrderItem
    order_items: List["OrderItem"] = Relationship(back_populates="product")

class InventoryMovement(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    product_id: str = Field(foreign_key="product.id")
    quantity: int
    container_code: Optional[str]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    movement_type: str  # "in" or "out"
    reference: Optional[str] = None
    
class Container(SQLModel, table=True):
    containerCode: str = Field(primary_key=True)
    containerType: str  # or Enum if you have one
    position: str
    emptyStatus: str = "EMPTY"  # Or use Enum if applicable
    containerModelCode: Optional[str] = None
    enterOrientation: Optional[str] = None  # Add this field
    contents: Optional[dict] = None  # Assuming contents is a dictionary


class Order(SQLModel, table=True):
    orderId: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    status: str = "pending"
    assignedContainers: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON)
    )

    # Relationship to OrderItem
    items: List["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    order_id: str = Field(foreign_key="order.orderId")
    product_id: str = Field(foreign_key="product.id")
    quantity: int
    picked_quantity: int = 0

    # Relationships
    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="order_items")

class Point(SQLModel, table=True):
    name: str = Field(primary_key=True)  # Original name from fleet manager
    position: str  # Same as name
    wms_name: Optional[str] = None  # Renamed point name in WMS system




