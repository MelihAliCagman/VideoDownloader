# YouTube Downloader

YouTube videolarını MP3 (ses) veya MP4 (video) olarak indiren, modern ve sade arayüzlü masaüstü uygulaması.

## Teknoloji

- **Python 3.10+**
- **customtkinter**: modern, koyu temalı arayüz
- **yt-dlp**: indirme motoru
- **imageio-ffmpeg**: pip ile gelen ffmpeg ikilisi (MP3 dönüştürme ve video+ses birleştirme için; elle ffmpeg kurulumu gerekmez)
- **Pillow**: video küçük resmini (thumbnail) göstermek için

## Dosya Yapısı

```
main.py            # Giriş noktası
app.py             # Arayüz (customtkinter)
downloader.py      # yt-dlp sarmalayıcı (arayüzden bağımsız)
requirements.txt
run.bat            # Windows'ta çift tıkla çalıştır
make_icon.py       # assets/icon.ico üretir
make_shortcut.ps1  # masaüstü kısayolu oluşturur
assets/            # logo (icon.png, icon.ico)
README.md
CLAUDE.md
```

## Özellikler

- URL yapıştır, "Getir" ile başlık/süre/küçük resim önizlemesi
- Format seçimi: **MP4 (video)** veya **MP3 (ses)**
- Kalite seçimi:
  - MP4: En iyi, 2160p, 1440p, 1080p, 720p, 480p, 360p
  - MP3: 320, 256, 192, 128 kbps
- Kayıt klasörü seçimi (varsayılan: `~/Downloads`)
- İlerleme çubuğu, hız ve kalan süre bilgisi
- İndirme arka plan thread'inde çalışır, arayüz donmaz

## Kurallar

- İndirme mantığı `downloader.py` içinde kalır; arayüz kodu yt-dlp'yi doğrudan çağırmaz.
- Arayüz güncellemeleri yalnızca ana thread'de yapılır (`after` ile).
- Arayüz metinleri Türkçe.
- Sade tutulur: oynatma listesi, kuyruk, ayar ekranı gibi ek özellikler istenmedikçe eklenmez.

## Çalıştırma

```
pip install -r requirements.txt
python main.py
```

YouTube sık değiştiği için indirme hatası alınırsa önce: `pip install -U yt-dlp`

## Notlar

- Yalnızca kişisel kullanım ve telif hakkı izni olan içerik için kullanın.
