from backend.database import get_db_connection, close_db_connection
from mysql.connector import Error

class Auth:
    """
    Authentication class for user signup and login.
    Uses the 'users' table in the database.
    """
    def __init__(self):
        # Open a new database connection for this instance
        self.connection = get_db_connection()
        self.current_user = None
        self.current_username = None
        
    def __del__(self):
        # Ensure the connection is closed when the object is deleted
        if self.connection:
            close_db_connection(self.connection)
    
    def signup(self, username, password, email, address=None, name=None, phone_number=None):
        """
        Register a new user.
        Args:
            username (str): The user's username (must be unique).
            password (str): The user's password (should be hashed in production).
            email (str): The user's email (must be unique).
            address (str, optional): The user's address.
            name (str, optional): The user's full name.
            phone_number (str, optional): The user's phone number.
        Returns:
            tuple: (success (bool), message (str))
        """
        if not self.connection or not self.connection.is_connected():
            return False, "Database connection error. Please try again later."
            
        try:
            cursor = self.connection.cursor()
            # Insert the new user into the users table
            cursor.execute(
                "INSERT INTO users (username, password, email, address, name, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                (username, password, email, address, name, phone_number)
            )
            self.connection.commit()
            return True, "User registered successfully"
        except Error as e:
            # Handle duplicate username/email or other DB errors
            return False, f"Error: {str(e)}"
    
    def login(self, username_or_email, password):
        """
        Authenticate a user by username or email and password.
        Args:
            username_or_email (str): The user's username or email.
            password (str): The user's password.
        Returns:
            tuple: (success (bool), message (str))
        """
        if not self.connection or not self.connection.is_connected():
            return False, "Database connection error. Please try again later."
            
        try:
            cursor = self.connection.cursor(dictionary=True)
            # Check if a user exists with the given username/email and password
            cursor.execute(
                "SELECT id, username, email, name FROM users WHERE (username = %s OR email = %s) AND password = %s",
                (username_or_email, username_or_email, password)
            )
            user = cursor.fetchone()
            if user:
                self.current_user = user
                self.current_username = user['username']
                return True, "Login successful"
            return False, "Invalid username/email or password"
        except Error as e:
            return False, f"Error: {str(e)}"
            
    def logout(self):
        """Log out the current user."""
        self.current_user = None
        self.current_username = None 
        