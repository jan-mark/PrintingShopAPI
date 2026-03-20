try:
    import requests
except ImportError:
    print("Missing dependency: requests")
    print("Install it with: pip install requests")
    raise

BASE_URL = "http://127.0.0.1:8000"


def handle_response(response):
    """Raise for bad status and safely parse JSON response."""
    response.raise_for_status()
    try:
        return response.json()
    except ValueError:
        return {"message": response.text}


def print_request_error(action, err):
    print(f"❌ Error {action}: {err}")

# CREATE ORDER
def create_order():
    try:
        name = input("Customer Name: ")
        print_type = input("Print Type (black_white / colored / photo_paper): ")
        pages = int(input("Number of Pages: "))
        notes = input("Notes (optional): ")

        payload = {
            "customer_name": name,
            "print_type": print_type,
            "num_pages": pages,
            "notes": notes
        }

        res = requests.post(f"{BASE_URL}/orders", json=payload, timeout=10)
        print("✅", handle_response(res))

    except requests.exceptions.RequestException as err:
        print_request_error("creating order", err)
    except ValueError:
        print("❌ Number of pages must be a valid integer")

# VIEW ALL ORDERS
def view_orders():
    try:
        res = requests.get(f"{BASE_URL}/orders", timeout=10)
        data = handle_response(res)

        print("\n📦 ALL ORDERS:")
        for order in data["orders"]:
            print(f"ID: {order['order_id']} | {order['customer_name']} | {order['print_type']} | Pages: {order['num_pages']} | Status: {order['status']}")

    except requests.exceptions.RequestException as err:
        print_request_error("fetching orders", err)

# GET ORDER BY ID
def get_order():
    try:
        order_id = int(input("Enter Order ID: "))
        res = requests.get(f"{BASE_URL}/orders/{order_id}", timeout=10)
        print("📄", handle_response(res))
    except requests.exceptions.RequestException as err:
        print_request_error("retrieving order", err)
    except ValueError:
        print("❌ Order ID must be a valid integer")

# UPDATE STATUS
def update_status():
    try:
        order_id = int(input("Order ID: "))
        status = input("New Status (pending / printing / completed): ")
        notes = input("New Notes (optional): ")

        payload = {
            "status": status,
            "notes": notes
        }

        res = requests.put(f"{BASE_URL}/orders/{order_id}/status", json=payload, timeout=10)
        print("🔄", handle_response(res))

    except requests.exceptions.RequestException as err:
        print_request_error("updating status", err)
    except ValueError:
        print("❌ Order ID must be a valid integer")

# DELETE ORDER
def delete_order():
    try:
        order_id = int(input("Order ID to delete: "))
        res = requests.delete(f"{BASE_URL}/orders/{order_id}", timeout=10)
        print("🗑️", handle_response(res))
    except requests.exceptions.RequestException as err:
        print_request_error("deleting order", err)
    except ValueError:
        print("❌ Order ID must be a valid integer")

# VIEW STATS
def view_stats():
    try:
        res = requests.get(f"{BASE_URL}/stats", timeout=10)
        print("📊", handle_response(res))
    except requests.exceptions.RequestException as err:
        print_request_error("fetching stats", err)

# MENU
def menu():
    while True:
        print("\n====== PRINTING SHOP CLIENT ======")
        print("1. Create Order")
        print("2. View All Orders")
        print("3. Get Order by ID")
        print("4. Update Order Status")
        print("5. Delete Order")
        print("6. View Statistics")
        print("7. Exit")

        choice = input("Select option: ")

        if choice == "1":
            create_order()
        elif choice == "2":
            view_orders()
        elif choice == "3":
            get_order()
        elif choice == "4":
            update_status()
        elif choice == "5":
            delete_order()
        elif choice == "6":
            view_stats()
        elif choice == "7":
            print("👋 Exiting...")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    menu()