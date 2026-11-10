"""assets/icon.ico dosyasını üretir (tek seferlik: python make_icon.py)."""
import os

from PIL import Image, ImageDraw

S = 1024
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, "assets"), exist_ok=True)

# Köşeleri yuvarlak, kırmızıdan koyu kırmızıya degrade zemin
grad = Image.new("RGB", (S, S))
px = grad.load()
top, bot = (255, 77, 94), (200, 22, 48)
for y in range(S):
    t = y / (S - 1)
    c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
    for x in range(S):
        px[x, y] = c
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle((0, 0, S - 1, S - 1), radius=230, fill=255)
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
img.paste(grad, (0, 0), mask)

d = ImageDraw.Draw(img)
white = (255, 255, 255, 255)
# Aşağı ok: gövde + üçgen uç
d.rounded_rectangle((440, 215, 584, 560), radius=40, fill=white)
d.polygon([(280, 500), (744, 500), (512, 770)], fill=white)
# Alt tepsi çizgisi
d.rounded_rectangle((250, 790, 774, 850), radius=30, fill=white)

img.save(os.path.join(here, "assets", "icon.png"))
img.save(os.path.join(here, "assets", "icon.ico"),
         sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("icon hazır")
