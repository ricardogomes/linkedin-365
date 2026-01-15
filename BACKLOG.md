# BACKLOG.md - Project Priorities and Action Items

## Next Actions

These are the immediate priorities for improving the tool:

### 1. Add image aspect ratio support (portrait)

**Priority**: High
**Status**: Not started

Currently, the tool only generates landscape images (1200x627). Add support for Instagram/LinkedIn portrait format (1080x1350) while keeping landscape as default.

See: `specs/aspect-ratio-support.md` for detailed specification.

---

### 2. Infer day number from date

**Priority**: High
**Status**: Not started

Allow users to specify a date and have the tool automatically calculate which day of the 365-day challenge it represents (based on start date of January 1, 2026). Keep explicit day parameter as an override.

See: `specs/infer-day-from-date.md` for specification.

---

### 3. Default to system date

**Priority**: Medium
**Status**: Not started

Make the date parameter optional, defaulting to today's date. Currently, if no date is provided, the tool uses today's date internally but users must always provide the day number.

See: `specs/default-system-date.md` for specification.

---

## Open Questions

### From initial code review:

1. **Font selection**: Should we bundle a specific font to ensure consistency across platforms, or keep the system font fallback approach?

2. **Batch generation**: If we add batch mode (generate images for a date range), should it:
   - Auto-increment days?
   - Allow topic specification per day (via CSV/JSON)?
   - Generate all possible combinations for testing?

3. **Validation**: Should we validate dates to ensure they're within 2026, or allow any year for flexibility?

4. **Output format**: Should we support other formats (JPEG, WebP) or stay PNG-only?

5. **Portrait layout**: For portrait format, should we use the same layout proportions, or redesign for vertical space?

---

## Ideas for Later

- Template variations (quote cards, milestone celebrations)
- Add icon/symbol per topic category
- Web interface for non-technical users
- Subtle background patterns or textures
- Custom font support with bundled fonts
- Configuration via YAML/JSON file
- Integration with social media APIs for auto-posting
