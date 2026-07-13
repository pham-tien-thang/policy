# Terms Language Switch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a complete English/Vietnamese switch to the Mix & Match Terms page.

**Architecture:** The standalone HTML contains one complete semantic document per language. A small inline script toggles `hidden`, page language metadata, button state, and equivalent section hashes without external dependencies.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python `unittest`

## Global Constraints

- English is visible by default.
- Vietnamese translates the full agreement and all 31 sections.
- Vietnamese IDs use the `vi-` prefix.
- Names, email, platform names, amounts, and Privacy Policy URL remain unchanged.
- The page remains dependency-free.

---

### Task 1: Add the bilingual structural contract

**Files:**
- Modify: `test/terms_mix_match_test.py`
- Test: `test/terms_mix_match_test.py`

**Interfaces:**
- Consumes: `terms_mix_match.html`.
- Produces: assertions for `#languageToggle`, `#content-en`, `#content-vi`, two ordered 31-section documents, valid language-local table-of-contents targets, and the toggle script.

- [ ] Write tests requiring English to be visible, Vietnamese to be hidden, and both documents to contain 31 ordered sections.
- [ ] Require Vietnamese copy markers from the agreement, sections 1, 13, 24, and 31.
- [ ] Require four `mailto:` links per language, one Privacy Policy link per language, and the toggle script metadata updates.
- [ ] Run `python3 -m unittest test/terms_mix_match_test.py`; expect failure because the bilingual structure is absent.

### Task 2: Add the switch and complete Vietnamese document

**Files:**
- Modify: `terms_mix_match.html`
- Test: `test/terms_mix_match_test.py`

**Interfaces:**
- Consumes: the bilingual structural contract from Task 1.
- Produces: the fixed language button, complete `#content-en` and `#content-vi` documents, and deterministic toggle behavior.

- [ ] Wrap the English `<main>` in `#content-en` and add the fixed accessible button.
- [ ] Add the complete Vietnamese `<main id="content-vi" lang="vi" hidden>` with `vi-` section IDs and links.
- [ ] Add inline JavaScript that toggles visibility, document language, title, button label, `aria-pressed`, and equivalent hashes.
- [ ] Run `python3 -m unittest test/terms_mix_match_test.py`; expect all tests to pass.

### Task 3: Verify the final standalone document

**Files:**
- Verify: `terms_mix_match.html`
- Verify: `test/terms_mix_match_test.py`

**Interfaces:**
- Consumes: the completed bilingual page.
- Produces: evidence that both languages and all links are structurally complete.

- [ ] Parse the HTML with `lxml` in strict recovery-disabled mode.
- [ ] Verify 62 total legal section headings, 62 valid table-of-contents targets, eight email links, and two Privacy Policy links.
- [ ] Run `python3 -m unittest test/terms_mix_match_test.py` and scan for trailing whitespace.
