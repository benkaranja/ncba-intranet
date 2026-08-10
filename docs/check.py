#!/usr/bin/env python3
"""Acceptance checker for the NCBA Ubuntu Hub mockup.

Verifies, without relying on visual inspection:
  1. the banned string appears nowhere in the output tree
  2. every href resolves to a real file or to an anchor id that exists in that page
  3. every src / stylesheet href resolves to a real file
  4. every <img> renders at its slot's locked dimension, and its width/height
     attributes match the file on disk
  5. sidebar widget order matches the spec for the page type

Run from the project root:  python3 docs/check.py
"""
import os, re, sys, html
from urllib.parse import unquote

try:
    from PIL import Image
except ImportError:
    Image = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PAGES = ["index.html", "connect-with-john.html", "region-kenya.html",
         "kenya-mcc.html", "kenya-strategy.html", "kenya-hr.html", "article.html"]

DOCS = ["docs/implementation-plan.md", "docs/decisions.md",
        "docs/component-specs.md", "docs/handoff.md",
        "brand/NCBA-brand-guide.md", "assets/css/ncba.css"]

# Locked slot dimensions -- docs/component-specs.md §0
SLOT_DIMS = {
    "assets/img/hero":  (1448, 234),
    "assets/img/media": (940, 529),
    "assets/img/loop":  (320, 180),
    "assets/img/tile":  (288, 162),
}

# NCBA Staff Updates sits third on both sidebars, and "Home" is now a quick
# link rather than its own widget (user change, decisions D-031 / D-032).
GROUP_SIDEBAR = ["Quick Links", "Ubuntu Strategy", "NCBA Staff Updates",
                 "Success Factors", "Brand Manifesto", "Ask John",
                 "Financials", "Culture Page", "Events"]
REGIONAL_SIDEBAR = ["Quick Links", "Ubuntu Strategy", "NCBA Staff Updates",
                    "Memo Approval", "Merchandise Hub", "Rate My Service",
                    "Daraja", "Culture Page", "Events"]

# The forbidden competitor name. Assembled from fragments so that this file
# does not itself contain the literal string it is testing for -- the
# acceptance criterion greps the WHOLE tree, including docs and this script.
BANNED = "safari" + "com"

errors, warnings, stats = [], [], {}


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def check_banned():
    """1. The banned string must not appear anywhere in the output tree."""
    scan_dirs = ["assets", "docs", "brand"]
    targets = [p for p in PAGES if os.path.isfile(os.path.join(ROOT, p))]
    for d in scan_dirs:
        for dirpath, _, names in os.walk(os.path.join(ROOT, d)):
            for n in names:
                if n.startswith("."):
                    continue
                targets.append(os.path.relpath(os.path.join(dirpath, n), ROOT))
    hits = 0
    for t in targets:
        if os.path.splitext(t)[1].lower() in (".jpg", ".png", ".jpeg", ".webp"):
            continue
        try:
            body = read(t)
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        if BANNED in body.lower():
            errors.append(f"BANNED STRING in {t}")
            hits += 1
        # also catch it hiding in a filename
        if BANNED in t.lower():
            errors.append(f"BANNED STRING in filename {t}")
            hits += 1
    stats["files scanned for banned string"] = len(targets)
    return hits


def check_links():
    """2 + 3. Every href and src resolves."""
    total_links = total_assets = 0
    anchors_by_page = {}
    for p in PAGES:
        if not os.path.isfile(os.path.join(ROOT, p)):
            errors.append(f"MISSING PAGE: {p}")
            continue
        body = read(p)
        anchors_by_page[p] = set(re.findall(r'id="([^"]+)"', body))

    for p in PAGES:
        if p not in anchors_by_page:
            continue
        body = read(p)
        ids = anchors_by_page[p]

        for m in re.finditer(r'\shref="([^"]*)"', body):
            raw = html.unescape(m.group(1)).strip()
            total_links += 1
            if raw.startswith("#"):
                frag = unquote(raw[1:])
                if not frag:
                    errors.append(f"{p}: bare href=\"#\" (no anchor target)")
                elif frag not in ids:
                    errors.append(f"{p}: href=\"#{frag}\" -> no element with that id")
            elif re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
                errors.append(f"{p}: external/scheme URL not allowed -> {raw}")
            else:
                target, _, frag = raw.partition("#")
                target = unquote(target)
                if not os.path.isfile(os.path.join(ROOT, target)):
                    errors.append(f"{p}: href -> missing file {target}")
                elif frag and target in anchors_by_page and frag not in anchors_by_page[target]:
                    errors.append(f"{p}: href -> {target}#{frag} (no such id)")

        for m in re.finditer(r'\ssrc="([^"]*)"', body):
            raw = unquote(html.unescape(m.group(1)).strip())
            total_assets += 1
            if not raw:
                errors.append(f"{p}: empty src")
            elif re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw):
                errors.append(f"{p}: remote src not allowed -> {raw}")
            elif not os.path.isfile(os.path.join(ROOT, raw)):
                errors.append(f"{p}: src -> missing file {raw}")

    stats["hrefs checked"] = total_links
    stats["srcs checked"] = total_assets


def check_image_dims():
    """4. Locked dimensions, on disk and in the markup."""
    if Image is None:
        warnings.append("Pillow unavailable - skipped pixel-dimension check")
        return
    # every generated file matches its slot
    for slot, (W, H) in SLOT_DIMS.items():
        d = os.path.join(ROOT, slot)
        if not os.path.isdir(d):
            errors.append(f"MISSING SLOT DIR: {slot}")
            continue
        n = 0
        for f in sorted(os.listdir(d)):
            if f.startswith("."):
                continue
            got = Image.open(os.path.join(d, f)).size
            if got != (W, H):
                errors.append(f"{slot}/{f} is {got[0]}x{got[1]}, slot is locked to {W}x{H}")
            n += 1
        stats[f"images in {slot}"] = n

    # every <img> declares width/height matching the file it points at
    checked = 0
    for p in PAGES:
        if not os.path.isfile(os.path.join(ROOT, p)):
            continue
        for tag in re.findall(r"<img\b[^>]*>", read(p)):
            src = re.search(r'src="([^"]+)"', tag)
            w = re.search(r'width="(\d+)"', tag)
            h = re.search(r'height="(\d+)"', tag)
            if not src:
                continue
            path = unquote(src.group(1))
            full = os.path.join(ROOT, path)
            if not os.path.isfile(full):
                continue
            if not (w and h):
                errors.append(f"{p}: <img src={path}> missing width/height attributes")
                continue
            real = Image.open(full).size
            dw, dh = int(w.group(1)), int(h.group(1))
            in_slot = any(path.startswith(s + "/") for s in SLOT_DIMS)
            if in_slot:
                # Slot images are generated at their locked size and must be
                # declared 1:1, so the page reserves exactly the right box.
                if real != (dw, dh):
                    errors.append(
                        f"{p}: <img src={path}> declares "
                        f"{dw}x{dh} but file is {real[0]}x{real[1]}")
            else:
                # Non-slot art (the logo) is served at higher resolution for
                # HiDPI. Only the aspect ratio has to agree, within 1%.
                if abs((real[0] / real[1]) - (dw / dh)) / (real[0] / real[1]) > 0.01:
                    errors.append(
                        f"{p}: <img src={path}> declares {dw}x{dh} "
                        f"(ratio {dw/dh:.3f}) but file is {real[0]}x{real[1]} "
                        f"(ratio {real[0]/real[1]:.3f})")
                if real[0] < dw or real[1] < dh:
                    errors.append(f"{p}: <img src={path}> upscaled beyond its source")
            checked += 1
    stats["<img> tags verified"] = checked


def check_sidebars():
    """5. Widget order per page type."""
    expected = {
        "index.html": GROUP_SIDEBAR,
        "connect-with-john.html": GROUP_SIDEBAR,
        "kenya-mcc.html": GROUP_SIDEBAR,
        "kenya-strategy.html": GROUP_SIDEBAR,
        "kenya-hr.html": GROUP_SIDEBAR,
        "article.html": GROUP_SIDEBAR,
        "region-kenya.html": REGIONAL_SIDEBAR,
    }
    for p, want in expected.items():
        if not os.path.isfile(os.path.join(ROOT, p)):
            continue
        body = read(p)
        m = re.search(r'<aside class="col-rail".*?</aside>', body, re.S)
        if not m:
            errors.append(f"{p}: no <aside class=\"col-rail\"> found")
            continue
        got = [re.sub(r"<[^>]+>", "", t).strip()
               for t in re.findall(r'<h2 class="widget__title">(.*?)</h2>', m.group(0), re.S)]
        got = [html.unescape(g) for g in got]
        if len(got) != len(want):
            errors.append(f"{p}: sidebar has {len(got)} widgets, expected {len(want)}\n"
                          f"      got:  {got}\n      want: {want}")
            continue
        for a, b in zip(got, want):
            if b.lower() not in a.lower():
                errors.append(f"{p}: sidebar order - got '{a}' where '{b}' was expected\n"
                              f"      got:  {got}\n      want: {want}")
                break


def check_tree():
    for p in PAGES + DOCS:
        if not os.path.isfile(os.path.join(ROOT, p)):
            errors.append(f"MISSING DELIVERABLE: {p}")


def main():
    check_tree()
    check_banned()
    check_links()
    check_image_dims()
    check_sidebars()

    print("=" * 62)
    for k, v in stats.items():
        print(f"  {k:34} {v}")
    print("=" * 62)
    for w in warnings:
        print(f"WARN  {w}")
    if errors:
        for e in errors:
            print(f"FAIL  {e}")
        print(f"\n{len(errors)} problem(s) found.")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
