# Component Specifications — NCBA Ubuntu Hub

Per-component reference: markup structure, CSS classes, dimensions and responsive behaviour.
Design tokens (`--ncba-magenta`, `--sp-4`, …) are defined in `brand/NCBA-brand-guide.md` and declared in `assets/css/ncba.css`.

---

## 0. Locked image dimensions — binding table

**Three slots. One dimension per slot, across all 7 pages.** Verified against the files on disk in Phase 4.

| Slot | CSS class | Locked size | Ratio | Used by | Crop rule |
|---|---|---|---|---|---|
| Hero banner | `.hero__img` | **1920 × 310** | 6.19:1 | Page header banner, all 7 pages — **full-bleed** | Centre; photographs anchored 0.18 from top |
| Main-column media | `.media__img` | **940 × 529** | 16:9 | Carousel slides · video thumbnails · full-width feature images · article hero | 1920 × 1080 sources uncropped |
| Loop thumbnail | `.loop__img` | **320 × 180** | 16:9 | Blog-loop side image (news **and** video variants) | 1:1 sources top-anchored |

Every `<img>` carries explicit `width` and `height` attributes equal to its slot size, so layout space is reserved before decode and pages do not reflow.

**Output directories** mirror the slots: `assets/img/hero/`, `assets/img/media/`, `assets/img/loop/`, plus `assets/img/ncba-logo-white.png` and `assets/img/ubuntu-texture.jpg` (a CSS background, not a slot).

---

## 1. Page shell

```html
<body>
  <a class="skip" href="#main">Skip to main content</a>
  <div class="suitebar">…</div>          <!-- 48px, purple -->
  <header class="sitehead">…</header>     <!-- 68px, magenta: logo + title + nav -->
  <nav class="subnav">…</nav>             <!-- 44px, white: L2/L3 pages only -->
  <section class="hero">…</section>       <!-- FULL BLEED, outside the canvas -->
  <div class="canvas">
    <div class="grid">
      <main class="col-main" id="main">…</main>
      <aside class="col-rail">…</aside>
    </div>
  </div>
  <footer class="sitefoot">…</footer>     <!-- magenta -->
</body>
```

| Element | Class | Height | Background |
|---|---|---|---|
| Suite bar | `.suitebar` | 48px | `--ncba-purple` |
| Site header | `.sitehead` | 68px | `--ncba-magenta` |
| Secondary nav | `.subnav` | 44px | `--surface`, `1px solid --line` bottom |
| Canvas | `.canvas` | — | `--surface`, `max-width: 1300px`, centred |
| Grid | `.grid` | — | `grid-template-columns: minmax(0,940px) 320px; gap: 40px` |

**Responsive:** < 1024px `.grid` becomes one column and `.col-rail` falls below `.col-main` at full width. < 720px `.sitehead__nav` scrolls horizontally (`overflow-x:auto`).

---

## 2. Suite bar — `.suitebar`

Waffle glyph · "SharePoint" wordmark · search field · right icon cluster · user avatar `NK`.
All inline SVG, 20px, `currentColor` white. Search is a non-submitting `<input type="search">` (decorative). Avatar is a 32px circle, `rgba(255,255,255,.18)`, initials at 12px/600.

---

## 3. Site header — `.sitehead`

```html
<header class="sitehead">
  <a class="sitehead__brand" href="index.html">
    <img src="assets/img/ncba-logo-white.png" alt="NCBA" width="71" height="26">
    <span class="sitehead__title">UBUNTU Hub</span>
  </a>
  <nav class="sitehead__nav" aria-label="Main">
    <ul>
      <li><a href="#main">About NCBA</a></li>
      <li class="has-menu"><a href="staff.html">Staff <svg class="caret">…</svg></a>
        <ul class="menu">…Existing Staff · New Staff…</ul></li>
      <li><a href="#news">Culture &amp; Change</a></li>
      <li class="has-menu"><a href="kenya-mcc.html">Departments <svg class="caret">…</svg></a>
        <ul class="menu">…MCC · Strategy · Human Resources · UBUNTU Hub…</ul></li>
      <li><a href="ubuntu-hub.html">UBUNTU Hub</a></li>
      <li><a class="is-external" href="https://ncbagroup.com/" target="_blank" rel="noopener noreferrer">
        NCBA Group <svg class="ext">…</svg><span class="visually-hidden"> (opens in a new tab)</span></a></li>
    </ul>
  </nav>
</header>
```

**Nav order (fixed on all nine pages, D-053):** About NCBA · Staff ▾ · Culture & Change · Departments ▾ · UBUNTU Hub · NCBA Group ↗

**Dropdowns `.menu`** — CSS-only, open on `:hover` and `:focus-within`. White panel, `--shadow-card-hover`, 220px wide, 8px radius, 36px rows.

**External item** — `NCBA Group` carries `.is-external`, an 11px `.ext` glyph, `target="_blank"`, `rel="noopener noreferrer"` and a `visually-hidden` "(opens in a new tab)". It is the **only** external URL permitted anywhere; `check.py` whitelists exactly that one (D-057).

| State | Treatment |
|---|---|
| Rest | `#FFFFFF` at 92% opacity, `--fs-nav` |
| Hover | 100% + `rgba(255,255,255,.12)` background |
| `.is-active` | 100%, weight 700, 3px `--ncba-yellow` bottom border |

---

## 4. Secondary nav — `.subnav`

Two variants.

**Departments strip** — on `kenya-mcc`, `kenya-strategy`, `kenya-hr`, `ubuntu-hub`. Four plain items: MCC · Strategy · Human Resources · UBUNTU Hub. Active item: `--ncba-magenta`, weight 700, 2px underline.

**Country strip** — retained on `region-kenya.html` only. Kenya · Uganda · Tanzania · Rwanda, each carrying a CSS-only dropdown of the four departments (D-038).

```html
<nav class="subnav" aria-label="Departments">
  <div class="subnav__inner">
    <div class="subnav__item"><a class="is-active" href="kenya-mcc.html">MCC</a></div>
    …
  </div>
</nav>
```

**`.subnav__inner` must not set `overflow-x: auto`** — it would clip the country dropdowns. It wraps instead.

---

## 4. Secondary nav — `.subnav`

L2/L3 pages only (`region-kenya`, `kenya-mcc`, `kenya-strategy`, `kenya-hr`).

Countries in **full**: Kenya · Uganda · Tanzania · Rwanda. **Each country carries a CSS-only dropdown** of MCC · Strategy · Human Resources (decision D-038), matching the flyout pattern of the main nav.

```html
<nav class="subnav" aria-label="Regions">
  <div class="subnav__inner">
    <div class="subnav__item has-submenu">
      <a class="is-active" href="region-kenya.html">Kenya <svg class="caret">…</svg></a>
      <ul class="submenu">
        <li><a href="kenya-mcc.html">MCC</a></li>
        <li><a href="kenya-strategy.html">Strategy</a></li>
        <li><a href="kenya-hr.html">Human Resources</a></li>
      </ul>
    </div>
    …
  </div>
</nav>
```

Countries all → `region-kenya.html` (only Kenya is built). Active country: `--ncba-magenta`, weight 700, 2px underline. Active department: magenta on `--ncba-magenta-tint` inside its dropdown.

**`.subnav__inner` must not set `overflow-x: auto`** — it would clip the dropdowns. It wraps instead.

---

## 5. Hero banner — `.hero`

```html
<section class="hero">
  <img class="hero__img" src="assets/img/hero/x.jpg" alt="…" width="1920" height="310">
  <div class="hero__flag"></div>                 <!-- Kenya page only -->
  <h1 class="visually-hidden">…</h1>
  <p class="visually-hidden">…</p>
</section>
```

Image **1920 × 310**, no radius, `object-fit: cover`.

**Full-bleed, outside `.canvas`, directly under the nav** (decision D-020), matching the live NCBA intranet. Rendered at the artwork's native size so it is not upscaled at common desktop widths.

**No title bar and no overlaid text** (decision D-028). Every NCBA hero asset carries its own baked-in headline, so any HTML text here duplicates it. The `<h1>` and its sub-line remain in the markup as `visually-hidden` — present for document structure and screen readers, painted nowhere. They must not be deleted outright or the page would have no heading at all.

The Ubuntu pattern is **baked into the supplied artwork's own edges** (D-045); no CSS strip is painted beside any image.

**Kenya variant** inserts `.hero__flag` directly under the image — a 6px full-width band, `linear-gradient(to right, #000 0 33.33%, #BB0000 33.33% 66.66%, #006600 66.66% 100%)`, pure CSS, no image file (decision D-005).

**Responsive:** < 720px the image switches to `aspect-ratio: 16/9` with `object-position: center`.

---

## 6. Carousel — `.carousel`

Used for the home-page updates carousel and the HR page carousel.

```html
<div class="carousel" data-carousel aria-roledescription="carousel" aria-label="…">
  <div class="carousel__viewport">
    <div class="carousel__track" data-track>
      <figure class="carousel__slide" data-title="…" data-text="…">
        <img class="media__img" src="assets/img/media/x.jpg" width="940" height="529" alt="…">
      </figure>
      …
    </div>
    <button class="carousel__btn carousel__btn--prev" data-prev type="button">…</button>
    <button class="carousel__btn carousel__btn--next" data-next type="button">…</button>
  </div>
  <div class="carousel__cap" data-cap aria-live="polite"><h3></h3><p></p></div>
  <div class="carousel__dots" data-dots></div>
</div>
```

Slides **940 × 529**. Track is `display:flex` with `transform: translateX(-100% * i)`, 400ms ease. Dots 10px, current dot `--ncba-magenta`.

**Caption sits below the viewport, never over the artwork** (D-017) — the artwork carries its own copy. Text lives in `data-title` / `data-text` and the script swaps it; `min-height: 76px` stops the page jumping between slides.

**Shared script (D-054).** One inline script binds to **every** `[data-carousel]` on the page, reading `[data-track]`, `[data-dots]`, `[data-cap]`, `[data-prev]`, `[data-next]`. Captions are optional, so the same script drives the hero slider, which has none. This is the only JavaScript in the project; no autoplay, no dependencies, and `prefers-reduced-motion: reduce` drops the transition.

---

## 6c. Hero slider — `.heroslider` (index.html)

Full-bleed rotator of four 1920 × 310 banners. **No HTML text** — the artwork carries its own headline (D-028, D-053).

```html
<section class="hero heroslider" data-carousel aria-roledescription="carousel" aria-label="…">
  <div class="heroslider__viewport">
    <div class="heroslider__track" data-track>
      <figure class="heroslider__slide"><img class="hero__img" … width="1920" height="310"></figure>
      …
    </div>
    <button class="heroslider__btn heroslider__btn--prev" data-prev type="button">…</button>
    <button class="heroslider__btn heroslider__btn--next" data-next type="button">…</button>
    <div class="heroslider__dots" data-dots></div>
  </div>
  <h1 class="visually-hidden">…</h1>
</section>
```

Arrows are 40px circles inset `--sp-6`; dots overlay the foot of the banner in white. Driven by the shared `[data-carousel]` script (D-054) — it has no `[data-cap]`, so the script skips the caption swap.

---

## 6d. Two-up media row — `.twoup`

Two video posters side by side in the main column, used for the GMD and HR messages on the home page.

```html
<div class="twoup">
  <div class="twoup__col">
    <h3 class="twoup__title">A message from the GMD</h3>
    <a class="media media--video" href="article.html">
      <img class="media__img" … width="940" height="529">
      <span class="media__play" aria-hidden="true"></span>
    </a>
    <p class="media__cap">…</p>
  </div>
  …
</div>
```

`grid-template-columns: 1fr 1fr`, gap `--sp-6`; play button shrinks to 52px. Stacks to one column below 720px.

**Legibility note:** each tile renders ~458px wide, so a 1920px source's baked body copy lands near 5px. These are **poster frames**, not reading material — the play button sets that expectation. Anything meant to be read must be full-width (D-056).

---

## 7. Video thumbnail — `.media.media--video`

```html
<a class="media media--video" href="article.html">
  <img class="media__img" src="assets/img/media/x.png" width="940" height="529" alt="…">
  <span class="media__play" aria-hidden="true"></span>
</a>
<p class="media__cap">…</p>
```

Image **940 × 529**. `.media__play` is a 64px circle, `rgba(255,255,255,.92)`, centred, containing a 22px magenta CSS triangle. Hover: circle → `#FFFFFF`, `scale(1.06)`. The whole tile is one link, so there is a single tab stop.

---

## 9. Blog-post loop — `.loop` / `.loop__item`

The core component, replicating the reference layout's flow.

```html
<section class="section" id="news">
  <div class="section__head"><h2>News</h2><a class="section__all" href="article.html">See all</a></div>
  <div class="loop">
    <article class="loop__item">
      <a class="loop__media" href="article.html">
        <img class="loop__img" src="assets/img/loop/x.png" width="320" height="180" alt="…">
      </a>
      <div class="loop__body">
        <span class="chip">#UbuntuSpirit</span>
        <h3 class="loop__title"><a href="article.html">…</a></h3>
        <p class="loop__excerpt">…</p>
        <a class="loop__more" href="article.html">Read article <span aria-hidden="true">→</span></a>
      </div>
    </article>
    …
  </div>
</section>
```

| Property | Value |
|---|---|
| Item grid | `320px 1fr`, gap `--sp-6` (24px) |
| Thumbnail | **320 × 180**, `--radius-md`, `object-fit: cover` |
| Separator | `1px solid --line` bottom, `padding-block: --sp-6` |
| Title | `--fs-h3` / 600 / `--ink` → `--ncba-magenta` on hover |
| Excerpt | `--fs-body-sm` / `--muted`, `-webkit-line-clamp: 3` |
| Video variant | `.loop__item--video` adds a 40px `.media__play` centred on the thumbnail |

Minimum **5 items** on `index.html`, `region-kenya.html`, `connect-with-john.html`, `kenya-mcc.html`, `kenya-strategy.html`, `kenya-hr.html`.
Every thumbnail, headline and "Read article" link → `article.html`.

**Responsive:** < 720px collapses to one column, thumbnail full width at 16:9 above the text.

---

## 10. Sidebar widget — `.widget`

```html
<section class="widget">
  <h2 class="widget__title">Quick Links</h2>
  <div class="widget__body">…</div>
</section>
```

Rail is **320px**. Widget: `--surface`, `1px solid --line`, `--radius-md`, `--shadow-card`, padding `--sp-4`, gap `--sp-6` between widgets. Title `--fs-h4`, with a 24px `--ncba-magenta` underline rule.

### 10.1 Quick Links — `.qlinks` (SharePoint Button layout)

Replicates the **Button layout** of the SharePoint Quick Links web part, as used in the "Active programs" section of `Reference/PAGES/Test Site - Sidebar Quick links.html`. Values were read from that file's own stylesheet (`.root-258`, `.thumbnail-257`, `.textArea-141`, `.labelTextWrapper-259`, `.css-149`), not approximated.

```html
<ul class="qlinks">
  <li><a href="#main">
    <span class="qlinks__icon" aria-hidden="true"><svg>…</svg></span>
    <span class="qlinks__label">Performance Management</span></a></li>
  …
</ul>
```

| Property | Value |
|---|---|
| Card | full width, `--radius-md` (4px), `1px solid rgba(255,255,255,.9)`, fill `--ncba-magenta` |
| Min height | 60px (40px content + 10px top/bottom margins) |
| Icon | 22 × 22px white inline SVG, `margin: 0 12px`, `align-self: center` |
| Label | 14px / **400** / 20px, white, `margin: 10px 0`, `padding-right: 14px`, 2-line clamp |
| Gap | `--sp-3` (12px) between buttons |
| Hover | Fill → `--ncba-magenta-light` `#AC3990` — **lightens**, matching SharePoint's own `.root-258:hover` rule (5.61:1 vs the native 5.55:1) |

The label weight is **400**, matching SharePoint. Semibold makes the rail read heavier than a native page.

Items: Performance Management · Career Management · Leave Management · Success Factors · CRM · NCBA Whistle Blowing (taken from the live Group page).

### 10.1b Resource links — `.reslinks`

Boxed document-link rows for text-only widgets, matching `.resource-links` in `Reference/index.html`.

| Property | Value |
|---|---|
| Row | min-height 40px, padding `--sp-2 --sp-3`, `1px solid --line`, `--radius-md` |
| Icon | 16 × 16px document glyph, `--ncba-magenta` |
| Label | `--fs-body-sm` (14px / 400) / `--body` |
| Hover | Border → `--ncba-magenta`, background `--ncba-magenta-tint` |
| Gap | `--sp-2` (8px) |

### 10.2 Link tile — `.tile`
Optional **288 × 162** image, then title 14/600 and one line of 12px `--muted` copy, with a magenta `→`. Whole tile is one link.

### 10.3 Events — `.events`
Date chip 48 × 48px, `--ncba-magenta-tint`, month 10px/700 uppercase magenta over day 18px/700 `--ink`; then title 14/600 and time 12px `--muted`. Rows separated by `--line`.

### 10.4 Staff Updates feed — `.feed` (regional sidebar only)

Viva Engage style card, matching `.staff-card` in `Reference/index.html`.

```html
<div class="feed">
  <article class="feed__item">
    <div class="feed__head">
      <span class="feed__avatar">NS</span>
      <span class="feed__who">
        <span class="feed__author">NCBA Staff Updates</span>
        <span class="feed__meta">1h ago</span>
      </span>
      <span class="feed__badge">Announcement</span>
    </div>
    <p class="feed__text">…</p>
    <a class="feed__tag" href="article.html">#NewNCBAHub</a>
    <span class="feed__views">Seen by 771</span>
    <input class="feed__comment" type="text" placeholder="Write a comment">
  </article>
</div>
```

Card `1px solid --line`, `--radius-md`, padding `--sp-3`. Avatar 32px circle, `--ncba-magenta-tint` on `--ncba-magenta`. Author 13px/600. Badge 10px/700 uppercase in the magenta tint. Text 13px/18px clamped to 3 lines. Comment field 32px tall, 16px radius, `--surface-alt`. Each comment input carries a `visually-hidden` label for screen readers.

### 10.5 Widget order — binding

| Sidebar | Pages | Order |
|---|---|---|
| **Group** | `index`, `connect-with-john`, `kenya-mcc`, `kenya-strategy`, `kenya-hr`, `article` | Quick Links · Ubuntu Strategy · Success Factors · Brand Manifesto · Ask John · Financials · Culture Page · Events |
| **Regional** | `region-kenya` | Quick Links · Home · Ubuntu Strategy · Memo Approval · Merchandise Hub · Rate My Service · Daraja · NCBA Staff Updates · Culture Page · Events |

---

## 11. We're Here to Help — `.help`

Pattern taken from `Reference/PAGES/Test Site - Were Here to Help.html`.
Heading "We're here to help", then a 4-column grid (`repeat(4, 1fr)`, gap `--sp-4`) of contact cards: 32px magenta circular icon, team name 14/600, address 12px `--muted`.
Addresses are **plain text, not `mailto:` links** (decision D-015).
**Responsive:** 2 columns < 1024px, 1 column < 640px.

---

## 11b. Ask-the-GMD composer — `.askbox`

Sits under the intro body copy on `connect-with-john.html`. Reads as a native SharePoint / Viva composer.

```html
<div class="askbox">
  <div class="askbox__head">
    <span class="askbox__avatar">NK</span>
    <span class="askbox__who">
      <span class="askbox__title">Ask John a question</span>
      <span class="askbox__meta">Goes to the Office of the Group Managing Director</span>
    </span>
  </div>
  <label class="visually-hidden" for="askq">Your question for the GMD</label>
  <textarea class="askbox__input" id="askq" rows="3" placeholder="…"></textarea>
  <div class="askbox__foot">
    <label class="askbox__check"><input type="checkbox" id="askanon"> Ask anonymously</label>
    <span class="askbox__actions">
      <button class="btn btn--secondary" type="button">Save draft</button>
      <button class="btn btn--primary" type="button">Submit question</button>
    </span>
  </div>
  <p class="askbox__note">…</p>
</div>
```

| Property | Value |
|---|---|
| Card | `--surface`, `1px solid --line`, `--radius-md`, `--shadow-card`, padding `--sp-4` |
| Avatar | 40px circle, `--ncba-magenta` on white, 14px/700 |
| Textarea | `--surface-alt` fill, `1px solid --line-strong`, `--radius-md`, min-height 88px, vertical resize |
| Focus | `2px solid --ncba-magenta`, fill lightens to `--surface` |
| Checkbox | 16px, `accent-color: --ncba-magenta` |
| Actions | right-aligned; secondary "Save draft" + primary "Submit question" |
| < 720px | footer stacks, actions right-aligned |

**No `<form>`, and every button is `type="button"`** (decision D-052). The mockup must not be able to submit anything. A SharePoint implementer would replace this with a Microsoft Forms web part or a Power Apps form.

---

## 12. Footer — `.sitefoot`

Rebuilt from `Reference/ncba colours.png` (decision D-006). Full-bleed `--ncba-magenta` bar, 64px tall, inner content constrained to 1300px. White NCBA logo left; LinkedIn · Facebook · Instagram right at 13px/600 white, 24px apart, underline on hover. Social links → `#main`.
**Responsive:** < 640px stacks and centres, height auto with 16px vertical padding.

---

## 13. Article page — `article.html`

| Block | Class | Notes |
|---|---|---|
| Hero image | `.article__hero` | `media-16x9` — **940 × 529** |
| Title | `.article__title` | `--fs-h1` |
| Byline | `.article__by` | 32px avatar initials · author 14/600 · role 12px `--muted` |
| Date | `.article__date` | `--fs-caption` `--muted` |
| Body | `.article__body` | `--fs-body`, `max-width: 68ch`, 16px paragraph spacing, h2/h3 subheads |
| Pull quote | `.pullquote` | 20px italic, 3px magenta left rule |
| Share row | `.share` | 3 secondary buttons — LinkedIn · Copy link · Email → `#main` |
| Related | `.related` | 3 cards → `kenya-mcc.html`, `kenya-strategy.html`, `kenya-hr.html`, thumbnails at **320 × 180** |

---

## 14. Link policy

Every `href` in every page resolves to one of the 7 HTML files or to an anchor id that **exists in that page**. Anchor ids present on every page: `#main`, `#news`, `#help`. `index.html` and `region-kenya.html` also carry `#events`.
No `mailto:`, no `tel:`, no external URLs, no bare `href="#"`.
