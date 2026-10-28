<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · **Polski** · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**System operacyjny dla zespołu agentów AI.** Jedno polecenie zamienia zwykły folder w zdyscyplinowane biuro: jedna tablica, z której pracuje każdy agent, na dowolnej platformie; niezależna kontrola jakości; zarządzanie decyzjami; pełny ślad audytowy; metryki wydajności eksportowane do Power BI oraz witryna zarządzania działająca z jednego pliku HTML.

Python 3.9 lub nowszy, bez zależności, bez serwera. Otwarte oprogramowanie na licencji MIT.

Strona internetowa: https://hakamidev.github.io/ProjectForge/

## Instalacja

Jedna linijka wklejona w terminalu. Pobiera narzędzie, uruchamia je, zadaje cztery pytania, a następnie otwiera witrynę zarządzania.

macOS i Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Na stronie można też najpierw wybrać platformę i preferowany język; oba wybory są przenoszone do polecenia instalacji i wstępnie zaznaczone w kreatorze.

## Jakie problemy rozwiązuje

- **Czaty zapominają.** Zasady i opisy ról znajdują się w folderze, a nie w pamięci czatu, więc każdy czat może wznowić pracę.
- **Agenci wchodzą sobie w drogę.** Jedna numerowana tablica; status „w toku” blokuje wiersz; suma kontrolna zapobiega sprzecznym zapisom.
- **Niesprawdzone wyniki.** Szef zapewnienia jakości orzeka o zaliczeniu lub odrzuceniu, zanim cokolwiek trafi do właściciela.
- **Zablokowane decyzje.** Najwyżej pięć otwartych decyzji oraz reguła 48 godzin, po której obowiązuje rekomendacja.
- **Nic nie jest mierzone.** `report` podaje wskaźnik realizacji, czas cyklu, odsetek zaliczonych kontroli QA i obciążenie według ról; `export` zapisuje pliki CSV dla Power BI.
- **Brak rozliczalności.** Każdy zapis na tablicy jest rejestrowany: kto, kiedy i co.
- **Dane wrażliwe w narzędziach zewnętrznych.** Wiążąca polityka danych z klasyfikacją i zatwierdzonymi narzędziami.

## Co otrzymujesz

- **80 specjalizacji** (strategia, gastronomia, nieruchomości, oprogramowanie, HR, edukacja i inne) z ponad 330 gotowymi rolami dodawanymi jednym kliknięciem.
- **130 gotowych umiejętności w 18 grupach.** Umiejętność to krótki plik opisujący, kiedy jej użyć, jakie są jej kroki, jaki jest wynik i kryterium akceptacji, dzięki czemu pracownik stosuje ją zamiast improwizować.
- **Cztery platformy:** Claude, ChatGPT, Grok i Gemini. Każdy pracownik może działać na innej platformie.
- **27 języków interfejsu** na stronie i w kreatorze. Preferowany język jest językiem zarządzania całym systemem i językiem komunikacji z pracownikami.
- **Witryna zarządzania** z jednego pliku HTML: tablica, zespół, decyzje, metryki, biblioteka gotowych poleceń oraz mechanizm uwagi, który wskazuje, co jest opóźnione lub czeka na Ciebie.

## Polecenia

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Platformy

| Platforma | Jak skonfigurować zespół |
| --- | --- |
| Claude | Utwórz projekt o nazwie takiej jak Twój projekt i dodaj wygenerowany folder. |
| ChatGPT | Utwórz projekt i prześlij pliki z folderu. |
| Grok | Utwórz projekt, wklej polecenie Compass do jego instrukcji i dodaj pliki. |
| Gemini | Utwórz Gem dla każdego pracownika, wklej jego polecenie do instrukcji i dodaj pliki w sekcji Knowledge. |

Przesyłaj pliki z folderu projektu w jego pierwotnej lokalizacji i ponownie przesyłaj to, co się zmienia. Według naszej najlepszej wiedzy Grok i Gemini nie zapisują bezpośrednio w folderze, więc ich wyniki przenieś do folderu samodzielnie. Kroki opierają się na publicznej dokumentacji z chwili pisania; interfejsy i limity ustalają te platformy i mogą się zmienić.

## Obecne ograniczenia

- Kreator i strona są dostępne w 27 językach, ale wygenerowane pliki projektu (zasady, opisy ról, tablica) oraz witryna zarządzania są na razie pisane po arabsku. Pracownicy dowiadują się, w jakim języku mają pracować, i odpowiadają Ci w nim.
- Nazwy plików, polecenia i słowa statusów tablicy pozostają po arabsku, ponieważ narzędzie odczytuje je dosłownie.
- Instalacja w systemie Windows nie została jeszcze przetestowana na prawdziwym komputerze.

## Dla programistów

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Kod źródłowy znajduje się w `forge/`; `tools/build-single.py` tworzy jednoplikowe narzędzie w `dist/`. Szablony są w `forge/templates/`, publiczna witryna w `site/`.

## Licencja

MIT.
