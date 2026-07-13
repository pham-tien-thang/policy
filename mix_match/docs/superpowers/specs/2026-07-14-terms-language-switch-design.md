# Terms Language Switch Design

## Scope

Add a complete English/Vietnamese switch to `terms_mix_match.html`. English remains the default. Vietnamese mode translates the heading, updated date, agreement, table of contents, all subheadings, and all 31 legal sections. Names, email addresses, product names, platform names, prices, and the Privacy Policy URL remain unchanged.

## Structure and behavior

- Keep the existing English document in `#content-en`.
- Add a complete Vietnamese document in `#content-vi`, hidden initially.
- Prefix Vietnamese section IDs with `vi-`; each table of contents links only to sections in the same language.
- Add a fixed `#languageToggle` button labeled `Dịch sang tiếng Việt` in English mode and `Translate to English` in Vietnamese mode.
- On toggle, update the visible document, `<html lang>`, `<title>`, `aria-pressed`, and the current section hash when possible.
- Keep all email and external links functional in both languages.

## Verification

Automated tests require 31 ordered sections and 31 valid table-of-contents targets in each language, the complete Vietnamese copy markers, four email links in each language, two Privacy Policy links total, default English visibility, and the language-switch script contract.
