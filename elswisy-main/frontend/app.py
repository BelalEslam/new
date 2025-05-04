import os
import sys
import tkinter as tk
import tkinter.messagebox as messagebox

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.screens.login_screen import LoginScreen
from frontend.screens.signup_screen import SignupScreen
from frontend.screens.product_list import ProductListScreen

class EcommerceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure the main window
        self.title("CartX - Ecommerce App")
        self.geometry("1200x800")
        self.minsize(800, 600)
        
        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Initialize screens
        self.login_screen = LoginScreen(self, self.show_products, self.show_signup)
        self.signup_screen = SignupScreen(self, self.show_login)
        self.product_screen = None  # Will be initialized when needed
        
        # Show login screen by default
        self.show_login()
    
    def show_login(self):
        """Show the login screen and hide others."""
        if self.product_screen:
            self.product_screen.grid_remove()
        self.signup_screen.grid_remove()
        self.login_screen.grid(row=0, column=0, sticky="nsew")
    
    def show_signup(self):
        """Show the signup screen and hide others."""
        if self.product_screen:
            self.product_screen.grid_remove()
        self.login_screen.grid_remove()
        self.signup_screen.grid(row=0, column=0, sticky="nsew")
    
    def show_products(self):
        """Show the products screen and hide others."""
        if not self.login_screen.auth:
            messagebox.showerror("Error", "Authentication system not initialized")
            return
            
        if not self.login_screen.auth.current_user:
            messagebox.showerror("Error", "Please login first")
            return
            
        # Create new product screen if it doesn't exist
        if not self.product_screen:
            self.product_screen = ProductListScreen(self, self.login_screen.auth)
            
        # Hide other screens
        self.login_screen.grid_remove()
        self.signup_screen.grid_remove()
        
        # Show product screen
        self.product_screen.grid(row=0, column=0, sticky="nsew")
        self.product_screen.tkraise()  # Bring to front

if __name__ == "__main__":
    app = EcommerceApp()
    app.mainloop() 