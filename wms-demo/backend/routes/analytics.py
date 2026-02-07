from datetime import datetime, timedelta

from fastapi import APIRouter
from sqlmodel import Session, select

from models import InventoryMovement


def get_analytics_router(engine):
    router = APIRouter()

    @router.get("/analytics/throughput")
    def get_throughput():
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=24)
        bucket_start = start_time.replace(minute=0, second=0, microsecond=0)

        buckets = {}
        for i in range(24):
            hour = bucket_start + timedelta(hours=i)
            buckets[hour] = 0

        with Session(engine) as session:
            movements = session.exec(
                select(InventoryMovement).where(InventoryMovement.timestamp >= start_time)
            ).all()
            for movement in movements:
                hour = movement.timestamp.replace(minute=0, second=0, microsecond=0)
                if hour in buckets:
                    buckets[hour] += 1

        data = [
            {
                "hour": hour.isoformat(),
                "count": count,
            }
            for hour, count in sorted(buckets.items())
        ]

        return {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "data": data,
        }

    return router
