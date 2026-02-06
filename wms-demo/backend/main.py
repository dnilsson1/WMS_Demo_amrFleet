# backend/main.py

from fastapi import FastAPI, HTTPException
from typing import List, Optional
from sqlmodel import SQLModel, Session, create_engine, select, delete
from models import *
import httpx
import uuid
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from schemas import OrderCreate, OrderItemCreate, StockAdjustment, PickOrderRequest, PointUpdate

DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI()

# CORS middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    ensure_ipconfig_columns()
    ensure_container_columns()
    # Initialize SKU Counter
    with Session(engine) as session:
        sku_counter = session.get(SKUCounter, 1)
        if not sku_counter:
            sku_counter = SKUCounter()
            session.add(sku_counter)
            session.commit()
    global ip_config
    ip_config = load_config()

# Update the load_config and save_config functions
def load_config():
    with Session(engine) as session:
        config_entry = session.query(IPConfig).first()
        if config_entry:
            return {
                "ip": config_entry.ip,
                "port": config_entry.port,
                "org_id": config_entry.org_id,
                "access_token": config_entry.access_token,
            }
        else:
            # If no configuration exists, set default values
            default_config = {
                "ip": "127.0.0.1",
                "port": "8000",
                "org_id": None,
                "access_token": None,
            }
            save_config(default_config)
            return default_config



def save_config(config):
    with Session(engine) as session:
        existing_config = session.query(IPConfig).first()
        if existing_config:
            # Update the existing configuration
            existing_config.ip = config["ip"]
            existing_config.port = config["port"]
            existing_config.org_id = config.get("org_id")
            existing_config.access_token = config.get("access_token")
        else:
            # Create a new configuration entry
            new_config = IPConfig(
                ip=config["ip"],
                port=config["port"],
                org_id=config.get("org_id"),
                access_token=config.get("access_token"),
            )
            session.add(new_config)
        session.commit()


def ensure_ipconfig_columns():
    with engine.connect() as connection:
        result = connection.exec_driver_sql("PRAGMA table_info(ipconfig)")
        existing_columns = {row[1] for row in result.fetchall()}
        if "org_id" not in existing_columns:
            connection.exec_driver_sql("ALTER TABLE ipconfig ADD COLUMN org_id TEXT")
        if "access_token" not in existing_columns:
            connection.exec_driver_sql("ALTER TABLE ipconfig ADD COLUMN access_token TEXT")
        connection.commit()


def ensure_container_columns():
    with engine.connect() as connection:
        result = connection.exec_driver_sql("PRAGMA table_info(container)")
        existing_columns = {row[1] for row in result.fetchall()}
        if "isNew" not in existing_columns:
            connection.exec_driver_sql("ALTER TABLE container ADD COLUMN isNew INTEGER")
        connection.commit()



def get_base_url():
    config = load_config()
    ip = config.get("ip", "127.0.0.1")  # Default to localhost if not set
    port = config.get("port", "8000")  # Default to port 8000 if not set
    return f"http://{ip}:{port}"


def get_fleet_headers():
    config = load_config()
    headers = {"Content-Type": "application/json"}
    access_token = config.get("access_token")
    if access_token:
        headers["Authorization"] = access_token
    return headers



# Fetch area codes from the external API
def get_area_codes():
    base_url = get_base_url()
    api_url = f"{base_url}/interfaces/api/amr/areaQuery"
    headers = get_fleet_headers()
    try:
        response = httpx.get(api_url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            areas = data.get("data", [])
            return [area.get("areaCode") for area in areas]
        else:
            raise HTTPException(
                status_code=500, detail=f"Error fetching areas: {data.get('message')}"
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to areaQuery API: {str(e)}"
        )

# Fetch nodes in specified areas
def get_nodes_in_areas(area_codes):
    base_url = get_base_url()
    api_url = f"{base_url}/interfaces/api/amr/areaNodesQuery"
    headers = get_fleet_headers()
    payload = {"areaCodes": area_codes}
    try:
        response = httpx.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get("success"):
            areas_with_nodes = data.get("data", [])
            nodes = []
            for area in areas_with_nodes:
                nodes.extend(area.get("nodeList", []))
            return nodes
        else:
            raise HTTPException(
                status_code=500, detail=f"Error fetching nodes: {data.get('message')}"
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to areaNodesQuery API: {str(e)}"
        )

# Fetch points from the Fleet Manager
def get_points():
    area_codes = get_area_codes()
    if not area_codes:
        return []
    nodes = get_nodes_in_areas(area_codes)
    if not nodes:
        return []
    with Session(engine) as session:
        points = []
        for node in nodes:
            # Check if point exists in the database
            point = session.get(Point, node)
            if point:
                points.append(point)
            else:
                # Add a new point if it doesn't exist
                point = Point(name=node, position=node, wms_name=node)
                session.add(point)
                points.append(point)
        session.commit()
    return points

# Endpoint to update the IP and Port configuration
@app.post("/set-ip")
def set_ip(ip_request: IPConfig):
    # Debugging: Log the received data
    print(f"Received IP Request: {ip_request}")

    # Validate the input
    if not ip_request.ip or not ip_request.port:
        raise HTTPException(status_code=400, detail="IP and Port are required.")

    config = {
        "ip": ip_request.ip,
        "port": ip_request.port,
        "org_id": ip_request.org_id,
        "access_token": ip_request.access_token,
    }
    save_config(config)
    return {"success": True, "message": "IP and Port updated successfully."}


# Endpoint to get the current IP and Port configuration
@app.get("/get-ip")
def get_ip():
    config = load_config()
    return config


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
        existing_container = session.get(Container, container.containerCode)
        if existing_container:
            raise HTTPException(status_code=400, detail="Container already exists")
        session.add(container)

        for product_id, quantity in container.contents.items():
            adjust_stock(product_id, quantity, container.containerCode)

        session.commit()

        # Extract container details to avoid DetachedInstanceError
        container_data = {
            "requestId": str(uuid.uuid4()),
            "containerType": container.containerType,
            "containerCode": container.containerCode,
            "position": container.position,
            "containerModelCode": container.containerModelCode,
            "enterOrientation": container.enterOrientation,
            "isNew": bool(container.isNew),
        }

    # Prepare payload for the external API
    base_url = get_base_url()
    api_url = f"{base_url}/interfaces/api/amr/containerIn"
    headers = get_fleet_headers()

    try:
        response = httpx.post(api_url, json=container_data, headers=headers)
        response.raise_for_status()
        try:
            response_data = response.json()
        except ValueError:
            raise HTTPException(
                status_code=500,
                detail=f"Fleet manager returned non-JSON response: {response.text}",
            )
        if response_data.get("success"):
            return {"requestId": container_data["requestId"], "success": True}
        else:
            raise HTTPException(
                status_code=500, detail=f"Error registering container: {response_data.get('message')}"
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to fleet manager API: {str(e)}"
        )


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
    base_url = get_base_url()
    api_url = f"{base_url}/interfaces/api/amr/containerQuery"
    payload = {"containerCode": container_code}
    headers = get_fleet_headers()

    try:
        response = httpx.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("success"):
            data = response_data.get("data")
            if data:
                return data[0]  # Assuming data is a list
            else:
                raise HTTPException(
                    status_code=404,
                    detail=f"Container {container_code} not found in fleet manager",
                )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error querying container: {response_data.get('message')}",
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to fleet manager API: {str(e)}",
        )


def submit_mission(mission_payload):
    base_url = get_base_url()
    api_url = f"{base_url}/interfaces/api/amr/submitMission"
    headers = get_fleet_headers()
    org_id = load_config().get("org_id")
    if org_id and "orgId" not in mission_payload:
        mission_payload = {**mission_payload, "orgId": org_id}

    try:
        response = httpx.post(api_url, json=mission_payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("success"):
            return response_data
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to submit mission: {response_data.get('message')}",
            )
    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to connect to fleet manager API: {str(e)}",
        )

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
                if not item_data.product_id:
                    raise HTTPException(status_code=400, detail="Product ID is required")
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
def pick_order(order_id: str, payload: PickOrderRequest):
    with Session(engine) as session:
        order = session.get(Order, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.status != "confirmed":
            raise HTTPException(status_code=400, detail="Order is not in 'confirmed' status")

        # Get the destination point (match by name or WMS-mapped name)
        destination = session.get(Point, payload.destination_name)
        if not destination:
            destination = session.exec(
                select(Point).where(Point.wms_name == payload.destination_name)
            ).first()
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
    # Best-effort sync from fleet manager, but always return stored points.
    try:
        get_points()
    except Exception:
        pass
    with Session(engine) as session:
        return session.exec(select(Point)).all()


@app.put("/points/{point_name}", response_model=Point)
def update_point_name(point_name: str, payload: PointUpdate):
    with Session(engine) as session:
        point = session.get(Point, point_name)
        if not point:
            raise HTTPException(status_code=404, detail="Point not found")
        if payload.position is not None:
            point.position = payload.position
        if payload.wms_name is not None:
            point.wms_name = payload.wms_name
        session.add(point)
        session.commit()
        session.refresh(point)
        return point


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
