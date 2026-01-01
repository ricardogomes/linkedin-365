#!/usr/bin/env python3
"""
LinkedIn Daily Post Image Generator

Generates consistent branded images for a 365-day posting challenge.
Usage: python generate.py <day> <topic> [--date "Month DD, YYYY"] [--output file.png]
"""

from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from pathlib import Path
import argparse
import sys

from config import (
    WIDTH, HEIGHT, COLORS, TOPICS, FONTS, LAYOUT, TOTAL_DAYS
)


def get_font(font_type: str, size: int) -> ImageFont.FreeTypeFont:
    """Load a font, falling back to system fonts if custom not specified."""
    custom_path = FONTS.get(font_type)
    
    if custom_path:
        try:
            return ImageFont.truetype(custom_path, size)
        except OSError:
            print(f"Warning: Could not load font {custom_path}, using system font")
    
    # Try common system fonts
    system_fonts = [
        # Linux
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if font_type == "bold" 
            else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        # Windows
        "C:/Windows/Fonts/arial.ttf",
    ]
    
    for font_path in system_fonts:
        try:
            return ImageFont.truetype(font_path, size)
        except OSError:
            continue
    
    # Ultimate fallback
    return ImageFont.load_default()


def generate_image(
    day: int,
    topic: str,
    date: str = None,
    output_path: str = None
) -> Path:
    """
    Generate a LinkedIn post image.
    
    Args:
        day: Day number (1-365)
        topic: Topic key from config.TOPICS
        date: Date string to display. Defaults to today.
        output_path: Output file path. Defaults to 'output/day_XXX.png'
    
    Returns:
        Path to the generated image
    
    Raises:
        ValueError: If topic is not recognized or day is out of range
    """
    # Validate inputs
    topic_lower = topic.lower()
    if topic_lower not in TOPICS:
        raise ValueError(f"Unknown topic '{topic}'. Available: {', '.join(TOPICS.keys())}")
    
    if not 1 <= day <= TOTAL_DAYS:
        raise ValueError(f"Day must be between 1 and {TOTAL_DAYS}")
    
    topic_config = TOPICS[topic_lower]
    accent_color = topic_config["color"]
    topic_label = topic_config["label"]
    
    # Default date to today
    if date is None:
        date = datetime.now().strftime("%B %d, %Y")
    
    # Default output path
    if output_path is None:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"day_{day:03d}_{topic_lower}.png"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load fonts
    font_large = get_font("bold", FONTS["size_large"])
    font_medium = get_font("regular", FONTS["size_medium"])
    font_small = get_font("regular", FONTS["size_small"])
    
    # Create image
    img = Image.new("RGB", (WIDTH, HEIGHT), COLORS["background"])
    draw = ImageDraw.Draw(img)
    
    center_x = WIDTH // 2
    
    # Draw day counter
    day_text = f"Day {day}/{TOTAL_DAYS}"
    bbox = draw.textbbox((0, 0), day_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    day_y = int(HEIGHT * LAYOUT["day_counter_y"])
    draw.text(
        (center_x - text_width // 2, day_y),
        day_text,
        font=font_large,
        fill=COLORS["text_primary"]
    )
    
    # Draw progress bar
    bar_width = LAYOUT["progress_bar_width"]
    bar_height = LAYOUT["progress_bar_height"]
    bar_x = center_x - bar_width // 2
    bar_y = int(HEIGHT * LAYOUT["progress_bar_y"])
    progress_fill = int((day / TOTAL_DAYS) * bar_width)
    
    # Progress bar background
    draw.rounded_rectangle(
        [bar_x, bar_y, bar_x + bar_width, bar_y + bar_height],
        radius=bar_height // 2,
        fill=COLORS["progress_bg"]
    )
    
    # Progress bar fill
    if progress_fill > 0:
        # Ensure minimum visible progress
        fill_width = max(progress_fill, bar_height)
        draw.rounded_rectangle(
            [bar_x, bar_y, bar_x + fill_width, bar_y + bar_height],
            radius=bar_height // 2,
            fill=accent_color
        )
    
    # Draw percentage
    percentage = f"{(day / TOTAL_DAYS * 100):.1f}%"
    bbox = draw.textbbox((0, 0), percentage, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(
        (center_x - text_width // 2, bar_y + bar_height + 12),
        percentage,
        font=font_small,
        fill=COLORS["text_secondary"]
    )
    
    # Draw topic pill
    padding_x, padding_y = 24, 12
    bbox = draw.textbbox((0, 0), topic_label, font=font_medium)
    pill_text_width = bbox[2] - bbox[0]
    pill_text_height = bbox[3] - bbox[1]
    pill_width = pill_text_width + padding_x * 2
    pill_height = pill_text_height + padding_y * 2
    pill_x = center_x - pill_width // 2
    pill_y = int(HEIGHT * LAYOUT["topic_pill_y"])
    
    draw.rounded_rectangle(
        [pill_x, pill_y, pill_x + pill_width, pill_y + pill_height],
        radius=pill_height // 2,
        fill=accent_color
    )
    draw.text(
        (pill_x + padding_x, pill_y + padding_y - 4),
        topic_label,
        font=font_medium,
        fill=COLORS["text_primary"]
    )
    
    # Draw date
    bbox = draw.textbbox((0, 0), date, font=font_small)
    text_width = bbox[2] - bbox[0]
    date_y = int(HEIGHT * LAYOUT["date_y"])
    draw.text(
        (center_x - text_width // 2, date_y),
        date,
        font=font_small,
        fill=COLORS["text_secondary"]
    )
    
    # Save image
    img.save(output_path, "PNG", quality=95)
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate LinkedIn daily post images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s 1 general --date "January 1, 2026"
  %(prog)s 42 cybersecurity
  %(prog)s 100 blockchain -o my_image.png

Available topics: {', '.join(TOPICS.keys())}
        """
    )
    parser.add_argument(
        "day",
        type=int,
        help=f"Day number (1-{TOTAL_DAYS})"
    )
    parser.add_argument(
        "topic",
        type=str,
        help="Post topic for color coding"
    )
    parser.add_argument(
        "--date", "-d",
        type=str,
        help="Date to display (default: today)"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: output/day_XXX_topic.png)"
    )
    
    args = parser.parse_args()
    
    try:
        output_path = generate_image(
            day=args.day,
            topic=args.topic,
            date=args.date,
            output_path=args.output
        )
        print(f"✓ Generated: {output_path}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
