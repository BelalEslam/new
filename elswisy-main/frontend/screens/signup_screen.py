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

class SignupScreen(tk.Frame):
    def __init__(self, master, switch_to_login):
        super().__init__(master)
        self.switch_to_login = switch_to_login
        self.auth = Auth()  # Initialize the backend Auth class
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
            center_frame, text="Create your account", font=BODY_FONT,
            bg=BACKGROUND_COLOR, fg=TEXT_COLOR
        )
        subheader.pack(pady=(0, 30))

        # Username
        username_label = tk.Label(center_frame, text="Username", font=SMALL_FONT,
                                bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        username_label.pack(fill="x", padx=40)
        self.username_entry = tk.Entry(center_frame, font=BODY_FONT, bd=2, relief="groove")
        self.username_entry.pack(padx=40, pady=(0, 10), ipady=6, fill="x")

        # Email
        email_label = tk.Label(center_frame, text="Email", font=SMALL_FONT,
                             bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        email_label.pack(fill="x", padx=40)
        self.email_entry = tk.Entry(center_frame, font=BODY_FONT, bd=2, relief="groove")
        self.email_entry.pack(padx=40, pady=(0, 10), ipady=6, fill="x")

        # Password
        password_label = tk.Label(center_frame, text="Password", font=SMALL_FONT,
                                bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        password_label.pack(fill="x", padx=40)
        self.password_entry = tk.Entry(center_frame, show="*", font=BODY_FONT, bd=2, relief="groove")
        self.password_entry.pack(padx=40, pady=(0, 10), ipady=6, fill="x")

        # Phone
        phone_label = tk.Label(center_frame, text="Phone Number", font=SMALL_FONT,
                             bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        phone_label.pack(fill="x", padx=40)
        self.phone_entry = tk.Entry(center_frame, font=BODY_FONT, bd=2, relief="groove")
        self.phone_entry.pack(padx=40, pady=(0, 10), ipady=6, fill="x")

        # Address
        address_label = tk.Label(center_frame, text="Address", font=SMALL_FONT,
                               bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        address_label.pack(fill="x", padx=40)
        
        # City
        city_label = tk.Label(center_frame, text="City", font=SMALL_FONT,
                            bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        city_label.pack(fill="x", padx=40)
        self.city_entry = tk.Entry(center_frame, font=BODY_FONT, bd=2, relief="groove")
        self.city_entry.pack(padx=40, pady=(0, 10), ipady=6, fill="x")

        # Street
        street_label = tk.Label(center_frame, text="Street", font=SMALL_FONT,
                              bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        street_label.pack(fill="x", padx=40)
        self.street_entry = tk.Entry(center_frame, font=BODY_FONT, bd=2, relief="groove")
        self.street_entry.pack(padx=40, pady=(0, 10), ipady=6, fill="x")

        # Building Number
        building_label = tk.Label(center_frame, text="Building Number", font=SMALL_FONT,
                                bg=BACKGROUND_COLOR, fg=TEXT_COLOR, anchor="w")
        building_label.pack(fill="x", padx=40)
        self.building_entry = tk.Entry(center_frame, font=BODY_FONT, bd=2, relief="groove")
        self.building_entry.pack(padx=40, pady=(0, 10), ipady=6, fill="x")

        # Sign Up button
        signup_button = tk.Button(
            center_frame, text="Sign Up", font=HEADER_FONT,
            bg=PRIMARY_COLOR, fg=BACKGROUND_COLOR,
            activebackground="#0056b3", activeforeground=BACKGROUND_COLOR,
            command=self.signup_action
        )
        signup_button.pack(padx=40, pady=(20, 10), ipadx=10, ipady=6, fill="x")

        # Footer
        footer = tk.Label(
            center_frame, text="Already have an account? Login", font=SMALL_FONT,
            bg=BACKGROUND_COLOR, fg=TEXT_COLOR, cursor="hand2"
        )
        footer.pack(side="bottom", pady=20)
        footer.bind("<Button-1>", lambda e: self.switch_to_login())

    def signup_action(self):
        """Handle the signup action when the signup button is clicked."""
        # Get all form values
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        phone = self.phone_entry.get().strip()
        city = self.city_entry.get().strip()
        street = self.street_entry.get().strip()
        building = self.building_entry.get().strip()

        # Validate required fields
        if not all([username, email, password, phone, city, street, building]):
            messagebox.showwarning("Missing Info", "Please fill in all fields.")
            return

        try:
            # Validate phone number and building number
            phone = int(phone)
            building = int(building)
        except ValueError:
            messagebox.showwarning("Invalid Input", "Phone number and building number must be numeric.")
            return

        # Combine address components
        full_address = f"{building} {street}, {city}"

        # Use the backend Auth class to handle signup
        success, message = self.auth.signup(
            username=username,
            password=password,
            email=email,
            address=full_address,
            phone_number=str(phone)
        )

        if success:
            messagebox.showinfo("Success", message)
            self.switch_to_login()
        else:
            messagebox.showerror("Sign Up Failed", message)
            # Clear sensitive fields on failure
            self.password_entry.delete(0, tk.END) 