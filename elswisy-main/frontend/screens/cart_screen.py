import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import backend functions for order creation
from backend.orders import create_order
from frontend.utils.constants import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    CARD_BACKGROUND, CARD_BORDER, ACCENT_COLOR
)
from frontend.utils.image_utils import load_product_image

class CartScreen(tk.Frame):
    def __init__(self, master, switch_to_products):
        super().__init__(master)
        self.switch_to_products = switch_to_products
        self.configure(bg=BACKGROUND_COLOR)
        
        # Configure the main frame to expand
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create main container with padding
        main_container = tk.Frame(self, bg=BACKGROUND_COLOR, padx=20, pady=20)
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(2, weight=1)

        # Header section
        header_frame = tk.Frame(main_container, bg=BACKGROUND_COLOR)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)

        # CartX Logo and Back button
        left_header = tk.Frame(header_frame, bg=BACKGROUND_COLOR)
        left_header.grid(row=0, column=0, sticky="w")
        
        back_button = tk.Button(left_header, text="← Back to Products", 
                              font=("Helvetica", 12),
                              bg=PRIMARY_COLOR, fg="white",
                              activebackground="#0056b3", activeforeground="white",
                              command=self.switch_to_products)
        back_button.pack(side="left", padx=(0, 20))

        # Cart title
        title_frame = tk.Frame(header_frame, bg=BACKGROUND_COLOR)
        title_frame.grid(row=0, column=1, sticky="e")
        
        title = tk.Label(title_frame, text="Your Cart", font=("Helvetica", 28, "bold"),
                        bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
        title.pack(side="right")

        # Content area with scrollbar
        content_frame = tk.Frame(main_container, bg=BACKGROUND_COLOR)
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Create canvas and scrollbar
        self.canvas = tk.Canvas(content_frame, bg=BACKGROUND_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)

        # Configure scrollable frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window in canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=self.canvas.winfo_reqwidth())
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Footer section with total and checkout button
        footer_frame = tk.Frame(main_container, bg=BACKGROUND_COLOR)
        footer_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        footer_frame.grid_columnconfigure(1, weight=1)

        # Total amount
        self.total_label = tk.Label(footer_frame, text="Total: $0.00", 
                                  font=("Helvetica", 16, "bold"),
                                  bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
        self.total_label.grid(row=0, column=0, sticky="w")

        # Checkout button
        checkout_button = tk.Button(footer_frame, text="Proceed to Checkout",
                                  font=("Helvetica", 14, "bold"),
                                  bg=ACCENT_COLOR, fg="white",
                                  activebackground="#1e7e34", activeforeground="white",
                                  command=self.proceed_to_checkout)
        checkout_button.grid(row=0, column=1, sticky="e", padx=(20, 0))

        # Initialize cart items (temporary storage until checkout)
        self.cart_items = []
        self.update_cart_display()

    def add_to_cart(self, product):
        """Add a product to the temporary cart storage"""
        # Check if product is already in cart
        for item in self.cart_items:
            if item["product_id"] == product["id"]:
                item["quantity"] += 1
                self.update_cart_display()
                return

        # Add new item to cart
        self.cart_items.append({
            "product_id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "quantity": 1
        })
        self.update_cart_display()

    def remove_from_cart(self, product_id):
        """Remove a product from the temporary cart storage"""
        self.cart_items = [item for item in self.cart_items if item["product_id"] != product_id]
        self.update_cart_display()

    def update_quantity(self, product_id, new_quantity):
        """Update the quantity of a product in the temporary cart storage"""
        for item in self.cart_items:
            if item["product_id"] == product_id:
                if new_quantity <= 0:
                    self.remove_from_cart(product_id)
                else:
                    item["quantity"] = new_quantity
                break
        self.update_cart_display()

    def update_cart_display(self):
        """Update the cart display with current items from temporary storage"""
        # Clear existing items
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not self.cart_items:
            # Show empty cart message with icon
            empty_icon = tk.Label(self.scrollable_frame, text="🛒", font=("Helvetica", 48), bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR)
            empty_icon.pack(pady=(50, 10))
            empty_label = tk.Label(self.scrollable_frame, 
                                 text="Your cart is empty",
                                 font=("Helvetica", 16),
                                 bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
            empty_label.pack()
            self.total_label.config(text="Total: $0.00")
            return

        # Calculate total
        total = sum(item["price"] * item["quantity"] for item in self.cart_items)
        self.total_label.config(text=f"Total: ${total:.2f}")

        for item in self.cart_items:
            item_frame = tk.Frame(self.scrollable_frame, bg=CARD_BACKGROUND, bd=1, relief="solid")
            item_frame.pack(fill="x", padx=20, pady=10)

            # Remove button (small icon, top-right)
            remove_button = tk.Button(item_frame, text="✕", font=("Helvetica", 10, "bold"),
                                    bg="#dc3545", fg="white", bd=0, relief="flat",
                                    command=lambda p_id=item["product_id"]: self.remove_from_cart(p_id))
            remove_button.place(relx=1.0, rely=0.0, anchor="ne", x=-5, y=5)

            # Product image (if available)
            image = load_product_image(item["name"], item.get("image_path", None))
            if image:
                image_label = tk.Label(item_frame, image=image, bg=CARD_BACKGROUND)
                image_label.image = image
                image_label.pack(side="left", padx=10, pady=10)

            # Product info
            info_frame = tk.Frame(item_frame, bg=CARD_BACKGROUND)
            info_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

            name_label = tk.Label(info_frame, text=item["name"],
                              font=("Helvetica", 12, "bold"),
                              bg=CARD_BACKGROUND, fg=TEXT_COLOR)
            name_label.pack(anchor="w")

            price_label = tk.Label(info_frame, text=f"${item['price']:.2f}",
                               font=("Helvetica", 12),
                               bg=CARD_BACKGROUND, fg=PRIMARY_COLOR)
            price_label.pack(anchor="w")

            # Quantity controls (+ and - buttons)
            quantity_frame = tk.Frame(item_frame, bg=CARD_BACKGROUND)
            quantity_frame.pack(side="right", padx=20, pady=10)

            decrease_btn = tk.Button(quantity_frame, text="-", font=("Helvetica", 12, "bold"),
                                    bg=PRIMARY_COLOR, fg="white", width=2, relief="flat",
                                    command=lambda p_id=item["product_id"]: self.update_quantity(p_id, item["quantity"] - 1))
            decrease_btn.pack(side="left", padx=2)

            quantity_label = tk.Label(quantity_frame, text=str(item["quantity"]), font=("Helvetica", 12),
                                    bg=CARD_BACKGROUND, fg=TEXT_COLOR, width=3)
            quantity_label.pack(side="left", padx=2)

            increase_btn = tk.Button(quantity_frame, text="+", font=("Helvetica", 12, "bold"),
                                    bg=PRIMARY_COLOR, fg="white", width=2, relief="flat",
                                    command=lambda p_id=item["product_id"]: self.update_quantity(p_id, item["quantity"] + 1))
            increase_btn.pack(side="left", padx=2)

        # Sticky footer for checkout (already present, but ensure it's always visible)
        self.master.update_idletasks()
        self.master.after(100, lambda: self.master.winfo_toplevel().geometry(f"{self.master.winfo_width()}x{self.master.winfo_height()}"))

    def proceed_to_checkout(self):
        """Handle the checkout process by creating an order in the database"""
        if not self.cart_items:
            messagebox.showwarning("Empty Cart", "Your cart is empty. Add some products first!")
            return

        try:
            # Prepare items for order creation
            order_items = [{
                "product_id": item["product_id"],
                "quantity": item["quantity"]
            } for item in self.cart_items]

            # Create order in database using backend function
            success, message, order_id = create_order(
                user_id=1,  # TODO: Get actual user ID from auth
                items=order_items
            )

            if success:
                messagebox.showinfo("Order Placed", f"Order #{order_id} has been placed successfully!")
                # Clear the temporary cart storage
                self.cart_items = []
                self.update_cart_display()
                self.switch_to_products()
            else:
                messagebox.showerror("Order Failed", message)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to place order: {str(e)}")
