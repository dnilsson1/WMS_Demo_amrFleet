# backend/main.py

from fastapi import FastAPI, HTTPException
from typing import List, Optional
from sqlmodel import SQLModel, Session, create_engine, select, delete
from models import *
import httpx
import uuid
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from schemas import OrderCreate, OrderItemCreate, StockAdjustment

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, echo=True)
app = FastAPI()

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    # Initialize SKU Counter
    with Session(engine) as session:
        sku_counter = session.get(SKUCounter, 1)
        if not sku_counter:
            sku_counter = SKUCounter()
            session.add(sku_counter)
            session.commit()
    global ip_config
    ip_config = load_config()

def load_config():
    with Session(engine) as session:
        config_entries = session.exec(select(IPConfig)).all()
        config = {entry.key: entry.value for entry in config_entries}
        if not config:
            # Set default values
            config = {"ip": "127.0.0.1", "port": "8000"}
            save_config(config)
        return config

def save_config(config):
    with Session(engine) as session:
        # Delete existing config
        session.exec(delete(IPConfig))
        session.commit()
        # Insert new config
        for key, value in config.items():
            config_entry = IPConfig(key=key, value=value)
            session.add(config_entry)
        session.commit()

# Endpoint to update the IP and Port configuration
@app.post("/set-ip")
def set_ip(ip_request: IPConfig):
    global ip_config
    ip_config = {"ip": ip_request.ip, "port": ip_request.port}
    save_config(ip_config)
    return {"success": True, "message": "IP and Port updated successfully."}

# Product endpoints
@app.post("/products/", response_model=Product)
def create_product(product: Product):
    with Session(engine) as session:
        # Generate SKU if not provided
        if not product.sku:
            sku_counter = session.get(SKUCounter, 1)
            sku_counter.last_sku += 1
            product.sku = str(sku_counter.last_sku)
            session.add(sku_counter)
        session.add(product)
        try:
            session.commit()
            session.refresh(product)
            return product
        except SQLAlchemyError as e:
            session.rollback()
            raise HTTPException(status_code=400, detail="Error creating product. Ensure all fields are valid and SKU is unique.")


@app.get("/products/", response_model=List[Product])
def list_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products

@app.post("/products/{product_id}/adjust-stock")
def adjust_stock(product_id: str, adjustment: StockAdjustment):
    quantity = adjustment.quantity
    container_code = adjustment.container_code
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        product.current_stock += quantity
        session.add(product)

        # Record inventory movement
        movement = InventoryMovement(
            product_id=product_id,
            quantity=quantity,
            container_code=container_code,
            movement_type="in" if quantity > 0 else "out",
            reference="stock_adjustment",
        )
        session.add(movement)

        # Update container contents if specified
        if container_code:
            container = session.get(Container, container_code)
            if not container:
                raise HTTPException(status_code=404, detail="Container not found")
            contents = container.contents or {}
            current_qty = contents.get(product_id, 0)
            new_qty = current_qty + quantity
            if new_qty > 0:
                contents[product_id] = new_qty
            else:
                contents.pop(product_id, None)
            container.contents = contents
            container.emptyStatus = EmptyStatus.EMPTY if not contents else EmptyStatus.FULL
            session.add(container)

        session.commit()
        return {"success": True, "new_stock_level": product.current_stock}

# Inventory movements endpoint
@app.get("/inventory/movements", response_model=List[InventoryMovement])
def list_inventory_movements(
    product_id: Optional[str] = None,
    container_code: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    with Session(engine) as session:
        query = select(InventoryMovement)
        if product_id:
            query = query.where(InventoryMovement.product_id == product_id)
        if container_code:
            query = query.where(InventoryMovement.container_code == container_code)
        if start_date:
            query = query.where(InventoryMovement.timestamp >= start_date)
        if end_date:
            query = query.where(InventoryMovement.timestamp <= end_date)
        movements = session.exec(query).all()
        return movements

# List containers
@app.get("/containers/", response_model=List[Container])
def list_containers():
    with Session(engine) as session:
        containers = session.exec(select(Container)).all()
        return containers

@app.post("/containers/entry")
def container_entry(container: Container):
    with Session(engine) as session:
        # Check if container already exists
        existing_container = session.get(Container, container.containerCode)
        if existing_container:
            raise HTTPException(status_code=400, detail="Container already exists")
        session.add(container)

        # Record initial inventory if container has contents
        for product_id, quantity in container.contents.items():
            adjust_stock(product_id, quantity, container.containerCode)

        session.commit()

    # Prepare payload for the external containerIn API
    request_id = str(uuid.uuid4())
    payload = {
        "requestId": request_id,
        "containerType": container.containerType.value if container.containerType else "",
        "containerCode": container.containerCode,
        "position": container.position,  # Use container's position
        "containerModelCode": "",  # Assuming container model code is not needed
        "enterOrientation": "",  # Assuming no special orientation is needed
        "isNew": False  # Assuming the container is not new
    }

    headers = {
        "Content-Type": "application/json"
    }

    # Define the external API URL
    api_url = f"http://{ip_config['ip']}:{ip_config['port']}/interfaces/api/amr/containerIn"

    try:
        # Send the request to the external containerIn API
        response = httpx.post(api_url, json=payload, headers=headers)

        # Handle response
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                return {"requestId": request_id, "success": True}
            else:
                raise HTTPException(status_code=500, detail=f"Failed to register container: {response_data.get('message')}")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error from external API: {response.text}")

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to external API: {str(e)}")

@app.post("/containers/{container_code}/add-product")
def add_product_to_container(
    container_code: str,
    product_id: str,
    quantity: int
):
    with Session(engine) as session:
        container = session.get(Container, container_code)
        if not container:
            raise HTTPException(status_code=404, detail="Container not found")

        product = session.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        adjust_stock(product_id, quantity, container_code)
        return {"success": True}

def find_containers_with_product(session: Session, product_id: str):
    containers_with_product = []
    containers = session.exec(select(Container)).all()
    for container in containers:
        if product_id in (container.contents or {}):
            containers_with_product.append(container)
    return containers_with_product

def query_container_info(container_code: str):
    api_url = f"http://{ip_config.get('ip', '127.0.0.1')}:{ip_config.get('port', '8000')}/interfaces/api/amr/containerQuery"
    payload = {
        "containerCode": container_code
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = httpx.post(api_url, json=payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                data = response_data.get("data")
                if data:
                    return data[0]  # Assuming data is a list
                else:
                    raise HTTPException(status_code=404, detail=f"Container {container_code} not found in fleet manager")
            else:
                raise HTTPException(status_code=500, detail=f"Error querying container: {response_data.get('message')}")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error querying container: {response.text}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to fleet manager API: {str(e)}")

def submit_mission(mission_payload):
    api_url = f"http://{ip_config.get('ip', '127.0.0.1')}:{ip_config.get('port', '8000')}/interfaces/api/amr/submitMission"
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = httpx.post(api_url, json=mission_payload, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                return response_data
            else:
                raise HTTPException(status_code=500, detail=f"Failed to submit mission: {response_data.get('message')}")
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error submitting mission: {response.text}")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to fleet manager API: {str(e)}")

# List orders
@app.get("/orders/", response_model=List[Order])
def list_orders():
    with Session(engine) as session:
        orders = session.exec(select(Order)).all()
        for order in orders:
            order.items = session.exec(select(OrderItem).where(OrderItem.order_id == order.orderId)).all()
        return orders

# Create order
@app.post("/orders/create", response_model=Order)
def create_order(order_data: OrderCreate):
    with Session(engine) as session:
        try:
            # Validate stock availability and adjust stock
            order_items = []
            for item_data in order_data.items:
                product = session.get(Product, item_data.product_id)
                if not product:
                    raise HTTPException(status_code=404, detail=f"Product {item_data.product_id} not found")
                if product.current_stock < item_data.quantity:
                    raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item_data.product_id}")

                # Adjust stock levels
                product.current_stock -= item_data.quantity
                session.add(product)

                # Create OrderItem instance
                order_item = OrderItem(
                    order_id=None,  # Will be set when order is created
                    product_id=item_data.product_id,
                    quantity=item_data.quantity,
                    picked_quantity=0
                )
                order_items.append(order_item)

            # Create order with status 'confirmed'
            order = Order(status="confirmed", items=order_items)
            session.add(order)
            session.commit()
            session.refresh(order)

            return order
        except SQLAlchemyError:
            session.rollback()
            raise HTTPException(status_code=500, detail="Internal Server Error")

# **Updated pick_order Endpoint**

@app.post("/orders/{order_id}/pick")
def pick_order(order_id: str, destination_name: str):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status != "confirmed":
            raise HTTPException(status_code=400, detail="Order is not in 'confirmed' status")

        # Get the destination point
        destination = session.get(Point, destination_name)
        if not destination:
            raise HTTPException(status_code=404, detail="Destination not found")

        destination_position_code = destination.position

        # Get order items
        order_items = session.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()

        # Map containers to items
        containers_to_move = {}
        for item in order_items:
            product_id = item.product_id

            # Find containers containing the product
            containers_with_product = find_containers_with_product(session, product_id)
            if not containers_with_product:
                raise HTTPException(status_code=404, detail=f"No container found for product {product_id}")

            # For simplicity, pick the first container
            container = containers_with_product[0]
            container_code = container.containerCode

            if container_code not in containers_to_move:
                containers_to_move[container_code] = []
            containers_to_move[container_code].append(item)

        # Submit missions for each container
        for container_code, items in containers_to_move.items():
            container_info = query_container_info(container_code)
            current_position = container_info.get('nodeCode')
            if not current_position:
                raise HTTPException(status_code=500, detail=f"Container {container_code} location not found")

            # Prepare mission data
            request_id = str(uuid.uuid4())
            mission_code = f"mission_{request_id}"
            mission_payload = {
                "orgId": "UNIVERSAL",
                "requestId": request_id,
                "missionCode": mission_code,
                "missionType": "RACK_MOVE",
                "robotType": "LIFT",  # Adjust based on your robot types
                "containerCode": container_code,
                "priority": 1,
                "lockRobotAfterFinish": False,
                "missionData": [
                    {
                        "sequence": 1,
                        "position": current_position,
                        "type": "NODE_POINT",
                        "putDown": False,
                        "passStrategy": "AUTO",
                        "waitingMillis": 0
                    },
                    {
                        "sequence": 2,
                        "position": destination_position_code,
                        "type": "NODE_POINT",
                        "putDown": True,
                        "passStrategy": "AUTO",
                        "waitingMillis": 0
                    }
                ]
            }

            # Submit mission to fleet manager
            submit_mission(mission_payload)

            # Update order assigned containers
            assigned_containers = order.assignedContainers or []
            if container_code not in assigned_containers:
                assigned_containers.append(container_code)
            order.assignedContainers = assigned_containers

        # Update order status
        order.status = "picking"
        session.add(order)
        session.commit()

        return order

# **complete_order Endpoint**

@app.post("/orders/{order_id}/complete")
def complete_order(order_id: str):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status != "picking":
            raise HTTPException(status_code=400, detail="Order is not in 'picking' status")
        # Update order status to 'completed'
        order.status = "completed"
        session.add(order)
        session.commit()
        return {"success": True, "message": "Order marked as completed"}

# Point management Section
@app.post("/points/", response_model=Point)
def add_point(point: Point):
    with Session(engine) as session:
        existing_point = session.get(Point, point.name)
        if existing_point:
            raise HTTPException(status_code=400, detail="Point already exists")
        session.add(point)
        session.commit()
        return point

@app.get("/points/", response_model=List[Point])
def list_points():
    with Session(engine) as session:
        points = session.exec(select(Point)).all()
        return points

@app.delete("/points/{point_name}")
def delete_point(point_name: str):
    with Session(engine) as session:
        point = session.get(Point, point_name)
        if point:
            session.delete(point)
            session.commit()
            return {"success": True}
        else:
            raise HTTPException(status_code=404, detail="Point not found")
