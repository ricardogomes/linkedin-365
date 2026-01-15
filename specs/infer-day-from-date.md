# Spec: Infer Day Number from Date

**Granularity Level**: MEDIUM
**Status**: Not started
**Priority**: High

## Overview

Allow users to provide a date instead of a day number, and automatically calculate which day of the 365-day challenge it represents. The challenge started on January 1, 2026.

## User Experience

Currently, users must manually calculate the day number:
```bash
# Today is January 15, 2026 (day 15)
python generate.py 15 cybersecurity
```

Desired behavior - users can provide the date and tool figures it out:
```bash
# Let the tool calculate it's day 15
python generate.py cybersecurity --date "January 15, 2026"
```

## Requirements

### 1. Make Day Parameter Optional

The day number should become optional when a date is provided. Users should be able to:
- Provide explicit day number (current behavior)
- Provide date and let tool infer the day
- Provide both day and date (day parameter overrides calculation)

### 2. Date Parsing

Accept the same date format currently supported: "Month DD, YYYY" (e.g., "January 15, 2026").

Extract the date and calculate: `day = (provided_date - start_date).days + 1`

Where start_date is January 1, 2026.

### 3. Validation

The tool should validate:
- Date is within 2026 (or should it accept any year? See open question in BACKLOG.md)
- Calculated day is between 1-365
- Date is parseable

Provide helpful error messages if validation fails.

### 4. CLI Changes

The CLI should accept:
```bash
# Explicit day (existing)
python generate.py 15 cybersecurity

# Inferred from date
python generate.py cybersecurity --date "January 15, 2026"

# Both provided - day parameter takes precedence
python generate.py 15 cybersecurity --date "December 1, 2026"
# Uses day 15, displays "December 1, 2026"
```

## Implementation Guidance

You decide:
- Exact argparse configuration (positional vs optional for day parameter)
- Date parsing approach (datetime.strptime, dateutil, etc.)
- Error message wording
- Whether to add a `--start-date` config option for flexibility
- Helper function structure

## Testing

Generate test cases covering:
- First day (January 1, 2026)
- Last day (December 31, 2026)
- Middle of year
- Invalid dates
- Out of range dates

## Documentation

Update README.md and CLAUDE.md to reflect new usage patterns.
