from backend.database import get_db_connection, close_db_connection
from mysql.connector import Error

def add_category(name, description=None):
    """
    Add a new category to the categories table.
    Args:
        name (str): Category name (required, must be unique).
        description (str, optional): Category description.
    Returns:
        tuple: (success (bool), message (str), category_id (int or None))
    """
    connection = get_db_connection()
    category_id = None
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO categories (name, description) VALUES (%s, %s)",
                (name, description)
            )
            connection.commit()
            category_id = cursor.lastrowid
            return True, "Category added successfully", category_id
        except Error as e:
            return False, f"Error: {str(e)}", None
        finally:
            close_db_connection(connection)
    return False, "Database connection failed", None

def get_all_categories():
    """
    Get all categories from the database.
    Returns:
        list: List of dictionaries containing category information.
    """
    connection = get_db_connection()
    categories = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()
        except Error as e:
            print(f"Error: {str(e)}")
        finally:
            close_db_connection(connection)
    return categories

if __name__ == "__main__":
    # First, let's see what categories we already have
    print("Current categories:")
    existing_categories = get_all_categories()
    for cat in existing_categories:
        print(f"- {cat['name']}")
    
    # Categories to add
    categories_to_add = [
        {
            "name": "Clothes",
            "description": "Stylish and comfortable clothing including t-shirts, jeans, dresses, and more."
        },
        {
            "name": "Bags",
            "description": "Fashionable and functional bags including backpacks, handbags, and travel bags."
        },
        {
            "name": "Footwear",
            "description": "Quality footwear including sneakers, formal shoes, sandals, and boots."
        },
        {
            "name": "Accessories",
            "description": "Fashion accessories including jewelry, watches, belts, and more."
        },
        {
            "name": "Electronics",
            "description": "Latest gadgets and electronic devices including smartphones, laptops, tablets, and accessories."
        }
    ]
    
    # Try to add each category
    print("\nAdding categories:")
    for category in categories_to_add:
        success, message, category_id = add_category(
            name=category["name"],
            description=category["description"]
        )
        print(f"Adding {category['name']}: {message}") 