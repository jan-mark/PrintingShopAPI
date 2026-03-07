# Printing Shop Order System API

A simple backend API built with FastAPI to manage printing orders in a printing shop. The system accepts printing orders and automatically computes the total printing cost. No database required - uses in-memory storage for conceptualization.

## Features

- ✅ Accept printing orders through API
- ✅ Automatic cost calculation based on print type and pages
- ✅ **Duplicate order prevention** - Prevents recording identical orders
- ✅ **Order status tracking** - Track orders through Pending, Printing, Completed
- ✅ **Order notes** - Add special instructions or notes to orders
- ✅ **Update order status** - Staff can update order status and notes
- ✅ View all orders
- ✅ Retrieve specific order information
- ✅ Delete orders
- ✅ Order statistics and revenue tracking
- ✅ In-memory storage (no database)
- ✅ Interactive API documentation (Swagger UI)

## Pricing

| Print Type | Price per Page (PHP) |
|------------|---------------------|
| Black & White | ₱2.00 |
| Colored | ₱5.00 |
| Photo Paper | ₱20.00 |

## Requirements

- Python 3.8 or higher

## Installation

1. **Navigate to project directory:**
   ```bash
   cd "c:\Users\JOHNMARK\PRINTINGAPI SYSTEM"
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

**Start the server:**
```bash
python main.py
```

The API will be available at:
- **API:** http://localhost:8000
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

## API Endpoints

### Root
- `GET /` - API information and pricing

### Orders
- `POST /orders` - Create new printing order
- `GET /orders` - View all orders
- `GET /orders/{order_id}` - Get specific order
- `PUT /orders/{order_id}/status` - Update order status and notes
- `DELETE /orders/{order_id}` - Delete order

### Statistics
- `GET /stats` - Order statistics and revenue

## Usage Examples

### 1. Create Order

**Request:**
```json
POST http://localhost:8000/orders

{
  "customer_name": "Juan Dela Cruz",
  "print_type": "colored",
  "num_pages": 10,
  "notes": "Please use glossy paper"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Order #1 created successfully",
  "order": {
    "order_id": 1,
    "customer_name": "Juan Dela Cruz",
    "print_type": "colored",
    "num_pages": 10,
    "price_per_page": 5.0,
    "total_cost": 50.0,
    "notes": "Please use glossy paper",
    "status": "pending",
    "created_at": "2026-03-07T10:30:00"
  }
}
```

**Note:** The `notes` field is optional. Orders are automatically created with `pending` status.

### 2. View All Orders

**Request:**
```bash
GET http://localhost:8000/orders
```

**Response:**
```json
{
  "success": true,
  "message": "Retrieved 1 order(s)",
  "total_orders": 1,
  "orders": [...]
}
```

### 3. Get Specific Order

**Request:**
```bash
GET http://localhost:8000/orders/1
```

### 4. Update Order Status

**Request:**
```json
PUT http://localhost:8000/orders/1/status

{
  "status": "printing",
  "notes": "Started printing at 2PM"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Order #1 status updated to printing",
  "order": {
    "order_id": 1,
    "customer_name": "Juan Dela Cruz",
    "print_type": "colored",
    "num_pages": 10,
    "price_per_page": 5.0,
    "total_cost": 50.0,
    "notes": "Started printing at 2PM",
    "status": "printing",
    "created_at": "2026-03-07T10:30:00"
  }
}
```

### 5. Get Statistics

**Request:**
```bash
GET http://localhost:8000/stats
```

**Response:**
```json
{
  "total_orders": 3,
  "total_revenue": 150.0,
  "breakdown_by_type": {
    "black_white": {"count": 1, "revenue": 50.0},
    "colored": {"count": 1, "revenue": 50.0},
    "photo_paper": {"count": 1, "revenue": 50.0}
  }
}
```

## Print Types

Use these values for `print_type`:
- `black_white` - Black & White (₱2.00/page)
- `colored` - Colored (₱5.00/page)
- `photo_paper` - Photo Paper (₱20.00/page)

## Order Status Values

Use these values for `status`:
- `pending` - Order is pending (default for new orders)
- `printing` - Order is currently being printed
- `completed` - Order is completed

## Duplicate Prevention

The system automatically prevents duplicate orders by checking:
- Customer name (case-insensitive)
- Print type
- Number of pages
- Notes

If an identical order exists and is not completed, you'll receive a `409 Conflict` error:
```json
{
  "detail": "Duplicate order detected. An identical order (#1) already exists for this customer."
}
```

## Testing with Browser

1. Open: http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the data
5. Click "Execute"

## Testing with cURL

### Create Order
```bash
curl -X POST "http://localhost:8000/orders" -H "Content-Type: application/json" -d "{\"customer_name\":\"Juan\",\"print_type\":\"colored\",\"num_pages\":10,\"notes\":\"Rush order\"}"
```

### Update Order Status
```bash
curl -X PUT "http://localhost:8000/orders/1/status" -H "Content-Type: application/json" -d "{\"status\":\"printing\"}"
```

### Get All Orders
```bash
curl http://localhost:8000/orders
```

## Project Structure

```
PRINTINGAPI SYSTEM/
├── main.py              # FastAPI application and endpoints
├── models.py            # Pydantic models
├── requirements.txt     # Dependencies
├── README.md           # Documentation
└── PrintingAPI PRD.txt # Product Requirements
```

## Notes

- **In-memory storage** - Data resets when server restarts
- **No database** - For conceptualization only
- **Duplicate prevention** - System checks for duplicate orders before creation
- **Auto-reload enabled** - Server automatically reloads when code changes
- All prices in Philippine Pesos (PHP)
- All new orders start with `pending` status

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /F /PID [ProcessID]
```

### Change Port
Edit the uvicorn.run line in [main.py](main.py):
```python
uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)  # Change to 8001
```

## License

Conceptualization project
