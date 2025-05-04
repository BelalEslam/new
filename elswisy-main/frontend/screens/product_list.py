# ui/product_list.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import backend functions for database operations
from backend.database import get_db_connection, close_db_connection
from backend.products import get_all_products, get_product_by_id, search_products_by_name
from mysql.connector import Error
from frontend.utils.constants import (
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR, BACKGROUND_COLOR,
    CARD_BACKGROUND, TEXT_COLOR, SUCCESS_COLOR, WARNING_COLOR,
    BORDER_COLOR, DISABLED_COLOR, TITLE_FONT, HEADER_FONT,
    BODY_FONT, SMALL_FONT
)
from frontend.utils.image_utils import load_product_image
from frontend.screens.cart_screen import CartScreen

class ProductListScreen(tk.Frame):
    def __init__(self, master, auth):
        super().__init__(master)
        self.connection = None
        self.auth = auth
        self.connect()
        self.configure(bg=BACKGROUND_COLOR)
        
        # Initialize cart screen
        self.cart_screen = CartScreen(master, self.show_products)
        self.cart_screen.grid(row=0, column=0, sticky="nsew")
        self.cart_screen.grid_remove()  # Hide cart screen initially
        
        # Dictionary to store quantity variables for each product
        self.quantity_vars = {}
        self.cart_items = []
        
        # Get current user's name
        self.current_user = self.get_current_user()
        
        # Configure root window to expand
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main container with padding
        main_container = tk.Frame(self, bg=BACKGROUND_COLOR)
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)

        # Header section with improved design
        header_frame = tk.Frame(main_container, bg=BACKGROUND_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        header_frame.grid_columnconfigure(1, weight=1)

        # Left header with logo and user info
        left_header = tk.Frame(header_frame, bg=BACKGROUND_COLOR)
        left_header.grid(row=0, column=0, sticky="w")
        
        # Logo with improved styling
        logo_frame = tk.Frame(left_header, bg=PRIMARY_COLOR, padx=15, pady=10)
        logo_frame.pack(side="left", padx=(0, 20))
        
        logo = tk.Label(logo_frame, text="CartX", font=TITLE_FONT,
                       bg=PRIMARY_COLOR, fg="white")
        logo.pack()

        # User info section
        user_frame = tk.Frame(left_header, bg=BACKGROUND_COLOR)
        user_frame.pack(side="left", padx=20)
        
        user_icon = tk.Label(user_frame, text="👤", font=HEADER_FONT,
                           bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
        user_icon.pack(side="left", padx=(0, 5))
        
        # Display actual username
        display_name = self.current_user if self.current_user and self.current_user != 'None' else 'User'
        self.user_name_label = tk.Label(user_frame, 
                                      text=f"Welcome, {display_name}",
                                      font=BODY_FONT,
                                      bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.user_name_label.pack(side="left")

        # Right header with search and cart
        right_header = tk.Frame(header_frame, bg=BACKGROUND_COLOR)
        right_header.grid(row=0, column=1, sticky="e")
        
        # Search bar with improved design
        search_frame = tk.Frame(right_header, bg=BACKGROUND_COLOR)
        search_frame.pack(side="left", padx=10)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda name, index, mode: self.filter_products())
        
        search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                              font=BODY_FONT, bg=CARD_BACKGROUND,
                              fg=TEXT_COLOR, relief="solid",
                              bd=1)
        search_entry.pack(side="left", padx=5)
        
        search_icon = tk.Label(search_frame, text="🔍", font=BODY_FONT,
                             bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
        search_icon.pack(side="left")
        
        # Cart button with improved design
        cart_button = tk.Button(right_header, text="🛒 Cart",
                              font=HEADER_FONT, bg=PRIMARY_COLOR,
                              fg="white", command=self.show_cart,
                              relief="flat", padx=15, pady=5)
        cart_button.pack(side="left", padx=10)

        # Create products container
        self.products_container = tk.Frame(main_container, bg=BACKGROUND_COLOR)
        self.products_container.grid(row=1, column=0, sticky="nsew")
        self.products_container.grid_columnconfigure(0, weight=1)
        self.products_container.grid_rowconfigure(0, weight=1)

        # Create scrollable canvas for products
        self.canvas = tk.Canvas(self.products_container, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.products_container, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Create frame inside canvas for products
        self.products_frame = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)
        self.products_frame_id = self.canvas.create_window((0, 0), window=self.products_frame, anchor="nw")

        # Bind canvas resize
        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.products_frame.bind("<Configure>", self.on_frame_configure)

        # Load products
        self.update_product_grid()

    def select_category(self, category):
        """Handle category selection"""
        for btn in self.category_buttons.values():
            btn['relief'] = 'flat'
        self.category_buttons[category]['relief'] = 'sunken'
        self.filter_products()

    def filter_products(self):
        """Filter products based on search text"""
        search_text = self.search_var.get().strip()
        
        if search_text:
            # Use the backend search function
            products = search_products_by_name(search_text)
        else:
            # If search is empty, show all products
            products = get_all_products()
            
        # Update the product grid with filtered results
        self.update_product_grid(products)
        
        # Update canvas scroll region
        self.products_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_resize(self, event):
        # Make the products_frame always match the canvas width
        self.canvas.itemconfig(self.products_frame_id, width=event.width)

    def on_frame_configure(self, event):
        # Update scrollregion to fit the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_product_grid(self, products=None):
        """Update the product grid with the given products"""
        if products is None:
            products = get_all_products()
            
        # Clear existing products
        for widget in self.products_frame.winfo_children():
            widget.destroy()
        
        # Calculate number of columns based on window width
        window_width = self.winfo_width()
        num_columns = max(3, window_width // 300)  # Minimum 3 columns
        
        # Map product names to their corresponding image files
        image_mapping = {
            "Classic White T-Shirt": "beige T-shirt.jpg",
            "Blue Denim Jeans": "burgandy jack .jpeg",
            "Urban Backpack": "black laptop bag.jpg",
            "Leather Tote Bag": "blue bag.jpg",
            "Running Sneakers": "newbalance sneakers.jpg",
            "Classic Leather Boots": "men brown sneakers.webp",
            "Silver Watch": "black laptop bag.jpg",  # Using bag as placeholder
            "Leather Belt": "brown bag.jpg",  # Using bag as placeholder
            "Wireless Earbuds": "blue bag.jpg",  # Using bag as placeholder
            "Smart Watch": "black laptop bag.jpg"  # Using bag as placeholder
        }
        
        # Create product cards
        for i, product in enumerate(products):
            row = i // num_columns
            col = i % num_columns
            
            # Create product card with improved styling
            card_frame = tk.Frame(self.products_frame, bg=CARD_BACKGROUND,
                                bd=1, relief="solid", padx=15, pady=15)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Product image container
            image_frame = tk.Frame(card_frame, bg=CARD_BACKGROUND, height=200)
            image_frame.pack(fill="x", pady=(0, 15))
            
            # Load and display product image
            image_file = image_mapping.get(product['name'], "Logo.png")
            print(f"Debug - Loading image for product: {product['name']}")
            print(f"Debug - Using image file: {image_file}")
            image = load_product_image(product['name'], image_file)
            if image:
                image_label = tk.Label(image_frame, image=image, bg=CARD_BACKGROUND)
                image_label.image = image  # Keep a reference to prevent garbage collection
                image_label.pack(expand=True)
            else:
                print(f"Debug - Failed to load image for product: {product['name']}")
            
            # Product details container
            details_frame = tk.Frame(card_frame, bg=CARD_BACKGROUND)
            details_frame.pack(fill="x", pady=(0, 10))
            
            # Product name with improved styling
            name_label = tk.Label(details_frame, text=product['name'],
                                font=("Inter", 14, "bold"),
                                bg=CARD_BACKGROUND, fg=TEXT_COLOR,
                                wraplength=250)
            name_label.pack(anchor="w", pady=(0, 5))
            
            # Product category with icon
            category_frame = tk.Frame(details_frame, bg=CARD_BACKGROUND)
            category_frame.pack(fill="x", pady=(0, 5))
            
            category_icon = tk.Label(category_frame, text="🏷️", font=("Inter", 10),
                                   bg=CARD_BACKGROUND, fg=TEXT_COLOR)
            category_icon.pack(side="left", padx=(0, 5))
            
            category_label = tk.Label(category_frame, text=product['category'],
                                    font=("Inter", 10),
                                    bg=CARD_BACKGROUND, fg=TEXT_COLOR)
            category_label.pack(side="left")
            
            # Product price with improved styling
            price_frame = tk.Frame(details_frame, bg=CARD_BACKGROUND)
            price_frame.pack(fill="x", pady=(0, 5))
            
            price_icon = tk.Label(price_frame, text="💰", font=("Inter", 10),
                                bg=CARD_BACKGROUND, fg=TEXT_COLOR)
            price_icon.pack(side="left", padx=(0, 5))
            
            price_label = tk.Label(price_frame, text=f"${product['price']:.2f}",
                                 font=("Inter", 16, "bold"),
                                 bg=CARD_BACKGROUND, fg=PRIMARY_COLOR)
            price_label.pack(side="left")
            
            # Stock status with icon
            stock_frame = tk.Frame(details_frame, bg=CARD_BACKGROUND)
            stock_frame.pack(fill="x", pady=(0, 10))
            
            stock_icon = tk.Label(stock_frame, text="📦", font=("Inter", 10),
                                bg=CARD_BACKGROUND, fg=TEXT_COLOR)
            stock_icon.pack(side="left", padx=(0, 5))
            
            stock_color = SUCCESS_COLOR if product['stock'] > 10 else WARNING_COLOR
            stock_label = tk.Label(stock_frame, text=f"Stock: {product['stock']}",
                                 font=("Inter", 10),
                                 bg=CARD_BACKGROUND, fg=stock_color)
            stock_label.pack(side="left")
            
            # Quantity controls with improved styling
            quantity_frame = tk.Frame(card_frame, bg=CARD_BACKGROUND)
            quantity_frame.pack(fill="x", pady=(0, 10))
            
            # Store quantity variable
            self.quantity_vars[product['id']] = tk.StringVar(value="1")
            
            # Decrease button
            decrease_btn = tk.Button(quantity_frame, text="-",
                                   font=("Inter", 10, "bold"),
                                   bg=PRIMARY_COLOR, fg="white",
                                   relief="flat",
                                   command=lambda p=product: self.update_quantity(p['id'], -1))
            decrease_btn.pack(side="left", padx=5)
            
            # Quantity display
            quantity_label = tk.Label(quantity_frame,
                                    textvariable=self.quantity_vars[product['id']],
                                    font=("Inter", 10),
                                    bg=CARD_BACKGROUND, fg=TEXT_COLOR,
                                    width=3)
            quantity_label.pack(side="left", padx=5)
            
            # Increase button
            increase_btn = tk.Button(quantity_frame, text="+",
                                   font=("Inter", 10, "bold"),
                                   bg=PRIMARY_COLOR, fg="white",
                                   relief="flat",
                                   command=lambda p=product: self.update_quantity(p['id'], 1))
            increase_btn.pack(side="left", padx=5)
            
            # Add to Cart button with improved styling
            add_cart_btn = tk.Button(card_frame, text="Add to Cart 🛒",
                                   font=("Inter", 12, "bold"),
                                   bg=PRIMARY_COLOR, fg="white",
                                   relief="flat",
                                   command=lambda p=product: self.add_to_cart(p, int(self.quantity_vars[p['id']].get())))
            add_cart_btn.pack(fill="x", pady=(5, 0))
            
            # Configure grid weights
            self.products_frame.grid_columnconfigure(col, weight=1)
            self.products_frame.grid_rowconfigure(row, weight=1)
            
        # Update canvas scroll region
        self.products_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def connect(self):
        """Establish a new database connection using backend function"""
        try:
            if not self.connection or not self.connection.is_connected():
                self.connection = get_db_connection()  # Backend function call
                if not self.connection:
                    raise Exception("Failed to connect to database")
        except Error as e:
            print(f"Error connecting to database: {e}")
            raise

    def __del__(self):
        """Close database connection using backend function"""
        if self.connection and self.connection.is_connected():
            close_db_connection(self.connection)  # Backend function call

    def update_quantity(self, product_id, change):
        """Update the quantity for a product"""
        if product_id in self.quantity_vars:
            current_quantity = int(self.quantity_vars[product_id].get())
            new_quantity = max(1, current_quantity + change)  # Ensure quantity is at least 1
            self.quantity_vars[product_id].set(str(new_quantity))

    def add_to_cart(self, product, quantity=1):
        """Add product to cart with specified quantity and show success message"""
        try:
            if product["stock"] <= 0:
                messagebox.showwarning("Out of Stock", "This product is currently out of stock.")
                return
                
            if quantity > product["stock"]:
                messagebox.showwarning("Insufficient Stock", 
                                     f"Only {product['stock']} items available in stock.")
                return
                
            # Add the product to cart with the specified quantity
            for _ in range(quantity):
                self.cart_screen.add_to_cart(product)
                
            messagebox.showinfo("Added to Cart", f"{quantity} {product['name']}(s) added to cart!")
            # Reset quantity to 1 after adding to cart
            self.quantity_vars[product["id"]].set("1")
        except Exception as e:
            print(f"Error adding product to cart: {e}")
            messagebox.showerror("Error", "Failed to add product to cart. Please try again.")

    def show_cart(self):
        """Show the cart screen"""
        self.grid_remove()
        self.cart_screen.grid()

    def show_products(self):
        """Show the products screen"""
        self.cart_screen.grid_remove()
        self.grid()
        # Refresh the user name in case it changed
        try:
            self.current_user = self.get_current_user()
            self.user_name_label.config(text=f"Welcome, {self.current_user}")
        except Exception as e:
            print(f"Error updating user name: {e}")

    def get_current_user(self):
        """Get the current user's name from the Auth instance"""
        if self.auth and self.auth.current_user:
            return self.auth.current_user.get('name', self.auth.current_user.get('username', 'User'))
        return "User"
