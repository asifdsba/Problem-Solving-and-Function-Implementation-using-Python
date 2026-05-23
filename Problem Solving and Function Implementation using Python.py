inventory_menu = [
    {"item_name": "Espresso", "unit_price": 3.0, "stock_level": 10},
    {"item_name": "Matcha", "unit_price": 2.5, "stock_level": 15},
    {"item_name": "Bagel", "unit_price": 5.0, "stock_level": 7},
    {"item_name": "Brownie", "unit_price": 4.0, "stock_level": 5}
]

active_orders = []
total_revenue = 0.0  

def find_item_by_name(search_query):
    
    for item in inventory_menu:
        if item["item_name"].lower() == search_query.lower():
            return item
    return None

def display_inventory():
    
    print("\n" + "="*30)
    print(f"{'ITEM':<12} | {'PRICE':<7} | {'STOCK'}")
    print("-" * 30)
    for item in inventory_menu:
        status = "In Stock" if item["stock_level"] > 0 else "SOLD OUT"
        print(f"{item['item_name']:<12} | ${item['unit_price']:<6.2f} | {item['stock_level']} ({status})")
    print("="*30 + "\n")

def process_new_order():
    """Handles the logic for taking a new customer order."""
    display_inventory()
    target_name = input("Enter item name to order: ").strip()
    target_item = find_item_by_name(target_name)

    if not target_item:
        print(">> Error: Item not found in menu.")
        return

    if target_item["stock_level"] <= 0:
        print(f">> Error: {target_item['item_name']} is currently out of stock.")
        return

    try:
        requested_qty = int(input(f"Enter quantity (Available: {target_item['stock_level']}): "))
        if 0 < requested_qty <= target_item["stock_level"]:
            # Update stock and add to active orders
            target_item["stock_level"] -= requested_qty
            order_entry = {
                "item_name": target_item["item_name"], 
                "quantity": requested_qty,
                "subtotal": requested_qty * target_item["unit_price"]
            }
            active_orders.append(order_entry)
            print(f">> Success: Added {requested_qty}x {target_item['item_name']} to orders.")
        else:
            print(">> Error: Invalid quantity amount.")
    except ValueError:
        print(">> Error: Please enter a whole number for quantity.")

def manage_order_completion():
    
    global total_revenue
    if not active_orders:
        print(">> No pending orders to process.")
        return

    print("\n--- Pending Orders ---")
    for i, order in enumerate(active_orders, 1):
        print(f"{i}. {order['quantity']}x {order['item_name']} - ${order['subtotal']:.2f}")

    try:
        idx = int(input("\nEnter order # to complete (0 to go back): ")) - 1
        if idx == -1: return

        if 0 <= idx < len(active_orders):
            selected_order = active_orders.pop(idx)
            is_cancelled = input("Was this order cancelled? (y/n): ").lower()
            
            if is_cancelled == 'y':
                # Restore stock if cancelled
                item = find_item_by_name(selected_order["item_name"])
                item["stock_level"] += selected_order["quantity"]
                print(">> Order cancelled. Stock replenished.")
            else:
                # Add to total revenue if successful
                total_revenue += selected_order["subtotal"]
                print(f">> Order marked as Complete. Total Revenue: ${total_revenue:.2f}")
        else:
            print(">> Error: Invalid order selection.")
    except ValueError:
        print(">> Error: Please enter a valid order number.")

def run_system():
    
    while True:
        print("\n--- CAFÉ MANAGEMENT SYSTEM ---")
        print("1. View Menu & Stock")
        print("2. Search for Item")
        print("3. Place New Order")
        print("4. Complete/Cancel Order")
        print("5. View Total Revenue") # Extra feature
        print("6. Exit")
        
        user_choice = input("Select an option (1-6): ")

        if user_choice == "1":
            display_inventory()
        elif user_choice == "2":
            query = input("Search item: ")
            match = find_item_by_name(query)
            if match:
                print(f"Result: {match['item_name']} - ${match['unit_price']} | Stock: {match['stock_level']}")
            else:
                print("No match found.")
        elif user_choice == "3":
            process_new_order()
        elif user_choice == "4":
            manage_order_completion()
        elif user_choice == "5":
            print(f"\n>> Total Revenue for this session: ${total_revenue:.2f}")
        elif user_choice == "6":
            print("Shutting down system. Goodbye!")
            break
        else:
            print(">> Invalid input. Please select 1-6.")


if __name__ == "__main__":
    run_system()