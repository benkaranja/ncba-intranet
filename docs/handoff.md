# Handoff — NCBA Ubuntu Hub mockup

**What this is:** a static, clickable mockup of a redesigned NCBA Group SharePoint intranet. It is a pitch artifact — it looks and clicks like the real thing, but contains no SharePoint deployment code.

**Date:** 2026-08-06

---

## 1. How to open it

Double-click **`index.html`**. That is the whole procedure — no server, no build, no install.

Every page opens the same way and every link works from `file://`. Paths are relative throughout, so the folder can be zipped, emailed, or moved anywhere and it will still work.

Tested in Chromium at 1440px, 1024px, 768px and 375px.

### What is clickable
- The full main menu, including the **Region** dropdown (hover or keyboard focus — CSS only, no JS)
- The secondary country/department nav on Kenya and the three department pages
- Every news headline, thumbnail and "Read article" link → `article.html`
- Sidebar widgets that point at built pages (Ubuntu Strategy, Ask John, Brand Manifesto, Home)
- The carousel on the home page — arrows and dots

### What is deliberately inert
Links with no page behind them resolve to an in-page anchor (`#main`, `#news`, `#help`, `#events`) rather than a dead `href="#"`. They will scroll rather than navigate. This keeps the zero-dead-links guarantee testable — see §5.

---

## 2. File map

```
index.html                Group home (L1) — banner, carousel, Ubuntu video, quote, 5 news, help
connect-with-john.html    GMD page (L1) — CEO banner, 5 video-thumbnail articles
region-kenya.html         Kenya (L2) — country banner + CSS flag, GMD video, quote, 5 news
kenya-mcc.html            Marketing, Communications & Citizenship (L3)
kenya-strategy.html       Strategy (L3) — Louisa Wandabwa feature + strategy video
kenya-hr.html             Human Resources (L3)
article.html              Full post view (L4) — hero, byline, body, share, related

assets/css/ncba.css       The single stylesheet. All design tokens live at the top.
assets/img/hero/          7 banners      — 1448 x 234
assets/img/media/         12 main-column images — 940 x 529
assets/img/loop/          20 blog thumbnails    — 320 x 180
assets/img/tile/          5 sidebar images      — 288 x 162
assets/img/ncba-logo-white.png   244 x 86, transparent
assets/img/ubuntu-texture.jpg    CSS background for quote block and campaign tags

brand/NCBA-brand-guide.md Colour, type, spacing, grid, component tokens, image table
docs/implementation-plan.md  Phased build plan with status
docs/decisions.md            Dated decision log (D-001 … D-023)
docs/component-specs.md      Per-component markup, classes, dimensions, responsive
docs/check.py                Automated acceptance checker — see §5
docs/handoff.md              This file
```

Source folders (`Reference/`, `Images/`) were **not modified**. Nothing was deleted, moved or renamed.

---

## 3. Rebuilding each component natively in SharePoint

The mockup was designed against real SharePoint web parts, so most of it maps 1:1. Where it does not, that is noted.

| Mockup component | Native SharePoint equivalent | Notes for the implementer |
|---|---|---|
| Suite bar | Microsoft 365 suite header | Comes free. The mockup recolours it to `#230B49`; native theming controls this via the site theme, not per-page CSS. |
| Site header + main nav | Hub site navigation | Set the hub nav once; it propagates. "Connect with John" sits between Group and Region. |
| Region dropdown | Hub nav cascading menu | Native supports one level of children — sufficient for the five countries. |
| Secondary nav | Site navigation (local) | On Kenya and the three department sites. |
| **Hero banner** | **Image web part, full-width section** | Must be placed in a **full-width section**, which requires the page layout to have one enabled. The title bar below it is a Text web part on a coloured full-width section. |
| Carousel | Hero web part (carousel layout) or News carousel | Native hero supports 5 tiles. Captions come from the item, not from the image. |
| Video thumbnail | Stream / Embed web part, or File viewer | The mockup uses a still + play button because there is no video file. Swap for the real Stream embed. |
| Quote block | Text web part with custom formatting | The Ubuntu pattern background needs either a section background image or a small CSS extension. |
| **Blog-post loop** | **News web part, "List" layout** | The closest native match. Campaign tags map to a managed metadata column surfaced via a page-property; if that is too heavy, use the News category field. |
| Campaign tag chip | — | No native equivalent with a textured fill. Either accept a flat brand colour or add an SPFx extension. **This is the one component that cannot be done with out-of-the-box web parts alone.** |
| **Quick Links buttons** | **Quick Links web part, Button layout** | Exactly what the mockup replicates — see `Reference/PAGES/Test Site - Sidebar Quick links.html`, "Active programs" section. Icons come from the Fluent icon set. |
| Resource link rows | Quick Links web part, Compact/List layout | — |
| Events | Events web part | Filter by category per site. |
| NCBA Staff Updates | Viva Engage (Yammer) web part | Conversations layout. |
| We're here to help | Quick Links or Text web part | See `Reference/PAGES/Test Site - Were Here to Help.html`. |
| Footer | Site footer | SharePoint's built-in footer supports a logo and links. |

### Two things to change for the real build

1. **Footer social links.** They currently point at `#main` so the mockup has zero dead links. Point them at the real LinkedIn / Facebook / Instagram URLs.
2. **"We're here to help" addresses.** They render as plain text, not `mailto:` links, for the same reason. Make them `mailto:` in the real build.

Both are one-line changes and both are recorded in `decisions.md` (D-006, D-015).

---

## 4. Design tokens

Everything visual is driven by custom properties at the top of `assets/css/ncba.css`. Changing a brand colour is a one-line edit:

```css
:root {
  --ncba-magenta: #9F197E;   /* header, footer, buttons, active states */
  --ncba-purple:  #230B49;   /* suite bar, dark panels, quote ground */
  --ncba-cyan:    #5CA5D3;   /* accent, links on dark */
  --ncba-yellow:  #F2E10E;   /* "Go for it" CTA only */
}
```

Every hex was sampled from the supplied NCBA artwork with Pillow rather than picked by eye. `brand/NCBA-brand-guide.md` records where each one came from, so the palette can be re-derived if the artwork changes.

---

## 5. Verifying it still holds together

```bash
python3 docs/check.py
```

Run from the project root. It checks, mechanically:

1. the forbidden competitor name appears **nowhere** in the tree (including these docs and the checker itself, which is why neither spells it out)
2. every `href` resolves to a real file, or to an anchor id that **actually exists on that page**
3. every `src` resolves to a real file, and nothing loads from a remote host
4. every image on disk matches its slot's locked dimension, and every `<img>` declares `width`/`height` matching the file it points at
5. the sidebar widget order matches the spec for that page type

Current state: **all checks pass** — 493 hrefs, 92 image references, 44 slot images.

It needs Python 3 and Pillow (`pip install pillow`). Without Pillow it still runs and skips the pixel checks.

### Image slots are binding

| Slot | Locked size | Where |
|---|---|---|
| `hero-banner` | 1448 × 234 | page banner, all 7 pages, full-bleed |
| `media-16x9` | 940 × 529 | carousel, video thumbnails, feature images, article hero |
| `loop-thumb` | 320 × 180 | blog-loop side image |
| `sidebar-tile` | 288 × 162 | sidebar imagery |

If you add an image, generate it at the slot size or the checker will fail. The regeneration rules — including that 1:1 sources are cropped **top-anchored** so headlines are not decapitated — are in `decisions.md` D-009 and D-010.

---

## 6. Known limitations

- **Not a SharePoint solution.** No SPFx, no page templates, no site scripts. Rebuilding is manual, guided by §3.
- **The carousel is the only JavaScript** — about 34 lines, inline in `index.html`. No autoplay, by choice.
- **Copy is placeholder.** Names carried over from the brief (Monica Kihia, Louisa Wandabwa, John Gachora, Nelly Wainaina) and NCBA brand terms are real; everything else is generic. **No financial figures, results or executive statements were invented** — the live intranet export contained a real profit headline, and it was deliberately not reused.
- **The Kenyan flag is CSS**, not an image, because no flag asset was supplied and inventing one would have broken the no-fabricated-assets rule (D-005).
- **Portrait assets are unused.** `KV Rollup Banner 1/2` (822 × 1768) and the `KV Jobs Banner` series (822 × 1079) are print formats with no web slot (D-011).
- **Right rail is long.** Ten widgets on the Kenya page is a lot of scrolling; worth pruning before it ships.
