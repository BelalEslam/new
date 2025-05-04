from backend.database import get_db_connection, close_db_connection
from mysql.connector import Error

def create_order(user_id, items, shipper_id=None):
    """
    Create a new order for a user.
    Args:
        user_id (int): The ID of the user placing the order.
        items (list of dict): Each dict must have 'product_id' and 'quantity'.
        shipper_id (int, optional): The ID of the shipper. Can be None.
    Returns:
        tuple: (success (bool), message (str), order_id (int or None))
    """
    connection = get_db_connection()  # Open a new database connection
    order_id = None
    if connection:
        try:
            cursor = connection.cursor()
            # Calculate the total price for the order by summing up each product's price * quantity
            total_price = 0
            for item in items:
                # Get the price of the product from the products table
                cursor.execute("SELECT price FROM products WHERE id = %s", (item['product_id'],))
                result = cursor.fetchone()
                if not result:
                    # If the product does not exist, return an error
                    return False, f"Product ID {item['product_id']} not found", None
                total_price += float(result[0]) * item['quantity']
            # Insert the new order into the orders table
            cursor.execute(
                "INSERT INTO orders (user_id, total_price, shipper_id) VALUES (%s, %s, %s)",
                (user_id, total_price, shipper_id)
            )
            order_id = cursor.lastrowid  # Get the ID of the newly created order
            # Insert each item into the order_items table
            for item in items:
                # Calculate the total price for this item (price * quantity)
                cursor.execute(
                    "SELECT price FROM products WHERE id = %s", (item['product_id'],))
                product_price = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (%s, %s, %s, %s)",
                    (order_id, item['product_id'], item['quantity'], float(item['quantity']) * float(product_price))
                )
            connection.commit()  # Commit all changes to the database
            return True, "Order created successfully", order_id
        except Error as e:
            # Handle any database errors
            return False, f"Error: {str(e)}", None
        finally:
            close_db_connection(connection)  # Always close the connection
    return False, "Database connection failed", None

