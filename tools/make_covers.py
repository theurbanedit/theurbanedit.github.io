"""Generate original abstract cover illustrations + brand assets for The Urban Edit.

Usage:  python tools/make_covers.py
Writes to assets/images/posts/ and assets/images/brand/.
Each cover is produced at 1600x1000 (article hero) and 800x500 (cards).
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSTS = os.path.join(ROOT, "assets", "images", "posts")
BRAND = os.path.join(ROOT, "assets", "images", "brand")
os.makedirs(POSTS, exist_ok=True)
os.makedirs(BRAND, exist_ok=True)

W, H = 1600, 1000
S = 2  # supersampling


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def gradient(size, top, bottom):
    w, h = size
    img = Image.new("RGB", size, top)
    d = ImageDraw.Draw(img)
    t, b = hexc(top), hexc(bottom)
    for y in range(h):
        k = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(t[i] + (b[i] - t[i]) * k) for i in range(3)))
    return img


def grain(img, amount=10, seed=1):
    rnd = random.Random(seed)
    noise = Image.effect_noise(img.size, 40).convert("L")
    noise = noise.point(lambda v: 128 + (v - 128) * amount // 40)
    overlay = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, Image.composite(img, overlay, Image.new("L", img.size, 235)), 0.25)


def finish(img, slug, seed):
    img = img.resize((W, H), Image.LANCZOS)
    img = grain(img, seed=seed)
    img.save(os.path.join(POSTS, f"{slug}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
    img.resize((800, 500), Image.LANCZOS).save(
        os.path.join(POSTS, f"{slug}-800.jpg"), "JPEG", quality=80, optimize=True, progressive=True)


def canvas(bg_top, bg_bottom):
    img = gradient((W * S, H * S), bg_top, bg_bottom)
    return img, ImageDraw.Draw(img)


def P(x, y):
    return (x * S, y * S)


def box(x0, y0, x1, y1):
    return [x0 * S, y0 * S, x1 * S, y1 * S]


def arch(d, x, y, w, h, fill):
    r = w / 2
    d.rectangle(box(x, y + r, x + w, y + h), fill=fill)
    d.pieslice(box(x, y, x + w, y + 2 * r), 180, 360, fill=fill)


# ---------------------------------------------------------------- covers
def coworking(slug):
    img, d = canvas("#EDE6D8", "#DCD3C0")
    for i, x in enumerate([170, 560, 950]):
        arch(d, x, 120, 300, 560, "#C9CDB4" if i != 1 else "#AEB88F")
        arch(d, x + 30, 150, 240, 530, "#F4EFE4")
    d.rectangle(box(0, 700, 1600, 1000), fill="#5B6B3A")
    d.rectangle(box(120, 650, 1480, 690), fill="#3E4A27")
    for x in range(200, 1450, 210):
        d.rectangle(box(x, 690, x + 14, 820), fill="#3E4A27")
        d.ellipse(box(x + 40, 560, x + 120, 640), fill="#C7704F")
    d.ellipse(box(1270, 130, 1470, 330), fill="#D9A15B")
    finish(img, slug, 1)


def sustainable(slug):
    img, d = canvas("#F1E6D9", "#E5D2BE")
    cols = ["#9B3D2C", "#C2775A", "#D9A988", "#B5523B", "#7A2E20"]
    for i in range(9):
        y = 180 + i * 85
        pts = [P(x, y + 70 * math.sin((x / 1600) * math.pi * 2 + i * 0.6)) for x in range(-50, 1700, 25)]
        pts += [P(1700, 1100), P(-50, 1100)]
        d.polygon(pts, fill=cols[i % len(cols)])
    d.ellipse(box(1150, 90, 1390, 330), fill="#F7EFE3")
    finish(img, slug, 2)


def ai(slug):
    img, d = canvas("#1E2547", "#2F3E73")
    rnd = random.Random(4)
    nodes = []
    for gx in range(9):
        for gy in range(6):
            x = 140 + gx * 165 + rnd.randint(-20, 20)
            y = 140 + gy * 150 + rnd.randint(-20, 20)
            nodes.append((x, y))
    for (x, y) in nodes:
        for (a, b) in nodes:
            if 0 < math.hypot(a - x, b - y) < 200 and rnd.random() < 0.35:
                d.line([P(x, y), P(a, b)], fill="#4E5FA0", width=2 * S)
    for (x, y) in nodes:
        r = rnd.choice([8, 12, 18])
        d.ellipse(box(x - r, y - r, x + r, y + r), fill=rnd.choice(["#9FB4F2", "#E9EDFB", "#6F86D6"]))
    glow = Image.new("RGB", img.size, (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse(box(950, 250, 1450, 750), fill=(120, 150, 255))
    glow = glow.filter(ImageFilter.GaussianBlur(120 * S))
    img = Image.blend(img, Image.composite(glow, img, glow.convert("L")), 0.35)
    finish(img, slug, 3)


def minimalist(slug):
    img, d = canvas("#F2EDE5", "#E9E2D6")
    d.rectangle(box(0, 720, 1600, 1000), fill="#D8CCBC")
    arch(d, 860, 140, 420, 580, "#E2D6C6")
    d.rectangle(box(220, 600, 760, 720), fill="#7A5C4F")
    d.rectangle(box(250, 560, 730, 610), fill="#9C7B6B")
    d.ellipse(box(420, 330, 560, 470), fill="#C7A68E")
    d.rectangle(box(486, 470, 494, 560), fill="#7A5C4F")
    d.ellipse(box(1010, 520, 1130, 720), fill="#5E6B4E")
    finish(img, slug, 4)


def home_workspace(slug):
    img, d = canvas("#ECE5DA", "#E0D6C7")
    d.rectangle(box(860, 120, 1380, 560), fill="#F6F1E8")
    d.rectangle(box(1110, 120, 1130, 560), fill="#D6CBBB")
    d.rectangle(box(860, 330, 1380, 348), fill="#D6CBBB")
    d.rectangle(box(0, 780, 1600, 1000), fill="#B9A894")
    d.rectangle(box(280, 600, 1320, 640), fill="#6E5848")
    d.rectangle(box(320, 640, 340, 860), fill="#6E5848")
    d.rectangle(box(1260, 640, 1280, 860), fill="#6E5848")
    d.rectangle(box(560, 420, 900, 600), fill="#3B3A36")
    d.rectangle(box(575, 435, 885, 585), fill="#8FA08A")
    d.rectangle(box(700, 600, 760, 612), fill="#3B3A36")
    d.polygon([P(380, 600), P(420, 470), P(460, 480), P(430, 600)], fill="#C7704F")
    d.ellipse(box(400, 450, 470, 500), fill="#E8C07A")
    d.ellipse(box(1150, 470, 1260, 600), fill="#5E6B4E")
    finish(img, slug, 5)


def habits(slug):
    img, d = canvas("#EFE5DC", "#E1CFC4")
    d.ellipse(box(560, 200, 1040, 680), fill="#C98B5E")
    for i, c in enumerate(["#B99BC3", "#8F6E9F", "#6B4C7A", "#4E365A", "#3A2744"]):
        y = 470 + i * 110
        d.rectangle(box(0, y, 1600, y + 110), fill=c)
    finish(img, slug, 6)


def remote(slug):
    img, d = canvas("#E7E4D8", "#D6D3C2")
    cx, cy = 800, 520
    for i, c in enumerate(["#2E6A6A", "#4E8A87", "#7FB0A8", "#B9D3C8", "#E7E4D8"]):
        r = 380 - i * 70
        d.ellipse(box(cx - r, cy - r, cx + r, cy + r), fill=c)
    for (a0, a1, r, col) in [(200, 330, 520, "#C7704F"), (10, 150, 470, "#8A5A2B"), (230, 300, 600, "#2E6A6A")]:
        d.arc(box(cx - r, cy - r, cx + r, cy + r), a0, a1, fill=col, width=6 * S)
    for (x, y) in [(330, 300), (1290, 380), (1180, 820)]:
        d.ellipse(box(x - 14, y - 14, x + 14, y + 14), fill="#C7704F")
    finish(img, slug, 7)


def marketing(slug):
    img, d = canvas("#F1E9DD", "#E6D9C6")
    heights = [180, 260, 230, 340, 420, 520]
    for i, h in enumerate(heights):
        x = 220 + i * 150
        d.rectangle(box(x, 860 - h, x + 100, 860), fill=["#E0B79B", "#C98B6C", "#A0522D"][i % 3])
    d.rectangle(box(160, 860, 1180, 872), fill="#2A2724")
    pts = [(1250, 300), (1420, 220), (1370, 460), (1500, 560), (1240, 640)]
    for a in pts:
        for b in pts:
            d.line([P(*a), P(*b)], fill="#6B5B4E", width=2 * S)
    for (x, y) in pts:
        d.ellipse(box(x - 30, y - 30, x + 30, y + 30), fill="#2A2724")
        d.ellipse(box(x - 14, y - 14, x + 14, y + 14), fill="#F1E9DD")
    finish(img, slug, 8)


def business(slug):
    img, d = canvas("#E9E3D6", "#DAD1BF")
    for i in range(6):
        x = 160 + i * 190
        top = 820 - i * 100
        d.rectangle(box(x, top, x + 190, 1000), fill=["#1F4E5F", "#2B6577", "#3F7C8C"][i % 3])
    d.ellipse(box(1240, 130, 1460, 350), fill="#D39B45")
    d.line([P(80, 900), P(1500, 900)], fill="#E9E3D6", width=3 * S)
    finish(img, slug, 9)


def creative(slug):
    img, d = canvas("#ECE7DD", "#DAD3C6")
    for i in range(6):
        w = 900 - i * 130
        h = 860 - i * 100
        x = 800 - w / 2
        y = 1000 - h
        arch(d, x, y, w, h, ["#45505A", "#5D6873", "#8A939A", "#B7BCBE", "#D9D3C4", "#F3EEE4"][i])
    d.rectangle(box(760, 600, 840, 1000), fill="#C8A452")
    d.ellipse(box(180, 140, 330, 290), fill="#C8A452")
    finish(img, slug, 10)


def lifestyle(slug):
    img, d = canvas("#F3E1C4", "#EBCDA3")
    d.ellipse(box(980, 220, 1300, 540), fill="#E39A4C")
    for i, c in enumerate(["#B7B98F", "#8E9C6D", "#6C7F52"]):
        base = 560 + i * 120
        pts = [P(x, base + 60 * math.sin(x / 260 + i)) for x in range(-20, 1640, 20)]
        pts += [P(1640, 1100), P(-20, 1100)]
        d.polygon(pts, fill=c)
    path = [P(300 + 60 * math.sin(t / 50), 1000 - t) for t in range(0, 330, 6)]
    d.line(path, fill="#F3E1C4", width=18 * S, joint="curve")
    finish(img, slug, 11)


def fashion_evo(slug):
    img, d = canvas("#F2E7E1", "#E8D5CC")
    d.rectangle(box(0, 0, 520, 1000), fill="#7D2E2A")
    d.rectangle(box(1180, 380, 1600, 1000), fill="#2A2422")
    for i, x in enumerate([560, 780, 1000]):
        c = ["#E5B8AE", "#C77F73", "#9B3D2C"][i]
        d.ellipse(box(x + 70, 160, x + 150, 240), fill=c)
        d.polygon([P(x + 110, 250), P(x + 20, 900), P(x + 200, 900)], fill=c)
        d.rectangle(box(x + 60, 330, x + 160, 360), fill="#F2E7E1")
    d.ellipse(box(160, 180, 360, 380), fill="#E5B8AE")
    finish(img, slug, 12)


COVERS = {
    "how-coworking-spaces-are-changing-modern-work": coworking,
    "the-future-of-sustainable-fashion": sustainable,
    "the-future-of-artificial-intelligence-in-everyday-life": ai,
    "minimalist-interior-design-ideas-for-modern-homes": minimalist,
    "how-to-design-a-productive-home-workspace": home_workspace,
    "essential-productivity-habits-for-professionals": habits,
    "the-rise-of-remote-work-around-the-world": remote,
    "how-digital-marketing-is-transforming-small-businesses": marketing,
    "essential-business-strategies-for-new-entrepreneurs": business,
    "how-creative-workspaces-encourage-innovation": creative,
    "modern-lifestyle-trends-worth-exploring": lifestyle,
    "the-evolution-of-modern-fashion-trends": fashion_evo,
}


# ---------------------------------------------------------------- brand
def font(name, size):
    for p in [os.path.join("C:/Windows/Fonts", name), os.path.join("/usr/share/fonts/truetype/dejavu", "DejaVuSerif.ttf")]:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def brand():
    # Monogram mark
    def mark(size, path):
        im = Image.new("RGB", (size * 4, size * 4), "#141414")
        dd = ImageDraw.Draw(im)
        f = font("georgiai.ttf", int(size * 4 * 0.62))
        tb = dd.textbbox((0, 0), "U", font=f)
        dd.text(((size * 4 - (tb[2] - tb[0])) / 2 - tb[0], (size * 4 - (tb[3] - tb[1])) / 2 - tb[1]), "U", font=f, fill="#FAF8F4")
        dd.rectangle([size * 4 * 0.3, size * 4 * 0.84, size * 4 * 0.7, size * 4 * 0.865], fill="#C7704F")
        im.resize((size, size), Image.LANCZOS).save(path)
    mark(512, os.path.join(BRAND, "logo-512.png"))
    mark(180, os.path.join(BRAND, "apple-touch-icon.png"))
    mark(32, os.path.join(BRAND, "favicon-32.png"))

    # Default social share image
    og = gradient((1200, 630), "#FAF8F4", "#F0EBE2")
    dd = ImageDraw.Draw(og)
    dd.rectangle([0, 0, 1200, 14], fill="#9B3D2C")
    f_it = font("georgiai.ttf", 96)
    f_rg = font("georgia.ttf", 96)
    f_sm = font("georgiai.ttf", 38)
    w1 = dd.textlength("The ", font=f_it)
    w2 = dd.textlength("Urban Edit", font=f_rg)
    x = (1200 - (w1 + w2)) / 2
    dd.text((x, 220), "The ", font=f_it, fill="#141414")
    dd.text((x + w1, 220), "Urban Edit", font=f_rg, fill="#141414")
    tag = "Ideas, Spaces & Stories for Modern Living."
    dd.text(((1200 - dd.textlength(tag, font=f_sm)) / 2, 360), tag, font=f_sm, fill="#5F5B55")
    dd.line([(520, 450), (680, 450)], fill="#9B3D2C", width=2)
    og.save(os.path.join(BRAND, "og-default.jpg"), "JPEG", quality=88, optimize=True)


if __name__ == "__main__":
    for slug, fn in COVERS.items():
        fn(slug)
        print("cover", slug)
    brand()
    print("brand assets done")
