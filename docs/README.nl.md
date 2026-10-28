<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · **Nederlands** · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Een besturingssysteem voor een team van AI-agents.** Eén opdracht verandert een gewone map in een gedisciplineerd kantoor: één bord waarmee alle agents werken, op elk platform; een onafhankelijke kwaliteitspoort; besluitvorming met vaste regels; een volledig auditspoor; prestatiemetingen die naar Power BI te exporteren zijn; en een beheersite die draait vanuit één HTML-bestand.

Python 3.9 of nieuwer, geen afhankelijkheden, geen server. Open source, met MIT-licentie.

Website: https://hakamidev.github.io/ProjectForge/

## Installatie

Eén regel, die je in een terminal plakt. Het downloadt de tool, voert die uit, stelt vier vragen en opent daarna je beheersite.

macOS en Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Op de site kun je ook vooraf je platform en voorkeurstaal kiezen; beide worden in de installatieopdracht opgenomen en in de wizard vooraf geselecteerd.

## Wat het oplost

- **Chats vergeten.** Regels en rolbeschrijvingen staan in de map, niet in het chatgeheugen, zodat elke chat het werk kan hervatten.
- **Agents komen elkaar in de weg.** Eén genummerd bord; "in uitvoering" vergrendelt een rij; een checksum-controle voorkomt conflicterende schrijfacties.
- **Ongecontroleerde output.** Een hoofd kwaliteitsborging beslist over geslaagd of gezakt voordat iets de eigenaar bereikt.
- **Vastgelopen besluiten.** Maximaal vijf openstaande besluiten en een regel van 48 uur, waarna de aanbeveling geldt.
- **Er wordt niets gemeten.** `report` geeft leverpercentage, doorlooptijd, QA-slagingspercentage en belasting per rol; `export` schrijft CSV-bestanden voor Power BI.
- **Geen verantwoording.** Elke schrijfactie op het bord wordt vastgelegd: wie, wanneer en wat.
- **Gevoelige gegevens in externe tools.** Een bindend gegevensbeleid met classificatie en goedgekeurde tools.

## Wat je krijgt

- **80 specialisaties** (strategie, restaurants, vastgoed, software, HR, onderwijs en meer) met meer dan 330 kant-en-klare rollen die je met één klik toevoegt.
- **130 kant-en-klare vaardigheden in 18 groepen.** Een vaardigheid is een kort bestand dat beschrijft wanneer je die gebruikt, de stappen, het resultaat en het acceptatiecriterium, zodat een medewerker de vaardigheid toepast in plaats van te improviseren.
- **Vier platforms:** Claude, ChatGPT, Grok en Gemini. Elke medewerker kan op een ander platform werken.
- **27 interfacetalen** op de website en in de wizard. De voorkeurstaal is de taal waarin je het hele systeem beheert en waarin je met de medewerkers communiceert.
- **Een beheersite** vanuit één HTML-bestand: bord, team, besluiten, meetwaarden, een bibliotheek met kant-en-klare opdrachten en een aandachtsmotor die aangeeft wat te laat is of op jou wacht.

## Opdrachten

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Platforms

| Platform | Hoe het team wordt ingericht |
| --- | --- |
| Claude | Maak een project met de naam van je project en voeg de gegenereerde map toe. |
| ChatGPT | Maak een project en upload de bestanden uit de map. |
| Grok | Maak een project, plak de Compass-opdracht in de instructies en voeg de bestanden toe. |
| Gemini | Maak een Gem per medewerker, plak de opdracht van die medewerker in de instructies en voeg de bestanden toe onder Knowledge. |

Upload de bestanden vanuit de projectmap op de oorspronkelijke locatie en upload opnieuw wat verandert. Voor zover wij weten schrijven Grok en Gemini niet rechtstreeks naar de map, dus verplaats hun output zelf naar de map. De stappen volgen de openbare documentatie op het moment van schrijven; interfaces en limieten worden door die platforms bepaald en kunnen veranderen.

## Huidige beperkingen

- De wizard en de website zijn beschikbaar in 27 talen, maar de gegenereerde projectbestanden (regels, rolbeschrijvingen, bord) en de beheersite zijn voorlopig in het Arabisch geschreven. Medewerkers krijgen te horen in welke taal ze moeten werken en antwoorden je in die taal.
- Bestandsnamen, opdrachten en de statuswoorden van het bord blijven in het Arabisch omdat de tool ze letterlijk leest.
- Installatie op Windows is nog niet getest op een echte machine.

## Voor ontwikkelaars

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

De broncode staat in `forge/`; `tools/build-single.py` maakt de tool als enkel bestand in `dist/`. De sjablonen staan in `forge/templates/` en de openbare site in `site/`.

## Licentie

MIT.
