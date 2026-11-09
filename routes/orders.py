from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from database import get_session
from models import Order, OrderCreate, OrderUpdate, StatusLog, OrderStatus
from datetime import datetime

router = APIRouter()


@router.post("/", response_model=Order)
def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    db_order = Order(**order.model_dump())

    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order


@router.get("/", response_model=list[Order])
def orders_list(
    status: OrderStatus | None = Query(
        default=None, description="Filter orders by status"
    ),
    created_date: str | None = Query(
        default=None, description="Filter orders by creation date (YYYY-MM-DD)"
    ),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        default=10, ge=1, le=100, description="Maximum number of records to return"
    ),
    session: Session = Depends(get_session),
):
    query = select(Order)

    if status:
        query = query.where(Order.status == status)

    if created_date:
        start_date = datetime.combine(created_date, datetime.min.time())
        end_date = datetime.combine(created_date, datetime.max.time())
        query = query.where(
            Order.created_at >= start_date, Order.created_at <= end_date
        )

    query = query.offset(skip).limit(limit)
    return session.exec(query).all()
