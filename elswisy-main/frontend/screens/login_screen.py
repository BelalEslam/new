import tkinter as tk
from tkinter import messagebox
import os
import sys

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.auth import Auth
from frontend.utils.constants import (
    PRIMARY_COLOR, BACKGROUND_COLOR, TEXT_COLOR,
    TITLE_FONT, HEADER_FONT, BODY_FONT, SMALL_FONT,
    ASSETS_DIR
)

class LoginScreen(tk.Frame):
    def __init__(self, master, switch_to_products, switch_to_signup):
        super().__init__(master)
        self.switch_to_products = switch_to_products
        self.switch_to_signup = switch_to_signup
        try:
            self.auth = Auth()  # Initialize the backend Auth class
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            self.auth = None
        self.configure(bg=BACKGROUND_COLOR)
        self.grid(row=0, column=0, sticky="nsew")

        # Load the background image
        bg_path = os.path.join(ASSETS_DIR, "background5.png")
        self.bg_image = tk.PhotoImage(file=bg_path)
        
        # Create a Canvas to display the background
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Set the background image on the Canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image)
        
        # Keep a reference to the image to prevent it from being garbage collected
        self.canvas.bg_image = self.bg_image

        # Create a frame for content
        center_frame = tk.Frame(self.canvas, bg=BACKGROUND_COLOR)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header = tk.Label(
            center_frame, text="CartX", font=TITLE_FONT,
            bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR
        )
        header.pack(pady=(40, 10))

        subheader = tk.Label(
            center_frame, text="Welcome back! Login to continue", font=BODY_FONT,
            bg=BACKGROUND_COLOR, fg=TEXT_COLOR
        )
        subheader.pack(pady=(0, 30))

        # Username label and entry
        username_label = tk.Label(center_frame, text="Username or Email", font=SMALL_FONT,
                                bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        username_label.pack(fill="x", padx=40)
        self.username_entry = tk.Entry(center_frame, font=BODY_FONT, bd=2, relief="groove")
        self.username_entry.pack(padx=40, pady=(0, 20), ipady=6, fill="x")

        # Password label and entry
        password_label = tk.Label(center_frame, text="Password", font=SMALL_FONT,
                                bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        password_label.pack(fill="x", padx=40)
        password_frame = tk.Frame(center_frame, bg=BACKGROUND_COLOR)
        password_frame.pack(padx=40, pady=(0, 20), fill="x")
        self.password_entry = tk.Entry(password_frame, show="*", font=BODY_FONT, bd=2, relief="groove")
        self.password_entry.pack(side="left", ipady=6, fill="x", expand=True)
        self.show_password = False
        self.toggle_btn = tk.Button(password_frame, text="Show", font=SMALL_FONT, width=6,
                                   command=self.toggle_password, relief="flat", bg=BACKGROUND_COLOR, fg=PRIMARY_COLOR, bd=0)
        self.toggle_btn.pack(side="left", padx=(5, 0))

        # Login button
        login_button = tk.Button(
            center_frame, text="Login", font=HEADER_FONT,
            bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR,
            activebackground="#0056b3", activeforeground=BACKGROUND_COLOR,
            command=self.login_action
        )
        login_button.pack(padx=40, pady=(10, 20), ipadx=10, ipady=6, fill="x")

        # Forgot Password
        forgot_label = tk.Label(
            center_frame, text="Forgot Password?", font=SMALL_FONT,
            bg=BACKGROUND_COLOR, fg=TEXT_COLOR, cursor="hand2"
        )
        forgot_label.pack()

        # Footer
        footer = tk.Label(
            center_frame, text="Don't have an account? Sign up", font=SMALL_FONT,
            bg=BACKGROUND_COLOR, fg=TEXT_COLOR, cursor="hand2"
        )
        footer.pack(side="bottom", pady=20)
        footer.bind("<Button-1>", lambda e: self.switch_to_signup())

    def login_action(self):
        """Handle the login action when the login button is clicked."""
        if not self.auth:
            messagebox.showerror("Error", "Database connection failed. Please restart the application.")
            return
            
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        success, message = self.auth.login(username, password)
        
        if success:
            messagebox.showinfo("Login Success", message)
            self.switch_to_products()
        else:
            messagebox.showerror("Login Failed", message)
            # Clear password field on failed login
            self.password_entry.delete(0, tk.END)

    def toggle_password(self):
        self.show_password = not self.show_password
        if self.show_password:
            self.password_entry.config(show="")
            self.toggle_btn.config(text="Hide")
        else:
            self.password_entry.config(show="*")
            self.toggle_btn.config(text="Show")
