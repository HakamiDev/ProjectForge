<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · **Bahasa Indonesia** · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Sistem operasi untuk tim agen AI.** Satu perintah mengubah folder biasa menjadi kantor yang disiplin: satu papan yang menjadi acuan semua agen di platform mana pun; gerbang kualitas yang independen; tata kelola keputusan; jejak audit lengkap; metrik kinerja yang dapat diekspor ke Power BI; dan situs manajemen yang berjalan dari satu berkas HTML.

Python 3.9 atau lebih baru, tanpa dependensi, tanpa server. Sumber terbuka, berlisensi MIT.

Situs web: https://hakamidev.github.io/ProjectForge/

## Instalasi

Satu baris yang ditempel ke terminal. Baris ini mengunduh alat, menjalankannya, mengajukan empat pertanyaan, lalu membuka situs manajemen Anda.

macOS dan Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Di situs, Anda juga dapat memilih platform dan bahasa pilihan terlebih dahulu; keduanya dibawa ke perintah instalasi dan sudah terpilih di wizard.

## Masalah yang diatasi

- **Obrolan melupakan konteks.** Aturan dan arahan peran disimpan di folder, bukan di memori obrolan, sehingga obrolan mana pun dapat melanjutkan pekerjaan.
- **Agen saling bertabrakan.** Satu papan bernomor; status "sedang dikerjakan" mengunci baris; pengaman checksum mencegah penulisan yang saling bertentangan.
- **Keluaran tanpa pemeriksaan.** Kepala penjaminan kualitas memutuskan lulus atau gagal sebelum apa pun sampai ke pemilik.
- **Keputusan yang macet.** Paling banyak lima keputusan terbuka, dan aturan 48 jam yang setelahnya rekomendasi berlaku.
- **Tidak ada yang terukur.** `report` memberikan tingkat penyelesaian, waktu siklus, tingkat kelulusan QA, dan beban per peran; `export` menulis berkas CSV untuk Power BI.
- **Tidak ada akuntabilitas.** Setiap penulisan ke papan dicatat: siapa, kapan, dan apa.
- **Data sensitif di alat eksternal.** Kebijakan data yang mengikat, dengan klasifikasi dan alat yang disetujui.

## Yang Anda dapatkan

- **80 spesialisasi** (strategi, restoran, properti, perangkat lunak, SDM, pendidikan, dan lainnya) dengan lebih dari 330 peran siap pakai yang dapat ditambahkan dengan satu klik.
- **130 skill siap pakai dalam 18 kelompok.** Skill adalah berkas singkat yang menjelaskan kapan digunakan, langkah-langkahnya, keluarannya, dan kriteria penerimaannya, sehingga karyawan menerapkannya alih-alih berimprovisasi.
- **Empat platform:** Claude, ChatGPT, Grok, dan Gemini. Setiap karyawan dapat bekerja di platform yang berbeda.
- **27 bahasa antarmuka** di situs web dan wizard. Bahasa pilihan adalah bahasa untuk mengelola seluruh sistem dan yang digunakan bersama karyawan.
- **Situs manajemen** dari satu berkas HTML: papan, tim, keputusan, metrik, pustaka perintah siap pakai, dan mesin perhatian yang menandai apa yang terlambat atau menunggu Anda.

## Perintah

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Platform

| Platform | Cara tim disiapkan |
| --- | --- |
| Claude | Buat proyek dengan nama proyek Anda dan tambahkan folder yang dihasilkan. |
| ChatGPT | Buat proyek dan unggah berkas-berkas folder. |
| Grok | Buat proyek, tempel perintah Compass ke instruksinya, lalu tambahkan berkasnya. |
| Gemini | Buat satu Gem per karyawan, tempel perintahnya ke instruksi, lalu tambahkan berkas di bawah Knowledge. |

Unggah berkas dari folder proyek di lokasi aslinya dan unggah ulang berkas yang berubah. Sepengetahuan kami, Grok dan Gemini tidak menulis langsung ke folder, jadi pindahkan keluaran mereka ke folder sendiri. Langkah-langkah ini mengikuti dokumentasi publik pada saat penulisan; antarmuka dan batasannya ditetapkan oleh platform tersebut dan dapat berubah.

## Batasan saat ini

- Wizard dan situs web tampil dalam 27 bahasa, tetapi berkas proyek yang dihasilkan (aturan, arahan peran, papan) dan situs manajemen untuk sementara ditulis dalam bahasa Arab. Karyawan diberi tahu bahasa yang harus dipakai bekerja dan menjawab Anda dalam bahasa itu.
- Nama berkas, perintah, dan kata status pada papan tetap dalam bahasa Arab karena alat ini membacanya apa adanya.
- Instalasi di Windows belum diuji pada mesin sungguhan.

## Untuk pengembang

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Kode sumber ada di `forge/`; `tools/build-single.py` menghasilkan alat satu berkas di `dist/`. Templat ada di `forge/templates/`, situs publik di `site/`.

## Lisensi

MIT.
