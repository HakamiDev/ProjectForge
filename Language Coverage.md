# Interface language coverage

Updated: 28 October 2026. Local candidate: 1.1.0.

The public site and creation wizard offer **27 languages**: Arabic, English, and 25 translated interfaces. Both selectors are generated from `forge/core.py: LANGUAGES`. CI checks that every listed language has translation data on both surfaces and that distributed artifacts match source.

| Language value | Code | Site | Wizard |
| --- | --- | --- | --- |
| العربية | ar | Available | Available |
| English | en | Available | Available |
| Français | fr | Available | Available |
| Español | es | Available | Available |
| Deutsch | de | Available | Available |
| Italiano | it | Available | Available |
| Português | pt | Available | Available |
| Nederlands | nl | Available | Available |
| Türkçe | tr | Available | Available |
| Русский (Russian) | ru | Available | Available |
| Українська (Ukrainian) | uk | Available | Available |
| Македонски (Macedonian) | mk | Available | Available |
| Polski | pl | Available | Available |
| Română | ro | Available | Available |
| Ελληνικά (Greek) | el | Available | Available |
| فارسی (Persian) | fa | Available | Available |
| اردو (Urdu) | ur | Available | Available |
| हिन्दी (Hindi) | hi | Available | Available |
| বাংলা (Bengali) | bn | Available | Available |
| Bahasa Indonesia | id | Available | Available |
| Bahasa Melayu | ms | Available | Available |
| Tiếng Việt | vi | Available | Available |
| ไทย (Thai) | th | Available | Available |
| 中文 (Chinese) | zh | Available | Available |
| 日本語 (Japanese) | ja | Available | Available |
| 한국어 (Korean) | ko | Available | Available |
| Kiswahili | sw | Available | Available |

## Scope and review limits

- Translation dictionaries include wizard commands, start-chat commands and server-error messages. Technical file paths, skill names and board status values stay literal. Role, preset and skill labels use English outside Arabic.
- Generated files on disk (including board, role briefs and command library) and the generated office UI remain primarily Arabic. Selecting a working language instructs agents to use that language; it does not translate every generated file.
- Translations have automated review. No native-speaker review or browser layout pass for this integrated candidate is claimed.
- Serbian, Croatian, Bosnian, Albanian and Bulgarian were stale selector entries without interface translation dictionaries. They are no longer advertised as translated interfaces. CLI users can still request an arbitrary working language.
- Hebrew is absent from the active language registry and translation dictionaries.
- Where translations previously relied on an unchanged English label (for example a shared product name), that identity mapping is now explicit; existing rendered wording is preserved.
