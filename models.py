from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional
from datetime import datetime


class PrintType(str, Enum):
    """Enum for available print types"""
    BLACK_WHITE = "black_white"
    COLORED = "colored"
    PHOTO_PAPER = "photo_paper"


class OrderStatus(str, Enum):
    """Enum for order status"""
    PENDING = "pending"
    PRINTING = "printing"
    COMPLETED = "completed"


class OrderCreate(BaseModel):
    """Model for creating a new order"""
    customer_name: str = Field(..., min_length=1, description="Name of the customer")
    print_type: PrintType = Field(..., description="Type of printing service")
    num_pages: int = Field(..., gt=0, description="Number of pages to print")
    notes: Optional[str] = Field(None, description="Special instructions or notes for the order")
    
    @validator('customer_name')
    def validate_customer_name(cls, v):
        if not v.strip():
            raise ValueError('Customer name cannot be empty')
        return v.strip()


class Order(BaseModel):
    """Model for order with computed details"""
    order_id: int = Field(..., description="Unique order identifier")
    customer_name: str = Field(..., description="Name of the customer")
    print_type: PrintType = Field(..., description="Type of printing service")
    num_pages: int = Field(..., description="Number of pages to print")
    price_per_page: float = Field(..., description="Price per page in PHP")
    total_cost: float = Field(..., description="Total cost in PHP")
    notes: Optional[str] = Field(None, description="Special instructions or notes")
    status: OrderStatus = Field(default=OrderStatus.PENDING, description="Order status")
    created_at: datetime = Field(default_factory=datetime.now, description="Order creation timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class OrderResponse(BaseModel):
    """Response model for order operations"""
    success: bool
    message: str
    order: Optional[Order] = None


class OrderListResponse(BaseModel):
    """Response model for listing all orders"""
    success: bool
    message: str
    total_orders: int
    orders: list[Order] = []


class OrderUpdate(BaseModel):
    """Model for updating order status"""
    status: OrderStatus = Field(..., description="New status for the order")
    notes: Optional[str] = Field(None, description="Optional notes to add or update")
