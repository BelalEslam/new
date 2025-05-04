import os

# Asset paths
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')
BACKGROUNDS_DIR = os.path.join(ASSETS_DIR)
PRODUCT_IMAGES_DIR = os.path.join(ASSETS_DIR)
LOGO_PATH = os.path.join(ASSETS_DIR, 'Logo.png')

# Color scheme
PRIMARY_COLOR = "#007BFF"      # Electric Blue
SECONDARY_COLOR = "#4F46E5"    # Indigo
ACCENT_COLOR = "#28A745"       # Green for stock status
BACKGROUND_COLOR = "#F4F1EB"   # Light Beige
CARD_BACKGROUND = "#FFFFFF"    # White
TEXT_COLOR = "#313715"         # Dark Olive Brown
SUCCESS_COLOR = "#059669"      # Green for success
WARNING_COLOR = "#D97706"      # Amber for warnings
BORDER_COLOR = "#E2E8F0"       # Light Gray for borders
DISABLED_COLOR = "#94A3B8"     # Gray for disabled elements
CARD_BORDER = "#E0E0E0"        # Light Gray

# Fonts
TITLE_FONT = ("Inter", 24, "bold")
HEADER_FONT = ("Inter", 16, "bold")
BODY_FONT = ("Inter", 12)
SMALL_FONT = ("Inter", 10) 