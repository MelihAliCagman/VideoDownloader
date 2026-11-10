import ctypes

from app import App

if __name__ == "__main__":
    # Görev çubuğunda Python yerine kendi ikonumuz görünsün
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("melih.youtubeindirici")
    except Exception:
        pass
    App().mainloop()
