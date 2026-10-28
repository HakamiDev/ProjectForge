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
