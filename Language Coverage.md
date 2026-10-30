# Interface language coverage

Updated: 31 October 2026. Release: v2.1.2.

The wizard, the public site and every generated project support **8 languages**: Arabic plus seven. The selector is generated from `forge/core.py: LANGUAGES`; the translation tables live in `forge/templates/loc.json` (project files, tool and management site) and in the wizard and site templates (interface).

| Language value | Code | Wizard | Public site | Project files | Management site | Project tool |
| --- | --- | --- | --- | --- | --- | --- |
| العربية | ar | Available | Available | Available | Available | Available |
| English | en | Available | Available | Available | Available | Available |
| Español | es | Available | Available | Available | Available | Available |
| Македонски (Macedonian) | mk | Available | Available | Available | Available | Available |
| Deutsch | de | Available | Available | Available | Available | Available |
| 中文 (Chinese) | zh | Available | Available | Available | Available | Available |
| Português | pt | Available | Available | Available | Available | Available |
| Русский (Russian) | ru | Available | Available | Available | Available | Available |

## Scope and review limits

- Choosing a language at the start localizes the generated files and their names, role briefs, skills, command library, reports, the whole management site and the project's own tool. The language is stored in `Agents/Team.json` (`lang_code`); a tool of another language refuses to run on the project.
- Exempt programmatic text stays English: structural file and folder names (for example `Agents/Board.md`, `Docs/Decision Log.md`), command names and options, CSV column headers, and code.
- Terminal messages follow the project language in the seven non-Arabic project tools (messages, prompts and `--help` descriptions). The installers and the wizard launcher follow `FORGE_LANGUAGE` from the install line. Arabic terminal output stays English because terminals do not shape right-to-left Arabic reliably; argparse's own headings and messages (`usage`, `positional arguments`, `options`, required/invalid-argument errors) follow the same language, through a translation table in `loc.json` (`cli`).
- The public site shows tool and agent command examples with each language's role names, statuses and values, and project-level commands run the project's own `Tools/Project Forge 1.py`.
- Register: the wizard and public site address the owner formally; the management site uses the informal register in German, Macedonian, Spanish and Portuguese. This is a known difference, not a defect.
- Left-to-right languages switch the management site to left-to-right layout; the header wraps when labels are long.
- CI checks that no Arabic remains in any generated file, file name or site page for each non-Arabic language.
- Translations have automated review. No native-speaker review is claimed.
- Consistency pass (29 October, final): one word per status in every language across the tool, the management site, the briefs and the wizard (Portuguese «Em curso», Chinese «已分派»); the wizard's command library names skills, statuses and the Automation Engineer in the reader's language in every entry; the public site drops a remembered language that is no longer offered and falls back to English; the wizard accepts `FORGE_LANGUAGE` written as the native, English or Arabic language name.
- Other languages removed from the registry (French, Italian, Dutch, Turkish, Ukrainian, Polish, Romanian, Greek, Persian, Urdu, Hindi, Bengali, Indonesian, Malay, Vietnamese, Thai, Japanese, Korean, Swahili) are no longer offered, because their coverage was limited to the wizard interface.
