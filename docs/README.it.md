<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · **Italiano** · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Un sistema operativo per un team di agenti AI.** Un solo comando trasforma una semplice cartella in un ufficio disciplinato: una bacheca unica da cui lavorano tutti gli agenti, su qualsiasi piattaforma; un controllo qualità indipendente; una governance delle decisioni; una traccia di audit completa; metriche di performance esportabili in Power BI; e un sito di gestione che funziona da un solo file HTML.

Python 3.9 o successivo, nessuna dipendenza, nessun server. Open source, con licenza MIT.

Sito web: https://hakamidev.github.io/ProjectForge/

## Installazione

Una sola riga, da incollare in un terminale. Scarica lo strumento, lo esegue, pone quattro domande e poi apre il tuo sito di gestione.

macOS e Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Il sito permette inoltre di scegliere in anticipo la piattaforma e la lingua preferita; entrambe vengono inserite nel comando di installazione e preselezionate nella procedura guidata.

## Quali problemi risolve

- **Le chat dimenticano.** Le regole e le schede dei ruoli risiedono nella cartella, non nella memoria della chat, quindi qualsiasi chat può riprendere il lavoro.
- **Gli agenti si scontrano.** Una bacheca numerata; "in corso" blocca una riga; un controllo tramite checksum impedisce scritture in conflitto.
- **Output non verificato.** Un responsabile della garanzia della qualità decide se promuovere o respingere il lavoro prima che raggiunga il titolare.
- **Decisioni in stallo.** Al massimo cinque decisioni aperte e una regola delle 48 ore, scadute le quali vale la raccomandazione.
- **Nulla viene misurato.** `report` fornisce tasso di consegna, tempo di ciclo, tasso di superamento del QA e carico per ruolo; `export` scrive file CSV per Power BI.
- **Nessuna responsabilità.** Ogni scrittura sulla bacheca viene registrata: chi, quando e che cosa.
- **Dati sensibili in strumenti esterni.** Una policy sui dati vincolante, con classificazione e strumenti approvati.

## Che cosa ottieni

- **80 specializzazioni** (strategia, ristorazione, immobiliare, software, risorse umane, istruzione e altro) con oltre 330 ruoli pronti da aggiungere con un clic.
- **130 competenze pronte in 18 gruppi.** Una competenza è un breve file che descrive quando usarla, i passaggi, il risultato e il criterio di accettazione, così il collaboratore la applica invece di improvvisare.
- **Quattro piattaforme:** Claude, ChatGPT, Grok e Gemini. Ogni collaboratore può lavorare su una piattaforma diversa.
- **27 lingue dell'interfaccia** sul sito web e nella procedura guidata. La lingua preferita è quella con cui si gestisce l'intero sistema e che si usa con i collaboratori.
- **Un sito di gestione** da un solo file HTML: bacheca, team, decisioni, metriche, una libreria di comandi pronti e un motore di attenzione che segnala ciò che è in ritardo o in attesa di te.

## Comandi

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Piattaforme

| Piattaforma | Come si configura il team |
| --- | --- |
| Claude | Crea un progetto con il nome del tuo progetto e aggiungi la cartella generata. |
| ChatGPT | Crea un progetto e carica i file della cartella. |
| Grok | Crea un progetto, incolla il comando Compass nelle sue istruzioni e aggiungi i file. |
| Gemini | Crea un Gem per ogni collaboratore, incolla il suo comando nelle istruzioni e aggiungi i file in Knowledge. |

Carica i file dalla cartella del progetto nella sua posizione originale e ricarica quelli che cambiano. Per quanto ne sappiamo, Grok e Gemini non scrivono direttamente nella cartella, quindi sposta tu stesso i loro output al suo interno. I passaggi seguono la documentazione pubblica al momento della stesura; le interfacce e i limiti sono definiti da tali piattaforme e possono cambiare.

## Limiti attuali

- La procedura guidata e il sito web sono disponibili in 27 lingue, ma i file di progetto generati (regole, schede dei ruoli, bacheca) e il sito di gestione sono per ora scritti in arabo. I collaboratori ricevono l'indicazione della lingua in cui lavorare e ti rispondono in quella lingua.
- I nomi dei file, i comandi e i termini di stato della bacheca restano in arabo perché lo strumento li legge alla lettera.
- L'installazione su Windows non è ancora stata testata su una macchina reale.

## Per gli sviluppatori

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Il codice sorgente si trova in `forge/`; `tools/build-single.py` produce lo strumento a file singolo in `dist/`. I modelli sono in `forge/templates/`, il sito pubblico in `site/`.

## Licenza

MIT.
