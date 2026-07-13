# Mix & Match Terms Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the interim Mix & Match Terms and Conditions HTML page from all supplied screenshots without inventing missing legal copy.

**Architecture:** A dependency-free semantic HTML document contains the agreement, a 31-item linked table of contents, and only the body sections supplied by screenshots. A Python standard-library test parses the document and validates structure, ordering, and link behavior.

**Tech Stack:** HTML5, CSS3, Python 3 `unittest` and `html.parser`

## Global Constraints

- Preserve screenshot wording, capitalization, and ordering.
- Include body content for sections 1–5 and 7–11 only.
- Do not create body copy for section 6 or sections 12–31.
- Use `mailto:meocungptt@gmail.com` for email links.
- Use `#prohibited-activities` for inline references to section 10.
- Keep the page standalone with no external dependencies.

---

### Task 1: Contract test for the reconstructed page

**Files:**
- Create: `test/terms_mix_match_test.py`
- Test: `test/terms_mix_match_test.py`

**Interfaces:**
- Consumes: `terms_mix_match.html` from the workspace root.
- Produces: executable structural and copy checks using `python3 -m unittest test/terms_mix_match_test.py`.

- [ ] **Step 1: Write the failing test**

  Implement a standard-library HTML parser that records IDs, links, heading text, and normalized document text. Assert the exact 31 table-of-contents labels; the available heading order `1, 2, 3, 4, 5, 7, 8, 9, 10, 11`; the agreement title and date; distinctive sentence fragments from every supplied screenshot; both email links; and both `PROHIBITED ACTIVITIES` internal references. Assert that no `6. PURCHASES AND PAYMENT` body heading is present.

- [ ] **Step 2: Run test to verify it fails**

  Run: `python3 -m unittest test/terms_mix_match_test.py`

  Expected: FAIL because `terms_mix_match.html` does not exist.

### Task 2: Reconstruct the interim Terms page

**Files:**
- Create: `terms_mix_match.html`
- Test: `test/terms_mix_match_test.py`

**Interfaces:**
- Consumes: the screenshot transcription contract from Task 1.
- Produces: a standalone HTML5 page with stable section IDs, working `mailto:` links, and working internal links.

- [ ] **Step 1: Add the semantic HTML structure and screenshot-matched CSS**

  Use `<main>`, `<nav aria-labelledby="table-of-contents">`, `<section>`, ordered and unordered lists. Use Arial/Helvetica; `#000` headings; `#595959` body copy; `#001eff` links; responsive horizontal padding; and vertical spacing that follows the screenshots.

- [ ] **Step 2: Transcribe supplied copy in exact order**

  Add the agreement and table of contents, then sections 1–5 and 7–11. Join screenshot continuations for section 2 and section 10 into their corresponding paragraphs and lists. Do not add an empty or visible section 6.

- [ ] **Step 3: Wire links**

  Link table-of-contents labels to stable slugs, email text to `mailto:meocungptt@gmail.com`, and inline `PROHIBITED ACTIVITIES` text to `#prohibited-activities`.

- [ ] **Step 4: Run the contract test**

  Run: `python3 -m unittest test/terms_mix_match_test.py`

  Expected: PASS.

### Task 3: Visual and final verification

**Files:**
- Verify: `terms_mix_match.html`
- Verify: `test/terms_mix_match_test.py`

**Interfaces:**
- Consumes: the completed standalone page.
- Produces: verified desktop and narrow-screen output ready for later screenshot additions.

- [ ] **Step 1: Open the page in the in-app browser**

  Verify the title, date, paragraph width, heading hierarchy, list indentation, gray copy, blue links, and section spacing against the supplied screenshots.

- [ ] **Step 2: Verify link behavior**

  Click the table-of-contents links for available sections and the inline `PROHIBITED ACTIVITIES` links. Inspect the email links for the correct `mailto:` target.

- [ ] **Step 3: Run final checks**

  Run: `python3 -m unittest test/terms_mix_match_test.py && git diff --check`

  Expected: all tests pass and `git diff --check` prints no errors.
