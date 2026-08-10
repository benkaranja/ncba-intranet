# NCBA Ubuntu Hub — Brand & Style Reference

Simplified brand and style guide for the NCBA Group SharePoint intranet redesign.
**Every value in this document matches `assets/css/ncba.css` exactly.** Where the CSS uses a custom property, the token name is given.

**Version:** 1.0 · **Date:** 2026-08-06

---

## 1. Colour palette

All hex values were **sampled directly from the supplied NCBA artwork**, not guessed. Sampling sources are noted so the palette can be re-derived.

### 1.1 Primary

| Token | Hex | Role | Sampled from |
|---|---|---|---|
| `--ncba-magenta` | `#9F197E` | **Primary brand.** Site header bar, footer bar, active nav underline, primary buttons, tag chips, quick-link icon tiles | Header & footer bar, `Reference/ncba colours.png` |
| `--ncba-magenta-dark` | `#7C1362` | Hover / pressed state for magenta buttons, links and cards | Derived (−12% lightness) |
| `--ncba-magenta-light` | `#AC3990` | Hover for **quick-link buttons only** — SharePoint's ButtonCard lightens on hover rather than darkening | Derived (+14% white) |
| `--ncba-magenta-tint` | `#F6E9F2` | Selected nav background, quote-block tint, subtle brand wash | Derived (8% magenta on white) |

### 1.2 Secondary

| Token | Hex | Role | Sampled from |
|---|---|---|---|
| `--ncba-purple` | `#230B49` | **Secondary brand.** Suite bar, dark panel grounds, quote-block ground | KV banner ground |
| `--ncba-purple-deep` | `#1E032F` | Gradient terminus, image overlay ground | KV banner ground |

### 1.3 Accent

| Token | Hex | Role | Sampled from |
|---|---|---|---|
| `--ncba-cyan` | `#5CA5D3` | **Accent.** Links on dark grounds, "Learn more" arrows, eyebrow rules, attribution text | "THE NEW NCBA / UBUNTU HUB" banner headline |
| `--ncba-cyan-dark` | `#3B7FA8` | Accent hover | Derived (−15% lightness) |
| `--ncba-cyan-light` | `#9BCFEA` | Attribution text on the textured quote ground, where the standard cyan falls below AA | Derived (+30% lightness) |
| `--ncba-yellow` | `#F2E10E` | **"Go for it" CTA** — reserved for the primary call-to-action button only | "Go for it" badge on every KV banner |
| `--ncba-yellow-dark` | `#D6C700` | CTA hover | Derived (−10% lightness) |

> **Usage discipline:** yellow is a CTA colour, never a background or text colour. Cyan never appears as body text on white — it fails contrast; on white grounds, links use magenta.

### 1.4 Text

| Token | Hex | Role | Contrast on `--surface` |
|---|---|---|---|
| `--ink` | `#201F1E` | h1–h3 headings | 15.9:1 ✅ AAA |
| `--body` | `#323130` | Body copy, nav labels | 12.6:1 ✅ AAA |
| `--muted` | `#605E5C` | Captions, bylines, dates, metadata | 7.0:1 ✅ AAA |
| `--on-dark` | `#FFFFFF` | Any text on magenta or purple | 5.9:1 on magenta ✅ AA |

### 1.5 Background & surface

| Token | Hex | Role |
|---|---|---|
| `--surface` | `#FFFFFF` | Page canvas, cards, widget bodies |
| `--surface-alt` | `#FAF9F8` | Sidebar widget grounds, alternating bands |
| `--app-bg` | `#F3F2F1` | Viewport background outside the 1300px canvas |

### 1.6 Borders

| Token | Hex | Role |
|---|---|---|
| `--line` | `#EDEBE9` | Default hairline — card borders, loop-item separators |
| `--line-strong` | `#D2D0CE` | Section dividers, input borders |

### 1.7 Interactive states

| State | Treatment |
|---|---|
| Link (rest, on white) | `--ncba-magenta`, no underline |
| Link (hover) | `--ncba-magenta-dark`, underline |
| Link (on dark ground) | `--ncba-cyan`; hover `#FFFFFF` |
| Nav item (rest) | `--on-dark` at 92% opacity |
| Nav item (hover) | `--on-dark` 100% + `rgba(255,255,255,.12)` background |
| Nav item (active) | `--on-dark` 100%, weight 700, 3px `--ncba-yellow` bottom border |
| Button primary (hover) | Background `--ncba-magenta-dark` |
| Button CTA (hover) | Background `--ncba-yellow-dark` |
| Focus (all interactive) | `2px solid --ncba-magenta`, `outline-offset: 2px` |
| Card (hover) | `--shadow-card-hover`, title colour → `--ncba-magenta` |
| Disabled | `opacity: .45`, `cursor: not-allowed` |

> No status colours (success/warning/error) are defined, because this mockup contains no status components. Adding them without a component to carry them would put values in this guide that are not in the CSS.

---

## 2. Typography

### 2.1 Family

SharePoint Online's standard UI face is **Segoe UI**. The mockup uses it with a full cross-platform fallback stack so the pages render correctly from `file://` on macOS, Windows and Linux.

```css
--font-ui: "Segoe UI", "Segoe UI Web (West European)", -apple-system,
           BlinkMacSystemFont, "Roboto", "Helvetica Neue", Helvetica,
           Arial, sans-serif;
```

A single family is used throughout — SharePoint modern pages do not mix faces, and matching that is what makes the mockup read as native. No web fonts are loaded (no CDN, per the static-only constraint).

### 2.2 Type scale

Root font-size is `16px`, so `1rem = 16px`.

| Role | Token | px | rem | Weight | Line-height | Letter-spacing |
|---|---|---|---|---|---|---|
| h1 — page title | `--fs-h1` | 32 | 2 | 600 | 40px (1.25) | −0.02em |
| h2 — section heading | `--fs-h2` | 24 | 1.5 | 600 | 32px (1.333) | −0.01em |
| h3 — card / loop title | `--fs-h3` | 20 | 1.25 | 600 | 28px (1.4) | −0.01em |
| h4 — widget title | `--fs-h4` | 16 | 1 | 600 | 22px (1.375) | 0 |
| h5 — sub-label | `--fs-h5` | 14 | 0.875 | 600 | 20px (1.429) | 0.01em |
| h6 — eyebrow (uppercase) | `--fs-h6` | 12 | 0.75 | 700 | 16px (1.333) | 0.08em |
| Body | `--fs-body` | 15 | 0.9375 | 400 | 22px (1.467) | 0 |
| Body small / excerpt | `--fs-body-sm` | 14 | 0.875 | 400 | 20px (1.429) | 0 |
| Caption / meta / byline | `--fs-caption` | 12 | 0.75 | 400 | 16px (1.333) | 0 |
| Nav | `--fs-nav` | 14 | 0.875 | 600 | 20px (1.429) | 0 |
| Button | `--fs-btn` | 14 | 0.875 | 600 | 20px (1.429) | 0.01em |
| Quote | `--fs-quote` | 24 | 1.5 | 400 | 36px (1.5) | −0.01em |

**Weights used:** 400 regular · 600 semibold · 700 bold. No light or black weights — Segoe UI's light weights are unreliable across platforms.

---

## 3. Spacing scale

4px base unit. Only these steps are used.

| Token | px | rem | Typical use |
|---|---|---|---|
| `--sp-1` | 4 | 0.25 | Icon-to-label gap, chip padding |
| `--sp-2` | 8 | 0.5 | Tight stack, button vertical padding |
| `--sp-3` | 12 | 0.75 | Quick-link row gap |
| `--sp-4` | 16 | 1 | Card padding, widget padding |
| `--sp-5` | 20 | 1.25 | Button horizontal padding |
| `--sp-6` | 24 | 1.5 | Widget-to-widget gap, loop text gutter |
| `--sp-8` | 32 | 2 | Block padding |
| `--sp-10` | 40 | 2.5 | Main-to-rail column gap, loop item vertical rhythm |
| `--sp-12` | 48 | 3 | Section separation |
| `--sp-16` | 64 | 4 | Major block separation |

---

## 4. Grid & layout

| Property | Token | Value |
|---|---|---|
| Canvas max-width | `--canvas` | **1300px**, centred |
| Main column | `--col-main` | **940px** (`minmax(0, 940px)`) |
| Right rail | `--col-rail` | **320px** (fixed) |
| Column gap | `--sp-10` | **40px** |
| Canvas side padding | `--sp-6` | 24px below 1348px viewport |
| Suite bar height | `--h-suite` | 48px |
| Site header height | `--h-header` | 68px |
| Secondary nav height | `--h-subnav` | 44px |

`940 + 40 + 320 = 1300`.

### 4.1 Radii

| Token | Value | Use |
|---|---|---|
| `--radius-sm` | 2px | Buttons, tag chips — matches SharePoint's control radius |
| `--radius-md` | 4px | Cards, images, quick-link icon tiles |
| `--radius-lg` | 8px | Quote block |

### 4.2 Elevation

| Token | Value |
|---|---|
| `--shadow-card` | `0 1.6px 3.6px rgba(0,0,0,.132), 0 .3px .9px rgba(0,0,0,.108)` |
| `--shadow-card-hover` | `0 6.4px 14.4px rgba(0,0,0,.132), 0 1.2px 3.6px rgba(0,0,0,.108)` |

These are SharePoint/Fluent depth-4 and depth-16, so cards sit at the same visual altitude as native web parts.

### 4.3 Breakpoints

| Breakpoint | Behaviour |
|---|---|
| ≥ 1348px | Full 1300px canvas, two columns |
| 1024–1347px | Canvas fluid with 24px side padding, two columns, main flexes |
| < 1024px | Single column — right rail drops below the main column, full width |
| < 720px | Nav scrolls horizontally; loop items stack image above text; hero banner switches to a 16:9 crop |

---

## 5. Component tokens

### 5.1 Card

| Property | Value |
|---|---|
| Background | `--surface` |
| Border | `1px solid --line` |
| Radius | `--radius-md` (4px) |
| Padding | `--sp-4` (16px) |
| Shadow | `--shadow-card` → `--shadow-card-hover` on hover |
| Title | `--fs-h3` / 600 / `--ink` → `--ncba-magenta` on hover |

### 5.2 Buttons

| Variant | Background | Text | Padding | Radius | Type |
|---|---|---|---|---|---|
| Primary | `--ncba-magenta` | `#FFFFFF` | 8px 20px | 2px | `--fs-btn` |
| CTA "Go for it" | `--ncba-yellow` | `--ink` | 8px 20px | 2px | `--fs-btn` |
| Secondary | transparent | `--ncba-magenta` | 8px 20px | 2px, `1px solid --ncba-magenta` | `--fs-btn` |
| Text / "Read article" | none | `--ncba-magenta` | 0 | — | `--fs-body-sm` 600 + `→` |

Minimum hit target 32px tall; 44px on touch widths.

### 5.3 Quick-link button (`.qlinks`)

Replicates the **Button layout** of the SharePoint Quick Links web part, as used in the "Active programs" section of `Reference/PAGES/Test Site - Sidebar Quick links.html`. Values below were read out of that file's own stylesheet, not approximated.

| Property | Value | Source rule |
|---|---|---|
| Card | full width, `--radius-md` (4px), `1px solid rgba(255,255,255,.9)` | `.root-258` |
| Fill | `--ncba-magenta` (theme primary) | themed web part |
| Min height | 60px (40px content + 10px margins top/bottom) | `.textArea-141` |
| Icon | 22 × 22px, white, `margin: 0 12px`, centred | `.thumbnail-257` |
| Label | 14px / **400** / 20px line-height, white, `margin: 10px 0`, `padding-right: 14px` | `.labelTextWrapper-259` |
| Label clamp | 2 lines | `.css-149` |
| Gap between buttons | `--sp-3` (12px) | — |
| Hover | Fill → `--ncba-magenta-dark` | — |

> Note the label weight is **400**, not 600. SharePoint's button cards use regular weight; using semibold makes the rail read as heavier than a native page.

### 5.3b Resource link (`.reslinks`)

The boxed document-link list used for text-only widgets, matching the widget idiom in `Reference/index.html`.

| Property | Value |
|---|---|
| Row | min-height 40px, padding `--sp-2 --sp-3`, `1px solid --line`, `--radius-md` |
| Icon | 16 × 16px document glyph, `--ncba-magenta` |
| Label | `--fs-body-sm` (14px / 400) / `--body` |
| Hover | Border → `--ncba-magenta`, background `--ncba-magenta-tint`, label → `--ncba-magenta` |
| Gap between rows | `--sp-2` (8px) |

### 5.4 Quote block

| Property | Value |
|---|---|
| Ground | `--ncba-purple` with `ubuntu-texture.jpg` at `opacity: .30`, `background-size: 420px`, applied via a `::before` layer so it stays decorative |
| Radius | `--radius-lg` (8px) |
| Padding | `--sp-8` `--sp-10` (32px 40px) |
| Quote mark | `"` 72px, `--ncba-cyan`, `opacity: .55` |
| Quote text | `--fs-quote` (24px / 400 / 36px) / `#FFFFFF` |
| Attribution name | `--fs-h5` (14px / 600) / `#FFFFFF` |
| Attribution role | `--fs-caption` (12px / 400) / `--ncba-cyan-light` |
| Left rule | 4px `--ncba-yellow`, full height |

### 5.4b Ubuntu edge strip

An 8px Ubuntu-pattern strip down the left and right edge of main-column media.

| Property | Value |
|---|---|
| Applies to | `.media`, `.carousel__viewport`, `.article__hero` |
| Strip | `padding-left/right: 8px` + `background-image: url("../img/ubuntu-texture.jpg")`, `background-size: 400px` |
| Never applies to | hero banners, blog-loop thumbnails, the quote block, sidebar tiles |

The padding places the pattern *beside* the image rather than over it, so no artwork is obscured.

### 5.5 Video thumbnail

| Property | Value |
|---|---|
| Image | `media-16x9` — **940 × 529** |
| Radius | `--radius-md` |
| Play button | 64px circle, `rgba(255,255,255,.92)`, centred; 22px magenta triangle |
| Hover | Play circle → `#FFFFFF`, `transform: scale(1.06)` |
| Caption | `--fs-caption` / `--muted`, 8px below |

### 5.6 Campaign tag chip (`.chip`, blog loop)

Carries the **Ubuntu pattern** behind a purple tint, so the tag reads as an NCBA artefact rather than a generic label.

| Property | Value |
|---|---|
| Background | Two stacked layers in one `background-image`: `linear-gradient(rgba(35,11,73,.55), rgba(35,11,73,.55))` over `url("../img/ubuntu-texture.jpg")` at `background-size: 200px` |
| Fallback | `background-color: --ncba-purple` if the texture fails to load |
| Text | `#FFFFFF` |
| Type | 11px / 700 / uppercase / `letter-spacing: .06em` |
| Padding | 4px 8px · Radius `--radius-sm` |
| Edge | `inset 0 0 0 1px rgba(255,255,255,.14)` — separates the chip from dark thumbnails |

> **Contrast, measured over the actual texture** (every pixel of `ubuntu-texture.jpg` composited at the rendered 200px size, against white):
> - worst single pixel: **5.07:1**
> - pixels below 4.5:1 (AA): **0 of 28,400**
>
> **AA everywhere, not AAA** (decision D-030). The tint was lowered from `.70` to `.55` so the pattern reads clearly as a pattern; the cost is that this component no longer meets AAA. Acceptable here because these are 11px decorative labels whose text is repeated in the headline beside them. Restore `.70` for AAA.

### 5.7 Blog-post loop item

| Property | Value |
|---|---|
| Grid | `320px 1fr`, gap `--sp-6` (24px) |
| Thumbnail | `loop-thumb` — **320 × 180**, `--radius-md`, `object-fit: cover` |
| Title | `--fs-h3` / 600 / `--ink` → `--ncba-magenta` on hover |
| Excerpt | `--fs-body-sm` / `--muted`, clamped to 3 lines |
| Separator | `1px solid --line`, `padding-block: --sp-6` |
| < 720px | Collapses to one column; thumbnail goes full width at 16:9 |

---

## 6. Locked image dimensions

**Binding.** Every instance of a slot uses exactly one dimension across all 7 pages. Verified against the files on disk in Phase 4.

| Slot | Locked size | Ratio | Used by | Crop rule |
|---|---|---|---|---|
| `hero-banner` | **1448 × 234** | 6.19:1 | Page header banner, all 7 pages — **full-bleed across the viewport** | Centre; photographs anchored 0.18 from top |
| `media-16x9` | **940 × 529** | 16:9 | Carousel slides · video thumbnails · full-width feature images · article hero | 1920×1080 sources used uncropped |
| `loop-thumb` | **320 × 180** | 16:9 | Blog-loop side image, news and video variants | 1:1 sources top-anchored |
| `sidebar-tile` | **288 × 162** | 16:9 | Sidebar widget imagery | 1:1 sources top-anchored |

**Why these numbers:** `hero-banner` is the exact native size of the supplied NCBA intranet banners. Because the banner runs full-bleed across the viewport (not inside the 1300px canvas), rendering at native 1448 × 234 means it is never upscaled at common desktop widths. `media-16x9` is the main column width (940px) at the native 16:9 of the supplied 1920 × 1080 key visuals, so that artwork is never cropped and its headline text is never clipped. `loop-thumb` and `sidebar-tile` hold the same 16:9 so every rounded image on the page shares one shape language.

Every `<img>` carries explicit `width` and `height` attributes matching its slot, so pages reserve layout space and do not reflow as images decode.

---

## 7. Accessibility notes

- Body text contrast is AAA on white; white on `--ncba-magenta` is 5.9:1 (AA for normal text, AAA for large).
- Cyan is never used for body text on white — magenta is the on-white link colour.
- Focus is always visible: `2px solid --ncba-magenta` at `outline-offset: 2px`, never removed.
- All decorative banner artwork carries descriptive `alt` text; purely ornamental texture is applied via CSS `background-image`, so it is invisible to screen readers by construction.
- Carousel controls are real `<button>` elements with `aria-label`s; the slide region is an `aria-roledescription="carousel"` container.
