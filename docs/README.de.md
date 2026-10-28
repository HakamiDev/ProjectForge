<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · **Deutsch** · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Ein Betriebssystem für ein Team aus KI-Agenten.** Ein einziger Befehl macht aus einem gewöhnlichen Ordner ein diszipliniertes Büro: ein gemeinsames Board, von dem alle Agenten auf jeder Plattform arbeiten; ein unabhängiges Qualitätstor; Entscheidungs-Governance; ein lückenloser Prüfpfad; Leistungskennzahlen, die sich nach Power BI exportieren lassen; und eine Verwaltungsseite, die aus einer einzigen HTML-Datei läuft.

Python 3.9 oder neuer, keine Abhängigkeiten, kein Server. Open Source, unter MIT-Lizenz.

Website: https://hakamidev.github.io/ProjectForge/

## Installation

Eine Zeile, in ein Terminal eingefügt. Sie lädt das Werkzeug herunter, führt es aus, stellt vier Fragen und öffnet anschließend Ihre Verwaltungsseite.

macOS und Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Auf der Website können Sie außerdem vorab Ihre Plattform und Ihre bevorzugte Sprache wählen; beides fließt in den Installationsbefehl ein und ist im Assistenten vorausgewählt.

## Was es löst

- **Chats vergessen.** Regeln und Rollenbeschreibungen liegen im Ordner, nicht im Chat-Gedächtnis, sodass jeder Chat die Arbeit wieder aufnehmen kann.
- **Agenten kollidieren.** Ein nummeriertes Board; „in Arbeit“ sperrt eine Zeile; eine Prüfsummen-Sperre verhindert widersprüchliche Schreibvorgänge.
- **Ungeprüfte Ergebnisse.** Ein Leiter der Qualitätssicherung entscheidet über Bestanden oder Nicht bestanden, bevor irgendetwas den Eigentümer erreicht.
- **Blockierte Entscheidungen.** Höchstens fünf offene Entscheidungen und eine 48-Stunden-Regel, nach der die Empfehlung gilt.
- **Nichts wird gemessen.** `report` liefert Lieferquote, Durchlaufzeit, QA-Bestehensquote und Auslastung je Rolle; `export` schreibt CSV-Dateien für Power BI.
- **Keine Nachvollziehbarkeit.** Jeder Schreibvorgang auf dem Board wird protokolliert: wer, wann und was.
- **Sensible Daten in externen Werkzeugen.** Eine verbindliche Datenrichtlinie mit Klassifizierung und freigegebenen Werkzeugen.

## Was Sie erhalten

- **80 Spezialisierungen** (Strategie, Gastronomie, Immobilien, Software, Personalwesen, Bildung und mehr) mit mehr als 330 fertigen Rollen, die Sie mit einem Klick hinzufügen.
- **130 fertige Skills in 18 Gruppen.** Ein Skill ist eine kurze Datei, die beschreibt, wann er einzusetzen ist, welche Schritte er umfasst, was er liefert und nach welchem Abnahmekriterium er bewertet wird, sodass ein Mitarbeiter ihn anwendet, statt zu improvisieren.
- **Vier Plattformen:** Claude, ChatGPT, Grok und Gemini. Jeder Mitarbeiter kann auf einer anderen Plattform arbeiten.
- **27 Oberflächensprachen** auf der Website und im Assistenten. Die bevorzugte Sprache ist die Sprache für die Verwaltung des gesamten Systems und die Sprache im Umgang mit den Mitarbeitern.
- **Eine Verwaltungsseite** aus einer einzigen HTML-Datei: Board, Team, Entscheidungen, Kennzahlen, eine Bibliothek fertiger Befehle und eine Aufmerksamkeits-Engine, die meldet, was überfällig ist oder auf Sie wartet.

## Befehle

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Plattformen

| Plattform | So wird das Team eingerichtet |
| --- | --- |
| Claude | Erstellen Sie ein Projekt mit dem Namen Ihres Projekts und fügen Sie den generierten Ordner hinzu. |
| ChatGPT | Erstellen Sie ein Projekt und laden Sie die Dateien des Ordners hoch. |
| Grok | Erstellen Sie ein Projekt, fügen Sie den Compass-Befehl in dessen Anweisungen ein und fügen Sie die Dateien hinzu. |
| Gemini | Erstellen Sie pro Mitarbeiter ein Gem, fügen Sie dessen Befehl in die Anweisungen ein und legen Sie die Dateien unter Knowledge ab. |

Laden Sie die Dateien aus dem Projektordner an seinem ursprünglichen Speicherort hoch und laden Sie Geändertes erneut hoch. Nach unserem Kenntnisstand schreiben Grok und Gemini nicht direkt in den Ordner; verschieben Sie deren Ergebnisse daher selbst in den Ordner. Die Schritte folgen der öffentlichen Dokumentation zum Zeitpunkt der Erstellung; Oberflächen und Limits werden von diesen Plattformen festgelegt und können sich ändern.

## Aktuelle Einschränkungen

- Der Assistent und die Website erscheinen in 27 Sprachen, die generierten Projektdateien (Regeln, Rollenbeschreibungen, Board) und die Verwaltungsseite sind derzeit jedoch auf Arabisch verfasst. Die Mitarbeiter erhalten die Anweisung, in welcher Sprache sie arbeiten, und antworten Ihnen in dieser Sprache.
- Dateinamen, Befehle und die Statusbegriffe des Boards bleiben Arabisch, da das Werkzeug sie wörtlich liest.
- Die Installation unter Windows wurde noch nicht auf einem echten Rechner getestet.

## Für Entwickler

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Der Quellcode liegt in `forge/`; `tools/build-single.py` erzeugt das Ein-Datei-Werkzeug in `dist/`. Die Vorlagen befinden sich in `forge/templates/`, die öffentliche Website in `site/`.

## Lizenz

MIT.
