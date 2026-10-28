<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · **Türkçe** · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**Yapay zekâ ajanlarından oluşan bir ekip için işletim sistemi.** Tek bir komut, sade bir klasörü disiplinli bir ofise dönüştürür: her platformda tüm ajanların çalıştığı tek bir pano; bağımsız bir kalite kapısı; karar yönetişimi; eksiksiz bir denetim izi; Power BI'a aktarılabilen performans metrikleri ve tek bir HTML dosyasından çalışan bir yönetim sitesi.

Python 3.9 veya üzeri, bağımlılık yok, sunucu yok. Açık kaynak, MIT lisanslı.

Web sitesi: https://hakamidev.github.io/ProjectForge/

## Kurulum

Terminale yapıştırılan tek bir satır. Aracı indirir, çalıştırır, dört soru sorar ve ardından yönetim sitenizi açar.

macOS ve Linux (Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows (PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

Site ayrıca önce platformunuzu ve tercih ettiğiniz dili seçmenize olanak tanır; her ikisi de kurulum komutuna eklenir ve sihirbazda önceden seçili gelir.

## Neyi çözer

- **Sohbetler unutur.** Kurallar ve rol tanımları sohbet belleğinde değil klasörde durur; bu sayede herhangi bir sohbet işi kaldığı yerden sürdürebilir.
- **Ajanlar çakışır.** Numaralı tek bir pano; "devam ediyor" durumu bir satırı kilitler; sağlama toplamı denetimi çakışan yazmaları önler.
- **Denetlenmemiş çıktı.** Kalite güvence sorumlusu, herhangi bir şey sahibine ulaşmadan önce geçti veya kaldı kararını verir.
- **Bekleyen kararlar.** En fazla beş açık karar ve 48 saat kuralı: bu sürenin sonunda öneri geçerli olur.
- **Hiçbir şey ölçülmez.** `report` teslim oranını, döngü süresini, kalite güvence başarı oranını ve rol başına iş yükünü verir; `export` Power BI için CSV dosyaları yazar.
- **Hesap verebilirlik yok.** Panoya yapılan her yazma kaydedilir: kim, ne zaman ve ne yazdı.
- **Hassas verilerin harici araçlarda kullanılması.** Sınıflandırma ve onaylı araçları içeren bağlayıcı bir veri politikası.

## Neler sunar

- **80 uzmanlık alanı** (strateji, restoranlar, gayrimenkul, yazılım, İK, eğitim ve daha fazlası) ve tek tıkla ekleyebileceğiniz 330'dan fazla hazır rol.
- **18 grupta 130 hazır beceri.** Beceri; ne zaman kullanılacağını, adımlarını, çıktısını ve kabul ölçütünü anlatan kısa bir dosyadır; böylece çalışan doğaçlama yapmak yerine onu uygular.
- **Dört platform:** Claude, ChatGPT, Grok ve Gemini. Her çalışan farklı bir platformda çalışabilir.
- **Web sitesinde ve sihirbazda 27 arayüz dili.** Tercih edilen dil, tüm sistemi yönetmek için kullanılan ve çalışanlarla iletişimde geçerli olan dildir.
- **Tek bir HTML dosyasından yönetim sitesi:** pano, ekip, kararlar, metrikler, hazır komutlar kitaplığı ve geciken veya sizden yanıt bekleyen işleri işaretleyen bir dikkat motoru.

## Komutlar

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## Platformlar

| Platform | Ekip nasıl kurulur |
| --- | --- |
| Claude | Projenizin adıyla bir proje oluşturun ve oluşturulan klasörü ekleyin. |
| ChatGPT | Bir proje oluşturun ve klasör dosyalarını yükleyin. |
| Grok | Bir proje oluşturun, Compass komutunu talimatlarına yapıştırın ve dosyaları ekleyin. |
| Gemini | Her çalışan için bir Gem oluşturun, komutunu talimatlara yapıştırın ve dosyaları Knowledge bölümünün altına ekleyin. |

Dosyaları proje klasöründen özgün konumunda yükleyin ve değişenleri yeniden yükleyin. Bildiğimiz kadarıyla Grok ve Gemini klasöre doğrudan yazmaz; bu nedenle çıktılarını klasöre kendiniz taşıyın. Adımlar, yazım sırasında kamuya açık belgelere dayanmaktadır; arayüzler ve sınırlar bu platformlar tarafından belirlenir ve değişebilir.

## Mevcut sınırlamalar

- Sihirbaz ve web sitesi 27 dilde görünür; ancak oluşturulan proje dosyaları (kurallar, rol tanımları, pano) ile yönetim sitesi şimdilik Arapça yazılmaktadır. Çalışanlara hangi dilde çalışacakları söylenir ve size o dilde yanıt verirler.
- Dosya adları, komutlar ve panonun durum sözcükleri, araç bunları birebir okuduğu için Arapça kalır.
- Windows kurulumu henüz gerçek bir makinede test edilmemiştir.

## Geliştiriciler için

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

Kaynak kod `forge/` içindedir; `tools/build-single.py`, `dist/` içinde tek dosyalı aracı üretir. Şablonlar `forge/templates/` içinde, herkese açık site ise `site/` içindedir.

## Lisans

MIT.
