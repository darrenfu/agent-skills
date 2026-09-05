---
name: school-calendar-source-finder
description: Find, verify, and document official school calendar sources for public districts and private schools, especially when the requested school year may not be visible from the main calendar page.
---

# School Calendar Source Finder

## Overview

Use this skill when a task requires finding school calendar sources, verifying that they match a requested academic year, extracting no-school or half-day dates, or explaining source status for schools whose calendars are not yet published.

## Workflow

1. Start with official sources.
   - Use district or school domains first.
   - Prefer official calendar PDFs, embedded calendar pages, iCal feeds, and official file hosts linked from school pages.
   - Browse live sources because school calendar links and publications change frequently.

2. Verify the school year before importing data.
   - Download or open the file and inspect visible text.
   - Confirm the requested academic year appears in the title, header, footer, or body.
   - If a page redirects to an older year, record that as stale and keep looking. Do not import old-year dates for a new-year request.

3. Preserve the hierarchy the source supports.
   - Public districts often publish one district calendar. Model district-level calendars first, then attach school and grade profiles to that source.
   - If a school publishes division calendars, keep those profiles separate, such as preschool, kindergarten, elementary, middle, upper, or all-school.

4. Classify every source.
   - `confirmed`: current-year official source was verified and can be used for dates.
   - `source-only`: official page or current-year source exists, but dates are not fully transcribed or grade-specific details are unclear.
   - `stale-source`: official page exists but links or redirects to a prior-year source.
   - `not-published`: no current-year official calendar was found after checking normal source paths.

5. Record evidence.
   - Save source URL, local file path if downloaded, checked date, status, and notes.
   - Include stale redirect notes when relevant so the next pass does not repeat the same false lead.
   - For generated apps or databases, keep unconfirmed items visible as source-status records but exclude them from confirmed overlap math.
   - When building a profile picker, hide `source-only`, `stale-source`, and `not-published` profiles until verified date rows exist. Keep those records in the source inventory instead of making them selectable.

## Extraction

- Prefer structured downloads over visual scraping when possible.
- For PDF calendars, use `pdftotext -layout` before parsing dates. The layout mode keeps month grids more readable.
- Normalize multi-day breaks as inclusive date ranges.
- Store half-days separately from full no-school days.
- Keep event titles close to source wording, but avoid copying long source text.

## Deeper Patterns

Read `references/patterns.md` when the first-pass source hunt does not find the requested year, when official links are stale, or when a school uses Finalsite, WordPress, HubSpot, or embedded calendar tooling.
