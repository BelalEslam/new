import os
import tkinter as tk

def load_product_image(product_name, image_url=None, assets_dir="../../../assets"):
    """
    Load product image or placeholder if not available.
    Args:
        product_name (str): Name of the product (for error messages)
        image_url (str, optional): Path to the product image
        assets_dir (str): Directory containing assets
    Returns:
        tk.PhotoImage or None: The loaded image or None if loading failed
    """
    try:
        # Get the absolute path to the assets directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        assets_path = os.path.abspath(os.path.join(current_dir, assets_dir))
        print(f"\nDebug - Loading image for product: {product_name}")
        print(f"Debug - Current directory: {current_dir}")
        print(f"Debug - Assets path: {assets_path}")
        
        # If image_url is provided, try to load it
        if image_url:
            image_path = os.path.join(assets_path, image_url)
            print(f"Debug - Trying to load image from: {image_path}")
            print(f"Debug - Image exists: {os.path.exists(image_path)}")
            if os.path.exists(image_path):
                try:
                    image = tk.PhotoImage(file=image_path)
                    print(f"Debug - Successfully loaded image: {image_path}")
                    # Resize the image to fit the card
                    width = image.width()
                    height = image.height()
                    max_size = 200  # Maximum dimension for the image
                    
                    if width > height:
                        subsample = max(1, width // max_size)
                    else:
                        subsample = max(1, height // max_size)
                        
                    image = image.subsample(subsample, subsample)
                    return image
                except tk.TclError as e:
                    print(f"Debug - Error loading image for {product_name}: {e}")
        
        # If no image_url or image not found, use placeholder
        placeholder_path = os.path.join(assets_path, "Logo.png")
        print(f"Debug - Trying to load placeholder from: {placeholder_path}")
        print(f"Debug - Placeholder exists: {os.path.exists(placeholder_path)}")
        if os.path.exists(placeholder_path):
            try:
                image = tk.PhotoImage(file=placeholder_path)
                print(f"Debug - Successfully loaded placeholder: {placeholder_path}")
                image = image.subsample(4, 4)  # Make placeholder smaller
                return image
            except tk.TclError as e:
                print(f"Debug - Error loading placeholder image: {e}")
                
        return None
    except Exception as e:
        print(f"Debug - Error in load_product_image: {e}")
        return None 