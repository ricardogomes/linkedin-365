# Spec: Default to System Date

**Granularity Level**: LOOSE
**Status**: Not started
**Priority**: Medium

## Intent

When the user runs the tool without specifying a date, use today's date automatically. This removes friction from daily usage.

## Current Behavior

The tool already defaults to today's date internally when no `--date` parameter is provided, but the displayed date may not match the day parameter if the user is generating images for past/future days.

## Desired Behavior

Make it seamless: running the tool on January 15, 2026 should automatically display "January 15, 2026" on the image without requiring the user to type it out.

## Notes

This likely combines with the "infer day from date" feature. If a user runs:
```bash
python generate.py cybersecurity
```

On January 15, 2026, the tool should:
1. Use today's date (January 15, 2026)
2. Calculate it's day 15 of the challenge
3. Generate the image with both pieces of information

## Implementation

Figure out the best interface and user experience. Consider edge cases like:
- What if it's not 2026 anymore?
- Should there be a warning if calculated day is > 365?
- How does this interact with explicit day/date overrides?
