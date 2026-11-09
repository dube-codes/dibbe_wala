from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone


# OrderStatus (Enum) -> preparing, picked_up, in_transit, delivered, cancelled
class OrderStatus(str, Enum):
    PREPARING = "preparing"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# Database table for Orders


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    delivery_address: str
    items: str  # Comma-separated list of items
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"},
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={
            "server_default": "CURRENT_TIMESTAMP",
            "onupdate": lambda: datetime.now(timezone.utc),
        },
    )


# Schema for creating a new order
class OrderCreate(SQLModel):
    customer_name: str
    delivery_address: str
    items: str  # Comma-separated list of items


# Schema for updating an order's status
class OrderUpdate(SQLModel):
    status: Optional[OrderStatus] = None
    delivery_address: Optional[str] = None


# Order status update log response schema
class StatusLog(SQLModel):
    order_id: int
    old_status: str
    new_status: str
    changed_at: datetime
