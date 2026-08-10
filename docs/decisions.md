# Decision Log — NCBA Ubuntu Hub

Dated record of layout interpretations, asset substitutions, colour mapping and anything ambiguous that had to be resolved. Newest phase last.

---

## 2026-08-06 — Phase 0: inventory

### D-001 · Source paths in the brief do not match disk
**Ambiguity:** The brief referenced `PAGES/`, `Intranet Banners and Posts/` and `Images/15 Louisa Wandabwa 1.png` at the project root. None of those paths exist.
**Resolved:** Used the real locations — `Reference/PAGES/`, `Reference/Intranet Banners and Posts/`, `Images/departments/15 Louisa Wandabwa 1.png`. `Images/Strategy Video Picture.png` was correct as stated. Full mapping table in `implementation-plan.md` §2.
**Why:** The intent is unambiguous; only the paths were wrong. Nothing was moved or renamed.

### D-002 · Filenames misreport dimensions
**Ambiguity:** `KV 2 Regional  Website Banner - 1448X234px.png` is actually **1440 × 380**, not 1448 × 234. Several other files' names disagree with their pixels.
**Resolved:** Every image was measured with Pillow. **Filenames are never trusted for dimensions.**
**Why:** Constraint 3 locks a dimension per slot. Trusting the filenames would have shipped mixed aspect ratios into the same slot.

### D-003 · The forbidden competitor name does not occur in any source
A case-insensitive grep for the forbidden name across all 7 files in `Reference/PAGES/` returns **0 hits**. The only material carrying that brand is the *reference screenshot* (`Reference/reference image.png`), which is studied for layout only and never copied into `assets/`. All page copy is newly written.

**This log, `implementation-plan.md` and `check.py` never spell the name out.** The acceptance criterion greps the entire tree, `docs/` included — so a document that quoted the string while explaining the rule would itself fail the check. `check.py` assembles the search term from fragments at runtime for exactly this reason. This was caught by running the checker rather than by inspection.

---

## 2026-08-06 — Phase 1: clarifications answered

### D-004 · SharePoint chrome — suite bar + site header, no command bar
**Question:** The reference image shows the full SharePoint chrome including the author command bar (New / Page details / Preview / Analytics / Share / Edit).
**Decided:** Render the **suite bar and site header only**. The command bar is omitted.
**Why:** The command bar is author-mode UI that ordinary staff never see. Keeping the suite bar preserves the "this is SharePoint" signal without dating the pitch with editing controls.

### D-005 · Kenya banner — CSS flag, no image file
**Problem:** No Kenyan flag asset exists in any supplied folder, and Constraint 2 forbids fabricating one. This met the brief's stop condition for a missing required asset, so it was raised rather than assumed.
**Decided:** Use `KV 2 Regional  Website Banner - 1448X234px.png` as the banner image with a "Karibu Kenya" HTML overlay, and render the Kenyan flag bands as **pure CSS / inline SVG**.
**Why:** No `<img src>` points at a non-existent file, so Constraint 2 holds. A CSS gradient is not an asset.

### D-006 · Footer — rebuilt in HTML/CSS from the screenshot
**Problem:** **No footer exists in any of the 7 SharePoint exports.** The brief said to reuse the original NCBA footer; the only NCBA footer that exists anywhere in the supplied material is in the `Reference/ncba colours.png` screenshot.
**Decided:** Rebuild it faithfully in HTML/CSS — magenta `#9F197E` bar, white NCBA logo left, LinkedIn / Facebook / Instagram right. Social links resolve to the in-page anchor `#main`.
**Why:** Real external URLs would violate "every href must resolve to a file in the tree or an in-page anchor". Flagged as the one place where a SharePoint implementer must substitute real social URLs — noted in `handoff.md`.

### D-007 · Logo — extracted from supplied banner artwork
**Problem:** No standalone NCBA logo file exists. The logo appears only burned into KV banner artwork.
**Decided:** Crop the white NCBA mark + wordmark from the top-right of a supplied KV banner, key the dark ground to transparency via luminance-to-alpha, and save as `assets/img/ncba-logo-white.png`.
**Why:** Derived from a genuine supplied asset rather than invented, and visually correct — a CSS text wordmark would have lost the distinctive NCBA mark. Verified the crop is clean before committing to it.

---

## 2026-08-06 — Phase 2: design decisions

### D-008 · Newer asset folder appeared mid-build and takes precedence
`Images/updated intranet website banners images/` (30 files) was added after Phase 0 inventory had already run. Where a filename appears in both it and `Reference/Intranet Banners and Posts/`, **the updated folder wins**.
**Consequence — two materially better assets became available:**
- `KV 3 Website Banner 1448X234px.png` reads **"WELCOME TO THE NEW NCBA UBUNTU HUB"**, an exact match for the index.html header banner the brief specifies. Before this, the closest available banner read "THE NEW NCBA HUB" and the word "Ubuntu" would have had to be supplied by an HTML overlay.
- `Ubuntu Texture.png` supplies an authentic Ubuntu pattern, now the ground for the quote block (see D-012).

### D-009 · Four image slots, everything 16:9 except the hero
**Interpretation:** Constraint 3 requires one locked dimension per slot type. The naive reading produced conflicts — a "video thumbnail" appears both full-width on `index.html` and as a small side excerpt on `connect-with-john.html`.
**Resolved:** Four slots, distinguished by position rather than by content type:

| Slot | Locked size |
|---|---|
| `hero-banner` | 1300 × 210 — **superseded by D-020: now 1448 × 234** |
| `media-16x9` (carousel · video thumb · feature image · article hero) | 940 × 529 |
| `loop-thumb` (news **and** video variants in the blog loop) | 320 × 180 |
| `sidebar-tile` | 288 × 162 |

**Why:** Defining the slot by position means the blog loop's rows all share one image size whether the item is a news post or a video, so rows never jag. Everything except the hero is 16:9, giving the page one shape language.

### D-010 · Crop anchoring rules, verified visually before locking
Test crops were rendered and inspected rather than reasoned about:
- **1920 × 1080 sources → no crop at `media-16x9`.** This is why the main column is 940px: 940 × 529 is exactly 16:9, so KV headline text and the "Go for it" badge are never clipped.
- **1:1 sources (1080 × 1080 ESHOT / POST) → top-anchored crop.** Centre-cropping to 16:9 decapitated the headlines ("THE NEW NCBA H▮B") and stranded half-lines of body copy. Top-anchoring keeps headline and face intact and drops only the lower CTA line, which the HTML re-states anyway.
- **Photographs → centre crop anchored 0.18 from top at `hero-banner`.** At 6.19:1 a centred crop cut off the subject's forehead.

### D-011 · Aspect-ratio outliers excluded
`KV Rollup Banner 1/2.png` (822 × 1768, portrait rollups) and the `KV Jobs Banner` series (822 × 1079) are print/portrait formats with no web slot at any locked dimension — cropping them to 16:9 would discard most of the artwork. **Not used.** No substitution needed; there is ample 16:9 and 1:1 material.

### D-012 · Monica Kihia quote block is typographic, not photographic
**Problem:** `Images/departments/2 Monica Kihia.png` is a full "HR MISSION 2025" key visual, not a portrait. Cropping it to a circular avatar would have produced a mangled fragment of a layout.
**Decided:** The quote block carries no photograph. It is a purple panel grounded in `ubuntu-texture.jpg` (14% opacity at the time — **raised to 30% in D-024**), with a yellow left rule and cyan attribution (**lightened in D-024**). The Monica Kihia KV is used at full width as a `media-16x9` feature image on `kenya-hr.html`, where it works as designed.

### D-013 · Colour mapping — reference layout to NCBA brand
The reference layout is recoloured, never re-used. Mapping:

| Reference role | NCBA replacement | Source of the value |
|---|---|---|
| Green suite bar | `--ncba-purple` `#230B49` | KV banner ground |
| Green site header / nav | `--ncba-magenta` `#9F197E` | The live NCBA header and footer bar |
| Green tag chips | `--ncba-magenta` `#9F197E` | Same |
| Green "Learn More" links | `--ncba-magenta` on white, `--ncba-cyan` `#5CA5D3` on dark | Banner headline colour |
| — (no equivalent) | `--ncba-yellow` `#F2E10E` CTA | "Go for it" badge on every KV banner |

Every value was sampled from the artwork with Pillow rather than eyeballed or taken from memory.

### D-014 · Placeholder links resolve to real anchors
"Zero dead links" is enforced literally. Nav and widget items without a built page point at a **real anchor id that exists in that page** (`#main`, `#news`, `#events`, `#help`) rather than a bare `href="#"`, so the Phase 4 checker can validate anchor targets instead of skipping them.

### D-015 · "We're Here to Help" emails are plain text, not `mailto:`
Contact addresses render as text spans. A `mailto:` is neither a file in the tree nor an in-page anchor, so including them would have forced the link checker to carry an exemption and weakened the zero-dead-links guarantee. Noted in `handoff.md` as a one-line change for the real build.

### D-016 · Brand guide written before the CSS, reconciled after
The brand guide is the specification `ncba.css` implements. Because the acceptance criteria require the guide to match the CSS *exactly*, Phase 4 re-reads the CSS and reconciles every documented value against it before sign-off.

---

## 2026-08-06 — Phase 3a: CSS + index.html

### D-017 · No HTML text is ever overlaid on the banner artwork
**Problem, found by rendering the page rather than by reading the code:** the reference layout overlays the page title on the banner and the slide caption on the carousel image. That works in the reference because its artwork is plain photography. **NCBA's artwork is fully designed and already carries its own baked-in headline and body copy.** Overlaying HTML text produced literal double-speak — the `<h1>` "Welcome to the NCBA Ubuntu Hub" sat directly on top of the banner's own "WELCOME TO THE NEW NCBA UBUNTU HUB", and the carousel caption repeated the GMD slide's printed copy underneath it.

**Decided:** text moves off the artwork in both components.
- **Hero:** `.hero__bar` — a purple title bar directly *below* the image, square top corners meeting the image, rounded bottom. **(Superseded by D-028: the bar was later removed entirely and the `<h1>` hidden.)** The `<h1>` stays visible and semantic; the artwork stays unobstructed. `.hero__overlay` was removed.
- **Carousel:** `.carousel__cap` moves below the viewport, and the prev/next buttons move *inside* `.carousel__viewport` so they stay centred on the image no matter how tall the caption runs. Captions live in `data-title` / `data-text` on each slide and the existing carousel script swaps them — four extra lines, no new dependency.

**Why this over the alternatives:** hiding the `<h1>` would have satisfied the brief's wording while losing the visible page title; picking artwork without text would have discarded most of the supplied library. Putting the title in a bar beneath the banner is also closer to how SharePoint actually composes a banner web part above a title region, so it reads as more native, not less.

This applies to all 7 pages — every hero asset in the library carries baked-in text, so the collision was never specific to the home page.

### D-018 · Logo is served at 3× and declared at display size
`assets/img/ncba-logo-white.png` is extracted at its native 244 × 86 from `KV 2 - Magic Happen 1920x1080px.png` — the largest clean instance of the mark in the library — and declared at 74 × 26 in the header and 68 × 24 in the footer for HiDPI sharpness. A first extraction from a 1448 × 234 banner gave only 63 × 25 and looked soft when scaled.

`docs/check.py` therefore applies two rules: images inside the four slot directories must match their locked size **exactly**, while non-slot art need only match the declared **aspect ratio within 1%** and must never be upscaled beyond its source. Without that distinction the checker would have forced the logo to be degraded to 74 × 26.

### D-020 · Hero banner is full-bleed, and the slot was re-locked to 1448 × 234
**Requested:** the header image should run the full width of the site, as it does on the live intranet.

**Done:** `.hero` moved out of `.canvas` and now sits directly under the nav, spanning the viewport. The title bar beneath it keeps its inner content constrained to the same 1300px measure as the grid, so the `<h1>` still lines up with the content below rather than drifting to the window edge.

**Consequence, and why the locked dimension changed:** at 1300 × 210 a full-bleed banner would be **upscaled** on any viewport wider than 1300px — soft edges on exactly the element that sets first impressions. The supplied banners are natively **1448 × 234**, so the `hero-banner` slot is re-locked to that and every hero re-rendered. The slot still holds one dimension across all 7 pages; it is now the artwork's true size instead of a size derived from a canvas the banner no longer sits inside. `docs/check.py` was updated to assert the new value.

### D-021 · Campaign tags carry the Ubuntu pattern
**Requested:** use the Ubuntu texture behind the coloured tags on the blog loop, tinted so the text still reads.

**Done:** `.chip` stacks a purple tint over `ubuntu-texture.jpg` in a single `background-image` — a gradient layer above the texture layer — so no extra element is needed. `background-color` stays set as a fallback if the texture fails to load.

**Tint chosen by measurement, not by eye.** Every pixel of the texture was composited at the rendered 200px size and checked against white: flat tint **17.28:1**, worst single pixel **12.68:1**, **zero** pixels below 7:1. The tag clears AAA for small text across the whole pattern rather than on average. Recorded in the brand guide.

### D-022 · Sidebar widgets rebuilt in the SharePoint idiom
**Requested:** use the widget style from `Reference/index.html`, which reads more like real SharePoint web parts; and build the Quick Links buttons in the style of the "Active programs" section of `Test Site - Sidebar Quick links.html`.

**Done — three widget idioms, all taken from the supplied files rather than invented:**
- **`.qlinks` — SharePoint Quick Links, Button layout.** The "Active programs" section is that web part in `ButtonCard` mode. Its real CSS was read out of the export: 4px radius, 1px border, 22px icon at `margin: 0 12px`, label 14px/**400**/20px with `margin: 10px 0` and `padding-right: 14px`, 40px min content height, 2-line clamp. Rendered as magenta filled buttons with white icon and label. Note the 400 weight — SharePoint uses regular here, and semibold makes the rail read heavier than a native page.
- **`.reslinks` — boxed document-link rows** for text-only widgets, matching the `.resource-links` pattern in `Reference/index.html` and the boxed link list in the reference layout's right rail.
- **`.feed` — Viva Engage card** for NCBA Staff Updates, matching `.staff-card`: avatar, author, relative time, category badge, clamped text, hashtag, "Seen by N", and a comment field.

`.widget` itself was flattened — border only, no drop shadow — because SharePoint web parts sit flat on the page and the shadow was making the rail float above the content.

### D-023 · The 7 pages are emitted from one chrome source
The suite bar, header, secondary nav, sidebars and footer are generated from a single definition rather than hand-copied seven times, because the acceptance criteria require them to render **identically** on every page and hand-copying reliably drifts.

**This is an authoring tool, not a build step.** The generator lives outside the delivered tree; the 7 delivered files are plain static HTML with no dependency on it and open directly from `file://`. Verified: the suite bar and footer are **byte-identical** across all 7 pages, and every page carries the same 15 nav links.

## 2026-08-06 — Phase 5: visual review of all 7 pages

### D-024 · Hero bar lightened, Ubuntu pattern made more visible
**Requested:** reduce the opacity of the bar under every header image, and make all Ubuntu textures more visible.

Each change trades legibility against visibility, so the limits were **measured** rather than eyeballed — every pixel of `ubuntu-texture.jpg` composited at its rendered size and checked against the text colour above it.

| Element | Was | Now | Worst-case contrast at the new value |
|---|---|---|---|
| `.hero__bar` | `--ncba-purple` solid | `rgba(35,11,73,.85)` | white title **11.34:1**, sub-line **9.17:1** — both AAA · **superseded by D-028, bar removed** |
| `.quote::before` | `opacity: .14` | `opacity: .30` | white quote text **7.72:1**, 0 of 126,000 pixels below 7:1 |
| `.chip` tint | `rgba(…,.86)` | `rgba(…,.70)` | white tag text **7.86:1**, 0 of 28,400 pixels below 7:1 |

**Both texture values sit exactly at their ceiling.** At quote opacity `.35`, 49 pixels drop below 7:1; at chip tint `.65`, 2 do, and by `.60` there are 200. These are the most visible the pattern can be without losing AAA.

**One casualty, fixed:** the quote block's cyan attribution role fell to **2.86:1** over the denser pattern — below AA. Added `--ncba-cyan-light` `#9BCFEA`, which holds **4.60:1** on every pixel. `--ncba-cyan` itself is unchanged and still used everywhere else.

### D-025 · Two supplied key visuals are the same artwork
`KV 4 - Make it Happen` and `KV 6 - Make it Happen` are **pixel-identical**. Both had been mapped to separate news items on `kenya-mcc.html`, which put two identical thumbnails in one news list.

Caught by hashing the rendered pixel data of every generated image rather than by trusting filenames — the same discipline as D-002. `loop-mcc-alt.jpg` was removed from the asset set and that news item now uses `loop-magic.jpg`. Verified afterwards: no two files in any slot are pixel-identical, and no page repeats a thumbnail.

### D-026 · Related-article cards: inline spans never broke to new lines
`.related__title` and `.related__desc` are `<span>`s and the CSS never set them to `display: block`, so the department name flowed inline directly after the headline — "…regional powerhouse Marketing, Communications & Citizenship" as one run of text. Both are now block-level.

Worth noting how this was found: it was **invisible in the screenshot at render scale** and only confirmed by reading the two elements' bounding boxes from the DOM. The same check across the other stacked label pairs (`.events__title`, `.feed__author`, `.article__author`, `.help__team`) found no other instances.

### D-027 · Quick-link button hover lightens, matching SharePoint
A slow CSS extraction over the 1.8 MB export finished after the buttons had already shipped, and surfaced one rule the faster pass had missed:

```css
.root-258:not(.emptyStateSecondary):hover { background-color: rgb(121,89,165); border-color: rgb(255,255,255) }
```

**SharePoint's ButtonCard lightens on hover**, to a lighter tint of the theme colour. My implementation darkened it to `--ncba-magenta-dark` — the hover was the one value in that component I chose rather than read from the source, and I had chosen the wrong direction.

Corrected with `--ncba-magenta-light` `#AC3990` (+14% white), scoped to `.qlinks a:hover` only. White label contrast **5.61:1**, effectively identical to the native rule's 5.55:1. Everything else that hovers — buttons, links, cards — still darkens, which is correct for those components.

Every other value in the earlier reading was confirmed unchanged: 4px radius, 1px white border, 22px icon at `margin: 0 12px`, label 14px/400/20px, `margin: 10px 0`, `padding-right: 14px`, 40px min content height, 2-line clamp.

## 2026-08-07 — Phase 6: requested revisions

### D-028 · Hero title bar removed; `<h1>` kept but hidden
**Requested:** remove `.hero__bar` from all header banners.

Done on all 7 pages. The banner artwork already carries its own headline, so the bar was saying the same thing twice — this is the same problem D-017 identified, resolved by deletion rather than relocation.

**One thing I did not delete:** every page still needs an `<h1>` for document structure and screen readers. The heading and its sub-line are now `class="visually-hidden"` — present in the markup and announced by assistive tech, painted nowhere. Removing them outright would have left all 7 pages with no heading at all.

### D-029 · Ubuntu pattern strip beside main-column media
**Requested:** a narrow (<5px) Ubuntu-texture strip left and right of banner images and carousels — but **not** on blog-loop images, header images, quote images or sidebar images.

Implemented as horizontal padding plus the texture as a background on `.media`, `.carousel__viewport` and `.article__hero` (**4px/160px here; respecified to 8px/400px in D-034**), so the strip sits *beside* the image rather than over it. No markup change was needed except wrapping the department feature images in `.media`.

**Reading of "banner images" vs "header images":** these could name the same thing, but the instruction excludes header images while including banner images, so "header image" = the full-bleed hero at the top of the page and "banner image" = the main-column media. Verified in the browser: `.carousel__viewport` and `.media` carry 4px padding + texture; `.hero`, `.loop__media` and `.tile__img` carry none.

**A side effect worth knowing:** on `index.html` the Ubuntu Spirit video now uses an artwork that is *itself* an Ubuntu pattern (D-033), so the strip beside it is invisible. Not a fault — just the two changes meeting.

### D-030 · Tag pattern made more visible — now AA, no longer AAA
**Requested:** make the pattern on the tag more visible. Tint lowered `.70` → `.55`.

| | Worst pixel | Below 4.5:1 | Verdict |
|---|---|---|---|
| Old `.70` | 7.86:1 | 0 | AAA |
| **New `.55`** | **5.07:1** | **0 of 28,400** | **AA, not AAA** |

**This is a real trade and worth stating plainly:** the tag text no longer meets AAA. It clears AA everywhere on the pattern with margin, and these are 11px bold decorative labels whose text is repeated in the headline beside them, so nothing is lost if a reader cannot resolve one. But the earlier AAA guarantee no longer holds for this component. Raising the tint back to `.70` restores it.

### D-031 · NCBA Group Home moved into the quick links
**Requested:** the NCBA Group home button belongs in `.qlinks`.

Added as the **first** quick-link button on all 7 pages, pointing at `index.html`, with a house glyph. The standalone "Home" widget on the regional sidebar was removed — it duplicated the new button. The regional sidebar therefore drops from 10 widgets to 9, and `docs/check.py` was updated so the order assertion matches.

### D-032 · NCBA Staff Updates promoted, and now on every page
**Requested:** move NCBA Staff Updates up, below Quick Links and Ubuntu Strategy, on **all** sidebar layouts.

Both sidebars now open: Quick Links → Ubuntu Strategy → NCBA Staff Updates. The feed previously appeared only on the regional sidebar; "all sidebar layouts" means it is now on the Group sidebar too, so it appears on all 7 pages. Both orders in `check.py` updated to match.

### D-033 · Two artwork swaps
- `connect-with-john.html` hero → `KV 1 Website Banner John Gachora 1448x234px.png`. Natively **1448 × 234**, so it drops into the hero slot with no crop at all — better than the previous photograph, which had to be cropped to a 6.19:1 band.
- The Ubuntu Spirit video thumbnail *and* the Ubuntu Strategy sidebar tile → `KV 2 - The Ubuntu Strategy Banner.png` ("IGNITE BELIEF — THE UBUNTU SPIRIT"). Natively 1920 × 1080, so uncropped at `media-16x9`.

### D-034 · Ubuntu edge strip respecified to 8px / 400px
The strip specified in D-029 was 4px at `background-size: 160px`, following the original "<5px" instruction. Respecified to the exact values requested:

```css
padding-left: 8px;
padding-right: 8px;
background-image: url("../img/ubuntu-texture.jpg");
background-size: 400px;
```

At 400px the pattern renders near its native scale (`ubuntu-texture.jpg` is 420 × 300), so individual motifs are legible rather than reading as coloured noise — which 160px did at 4px wide. Applies to the same three elements and the same exclusions as D-029: `.media`, `.carousel__viewport`, `.article__hero`; never hero banners, blog-loop thumbnails, the quote block or sidebar imagery. Verified in the browser.

### D-035 · Quote-block left rule is now the Ubuntu pattern
The 4px flat `--ncba-yellow` rule on `.quote` is replaced by an 8px Ubuntu-pattern strip, matching the strip beside main-column media (D-034).

Drawn as `.quote::after` — an absolutely positioned 8px column — rather than a border, so it layers above the `::before` texture ground. The quote text is inset 40px by the block's own padding plus 56px by `.quote__text`, so the strip never crowds it. `border-left` is now `0`.

### D-036 · John Gachora banner re-rendered from an updated source
`KV 1 Website Banner John Gachora 1448x234px.png` was **replaced on disk at 14:30**, after `hero-john.jpg` had already been generated from the earlier version at 11:01. Detected by comparing modification times rather than assuming the existing render was current. Re-rendered; mean pixel difference against the new source is **1.07** (JPEG noise only).

Worth noting as a general hazard: the generated `assets/img/**` are derived files. If a source is swapped, the build must be re-run or the site silently keeps serving the old artwork.

### D-037 · Dedicated GMD message artwork
`A MESSAGE FROM THE GMD.png` (1920 × 1080) now supplies `video-gmd.jpg`, replacing `KV 1 - GMD FIRESIDE CHAT-1.png`. Native 16:9, so uncropped at `media-16x9`.

**Scope:** exactly one `.media media--video` carries the heading "A message from the GMD" — the video on `region-kenya.html`. The index carousel's first slide is captioned "A message from the Group Managing Director", but that is a carousel slide, not the video component the instruction named, so it was left on `carousel-gmd.jpg`. Flagged rather than assumed.

### D-038 · Departments became a dropdown under every country
The secondary nav previously ran the four countries, a divider, then MCC · Strategy · Human Resources as flat siblings. Each country now carries its own CSS-only dropdown of the three department pages, matching the flyout the main nav already uses for Region.

- `.subnav__item.has-submenu` + `.submenu`, opening on `:hover` and `:focus-within`. No JS.
- Active country keeps the magenta underline; the active department is highlighted **inside** its dropdown on `--ncba-magenta-tint`.
- **`.subnav__inner` lost `overflow-x: auto`** — it would have clipped the dropdowns outright. With four countries the row fits, and it wraps rather than scrolls. This was the one non-obvious consequence of the change.

### D-039 · Côte d'Ivoire removed
Dropped from `COUNTRIES`, so it disappears from both the main-nav Region flyout and every secondary nav. Also removed from `implementation-plan.md` and `component-specs.md`; a tree-wide grep for "ivoire|ivory" now returns nothing.

### D-019 · The acceptance grep covers `docs/` too
Running the checker revealed that `implementation-plan.md`, `decisions.md` and `check.py` all contained the forbidden competitor name **while documenting the rule forbidding it** — which would have failed `grep -ril` over the tree. All three now refer to it only obliquely, and `check.py` assembles the search term from fragments at runtime. Caught by tooling, not by eye; a good argument for writing the checker before the pages.
