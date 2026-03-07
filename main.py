from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from models import (
    Order, OrderCreate, OrderResponse, OrderListResponse, PrintType, OrderStatus, OrderUpdate
)
from typing import Dict
from datetime import datetime
import uvicorn


# Initialize FastAPI app
app = FastAPI(
    title="Printing Shop Order System API",
    description="A simple backend API to manage printing orders in a printing shop",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pricing configuration (in PHP)
PRICING: Dict[PrintType, float] = {
    PrintType.BLACK_WHITE: 2.00,
    PrintType.COLORED: 5.00,
    PrintType.PHOTO_PAPER: 20.00
}

# In-memory storage for orders (no database)
orders_db: Dict[int, Order] = {}
order_counter = 0


def get_next_order_id() -> int:
    """Generate next order ID"""
    global order_counter
    order_counter += 1
    return order_counter


def calculate_total_cost(print_type: PrintType, num_pages: int) -> tuple[float, float]:
    """
    Calculate total cost for an order
    
    Args:
        print_type: Type of printing
        num_pages: Number of pages
        
    Returns:
        Tuple of (price_per_page, total_cost)
    """
    price_per_page = PRICING[print_type]
    total_cost = price_per_page * num_pages
    return price_per_page, total_cost


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Printing Shop Order System API",
        "version": "1.0.0",
        "pricing": {
            "black_white": f"PHP {PRICING[PrintType.BLACK_WHITE]:.2f} per page",
            "colored": f"PHP {PRICING[PrintType.COLORED]:.2f} per page",
            "photo_paper": f"PHP {PRICING[PrintType.PHOTO_PAPER]:.2f} per page"
        },
        "endpoints": {
            "create_order": "POST /orders",
            "get_all_orders": "GET /orders",
            "get_order_by_id": "GET /orders/{order_id}",            "update_order_status": "PUT /orders/{order_id}/status",            "delete_order": "DELETE /orders/{order_id}"
        }
    }


@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED, tags=["Orders"])
async def create_order(order_data: OrderCreate):
    """
    Create a new printing order
    
    Accepts printing order details and automatically computes total cost.
    
    - **customer_name**: Name of the customer
    - **print_type**: Type of printing (black_white, colored, photo_paper)
    - **num_pages**: Number of pages to print
    - **notes**: Optional special instructions or notes
    
    Returns the created order with automatically computed total cost
    """
    try:
        # Check for duplicate orders (same customer, print type, num_pages, and notes)
        for existing_order in orders_db.values():
            if (existing_order.customer_name.lower() == order_data.customer_name.lower() and
                existing_order.print_type == order_data.print_type and
                existing_order.num_pages == order_data.num_pages and
                existing_order.notes == order_data.notes and
                existing_order.status != OrderStatus.COMPLETED):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Duplicate order detected. An identical order (#{existing_order.order_id}) already exists for this customer."
                )
        
        # Generate order ID
        order_id = get_next_order_id()
        
        # Calculate pricing
        price_per_page, total_cost = calculate_total_cost(
            order_data.print_type, 
            order_data.num_pages
        )
        
        # Create order object
        new_order = Order(
            order_id=order_id,
            customer_name=order_data.customer_name,
            print_type=order_data.print_type,
            num_pages=order_data.num_pages,
            price_per_page=price_per_page,
            total_cost=total_cost,
            notes=order_data.notes,
            status=OrderStatus.PENDING,
            created_at=datetime.now()
        )
        
        # Store in memory
        orders_db[order_id] = new_order
        
        return OrderResponse(
            success=True,
            message=f"Order #{order_id} created successfully",
            order=new_order
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create order: {str(e)}"
        )


@app.get("/orders", response_model=OrderListResponse, tags=["Orders"])
async def get_all_orders():
    """
    View all printing orders
    
    Returns a list of all orders stored in the system
    """
    orders_list = list(orders_db.values())
    
    return OrderListResponse(
        success=True,
        message=f"Retrieved {len(orders_list)} order(s)",
        total_orders=len(orders_list),
        orders=orders_list
    )


@app.get("/orders/{order_id}", response_model=OrderResponse, tags=["Orders"])
async def get_order_by_id(order_id: int):
    """
    Retrieve specific order information by ID
    
    - **order_id**: The unique identifier of the order
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order #{order_id} not found"
        )
    
    return OrderResponse(
        success=True,
        message=f"Order #{order_id} retrieved successfully",
        order=orders_db[order_id]
    )


@app.delete("/orders/{order_id}", tags=["Orders"])
async def delete_order(order_id: int):
    """
    Delete a specific order by ID
    
    - **order_id**: The unique identifier of the order to delete
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order #{order_id} not found"
        )
    
    deleted_order = orders_db.pop(order_id)
    
    return {
        "success": True,
        "message": f"Order #{order_id} for {deleted_order.customer_name} deleted successfully"
    }


@app.put("/orders/{order_id}/status", response_model=OrderResponse, tags=["Orders"])
async def update_order_status(order_id: int, update_data: OrderUpdate):
    """
    Update the status of a specific order
    
    - **order_id**: The unique identifier of the order
    - **status**: New status (pending, printing, completed)
    - **notes**: Optional notes to add or update
    """
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order #{order_id} not found"
        )
    
    order = orders_db[order_id]
    order.status = update_data.status
    
    if update_data.notes is not None:
        order.notes = update_data.notes
    
    return OrderResponse(
        success=True,
        message=f"Order #{order_id} status updated to {update_data.status.value}",
        order=order
    )


@app.get("/stats", tags=["Statistics"])
async def get_statistics():
    """
    Get statistics about orders
    
    Returns total orders, revenue, and breakdown by print type
    """
    if not orders_db:
        return {
            "total_orders": 0,
            "total_revenue": 0.0,
            "breakdown_by_type": {}
        }
    
    total_revenue = sum(order.total_cost for order in orders_db.values())
    
    breakdown = {
        "black_white": {"count": 0, "revenue": 0.0},
        "colored": {"count": 0, "revenue": 0.0},
        "photo_paper": {"count": 0, "revenue": 0.0}
    }
    
    for order in orders_db.values():
        breakdown[order.print_type.value]["count"] += 1
        breakdown[order.print_type.value]["revenue"] += order.total_cost
    
    return {
        "total_orders": len(orders_db),
        "total_revenue": round(total_revenue, 2),
        "breakdown_by_type": breakdown
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
