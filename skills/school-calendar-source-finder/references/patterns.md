# School Calendar Source Patterns

## Finalsite

- Search the school or district name plus the target year and `calendar pdf`.
- Official PDFs often live under `resources.finalsite.net`.
- If the visible page is dynamic, inspect page source and resource links for PDF paths.
- Download the file and run:

```bash
pdftotext -layout source.pdf -
```

- Treat search snippets as leads only. The PDF text must confirm the year.

## WordPress

- Check `page-sitemap.xml` for hidden calendar or download pages.
- Check `wp-json/wp/v2/pages?search=calendar` when sitemap links are sparse.
- Follow redirects with headers before trusting a link:

```bash
curl -IL "https://example-school.org/school-year-calendar/"
```

- WordPress pages may redirect to old PDFs. Record the stale redirect, then look for current files in the same official media or host pattern.

## HubSpot File Hosts

- Some private schools host admissions documents on HubSpot.
- If an official link points to an old file, inspect the URL structure for year, campus, and filename patterns.
- Probe only plausible current-year paths on the same official host, then verify by downloading and reading the PDF.
- Example pattern from this crawl: BASIS Bellevue's public redirect pointed to a 2025-2026 PDF, but the verified 2026-2027 file existed in the official `2026-2027 Admissions Documents/Bellevue` HubSpot folder.

## Embedded Calendars and iCal

- Look for iCal, RSS, JSON, or API links behind embedded calendars.
- If the embed is grade-filtered, preserve the filter or division name in the extracted profile.
- If an embedded calendar only exposes rolling events and not the requested academic year, classify it as `source-only` unless the requested dates are visible and verifiable.

## Public Districts

- District calendars are usually the authoritative base calendar.
- Only split by school or grade when the district publishes school-specific or grade-specific date differences.
- If grade-specific differences are limited to conference days, keep a district profile plus specific school or grade profiles for those differences.

## Private Schools

- Private schools often publish division-specific PDFs.
- Keep division profiles separate even when most dates overlap, because conference days, orientation, early release, or last day can differ.
- If the school is notable but has no public current-year calendar, keep a `not-published` profile with source notes rather than filling with guesses.

## Data Rules

- Use source statuses consistently: `confirmed`, `source-only`, `stale-source`, `not-published`.
- Do not put stale or unconfirmed dates into confirmed comparison math.
- Keep the source inventory visible to users so missing calendars are transparent and easy to update later.
- In user-facing builders, make only `confirmed` profiles with verified date rows selectable. Keep `source-only`, `stale-source`, and `not-published` entries visible only in the source inventory.
- Save local copies of PDFs when the final artifact needs reproducibility.
