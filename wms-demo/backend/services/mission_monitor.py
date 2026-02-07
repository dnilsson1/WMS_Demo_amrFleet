import asyncio
import httpx

from sqlmodel import Session, select

from models import Order

DEFAULT_POLL_INTERVAL = 5

TERMINAL_FAILURE_STATUSES = {31, 35, 50, 60}
TERMINAL_SUCCESS_STATUS = 30
ACTIVE_STATUSES = {10, 20, 25, 28}


def resolve_order_status(statuses):
    if not statuses:
        return None
    if any(status in TERMINAL_FAILURE_STATUSES for status in statuses):
        return "failed"
    if all(status == TERMINAL_SUCCESS_STATUS for status in statuses):
        return "completed"
    if any(status in ACTIVE_STATUSES for status in statuses):
        return "picking"
    return None


async def fetch_container_job_status(client, base_url, headers, container_code):
    url = f"{base_url}/interfaces/api/amr/jobQuery"
    payload = {
        "containerCode": container_code,
        "limit": 1,
    }
    response = await client.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    response_data = response.json()
    if not response_data.get("success"):
        return None
    jobs = response_data.get("data") or []
    if not jobs:
        return None
    return jobs[0].get("status")


async def mission_monitor_loop(get_base_url, get_fleet_headers, engine, interval=DEFAULT_POLL_INTERVAL):
    async with httpx.AsyncClient() as client:
        while True:
            try:
                base_url = get_base_url()
                headers = get_fleet_headers()
                with Session(engine) as session:
                    orders = session.exec(
                        select(Order).where(Order.status == "picking")
                    ).all()
                    for order in orders:
                        container_codes = order.assignedContainers or []
                        if not container_codes:
                            continue
                        statuses = []
                        for container_code in container_codes:
                            status = await fetch_container_job_status(
                                client, base_url, headers, container_code
                            )
                            if status is not None:
                                statuses.append(status)
                        new_status = resolve_order_status(statuses)
                        if new_status and new_status != order.status:
                            order.status = new_status
                            session.add(order)
                    session.commit()
            except Exception:
                # Keep the loop running even if the fleet manager is down.
                pass
            await asyncio.sleep(interval)


def start_mission_monitor(get_base_url, get_fleet_headers, engine, interval=DEFAULT_POLL_INTERVAL):
    return asyncio.create_task(
        mission_monitor_loop(get_base_url, get_fleet_headers, engine, interval)
    )
