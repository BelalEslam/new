from database import get_db_connection, close_db_connection
from mysql.connector import Error

def admin_login(username, password):
    """
    Authenticate an admin user by username and password.
    Args:
        username (str): The admin's username.
        password (str): The admin's password (should be hashed in production).
    Returns:
        tuple: (success (bool), message (str))
    """
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id FROM admins WHERE username = %s AND password = %s",
                (username, password)
            )
            if cursor.fetchone():
                return True, "Admin login successful"
            return False, "Invalid admin username or password"
        except Error as e:
            return False, f"Error: {str(e)}"
        finally:
            close_db_connection(connection)
    return False, "Database connection failed"

# Example usage
if __name__ == "__main__":
    success, message = admin_login('hesham', '1234')
    print(f"Success: {success}, Message: {message}") 