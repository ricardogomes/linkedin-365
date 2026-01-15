# BACKLOG.md - Project Priorities and Action Items

## Next Actions

No immediate priorities. The core feature set is complete.

---

## Completed

### 1. Add image aspect ratio support (portrait) ✓

**Priority**: High
**Status**: ✓ Completed (commit: 0f8d4f7)
**Spec granularity**: Detailed

Implemented portrait format (1080x1350) alongside landscape (1200x627):
- New `--aspect-ratio` / `-a` CLI parameter (case insensitive)
- Portrait-optimized layout with adjusted vertical spacing
- Automatic `_portrait` suffix in default filenames
- ASPECT_RATIOS config structure in config.py

**Learnings**: Detailed spec with exact parameters and edge cases made implementation straightforward. No ambiguity or back-and-forth needed.

---

### 2. Infer day number from date ✓

**Priority**: High
**Status**: ✓ Completed (commit: 0f8d4f7)
**Spec granularity**: Medium

Day number automatically calculated from date (based on Jan 1, 2026 start):
- `--day` parameter is now optional
- Calculates from `--date` if day not provided
- Explicit `--day` overrides calculation
- Validation: rejects dates before start or > 365 days after

**Learnings**: Medium spec with clear requirements but implementation flexibility worked well. Agent made reasonable CLI design choices.

---

### 3. Default to system date ✓

**Priority**: Medium
**Status**: ✓ Completed (commit: 0f8d4f7)
**Spec granularity**: Loose

Date defaults to today for frictionless daily usage:
- Combined with day inference: `python generate.py <topic>` generates today's image
- Zero configuration for daily workflow

**Learnings**: Loose spec (intent-only) required more interpretation but enabled creative UX design. Agent successfully combined with date inference.

---

## Open Questions

### From initial implementation:

1. **Font selection**: Should we bundle a specific font to ensure consistency across platforms, or keep the system font fallback approach?

2. **Batch generation**: If we add batch mode (generate images for a date range), should it:
   - Auto-increment days?
   - Allow topic specification per day (via CSV/JSON)?
   - Generate all possible combinations for testing?

3. **Date validation strictness**: Current implementation rejects dates outside 2026. Should we allow any year for flexibility (e.g., generating retroactive or future content)?

4. **Output format**: Should we support other formats (JPEG, WebP) or stay PNG-only?

5. **Backward compatibility**: Old CLI usage `python generate.py 1 general` no longer works. Should we support it via position detection, or is documentation update sufficient?

6. **Error messages**: Should date parsing support multiple formats (ISO 8601, etc.) or stay strict to "Month DD, YYYY"?

---

## Ideas for Later

### New features
- Template variations (quote cards, milestone celebrations, achievement badges)
- Add icon/symbol per topic category
- Web interface for non-technical users
- Subtle background patterns or textures
- Custom font support with bundled fonts
- Configuration via YAML/JSON file
- Integration with social media APIs for auto-posting
- Batch generation mode for date ranges

### Code quality
- Add unit tests for core functions (parse_date, calculate_day_from_date, generate_image)
- Add integration tests for CLI
- Type checking with mypy
- Linting with ruff or pylint
- Pre-commit hooks for quality checks

### Developer experience
- Add `--version` flag
- Add `--list-topics` flag
- Better error messages with suggestions
- Progress indicator for batch operations
- Dry-run mode to preview output path without generating

### Distribution
- Package for PyPI
- Add GitHub Actions for CI/CD
- Create releases with binaries (PyInstaller/Nuitka)
- Docker container for consistent environments
