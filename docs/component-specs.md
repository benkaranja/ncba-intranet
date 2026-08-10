# Component Specifications — NCBA Ubuntu Hub

Per-component reference: markup structure, CSS classes, dimensions and responsive behaviour.
Design tokens (`--ncba-magenta`, `--sp-4`, …) are defined in `brand/NCBA-brand-guide.md` and declared in `assets/css/ncba.css`.

---

## 0. Locked image dimensions — binding table

**One dimension per slot, across all 7 pages.** Verified against the files on disk in Phase 4.

| Slot | CSS class | Locked size | Ratio | Used by | Crop rule |
|---|---|---|---|---|---|
| Hero banner | `.hero__img` | **1448 × 234** | 6.19:1 | Page header banner, all 7 pages — **full-bleed** | Centre; photographs anchored 0.18 from top |
| Main-column media | `.media__img` | **940 × 529** | 16:9 | Carousel slides · video thumbnails · full-width feature images · article hero | 1920 × 1080 sources uncropped |
| Loop thumbnail | `.loop__img` | **320 × 180** | 16:9 | Blog-loop side image (news **and** video variants) | 1:1 sources top-anchored |
| Sidebar tile | `.tile__img` | **288 × 162** | 16:9 | Sidebar widget imagery | 1:1 sources top-anchored |

Every `<img>` carries explicit `width` and `height` attributes equal to its slot size, so layout space is reserved before decode and pages do not reflow.

**Output directories** mirror the slots: `assets/img/hero/`, `assets/img/media/`, `assets/img/loop/`, `assets/img/tile/`, plus `assets/img/ncba-logo-white.png`.

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
    <img src="assets/img/ncba-logo-white.png" alt="NCBA" width="88" height="26">
    <span class="sitehead__title">Ubuntu Hub</span>
  </a>
  <nav class="sitehead__nav" aria-label="Main">
    <ul>
      <li><a class="is-active" href="index.html">Group</a></li>
      <li><a href="connect-with-john.html">Connect with John</a></li>
      <li class="has-menu">
        <a href="region-kenya.html">Region <svg class="caret">…</svg></a>
        <ul class="menu">…5 countries…</ul>
      </li>
      …
    </ul>
  </nav>
</header>
```

**Nav order (fixed on all 7 pages):** Group · Connect with John · Region ▾ · Connect to Systems · Form Downloads · BUZZ · Rate My Service · Culture & Change · Automation Center · Sustainability

**Region dropdown `.menu`** — CSS-only, opens on `:hover` and `:focus-within`. Items: Kenya · Uganda · Tanzania · Rwanda, all → `region-kenya.html`. White panel, `--shadow-card-hover`, 220px wide, 8px radius, 36px rows.

| State | Treatment |
|---|---|
| Rest | `#FFFFFF` at 92% opacity, `--fs-nav` |
| Hover | 100% + `rgba(255,255,255,.12)` background |
| `.is-active` | 100%, weight 700, 3px `--ncba-yellow` bottom border |

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
  <img class="hero__img" src="assets/img/hero/x.jpg" alt="…" width="1448" height="234">
  <div class="hero__flag"></div>                 <!-- Kenya page only -->
  <h1 class="visually-hidden">…</h1>
  <p class="visually-hidden">…</p>
</section>
```

Image **1448 × 234**, no radius, `object-fit: cover`.

**Full-bleed, outside `.canvas`, directly under the nav** (decision D-020), matching the live NCBA intranet. Rendered at the artwork's native size so it is not upscaled at common desktop widths.

**No title bar and no overlaid text** (decision D-028). Every NCBA hero asset carries its own baked-in headline, so any HTML text here duplicates it. The `<h1>` and its sub-line remain in the markup as `visually-hidden` — present for document structure and screen readers, painted nowhere. They must not be deleted outright or the page would have no heading at all.

The Ubuntu pattern is **baked into the supplied artwork's own edges** (D-045); no CSS strip is painted beside any image.

**Kenya variant** inserts `.hero__flag` directly under the image — a 6px full-width band, `linear-gradient(to right, #000 0 33.33%, #BB0000 33.33% 66.66%, #006600 66.66% 100%)`, pure CSS, no image file (decision D-005).

**Responsive:** < 720px the image switches to `aspect-ratio: 16/9` with `object-position: center`.

---

## 6. Carousel — `.carousel` (index.html only)

```html
<div class="carousel" aria-roledescription="carousel" aria-label="NCBA Group highlights">
  <div class="carousel__viewport">
    <div class="carousel__track" id="carouselTrack">
      <figure class="carousel__slide" data-title="…" data-text="…">
        <img class="media__img" src="assets/img/media/x.jpg" width="940" height="529" alt="…">
      </figure>
      …
    </div>
    <button class="carousel__btn carousel__btn--prev" id="carouselPrev" aria-label="Previous slide">…</button>
    <button class="carousel__btn carousel__btn--next" id="carouselNext" aria-label="Next slide">…</button>
  </div>
  <div class="carousel__cap" id="carouselCap" aria-live="polite"><h3></h3><p></p></div>
  <div class="carousel__dots" id="carouselDots"></div>
</div>
```

Slides **940 × 529**. Track is `display:flex` with `transform: translateX(-100% * i)` and a 400ms ease transition. Dots are 10px, `--line-strong`, current dot `--ncba-magenta`.

**The caption sits below the viewport, not over the slide** (decision D-017) — the artwork carries its own copy. Caption text lives in `data-title` / `data-text` on each slide and the script swaps it on change; `.carousel__cap` has `min-height: 76px` so the page does not jump between slides of differing caption length.

**The prev/next buttons live inside `.carousel__viewport`**, which is the positioning context. That keeps them vertically centred on the *image* rather than on the image-plus-caption box. 36px circles, `rgba(255,255,255,.9)`, `--shadow-card`.

**JS — the only script in the project.** ~34 lines of vanilla JS inline at the end of `index.html`: index state, prev/next, dot click, caption swap, and `aria-hidden` on non-current slides. No autoplay — it steals focus and is a common accessibility complaint. No dependencies. `prefers-reduced-motion: reduce` drops the transition.

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

## 8. Quote block — `.quote`

```html
<figure class="quote">
  <blockquote class="quote__text">…</blockquote>
  <figcaption class="quote__by">
    <span class="quote__name">Monica Kihia</span>
    <span class="quote__role">Group Director, HR and Culture</span>
  </figcaption>
</figure>
```

Full width of the main column. Ground `--ncba-purple` with `assets/img/tile/ubuntu-texture.png` as a CSS `background-image` at `opacity:.14` / `background-size:420px` — applied via a `::before` layer so it is decorative and invisible to screen readers. 8px Ubuntu-pattern left strip (`.quote::after`), `--radius-lg`, padding 32px 40px. Quote `--fs-quote` white; name 14/600 white; role 12/400 `--ncba-cyan`.

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
