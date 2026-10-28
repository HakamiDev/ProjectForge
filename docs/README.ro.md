<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · **Română** · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Un sistem de operare pentru o echipă de agenți AI.** O singură comandă transformă un simplu dosar într-un birou disciplinat: un singur tablou din care lucrează fiecare agent, pe orice platformă; o poartă independentă de calitate; guvernanța deciziilor; o pistă de audit completă; indicatori de performanță exportabili în Power BI și un site de management care rulează dintr-un singur fișier HTML.

Python 3.9 sau mai nou, fără dependențe, fără server. Cod deschis, sub licență MIT.

Site web: https://hakamidev.github.io/ProjectForge/

## Instalare

O singură linie, lipită într-un terminal. Descarcă instrumentul, îl rulează, pune patru întrebări, apoi deschide site-ul de management.

macOS și Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Site-ul vă permite, de asemenea, să alegeți mai întâi platforma și limba preferată; ambele sunt preluate în comanda de instalare și preselectate în asistent.

## Ce rezolvă

- **Conversațiile uită.** Regulile și fișele de rol se află în dosar, nu în memoria conversației, astfel încât orice conversație poate relua lucrul.
- **Agenții se ciocnesc.** Un singur tablou numerotat; starea „în curs” blochează un rând; o sumă de control previne scrierile conflictuale.
- **Rezultate neverificate.** Un șef al asigurării calității hotărăște dacă rezultatul este admis sau respins înainte ca ceva să ajungă la proprietar.
- **Decizii blocate.** Cel mult cinci decizii deschise și o regulă de 48 de ore, după care recomandarea rămâne în vigoare.
- **Nimic nu este măsurat.** `report` oferă rata de livrare, durata ciclului, rata de promovare a verificărilor QA și încărcarea pe roluri; `export` scrie fișiere CSV pentru Power BI.
- **Lipsa responsabilității.** Fiecare scriere în tablou este înregistrată: cine, când și ce.
- **Date sensibile în instrumente externe.** O politică obligatorie privind datele, cu clasificare și instrumente aprobate.

## Ce primiți

- **80 de specializări** (strategie, restaurante, imobiliare, software, resurse umane, educație și altele) cu peste 330 de roluri gata făcute, pe care le adăugați dintr-un clic.
- **130 de abilități gata făcute în 18 grupuri.** O abilitate este un fișier scurt care descrie când se folosește, pașii ei, rezultatul și criteriul de acceptare, astfel încât un angajat o aplică în loc să improvizeze.
- **Patru platforme:** Claude, ChatGPT, Grok și Gemini. Fiecare angajat poate lucra pe o platformă diferită.
- **27 de limbi de interfață** pe site și în asistent. Limba preferată este limba de administrare a întregului sistem și cea folosită cu angajații.
- **Un site de management** dintr-un singur fișier HTML: tablou, echipă, decizii, indicatori, o bibliotecă de comenzi gata făcute și un motor de atenție care semnalează ce întârzie sau ce așteaptă răspunsul dumneavoastră.

## Comenzi

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Platforme

| Platformă | Cum se configurează echipa |
| --- | --- |
| Claude | Creați un proiect cu numele proiectului dumneavoastră și adăugați dosarul generat. |
| ChatGPT | Creați un proiect și încărcați fișierele din dosar. |
| Grok | Creați un proiect, lipiți comanda Compass în instrucțiunile lui și adăugați fișierele. |
| Gemini | Creați un Gem pentru fiecare angajat, lipiți comanda lui în instrucțiuni și adăugați fișierele la Knowledge. |

Încărcați fișierele din dosarul proiectului în locația sa originală și reîncărcați ceea ce se modifică. Din câte știm, Grok și Gemini nu scriu direct în dosar, așa că mutați singuri rezultatele lor în dosar. Pașii urmează documentația publică de la momentul redactării; interfețele și limitele sunt stabilite de aceste platforme și se pot schimba.

## Limite actuale

- Asistentul și site-ul web apar în 27 de limbi, dar fișierele de proiect generate (reguli, fișe de rol, tablou) și site-ul de management sunt scrise deocamdată în limba arabă. Angajaților li se spune în ce limbă să lucreze și vă răspund în ea.
- Numele fișierelor, comenzile și cuvintele de stare ale tabloului rămân în arabă, deoarece instrumentul le citește literal.
- Instalarea pe Windows nu a fost încă testată pe o mașină reală.

## Pentru dezvoltatori

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Codul sursă se află în `forge/`; `tools/build-single.py` produce instrumentul dintr-un singur fișier în `dist/`. Șabloanele sunt în `forge/templates/`, site-ul public în `site/`.

## Licență

MIT.
