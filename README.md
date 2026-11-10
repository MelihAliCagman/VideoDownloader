<div align="center">

<img src="assets/icon.png" width="110" alt="Video Downloader logosu">

# Video Downloader

**YouTube videolarını MP4 veya MP3 olarak indir. Modern, sade, tek pencere.**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![yt-dlp](https://img.shields.io/badge/yt--dlp-powered-ff3b4e)
![Platform](https://img.shields.io/badge/Windows-0078D6?logo=windows&logoColor=white)

</div>

---

## Özellikler

- **MP4 (video)** ve **MP3 (ses)** olarak indirme
- **Kalite seçimi**
  - Video: En iyi, 2160p, 1440p, 1080p, 720p, 480p, 360p
  - Ses: 320, 256, 192, 128 kbps
- Bağlantıyı yapıştırınca **küçük resim, başlık, kanal ve süre önizlemesi**
- İlerleme çubuğu, **hız** ve **kalan süre** bilgisi
- İstediğin an **iptal** etme
- Kayıt klasörü seçimi (varsayılan: İndirilenler)
- Koyu temalı, sade arayüz. İndirme arka planda çalışır, pencere donmaz
- **ffmpeg kurmana gerek yok**, `imageio-ffmpeg` paketiyle otomatik gelir

## Kurulum

Gereksinim: **Python 3.10+**

```bash
git clone https://github.com/MelihAliCagman/VideoDownloader.git
cd VideoDownloader

python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

## Çalıştırma

```bash
.venv\Scripts\python main.py
```

Windows'ta `run.bat` dosyasına çift tıklamak da yeterli. İlk çalıştırmada kurulumu kendisi yapar.

### Masaüstü kısayolu

Logolu bir masaüstü kısayolu için kurulumdan sonra bir kez çalıştır:

```powershell
powershell -ExecutionPolicy Bypass -File make_shortcut.ps1
```

## Kullanım

1. YouTube bağlantısını yapıştır ve **Getir**'e bas
2. **Format** (MP4 / MP3) ve **kalite** seç
3. Gerekirse kayıt klasörünü değiştir
4. **İndir**'e bas

## Proje yapısı

```
main.py             Giriş noktası
app.py              Arayüz (customtkinter)
downloader.py       yt-dlp sarmalayıcı, arayüzden bağımsız
make_icon.py        Logoyu üretir (assets/icon.ico)
make_shortcut.ps1   Masaüstü kısayolu oluşturur
run.bat             Windows'ta tek tıkla çalıştırma
```

## Teknolojiler

[customtkinter](https://github.com/TomSchimansky/CustomTkinter) · [yt-dlp](https://github.com/yt-dlp/yt-dlp) · [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) · [Pillow](https://python-pillow.org/)

## Sorun giderme

YouTube sık değişir. İndirme hatası alırsan önce yt-dlp'yi güncelle:

```bash
.venv\Scripts\pip install -U yt-dlp
```

## Yasal uyarı

Bu araç yalnızca kişisel kullanım ve indirme izni olan içerikler içindir. Telif hakkıyla korunan içerikleri indirmek ve paylaşmak, YouTube Hizmet Şartları'na ve bulunduğun ülkenin yasalarına aykırı olabilir. Sorumluluk kullanıcıya aittir.
