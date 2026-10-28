<p align="center"><img src="site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

**English** · [العربية](docs/README.ar.md) · [Français](docs/README.fr.md) · [Español](docs/README.es.md) · [Deutsch](docs/README.de.md) · [Italiano](docs/README.it.md) · [Português](docs/README.pt.md) · [Nederlands](docs/README.nl.md) · [Türkçe](docs/README.tr.md) · [Русский](docs/README.ru.md) · [Українська](docs/README.uk.md) · [Македонски](docs/README.mk.md) · [Polski](docs/README.pl.md) · [Română](docs/README.ro.md) · [Ελληνικά](docs/README.el.md) · [فارسی](docs/README.fa.md) · [اردو](docs/README.ur.md) · [हिन्दी](docs/README.hi.md) · [বাংলা](docs/README.bn.md) · [Bahasa Indonesia](docs/README.id.md) · [Bahasa Melayu](docs/README.ms.md) · [Tiếng Việt](docs/README.vi.md) · [ไทย](docs/README.th.md) · [中文](docs/README.zh.md) · [日本語](docs/README.ja.md) · [한국어](docs/README.ko.md) · [Kiswahili](docs/README.sw.md)

</p>

**An operating system for a team of AI agents.** One command turns a plain folder into a disciplined office: a single board every agent works from, on any platform; an independent quality gate; decision governance; a full audit trail; performance metrics that export to Power BI; and a management site that runs from a single HTML file.

Python 3.9 or later, no dependencies, no server. Open source, MIT licensed.

Website: https://hakamidev.github.io/ProjectForge/

## Install

One line, pasted into a terminal. It downloads the tool, runs it, asks four questions, then opens your management site.

macOS and Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

The site also lets you pick your platform and preferred language first; both are carried into the install command and preselected in the wizard.

## What it solves

- **Chats forget.** Rules and role briefs live in the folder, not in chat memory, so any chat can resume the work.
- **Agents collide.** One numbered board; "in progress" locks a row; a checksum guard prevents conflicting writes.
- **Unchecked output.** A head of quality assurance rules pass or fail before anything reaches the owner.
- **Stalled decisions.** At most five open decisions, and a 48-hour rule after which the recommendation stands.
- **Nothing is measured.** `report` gives delivery rate, cycle time, QA pass rate and load per role; `export` writes CSV files for Power BI.
- **No accountability.** Every board write is logged: who, when and what.
- **Sensitive data in external tools.** A binding data policy with classification and approved tools.

## What you get

- **80 specialisations** (strategy, restaurants, real estate, software, HR, education and more) with more than 330 ready roles you add in one click.
- **130 ready skills in 18 groups.** A skill is a short file describing when to use it, its steps, its output and its acceptance criterion, so an employee applies it instead of improvising.
- **Four platforms:** Claude, ChatGPT, Grok and Gemini. Each employee can work on a different platform.
- **27 interface languages** on the website and in the wizard. The preferred language is the language for managing the whole system and the one used with the employees.
- **A management site** from one HTML file: board, team, decisions, metrics, a library of ready commands, and an attention engine that flags what is late or waiting on you.

## Commands

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Platforms

| Platform | How the team is set up |
| --- | --- |
| Claude | Create a project named after your project and add the generated folder. |
| ChatGPT | Create a project and upload the folder files. |
| Grok | Create a project, paste the Compass command into its instructions, and add the files. |
| Gemini | Create a Gem per employee, paste its command into the instructions, and add the files under Knowledge. |

Upload the files from the project folder in its original location and re-upload what changes. To the best of our knowledge Grok and Gemini do not write into the folder directly, so move their outputs into the folder yourself. The steps follow public documentation at the time of writing; interfaces and limits are set by those platforms and may change.

## Current limits

- The wizard and the website appear in 27 languages, but the generated project files (rules, role briefs, board) and the management site are written in Arabic for now. Employees are told which language to work in and answer you in it.
- File names, commands and the board's status words stay in Arabic because the tool reads them literally.
- Windows installation has not yet been tested on a real machine.

## For developers

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

The source is in `forge/`; `tools/build-single.py` produces the single-file tool in `dist/`. Templates are in `forge/templates/`, the public site in `site/`.

## License

MIT.
