"""
Configuration for LinkedIn image generator.
Edit this file to customize colors, topics, and dimensions.
"""

# Image dimensions (LinkedIn landscape recommended)
# NOTE: WIDTH, HEIGHT, and LAYOUT are kept for backward compatibility
# Use ASPECT_RATIOS for new code
WIDTH = 1200
HEIGHT = 627

# Color scheme
COLORS = {
    "background": "#0F172A",      # Dark blue-gray
    "text_primary": "#F8FAFC",    # Off-white
    "text_secondary": "#94A3B8",  # Muted gray
    "progress_bg": "#1E293B",     # Slightly lighter than background
}

# Topic configuration
# Add or modify topics here
TOPICS = {
    "cybersecurity": {
        "color": "#3B82F6",  # Blue
        "label": "Cybersecurity",
    },
    "blockchain": {
        "color": "#F59E0B",  # Orange
        "label": "Blockchain",
    },
    "cryptography": {
        "color": "#10B981",  # Green
        "label": "Cryptography",
    },
    "ai": {
        "color": "#06B6D4",  # Cyan
        "label": "Artificial Intelligence",
    },
    "general": {
        "color": "#8B5CF6",  # Purple
        "label": "General",
    },
}

# Typography settings
FONTS = {
    # Font paths - modify these if you have custom fonts
    # Set to None to use system defaults
    "bold": None,    # e.g., "/path/to/YourFont-Bold.ttf"
    "regular": None, # e.g., "/path/to/YourFont-Regular.ttf"
    
    # Font sizes
    "size_large": 120,   # Day counter
    "size_medium": 36,   # Topic label
    "size_small": 28,    # Date and percentage
}

# Layout settings (vertical positions as percentage of height)
LAYOUT = {
    "day_counter_y": 0.26,    # Day X/365 position
    "progress_bar_y": 0.51,   # Progress bar position
    "progress_bar_width": 800,
    "progress_bar_height": 16,
    "topic_pill_y": 0.67,     # Topic pill position
    "date_y": 0.85,           # Date position
}

# Aspect ratio configurations
ASPECT_RATIOS = {
    "landscape": {
        "width": 1200,
        "height": 627,
        "layout": {
            "day_counter_y": 0.26,
            "progress_bar_y": 0.51,
            "progress_bar_width": 800,
            "progress_bar_height": 16,
            "topic_pill_y": 0.67,
            "date_y": 0.85,
        }
    },
    "portrait": {
        "width": 1080,
        "height": 1350,
        "layout": {
            "day_counter_y": 0.20,
            "progress_bar_y": 0.45,
            "progress_bar_width": 700,
            "progress_bar_height": 16,
            "topic_pill_y": 0.65,
            "date_y": 0.88,
        }
    }
}

# Challenge settings
TOTAL_DAYS = 365
YEAR = 2026
START_DATE = "January 1, 2026"
