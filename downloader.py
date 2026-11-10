"""yt-dlp sarmalayıcı. Arayüzden bağımsızdır."""
import os

import imageio_ffmpeg
import yt_dlp

VIDEO_QUALITIES = ["En iyi", "2160p", "1440p", "1080p", "720p", "480p", "360p"]
AUDIO_QUALITIES = ["320 kbps", "256 kbps", "192 kbps", "128 kbps"]


class Cancelled(Exception):
    pass


def _base_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
    }


def fetch_info(url):
    """Video bilgisini (başlık, süre, küçük resim) indirmeden getirir."""
    with yt_dlp.YoutubeDL({**_base_opts(), "skip_download": True}) as ydl:
        return ydl.extract_info(url, download=False)


def _video_format(quality):
    if quality == "En iyi":
        return "bestvideo+bestaudio/best"
    h = int(quality.rstrip("p"))
    return f"bestvideo[height<={h}]+bestaudio/best[height<={h}]/best"


def download(url, fmt, quality, out_dir, on_progress, is_cancelled=lambda: False):
    """fmt: 'mp4' veya 'mp3'. on_progress(yüzde, durum_metni) çağrılır."""

    def hook(d):
        if is_cancelled():
            raise Cancelled()
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            pct = d["downloaded_bytes"] / total * 100 if total else 0
            speed = d.get("speed")
            eta = d.get("eta")
            parts = []
            if speed:
                parts.append(f"{speed / 1024 / 1024:.1f} MB/s")
            if eta is not None:
                parts.append(f"{int(eta)} sn kaldı")
            on_progress(pct, " · ".join(parts) or "İndiriliyor...")
        elif d["status"] == "finished":
            on_progress(100, "Dönüştürülüyor...")

    opts = {
        **_base_opts(),
        "outtmpl": os.path.join(out_dir, "%(title)s.%(ext)s"),
        "progress_hooks": [hook],
        "restrictfilenames": False,
        "windowsfilenames": True,
    }
    if fmt == "mp3":
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": quality.split()[0],
        }]
    else:
        opts["format"] = _video_format(quality)
        opts["merge_output_format"] = "mp4"

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
