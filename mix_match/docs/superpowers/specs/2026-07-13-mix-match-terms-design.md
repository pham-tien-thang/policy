# Mix & Match Terms Page Design

## Scope

Create an interim English Terms and Conditions page from the screenshots supplied on July 13, 2026. Preserve every visible sentence and the screenshot order. The currently supplied body content covers the introduction, table of contents, sections 1–5, and sections 7–11. Do not invent section 6 or sections 12–31.

## Structure

- Create `terms_mix_match.html` as a standalone, dependency-free HTML document.
- Reproduce the title, last-updated date, agreement text, and all 31 table-of-contents labels.
- Add body sections only where screenshot text is available: 1, 2, 3, 4, 5, 7, 8, 9, 10, and 11.
- Give available headings stable IDs based on their English slugs. Table-of-contents entries link to those IDs; unavailable entries keep their future IDs so later screenshots can be appended without changing the table of contents.

## Links

- Render `meocungptt@gmail.com` as `mailto:meocungptt@gmail.com` everywhere it appears.
- Link every blue `PROHIBITED ACTIVITIES` reference to `#prohibited-activities`.
- Render all table-of-contents rows as blue in-page links.

## Presentation

Use Arial/Helvetica, black headings, gray body copy, blue links, and responsive spacing matching the screenshots. Use semantic headings, paragraphs, lists, and sections while preserving the visible wording and capitalization.

## Verification

Automated checks verify file structure, section order, required copy fragments, email links, internal links, and absence of invented section-6 body text. Browser verification checks desktop and narrow layouts, readable typography, and anchor behavior.
