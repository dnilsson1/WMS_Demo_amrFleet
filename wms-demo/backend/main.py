# backend/main.py
from fastapi import FastAPI, HTTPException
from typing import List, Optional
import json
import uuid
from datetime import datetime
from models import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

JSON_FILE_PATH = "./data.json"

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (replace with database in production)
products = {}
containers = {}
orders = {}
inventory_movements = []

def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

products = load_data('products.json')
containers = load_data('containers.json')
orders = load_data('orders.json')
inventory_movements = load_data('inventory_movements.json')

def save_data(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
save_data(products, 'products.json')
save_data(containers, 'containers.json')
save_data(orders, 'orders.json')
save_data(inventory_movements, 'inventory_movements.json')

# Product management endpoints
@app.post("/products/", response_model=Product)
async def create_product(product: Product):
    if not product.id:
        product.id = str()
    products[product.id] = product
    return product

@app.get("/products/", response_model=List[Product])
async def list_products():
    return list(products.values())

@app.post("/products/{product_id}/adjust-stock")
async def adjust_stock(product_id: str, quantity: int, container_code: Optional[str] = None):
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = products[product_id]
    product.current_stock += quantity
    
    # Record inventory movement
    movement = InventoryMovement(
        product_id=product_id,
        quantity=quantity,
        container_code=container_code,
        movement_type="in" if quantity > 0 else "out",
        reference="stock_adjustment"
    )
    inventory_movements.append(movement)
    
    # Update container contents if specified
    if container_code:
        if container_code not in containers:
            raise HTTPException(status_code=404, detail="Container not found")
        container = containers[container_code]
        current_qty = container.contents.get(product_id, 0)
        new_qty = current_qty + quantity
        if new_qty > 0:
            container.contents[product_id] = new_qty
        else:
            container.contents.pop(product_id, None)
        
        # Update container empty status
        container.emptyStatus = EmptyStatus.EMPTY if not container.contents else EmptyStatus.FULL
    
    return {"success": True, "new_stock_level": product.current_stock}

@app.get("/inventory/movements")
async def list_inventory_movements(
    product_id: Optional[str] = None,
    container_code: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    movements = inventory_movements
    
    if product_id:
        movements = [m for m in movements if m.product_id == product_id]
    if container_code:
        movements = [m for m in movements if m.container_code == container_code]
    if start_date:
        movements = [m for m in movements if m.timestamp >= start_date]
    if end_date:
        movements = [m for m in movements if m.timestamp <= end_date]
    
    return movements

# List containers
@app.get("/containers/", response_model=List[Container])
async def list_containers():
    return list(containers.values())

# Enhanced container endpoints
@app.post("/containers/entry")
async def container_entry(container: Container):
    request_id = str(uuid.uuid4())
    containers[container.containerCode] = container
    
    # Record initial inventory if container has contents
    for product_id, quantity in container.contents.items():
        await adjust_stock(product_id, quantity, container.containerCode)
    
    return {"requestId": request_id, "success": True}

@app.post("/containers/{container_code}/add-product")
async def add_product_to_container(
    container_code: str,
    product_id: str,
    quantity: int
):
    if container_code not in containers:
        raise HTTPException(status_code=404, detail="Container not found")
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    await adjust_stock(product_id, quantity, container_code)
    return {"success": True}

# List orders
@app.get("/orders/", response_model=List[Order])
async def list_orders():
    return list(orders.values())

# Enhanced order endpoints
@app.post("/orders/create")
async def create_order(items: List[OrderItem]):
    order_id = str(uuid.uuid4())
    
    # Validate stock availability
    for item in items:
        if item.product_id not in products:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        if products[item.product_id].current_stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.product_id}")
    
    order = Order(orderId=order_id, items=items)
    orders[order_id] = order
    return order

@app.post("/orders/{order_id}/pick")
async def pick_order(order_id: str, container_code: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    if container_code not in containers:
        raise HTTPException(status_code=404, detail="Container not found")
    
    order = orders[order_id]
    container = containers[container_code]
    
    # Assign container to order
    order.assignedContainer = container_code
    order.status = "picking"
    
    # Move products to container
    for item in order.items:
        await add_product_to_container(container_code, item.product_id, -item.quantity)
        item.picked_quantity = item.quantity
    
    return order