# CLAUDE.md - Project Context for Claude Code

## Project Overview

This is a Python tool that generates consistent, branded images for a 365-day LinkedIn posting challenge. The goal is to post daily about cybersecurity, blockchain, cryptography, and AI topics throughout 2026.

## Meta-Purpose: AI-Driven Development Experiment

This project is itself an experiment in fully AI-driven development with human oversight. The process of building it is as important as the output.

### Development Principles

1. **Human-at-the-helm, not human-in-the-loop**: Direction is set through documentation (CLAUDE.md, specs, backlog). The agent executes autonomously against those specifications. Feedback and course-correction happen between runs, not during execution. No approval gates or step-by-step intervention during implementation.

   The documentation IS the steering mechanism. If output isn't adequate, the response is to refine documentation and run again—not to add control checkpoints during execution.

2. **Documented process**: Decisions and learnings are tracked in the repository. The git history tells the story of how features evolved.

3. **Iterative quality**: Best practices in development, testing, deployment, and security are applied incrementally. We don't over-engineer upfront, but we don't skip fundamentals either.

4. **Learning over shipping**: Experimenting with approaches and understanding trade-offs matters more than velocity. This is a learning laboratory, not a production sprint.

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

## Current State

The tool is functional and generates high-quality images. Core capabilities:

- **Image generation**: Single-image CLI with topic, optional day, date, aspect ratio, and output path
- **Five topic categories**: cybersecurity (blue), blockchain (orange), cryptography (green), ai (cyan), general (purple)
- **Multiple aspect ratios**: 1200x627 landscape (LinkedIn) and 1080x1350 portrait (Instagram/LinkedIn)
- **Smart date handling**: Automatically calculates day number from date (based on Jan 1, 2026 start), defaults to today
- **Visual elements**: Day counter, progress bar, topic pill, date display
- **Configuration**: Separated into `config.py` with aspect ratio-specific layouts
- **Font handling**: System font fallback (DejaVu Sans on Linux, Helvetica on macOS, Arial on Windows)
- **Dependencies**: Minimal (Python 3.8+, Pillow), managed via uv

## Code Conventions

Patterns observed in the codebase:

- **Separation of concerns**: Configuration (`config.py`) separate from logic (`generate.py`)
- **Type hints**: Function signatures use type annotations
- **Docstrings**: Functions include docstring documentation
- **Error handling**: ValueError for invalid inputs with descriptive messages
- **Path management**: Using pathlib.Path for cross-platform compatibility
- **CLI**: argparse with help text and examples
- **Output**: Clear success/error messages with emoji for visual feedback

## Key Design Decisions

1. **Dark background**: Tech aesthetic, easy on eyes, stands out in LinkedIn feed
2. **Color-coded topics**: Instantly recognizable categories with distinct colors
3. **Minimal design**: Day counter, progress bar, topic pill, date - nothing more
4. **No personal branding**: Focus is on content, not the person
5. **Multi-platform formats**: Landscape (1200x627) for LinkedIn/Twitter, Portrait (1080x1350) for Instagram
6. **Smart defaults**: Automatically uses today's date and calculates day number for frictionless daily use

## Usage

```bash
# Generate an image
python generate.py <topic> [--day N] [--date "Month DD, YYYY"] [--aspect-ratio landscape|portrait] [--output filename.png]

# Examples
python generate.py general  # Uses today's date, infers day number
python generate.py cybersecurity --date "January 15, 2026"  # Infers day 15
python generate.py blockchain --day 100  # Explicit day number
python generate.py ai --aspect-ratio portrait  # Portrait format for Instagram
python generate.py cryptography --day 42 -a portrait -o custom_name.png
```

## Topics

- `cybersecurity` - Blue (#3B82F6)
- `blockchain` - Orange (#F59E0B)
- `cryptography` - Green (#10B981)
- `ai` - Cyan (#06B6D4)
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
