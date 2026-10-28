# v1.1.8 — Site copy and dropdown alignment

- The generated project office now follows the working language: for any non-Arabic project it displays in English, left to right (about 1,000 interface phrases translated). Arabic projects are unchanged. Names of preset roles and project data stay as written.
- The desktop-icon button shows a clear bilingual message when macOS blocks updating an existing icon.
- Public homepage leads with the unified agent-team promise, followed by six concrete capabilities in Arabic and English.
- Dropdown indicators align with the reading direction on the public site, wizard, and generated project office.
- Project-office settings now include working section order and visibility, labels, accent, font size, density, and local export/import, alongside the existing appearance controls.
- This release builds on the unified 27-language tool (80 specialties, 334 roles, 130 skills). Interface translations beyond Arabic and English retain their existing coverage.
- Local validation: 25 unit tests, 3 release checks, standalone selftest. Browser QA and an actual Windows install remain separate checks.

# Local candidate 1.1.0

Updated: 28 October 2026. This document does not claim a published release.

## Integration

The starting repository already included merge commit `1e848d8`, combining the design and language-review branches. This candidate preserves that merge instead of overwriting it with the older design package. The reviewed translation values and the design CSS, fonts and office template are retained.

## Corrections

- One interface-language registry drives the wizard and public site: 27 languages with dictionaries, instead of 32 selector choices. See `Language Coverage.md`.
- README distinguishes translated interfaces from primarily Arabic generated project files and documents 80 presets, 334 roles, 130 skills and 18 skill groups.
- Rebuilt public site and standalone tool come from the same source tree. CI checks artifact parity after building both.
- Regression tests check dictionary coverage, language-registry injection, standalone template/catalog parity and project creation in all 27 working languages.

## Validation limits

See `Verification Results.json` for local checks. Browser rendering of this integrated candidate and installation on an actual Windows device remain unverified. No claim is made about remote CI, the current published site, a clean-device installation or native-speaker translation review. Publishing and pushing remain owner actions.
