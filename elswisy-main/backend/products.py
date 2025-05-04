from backend.database import get_db_connection, close_db_connection
from mysql.connector import Error

# Product-related database functions

def get_all_products():
    """
    Fetch all products with their category names.
    Returns:
        list of dict: Each dict contains product info and category name.
    """
    connection = get_db_connection()
    products = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            # Join products with categories to get category name
            cursor.execute('''
                SELECT p.id, p.name, p.description, p.price, p.stock, p.image_path, c.name AS category
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
            ''')
            products = cursor.fetchall()
        except Error as e:
            print(f"Error fetching products: {str(e)}")
        finally:
            close_db_connection(connection)
    return products

def add_product(name, price, stock, description=None, category_id=None, image_path=None):
    """
    Add a new product to the products table.
    Args:
        name (str): Product name (required).
        price (float): Product price (required).
        stock (int): Stock quantity (required).
        description (str, optional): Product description.
        category_id (int, optional): Category ID (foreign key).
        image_path (str, optional): Path or URL to product image.
    Returns:
        tuple: (success (bool), message (str), product_id (int or None))
    """
    connection = get_db_connection()
    product_id = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO products (name, description, price, stock, category_id, image_path)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (name, description, price, stock, category_id, image_path)
            )
            connection.commit()
            product_id = cursor.lastrowid
            return True, "Product added successfully", product_id
        except Error as e:
            return False, f"Error: {str(e)}", None
        finally:
            close_db_connection(connection)
    return False, "Database connection failed", None

def get_product_by_id(product_id):
    """
    Fetch a single product by its ID (with category name).
    Args:
        product_id (int): The product's unique ID.
    Returns:
        dict or None: Product info if found, else None.
    """
    connection = get_db_connection()
    product = None
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.id, p.name, p.description, p.price, p.stock, p.image_path, c.name AS category
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.id = %s
            ''', (product_id,))
            product = cursor.fetchone()
        except Error as e:
            print(f"Error fetching product by ID: {str(e)}")
        finally:
            close_db_connection(connection)
    return product

def search_products_by_name(name):
    """
    Search for products by (partial) name match.
    Args:
        name (str): The search string (case-insensitive, partial match).
    Returns:
        list of dict: Matching products with category names.
    """
    connection = get_db_connection()
    products = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute('''
                SELECT p.id, p.name, p.description, p.price, p.stock, p.image_path, c.name AS category
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.id
                WHERE p.name LIKE %s
            ''', (f"%{name}%",))
            products = cursor.fetchall()
        except Error as e:
            print(f"Error searching products by name: {str(e)}")
        finally:
            close_db_connection(connection)
    return products

def get_category_id_by_name(name):
    """Get category ID by name."""
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM categories WHERE name = %s", (name,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Error getting category ID: {str(e)}")
        finally:
            close_db_connection(connection)
    return None

if __name__ == "__main__":
    # Sample products for each category
    products_to_add = [
        # Clothes
        {
            "name": "Classic White T-Shirt",
            "description": "Comfortable cotton t-shirt perfect for everyday wear",
            "price": 19.99,
            "stock": 50,
            "category": "Clothes",
            "image_path": "clothes/white_tshirt.jpg"
        },
        {
            "name": "Blue Denim Jeans",
            "description": "Classic fit blue jeans with comfortable stretch",
            "price": 59.99,
            "stock": 30,
            "category": "Clothes",
            "image_path": "clothes/blue_jeans.jpg"
        },
        # Bags
        {
            "name": "Urban Backpack",
            "description": "Spacious backpack with laptop compartment",
            "price": 45.99,
            "stock": 25,
            "category": "Bags",
            "image_path": "bags/urban_backpack.jpg"
        },
        {
            "name": "Leather Tote Bag",
            "description": "Elegant leather tote perfect for work",
            "price": 79.99,
            "stock": 15,
            "category": "Bags",
            "image_path": "bags/leather_tote.jpg"
        },
        # Footwear
        {
            "name": "Running Sneakers",
            "description": "Lightweight and comfortable running shoes",
            "price": 89.99,
            "stock": 40,
            "category": "Footwear",
            "image_path": "footwear/running_sneakers.jpg"
        },
        {
            "name": "Classic Leather Boots",
            "description": "Durable leather boots for all occasions",
            "price": 129.99,
            "stock": 20,
            "category": "Footwear",
            "image_path": "footwear/leather_boots.jpg"
        },
        # Accessories
        {
            "name": "Silver Watch",
            "description": "Elegant silver watch with leather strap",
            "price": 149.99,
            "stock": 15,
            "category": "Accessories",
            "image_path": "accessories/silver_watch.jpg"
        },
        {
            "name": "Leather Belt",
            "description": "Classic brown leather belt",
            "price": 34.99,
            "stock": 35,
            "category": "Accessories",
            "image_path": "accessories/leather_belt.jpg"
        },
        # Electronics
        {
            "name": "Wireless Earbuds",
            "description": "High-quality wireless earbuds with noise cancellation",
            "price": 129.99,
            "stock": 30,
            "category": "Electronics",
            "image_path": "electronics/wireless_earbuds.jpg"
        },
        {
            "name": "Smart Watch",
            "description": "Feature-rich smartwatch with health tracking",
            "price": 199.99,
            "stock": 20,
            "category": "Electronics",
            "image_path": "electronics/smart_watch.jpg"
        }
    ]
    
    print("Adding products:")
    for product in products_to_add:
        # Get category ID
        category_id = get_category_id_by_name(product["category"])
        if category_id:
            # Add product
            success, message, product_id = add_product(
                name=product["name"],
                description=product["description"],
                price=product["price"],
                stock=product["stock"],
                category_id=category_id,
                image_path=product["image_path"]
            )
            print(f"Adding {product['name']}: {message}")
        else:
            print(f"Category not found: {product['category']}")
    
    print("\nAll products after adding:")
    all_products = get_all_products()
    for product in all_products:
        print(f"- {product['name']} ({product['category']}): ${product['price']}")


