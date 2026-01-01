# CLAUDE.md - Project Context for Claude Code

## Project Overview

This is a Python tool that generates consistent, branded images for a 365-day LinkedIn posting challenge. The goal is to post daily about cybersecurity, blockchain, and cryptography topics throughout 2026.

## Purpose

- Generate LinkedIn-optimized images (1200x627 landscape)
- Visual consistency across all 365 posts
- Color-coded topics for easy recognition
- Progress tracking with day counter and progress bar

## Architecture

```
linkedin-365/
├── generate.py          # Main image generation script
├── config.py            # Configuration (colors, topics, dimensions)
├── pyproject.toml       # Project metadata and dependencies (uv/pip)
├── requirements.txt     # Legacy pip dependencies
├── samples/             # Sample generated images
└── output/              # Generated images (gitignored)
```

## Key Design Decisions

1. **Dark background**: Tech aesthetic, easy on eyes, stands out in LinkedIn feed
2. **Color-coded topics**: Blue (cybersecurity), Orange (blockchain), Green (cryptography), Purple (general)
3. **Minimal design**: Day counter, progress bar, topic pill, date - nothing more
4. **No personal branding**: Focus is on content, not the person

## Usage

```bash
# Generate an image
python generate.py <day> <topic> [--date "Month DD, YYYY"] [--output filename.png]

# Examples
python generate.py 1 general --date "January 1, 2026"
python generate.py 42 cybersecurity
python generate.py 100 blockchain -o custom_name.png
```

## Topics

- `cybersecurity` - Blue (#3B82F6)
- `blockchain` - Orange (#F59E0B)
- `cryptography` - Green (#10B981)
- `general` - Purple (#8B5CF6)

## Potential Improvements

- [ ] Add custom font support (currently uses system DejaVu Sans)
- [ ] Add subtle background patterns or textures
- [ ] Batch generation mode for multiple days
- [ ] Template variations (quote cards, milestone celebrations)
- [ ] Add icon/symbol per topic category
- [ ] Configuration file for easy customization
- [ ] Web interface for non-technical use

## Dependencies

- Python 3.8+
- Pillow

Install with uv (preferred):
```bash
uv sync
```

Or with pip:
```bash
pip install -r requirements.txt
``` (PIL)

## Testing Changes

After making changes, generate sample images across different scenarios:

```bash
python generate.py 1 general --date "January 1, 2026" -o samples/day_001.png
python generate.py 50 cybersecurity -o samples/day_050.png
python generate.py 182 blockchain -o samples/day_182.png
python generate.py 365 cryptography --date "December 31, 2026" -o samples/day_365.png
```

Check that:
- Text is readable and well-positioned
- Progress bar scales correctly (especially at 1, ~50%, and 100%)
- Colors are visually distinct
- Image dimensions are correct (1200x627)

## Owner Context

Ricardo is a university professor researching blockchain in healthcare, cybersecurity and cryptography. This tool supports his "learning in public" approach to document his journey and showcase work alongside students and colleagues.
