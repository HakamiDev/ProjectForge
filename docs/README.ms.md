<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · **Bahasa Melayu** · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Sistem pengendalian untuk pasukan ejen AI.** Satu arahan menukar folder biasa menjadi pejabat yang berdisiplin: satu papan tunggal yang menjadi rujukan semua ejen, pada mana-mana platform; pintu kualiti yang bebas; tadbir urus keputusan; jejak audit yang lengkap; metrik prestasi yang boleh dieksport ke Power BI; dan tapak pengurusan yang berjalan daripada satu fail HTML.

Python 3.9 atau lebih baharu, tanpa kebergantungan, tanpa pelayan. Sumber terbuka, berlesen MIT.

Laman web: https://hakamidev.github.io/ProjectForge/

## Pemasangan

Satu baris, ditampal ke dalam terminal. Baris ini memuat turun alat tersebut, menjalankannya, mengemukakan empat soalan, kemudian membuka tapak pengurusan anda.

macOS dan Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Laman web juga membolehkan anda memilih platform dan bahasa pilihan terlebih dahulu; kedua-duanya dibawa ke dalam arahan pemasangan dan dipilih awal dalam wizard.

## Masalah yang diselesaikan

- **Sembang melupakan segala-galanya.** Peraturan dan ringkasan peranan disimpan dalam folder, bukan dalam ingatan sembang, supaya mana-mana sembang boleh menyambung kerja.
- **Ejen bertembung.** Satu papan bernombor; "dalam proses" mengunci sesuatu baris; pengawal checksum menghalang penulisan yang bercanggah.
- **Hasil kerja tidak disemak.** Ketua jaminan kualiti memutuskan lulus atau gagal sebelum sebarang hasil sampai kepada pemilik.
- **Keputusan tergendala.** Paling banyak lima keputusan terbuka, dan peraturan 48 jam yang selepasnya cadangan dikekalkan sebagai keputusan.
- **Tiada apa-apa yang diukur.** `report` memberikan kadar penghantaran, masa kitaran, kadar kelulusan QA dan beban bagi setiap peranan; `export` menulis fail CSV untuk Power BI.
- **Tiada akauntabiliti.** Setiap penulisan pada papan direkodkan: siapa, bila dan apa.
- **Data sensitif dalam alat luaran.** Dasar data yang mengikat dengan pengelasan dan alat yang diluluskan.

## Apa yang anda dapat

- **80 kepakaran** (strategi, restoran, hartanah, perisian, HR, pendidikan dan banyak lagi) dengan lebih daripada 330 peranan sedia ada yang boleh anda tambah dengan satu klik.
- **130 kemahiran sedia ada dalam 18 kumpulan.** Kemahiran ialah fail ringkas yang menerangkan bila ia digunakan, langkahnya, hasilnya dan kriteria penerimaannya, supaya pekerja menerapkannya dan tidak bertindak mengikut agakan.
- **Empat platform:** Claude, ChatGPT, Grok dan Gemini. Setiap pekerja boleh bekerja pada platform yang berbeza.
- **27 bahasa antara muka** pada laman web dan dalam wizard. Bahasa pilihan ialah bahasa untuk mengurus seluruh sistem dan bahasa yang digunakan bersama pekerja.
- **Tapak pengurusan** daripada satu fail HTML: papan, pasukan, keputusan, metrik, pustaka arahan sedia ada, dan enjin perhatian yang menandakan perkara yang lewat atau menunggu anda.

## Arahan

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Platform

| Platform | Cara pasukan disediakan |
| --- | --- |
| Claude | Cipta projek dengan nama projek anda dan tambahkan folder yang dijana. |
| ChatGPT | Cipta projek dan muat naik fail dalam folder. |
| Grok | Cipta projek, tampal arahan Compass ke dalam arahan projek, dan tambahkan fail. |
| Gemini | Cipta satu Gem bagi setiap pekerja, tampal arahannya ke dalam arahan Gem, dan tambahkan fail di bawah Knowledge. |

Muat naik fail daripada folder projek di lokasi asalnya dan muat naik semula fail yang berubah. Setakat pengetahuan kami, Grok dan Gemini tidak menulis terus ke dalam folder, jadi alihkan hasil kerja mereka ke dalam folder sendiri. Langkah-langkah ini mengikut dokumentasi awam pada masa penulisan; antara muka dan had ditetapkan oleh platform tersebut dan mungkin berubah.

## Had semasa

- Wizard dan laman web tersedia dalam 27 bahasa, tetapi fail projek yang dijana (peraturan, ringkasan peranan, papan) dan tapak pengurusan buat masa ini ditulis dalam bahasa Arab. Pekerja diberitahu bahasa yang perlu digunakan dan menjawab anda dalam bahasa itu.
- Nama fail, arahan dan perkataan status papan kekal dalam bahasa Arab kerana alat ini membacanya secara literal.
- Pemasangan pada Windows belum diuji pada mesin sebenar.

## Untuk pembangun

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Kod sumber berada dalam `forge/`; `tools/build-single.py` menghasilkan alat satu fail dalam `dist/`. Templat berada dalam `forge/templates/`, laman web awam dalam `site/`.

## Lesen

MIT.
