# Spec: Add Image Aspect Ratio Support

**Granularity Level**: DETAILED
**Status**: Not started
**Priority**: High

## Overview

Add support for portrait-oriented images (1080x1350) alongside the current landscape format (1200x627), allowing users to generate images optimized for different social media platforms.

## Requirements

### 1. New CLI Parameter

Add `--aspect-ratio` (or `-a`) flag to the CLI:

```bash
python generate.py <day> <topic> [--aspect-ratio {landscape,portrait}] [other options...]
```

**Parameter specification:**
- Long form: `--aspect-ratio`
- Short form: `-a`
- Type: String choice
- Allowed values: `landscape`, `portrait`
- Default: `landscape`
- Case insensitive: Accept `Landscape`, `PORTRAIT`, etc.

### 2. Image Dimensions

Map aspect ratios to specific dimensions:

| Aspect Ratio | Width | Height | Use Case |
|--------------|-------|--------|----------|
| landscape | 1200 | 627 | LinkedIn, Twitter/X (current) |
| portrait | 1080 | 1350 | Instagram, LinkedIn portrait |

### 3. Layout Adaptation

Portrait layout must maintain readability and visual hierarchy. Adjust the vertical spacing:

**Portrait-specific layout constants:**
```python
LAYOUT_PORTRAIT = {
    "day_counter_y": 0.20,    # Slightly higher than landscape
    "progress_bar_y": 0.45,   # Centered vertically
    "progress_bar_width": 700, # Narrower to fit width
    "progress_bar_height": 16,
    "topic_pill_y": 0.65,
    "date_y": 0.88,           # Lower due to more vertical space
}
```

**Font size adjustments for portrait:**
- No changes needed - existing sizes work well for portrait
- Keep all existing font sizes the same

### 4. Configuration Changes

Update `config.py`:

```python
# Add new constants
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

# Deprecate top-level WIDTH, HEIGHT, LAYOUT constants
# (Keep for backward compatibility, but document as deprecated)
```

### 5. Code Changes

**Function signature update:**
```python
def generate_image(
    day: int,
    topic: str,
    date: str = None,
    output_path: str = None,
    aspect_ratio: str = "landscape"
) -> Path:
    """
    Generate a LinkedIn post image.

    Args:
        day: Day number (1-365)
        topic: Topic key from config.TOPICS
        date: Date string to display. Defaults to today.
        output_path: Output file path. Defaults to 'output/day_XXX_topic_aspect.png'
        aspect_ratio: Image aspect ratio ('landscape' or 'portrait'). Defaults to 'landscape'.

    Returns:
        Path to the generated image

    Raises:
        ValueError: If topic is not recognized, day is out of range, or aspect_ratio is invalid
    """
```

**Validation:**
- Convert aspect_ratio to lowercase before validation
- Raise ValueError if aspect_ratio not in `["landscape", "portrait"]`
- Error message: `"Invalid aspect ratio '{value}'. Must be 'landscape' or 'portrait'"`

**Default output path naming:**
- Landscape: `output/day_XXX_topic.png` (existing)
- Portrait: `output/day_XXX_topic_portrait.png` (new)

### 6. Examples

```bash
# Generate landscape (default, existing behavior)
python generate.py 1 general
# Output: output/day_001_general.png

# Generate landscape explicitly
python generate.py 1 general --aspect-ratio landscape
# Output: output/day_001_general.png

# Generate portrait
python generate.py 1 general --aspect-ratio portrait
# Output: output/day_001_general_portrait.png

# Generate portrait with custom output
python generate.py 42 cybersecurity -a portrait -o my_instagram_post.png
# Output: my_instagram_post.png
```

### 7. Edge Cases

| Case | Expected Behavior |
|------|-------------------|
| `--aspect-ratio LANDSCAPE` | Accept (case insensitive), convert to lowercase |
| `--aspect-ratio square` | Reject with ValueError |
| `-a portrait -o custom.png` | Use custom filename, ignore default naming |
| Progress bar on portrait | Scale width to 700px, maintain all other styling |
| Long topic label in portrait | Allow wrapping if needed (unlikely with current topics) |

### 8. Testing Requirements

Generate test images for all combinations:

```bash
# Test landscape (existing, ensure no regression)
python generate.py 1 general -a landscape -o samples/landscape_day_001.png
python generate.py 182 blockchain -a landscape -o samples/landscape_day_182.png
python generate.py 365 ai -a landscape -o samples/landscape_day_365.png

# Test portrait (new)
python generate.py 1 general -a portrait -o samples/portrait_day_001.png
python generate.py 182 blockchain -a portrait -o samples/portrait_day_182.png
python generate.py 365 ai -a portrait -o samples/portrait_day_365.png

# Test all topics in portrait
python generate.py 50 cybersecurity -a portrait -o samples/portrait_cybersecurity.png
python generate.py 50 blockchain -a portrait -o samples/portrait_blockchain.png
python generate.py 50 cryptography -a portrait -o samples/portrait_cryptography.png
python generate.py 50 ai -a portrait -o samples/portrait_ai.png
python generate.py 50 general -a portrait -o samples/portrait_general.png
```

**Visual checks:**
- Text is readable and well-positioned
- Progress bar looks proportional
- Topic pill is centered
- No text overflow or clipping
- Colors remain consistent across formats

### 9. Documentation Updates

Update:
- `README.md`: Add aspect-ratio parameter to usage section
- `CLAUDE.md`: Update current state to mention dual aspect ratio support
- CLI help text: Add description for new parameter

### 10. Implementation Notes

**Order of implementation:**
1. Add ASPECT_RATIOS config to config.py
2. Update generate_image() signature to accept aspect_ratio parameter
3. Add validation for aspect_ratio parameter
4. Update image creation to use selected dimensions/layout
5. Update default output path logic
6. Add argparse parameter
7. Test and generate sample images
8. Update documentation

**Backward compatibility:**
- Existing scripts using default behavior continue to work
- Existing WIDTH, HEIGHT, LAYOUT constants remain for transition period
- Deprecation warnings not needed yet (small project)
