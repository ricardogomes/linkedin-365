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
    WIDTH, HEIGHT, COLORS, TOPICS, FONTS, LAYOUT, TOTAL_DAYS,
    ASPECT_RATIOS, START_DATE
)


def parse_date(date_str: str) -> datetime:
    """Parse a date string in format 'Month DD, YYYY'."""
    try:
        return datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
        raise ValueError(f"Invalid date format '{date_str}'. Expected format: 'Month DD, YYYY' (e.g., 'January 15, 2026')")


def calculate_day_from_date(date_str: str, start_date_str: str = START_DATE) -> int:
    """
    Calculate the day number from a date string.

    Args:
        date_str: Date string in format "Month DD, YYYY"
        start_date_str: Start date of the challenge

    Returns:
        Day number (1-365)

    Raises:
        ValueError: If date is before start date or more than 365 days after
    """
    target_date = parse_date(date_str)
    start_date = parse_date(start_date_str)

    day_number = (target_date - start_date).days + 1

    if day_number < 1:
        raise ValueError(f"Date '{date_str}' is before challenge start date '{start_date_str}'")
    if day_number > TOTAL_DAYS:
        raise ValueError(f"Date '{date_str}' is more than {TOTAL_DAYS} days after start date")

    return day_number


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
    topic: str,
    day: int = None,
    date: str = None,
    output_path: str = None,
    aspect_ratio: str = "landscape"
) -> Path:
    """
    Generate a LinkedIn post image.

    Args:
        topic: Topic key from config.TOPICS
        day: Day number (1-365). If not provided, calculated from date.
        date: Date string to display. Defaults to today. If day is not provided, used to calculate day number.
        output_path: Output file path. Defaults to 'output/day_XXX_topic[_portrait].png'
        aspect_ratio: Image aspect ratio ('landscape' or 'portrait'). Defaults to 'landscape'.

    Returns:
        Path to the generated image

    Raises:
        ValueError: If topic is not recognized, day is out of range, or aspect_ratio is invalid
    """
    # Validate topic
    topic_lower = topic.lower()
    if topic_lower not in TOPICS:
        raise ValueError(f"Unknown topic '{topic}'. Available: {', '.join(TOPICS.keys())}")

    # Validate aspect ratio
    aspect_ratio_lower = aspect_ratio.lower()
    if aspect_ratio_lower not in ASPECT_RATIOS:
        raise ValueError(f"Invalid aspect ratio '{aspect_ratio}'. Must be 'landscape' or 'portrait'")

    # Get aspect ratio config
    ratio_config = ASPECT_RATIOS[aspect_ratio_lower]
    width = ratio_config["width"]
    height = ratio_config["height"]
    layout = ratio_config["layout"]

    # Handle date and day logic
    if date is None:
        # Default to today's date
        date = datetime.now().strftime("%B %d, %Y")

    if day is None:
        # Calculate day from date
        day = calculate_day_from_date(date)
    else:
        # Validate explicit day parameter
        if not 1 <= day <= TOTAL_DAYS:
            raise ValueError(f"Day must be between 1 and {TOTAL_DAYS}")

    topic_config = TOPICS[topic_lower]
    accent_color = topic_config["color"]
    topic_label = topic_config["label"]

    # Default output path
    if output_path is None:
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        if aspect_ratio_lower == "portrait":
            output_path = output_dir / f"day_{day:03d}_{topic_lower}_portrait.png"
        else:
            output_path = output_dir / f"day_{day:03d}_{topic_lower}.png"
    else:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load fonts
    font_large = get_font("bold", FONTS["size_large"])
    font_medium = get_font("regular", FONTS["size_medium"])
    font_small = get_font("regular", FONTS["size_small"])

    # Create image
    img = Image.new("RGB", (width, height), COLORS["background"])
    draw = ImageDraw.Draw(img)

    center_x = width // 2

    # Draw day counter
    day_text = f"Day {day}/{TOTAL_DAYS}"
    bbox = draw.textbbox((0, 0), day_text, font=font_large)
    text_width = bbox[2] - bbox[0]
    day_y = int(height * layout["day_counter_y"])
    draw.text(
        (center_x - text_width // 2, day_y),
        day_text,
        font=font_large,
        fill=COLORS["text_primary"]
    )

    # Draw progress bar
    bar_width = layout["progress_bar_width"]
    bar_height = layout["progress_bar_height"]
    bar_x = center_x - bar_width // 2
    bar_y = int(height * layout["progress_bar_y"])
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
    pill_y = int(height * layout["topic_pill_y"])

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
    date_y = int(height * layout["date_y"])
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
  # Use today's date and infer day number
  %(prog)s general

  # Specify a date and infer day number
  %(prog)s cybersecurity --date "January 15, 2026"

  # Explicit day number
  %(prog)s cybersecurity --day 42

  # Portrait format for Instagram
  %(prog)s blockchain --aspect-ratio portrait

  # Custom output path
  %(prog)s blockchain --day 100 -o my_image.png

Available topics: {', '.join(TOPICS.keys())}
Available aspect ratios: {', '.join(ASPECT_RATIOS.keys())}
        """
    )
    parser.add_argument(
        "topic",
        type=str,
        help="Post topic for color coding"
    )
    parser.add_argument(
        "--day",
        type=int,
        help=f"Day number (1-{TOTAL_DAYS}). If not provided, calculated from date."
    )
    parser.add_argument(
        "--date", "-d",
        type=str,
        help="Date to display (default: today). Used to calculate day if day not provided."
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        type=str,
        default="landscape",
        help="Image aspect ratio: 'landscape' (1200x627) or 'portrait' (1080x1350). Default: landscape"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: output/day_XXX_topic[_portrait].png)"
    )

    args = parser.parse_args()

    try:
        output_path = generate_image(
            topic=args.topic,
            day=args.day,
            date=args.date,
            output_path=args.output,
            aspect_ratio=args.aspect_ratio
        )
        print(f"✓ Generated: {output_path}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
