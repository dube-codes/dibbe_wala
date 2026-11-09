from fastapi import APIRouter, Depends, Query
from datetime import datetime, date, timezone
from sqlmodel import Session, select, func
from models import Order, OrderStatus
from database import get_session

router = APIRouter()


@router.get("/daily")
def daily_stats(
    stats_date: date | None = Query(
        default=None, description="Date for stats in YYYY-MM-DD format"
    ),
    session: Session = Depends(get_session),
):
    if stats_date is None:
        stats_date = date.today()

    print(f"Generating stats for date: {stats_date}")

    start = datetime.combine(stats_date, datetime.min.time(), tzinfo=timezone.utc)
    end = datetime.combine(stats_date, datetime.max.time(), tzinfo=timezone.utc)

    stats = {}
    total = 0

    for status in OrderStatus:
        count = session.exec(
            select(func.count(Order.id)).where(
                Order.created_at >= start,
                Order.created_at <= end,
                Order.status == status,
            )
        ).one()

        stats[status.value] = count
        total += count

    return {"date": stats_date.isoformat(), "total_orders": total, "by_status": stats}
