# Printing Shop Order System API

A simple backend API built with FastAPI to manage printing orders in a printing shop. The system accepts printing orders and automatically computes the total printing cost. No database required - uses in-memory storage for conceptualization.

## Features

- ✅ Accept printing orders through API
- ✅ Automatic cost calculation based on print type and pages
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
  "num_pages": 10
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
    "created_at": "2026-03-07T10:30:00"
  }
}
```

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

### 4. Get Statistics

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

## Testing with Browser

1. Open: http://localhost:8000/docs
2. Click on any endpoint
3. Click "Try it out"
4. Fill in the data
5. Click "Execute"

## Testing with cURL

### Create Order
```bash
curl -X POST "http://localhost:8000/orders" -H "Content-Type: application/json" -d "{\"customer_name\":\"Juan\",\"print_type\":\"colored\",\"num_pages\":10}"
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
- All prices in Philippine Pesos (PHP)

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process
taskkill /F /PID [ProcessID]
```

### Change Port
Edit [main.py](main.py) line 224:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Change to 8001
```

## License

Conceptualization project
