import io
import os
import threading
import urllib.request
from tkinter import filedialog

import customtkinter as ctk
from PIL import Image

import downloader

ICON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.ico")
BG = "#0f0f13"
CARD = "#1a1a22"
ACCENT = "#ff3b4e"
ACCENT_HOVER = "#e02d40"
MUTED = "#8b8b99"


def fmt_duration(sec):
    if not sec:
        return ""
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("YouTube İndirici")
        self.geometry("560x640")
        self.minsize(520, 600)
        self.configure(fg_color=BG)
        # customtkinter kendi ikonunu geç yükler; bizimkini ondan sonra ayarla
        self.after(250, lambda: self.iconbitmap(ICON))

        self.out_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        self.cancel = False
        self.busy = False
        self.info_ok = False

        self._build()

    # ---------- arayüz ----------
    def _build(self):
        wrap = ctk.CTkFrame(self, fg_color="transparent")
        wrap.pack(fill="both", expand=True, padx=28, pady=24)

        ctk.CTkLabel(wrap, text="YouTube İndirici",
                     font=ctk.CTkFont(size=26, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(wrap, text="Videoları MP4 veya MP3 olarak indir",
                     text_color=MUTED).pack(anchor="w", pady=(0, 18))

        # URL
        row = ctk.CTkFrame(wrap, fg_color="transparent")
        row.pack(fill="x")
        self.url = ctk.CTkEntry(row, height=42, corner_radius=10, fg_color=CARD,
                                border_width=0, placeholder_text="Video bağlantısını yapıştır...")
        self.url.pack(side="left", fill="x", expand=True)
        self.url.bind("<Return>", lambda e: self.fetch())
        self.fetch_btn = ctk.CTkButton(row, text="Getir", width=80, height=42, corner_radius=10,
                                       fg_color=ACCENT, hover_color=ACCENT_HOVER, command=self.fetch)
        self.fetch_btn.pack(side="left", padx=(8, 0))

        # Önizleme
        self.preview = ctk.CTkFrame(wrap, fg_color=CARD, corner_radius=14)
        self.preview.pack(fill="x", pady=16)
        self.thumb = ctk.CTkLabel(self.preview, text="", width=120, height=68)
        self.thumb.pack(side="left", padx=12, pady=12)
        txt = ctk.CTkFrame(self.preview, fg_color="transparent")
        txt.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.title_lbl = ctk.CTkLabel(txt, text="Henüz video seçilmedi", anchor="w", justify="left",
                                      wraplength=320, font=ctk.CTkFont(size=14, weight="bold"))
        self.title_lbl.pack(anchor="w", pady=(14, 2))
        self.meta_lbl = ctk.CTkLabel(txt, text="", anchor="w", text_color=MUTED)
        self.meta_lbl.pack(anchor="w")

        # Format
        ctk.CTkLabel(wrap, text="Format", text_color=MUTED).pack(anchor="w")
        self.fmt = ctk.CTkSegmentedButton(
            wrap, values=["MP4 (Video)", "MP3 (Ses)"], height=38, corner_radius=10,
            fg_color=CARD, selected_color=ACCENT, selected_hover_color=ACCENT_HOVER,
            unselected_color=CARD, command=self._on_format)
        self.fmt.set("MP4 (Video)")
        self.fmt.pack(fill="x", pady=(4, 14))

        # Kalite
        ctk.CTkLabel(wrap, text="Kalite", text_color=MUTED).pack(anchor="w")
        self.quality = ctk.CTkOptionMenu(
            wrap, values=downloader.VIDEO_QUALITIES, height=38, corner_radius=10,
            fg_color=CARD, button_color=CARD, button_hover_color="#24242e",
            dropdown_fg_color=CARD)
        self.quality.set("1080p")
        self.quality.pack(fill="x", pady=(4, 14))

        # Klasör
        ctk.CTkLabel(wrap, text="Kayıt klasörü", text_color=MUTED).pack(anchor="w")
        frow = ctk.CTkFrame(wrap, fg_color="transparent")
        frow.pack(fill="x", pady=(4, 18))
        self.dir_lbl = ctk.CTkLabel(frow, text=self.out_dir, anchor="w", fg_color=CARD,
                                    corner_radius=10, height=38)
        self.dir_lbl.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(frow, text="Seç", width=70, height=38, corner_radius=10, fg_color=CARD,
                      hover_color="#24242e", command=self.pick_dir).pack(side="left", padx=(8, 0))

        # İndir
        self.dl_btn = ctk.CTkButton(wrap, text="İndir", height=48, corner_radius=12,
                                    font=ctk.CTkFont(size=16, weight="bold"),
                                    fg_color=ACCENT, hover_color=ACCENT_HOVER, command=self.start)
        self.dl_btn.pack(fill="x")

        self.bar = ctk.CTkProgressBar(wrap, height=8, progress_color=ACCENT, fg_color=CARD)
        self.bar.set(0)
        self.bar.pack(fill="x", pady=(16, 6))
        self.status = ctk.CTkLabel(wrap, text="", text_color=MUTED, wraplength=500)
        self.status.pack(anchor="w")

    # ---------- olaylar ----------
    def _on_format(self, value):
        if value.startswith("MP3"):
            self.quality.configure(values=downloader.AUDIO_QUALITIES)
            self.quality.set("320 kbps")
        else:
            self.quality.configure(values=downloader.VIDEO_QUALITIES)
            self.quality.set("1080p")

    def pick_dir(self):
        d = filedialog.askdirectory(initialdir=self.out_dir)
        if d:
            self.out_dir = d
            self.dir_lbl.configure(text=d)

    def _set_status(self, text, color=MUTED):
        self.status.configure(text=text, text_color=color)

    # ---------- bilgi getirme ----------
    def fetch(self):
        url = self.url.get().strip()
        if not url or self.busy:
            return
        self.fetch_btn.configure(state="disabled", text="...")
        self._set_status("Video bilgisi alınıyor...")

        def work():
            try:
                info = downloader.fetch_info(url)
                img = None
                if info.get("thumbnail"):
                    try:
                        data = urllib.request.urlopen(info["thumbnail"], timeout=10).read()
                        img = Image.open(io.BytesIO(data)).convert("RGB")
                    except Exception:
                        pass
                self.after(0, lambda: self._show_info(info, img))
            except Exception as e:
                self.after(0, lambda: self._fetch_failed(e))

        threading.Thread(target=work, daemon=True).start()

    def _show_info(self, info, img):
        self.fetch_btn.configure(state="normal", text="Getir")
        self.info_ok = True
        self.title_lbl.configure(text=info.get("title", "Başlıksız"))
        meta = " · ".join(x for x in (info.get("uploader"), fmt_duration(info.get("duration"))) if x)
        self.meta_lbl.configure(text=meta)
        if img:
            img.thumbnail((120, 68))
            self._thumb_img = ctk.CTkImage(img, size=img.size)
            self.thumb.configure(image=self._thumb_img)
        self._set_status("")

    def _fetch_failed(self, e):
        self.fetch_btn.configure(state="normal", text="Getir")
        self._set_status("Video bulunamadı. Bağlantıyı kontrol et.", ACCENT)

    # ---------- indirme ----------
    def start(self):
        if self.busy:
            self.cancel = True
            self._set_status("İptal ediliyor...")
            return
        url = self.url.get().strip()
        if not url:
            self._set_status("Önce bir bağlantı yapıştır.", ACCENT)
            return

        fmt = "mp3" if self.fmt.get().startswith("MP3") else "mp4"
        quality = self.quality.get()
        self.busy, self.cancel = True, False
        self.dl_btn.configure(text="İptal", fg_color=CARD, hover_color="#24242e")
        self.bar.set(0)
        self._set_status("Başlıyor...")

        def progress(pct, text):
            self.after(0, lambda: (self.bar.set(pct / 100), self._set_status(text)))

        def work():
            try:
                downloader.download(url, fmt, quality, self.out_dir, progress,
                                    lambda: self.cancel)
                self.after(0, lambda: self._done("Tamamlandı ✓  " + self.out_dir, True))
            except downloader.Cancelled:
                self.after(0, lambda: self._done("İptal edildi.", False))
            except Exception as e:
                if isinstance(e.__context__, downloader.Cancelled):
                    self.after(0, lambda: self._done("İptal edildi.", False))
                else:
                    self.after(0, lambda: self._done("İndirme başarısız. Bağlantıyı kontrol et.", False, True))

        threading.Thread(target=work, daemon=True).start()

    def _done(self, msg, ok, error=False):
        self.busy = False
        self.dl_btn.configure(text="İndir", fg_color=ACCENT, hover_color=ACCENT_HOVER)
        if not ok:
            self.bar.set(0)
        self._set_status(msg, "#4ade80" if ok else (ACCENT if error else MUTED))
