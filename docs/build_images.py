#!/usr/bin/env python3
"""Generate assets/img/** at the locked slot dimensions.
Sources are opened read-only and never modified."""
import os, sys, glob
from PIL import Image

ROOT = "/Volumes/Creative_Onpremise/Ben Karanja/2026/NCBA/SHAREPOINT DESIGN claude"
U = os.path.join(ROOT, "Images/updated intranet website banners images")
R = os.path.join(ROOT, "Reference/Intranet Banners and Posts")
D = os.path.join(ROOT, "Images/departments")
I = os.path.join(ROOT, "Images")
OUT = os.path.join(ROOT, "assets/img")

SLOT = {"hero": (1920, 310), "media": (940, 529), "loop": (320, 180)}

def cover(src, W, H, anchor=0.5):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    tr, sr = W / H, w / h
    if abs(sr - tr) > 1e-6:
        if sr > tr:
            nw = int(round(h * tr)); x = (w - nw) // 2
            im = im.crop((x, 0, x + nw, h))
        else:
            nh = int(round(w / tr)); y = int(round((h - nh) * anchor))
            im = im.crop((0, y, w, y + nh))
    return im.resize((W, H), Image.LANCZOS)

JOBS = [
    # ---- hero 1920x310 ------------------------------------------------
    ("hero", "hero-slide-1",  f"{U}/Website Banner 1920x310px 1.png", .5),
    ("hero", "hero-slide-2",  f"{U}/Website Banner 1920x310px 2.png", .5),
    ("hero", "hero-slide-3",  f"{U}/Website Banner 1920x310px 3.png", .5),
    ("hero", "hero-slide-4",  f"{U}/Website Banner 1920x310px 4.png", .5),
    ("hero", "hero-john",     f"{U}/KV 1 Website Banner John Gachora 1448x234px.png", .5),
    ("hero", "hero-kenya",    f"{U}/KV 3 Website Banner 1920x310px 2.png", .5),
    ("hero", "hero-mcc",      f"{U}/KV 2 Website Banner 1448X234px.png", .5),
    ("hero", "hero-strategy", f"{U}/KV 1 Website Banner 1448x234px.png", .5),
    ("hero", "hero-hr",       f"{U}/KV 1 Website Banner 1448x234px copy.png", .5),
    ("hero", "hero-article",  f"{U}/NCBA INTRANET EMAILER BANNER 1448x380px.png", .5),
    ("hero", "hero-ubuntu",   f"{U}/KV 3 Website Banner 1448X234px.png", .5),
    ("hero", "hero-staff",    f"{U}/Artboard 1 copy.png", .5),

    # ---- media 940x529 (1920x1080 sources uncropped) --------------------
    ("media", "gmd-quote",      f"{U}/GMD Quote.png", .5),
    ("media", "monica-quote",   f"{U}/2 Monicah Kihia QUOTE.png", .5),
    ("media", "ubuntu-spirit",  f"{U}/ 2026 -2030 Ubuntu Strategy.png", .5),
    ("media", "upd-friday",     f"{U}/01. go for it friday.png", .5),
    ("media", "upd-webinars",   f"{U}/02. Upcoming Webinars.png", .5),
    ("media", "upd-hrchat",     f"{U}/03. HR CHAT.png", .5),
    ("media", "upd-events",     f"{U}/04. Past events.png", .5),
    ("media", "hr-lastweek",    f"{U}/HR PAGE. 01. EMPL0YEE VIDEO.png", .5),
    ("media", "hr-august",      f"{U}/HR PAGE. 02. EMPL0YEE VIDEO.png", .5),
    ("media", "hr-gogetters",   f"{U}/HR PAGE. 03. EMPL0YEE VIDEO.png", .5),
    ("media", "video-gmd",      f"{U}/A MESSAGE FROM THE GMD.png", .5),
    ("media", "video-strategy", f"{I}/Strategy Video Picture.png", .5),
    ("media", "feature-louisa", f"{U}/15 Louisa Wandabwa 1.png", .5),
    ("media", "feature-nelly",  f"{U}/5 Nelly Wainaina.png", .5),
    ("media", "feature-monica", f"{U}/2 Monicah Kihia.png", .5),
    ("media", "article-hero",   f"{U}/KV 5 - Go Getters 1920x1080px.png", .5),

    # ---- loop 320x180 (1:1 sources top-anchored) ------------------------
    ("loop", "loop-social",     f"{U}/ESHOT 1.png", 0.0),
    ("loop", "loop-fireside",   f"{U}/ESHOT 2.png", 0.0),
    ("loop", "loop-tea",        f"{U}/ESHOT 3.png", 0.0),
    ("loop", "loop-halloffame", f"{U}/ESHOT 4.png", 0.0),
    ("loop", "loop-teaser",     f"{U}/POST TEASER.png", 0.0),
    ("loop", "loop-hub-live",   f"{U}/POST 4.png", 0.0),
    ("loop", "loop-kpis",       f"{U}/POST 5.png", 0.0),
    ("loop", "loop-welcome",    f"{U}/POST 1.png", 0.0),
    ("loop", "loop-branch-gmd", f"{U}/POST 3.png", 0.0),
    ("loop", "loop-mcc",        f"{R}/KV 4 - Make it Happen 1920x1080px.png", .5),
    ("loop", "loop-gogetters",  f"{U}/KV 5 - Go Getters 1920x1080px.png", .5),
    ("loop", "loop-magic",      f"{U}/KV 2 - Magic Happen 1920x1080px.png", .5),
    ("loop", "loop-john",       f"{D}/1 John Gachora.png", .5),
    ("loop", "loop-monica",     f"{U}/2 Monicah Kihia.png", .5),
    ("loop", "loop-nelly",      f"{U}/5 Nelly Wainaina.png", .5),
    ("loop", "loop-louisa",     f"{U}/15 Louisa Wandabwa 1.png", .5),
    ("loop", "loop-gmd-desk",   f"{I}/GMD ALTERNATE 2 FOR DIGITAL MEDIA REPORTS.jpg", .18),
    ("loop", "loop-live",       f"{U}/NCBA SCREENSAVER 1.png", .5),
    ("loop", "loop-strategy",   f"{U}/ 2026 -2030 Ubuntu Strategy.png", .5),
]

def main():
    missing = [j for j in JOBS if not os.path.isfile(j[2])]
    if missing:
        for _, n, s, _ in missing:
            print(f"MISSING SOURCE for {n}: {s}", file=sys.stderr)
        sys.exit(1)
    for slot, name, src, anchor in JOBS:
        W, H = SLOT[slot]
        d = os.path.join(OUT, slot); os.makedirs(d, exist_ok=True)
        cover(src, W, H, anchor).save(os.path.join(d, name + ".jpg"),
                                      "JPEG", quality=86, optimize=True, progressive=True)
        print(f"{slot:6} {W}x{H}  {name}.jpg")

    tex = Image.open(f"{U}/Ubuntu Texture.png").convert("RGB")
    tex.thumbnail((420, 420), Image.LANCZOS)
    tex.save(os.path.join(OUT, "ubuntu-texture.jpg"), "JPEG", quality=82, optimize=True)
    print(f"bg     {tex.size[0]}x{tex.size[1]}  ubuntu-texture.jpg")

    # Logo: search inside the baked Ubuntu edge strip; reject anything whose
    # aspect ratio is not the NCBA lockup (~2.8:1) -- see D-047.
    best = None
    for f in sorted(glob.glob(os.path.join(U, "*.png"))):
        try: im = Image.open(f).convert("RGB")
        except Exception: continue
        w, h = im.size
        if w < 1400: continue
        reg = im.crop((int(w*.78), 0, int(w*.965), int(h*.16)))
        g = reg.convert("L"); px = g.load(); xs, ys = [], []
        for y in range(g.size[1]):
            for x in range(g.size[0]):
                if px[x, y] > 170: xs.append(x); ys.append(y)
        if not xs: continue
        bw, bh = max(xs)-min(xs), max(ys)-min(ys)
        if bh == 0: continue
        if not (2.3 < bw/bh < 3.4) or bw < 150: continue
        if best is None or bw > best[0]:
            best = (bw, f, reg, (min(xs), min(ys), max(xs), max(ys)))
    if best is None:
        print("LOGO: no candidate passed the aspect check -- left untouched", file=sys.stderr)
    else:
        bw, f, reg, bb = best
        pad = 4
        box = (max(0, bb[0]-pad), max(0, bb[1]-pad),
               min(reg.size[0], bb[2]+pad+1), min(reg.size[1], bb[3]+pad+1))
        logo = reg.crop(box); lg = logo.convert("L")
        out = Image.new("RGBA", logo.size); lp, op = lg.load(), out.load()
        for y in range(logo.size[1]):
            for x in range(logo.size[0]):
                v = lp[x, y]
                op[x, y] = (255, 255, 255, 0 if v < 40 else min(255, int((v-40)*255/160)))
        out.save(os.path.join(OUT, "ncba-logo-white.png"))
        print("logo   %dx%d  ncba-logo-white.png (aspect %.2f, from %s)"
              % (out.size[0], out.size[1], out.size[0]/out.size[1], os.path.basename(f)))

if __name__ == "__main__":
    main()
