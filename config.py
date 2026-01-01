"""
Configuration for LinkedIn image generator.
Edit this file to customize colors, topics, and dimensions.
"""

# Image dimensions (LinkedIn landscape recommended)
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

# Challenge settings
TOTAL_DAYS = 365
YEAR = 2026
