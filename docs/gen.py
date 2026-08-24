#!/usr/bin/env python3
"""Emit the static HTML pages of the NCBA UBUNTU Hub mockup.

AUTHORING tool, not a build step: it writes plain static HTML once. The
delivered pages have no dependency on it and open directly from file://.
It exists so the header, secondary nav, sidebars and footer are provably
identical on every page rather than hand-copied nine times.
"""
import os

ROOT = "/Volumes/Creative_Onpremise/Ben Karanja/2026/NCBA/SHAREPOINT DESIGN claude"

# --------------------------------------------------------------------------
# icons
# --------------------------------------------------------------------------
def svg(paths, sw="1.7", vb="0 0 22 22"):
    return ('<svg viewBox="%s" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            % (vb, sw, paths))

IC_COMPASS = svg('<circle cx="11" cy="11" r="8"/><path d="m14.5 7.5-2 5-5 2 2-5z"/>')
IC_STAR    = svg('<path d="m11 3 2.4 4.9 5.4.8-3.9 3.8.9 5.4L11 15.4 6.2 17.9l.9-5.4L3.2 8.7l5.4-.8z"/>')
IC_BADGE   = svg('<path d="M11 3l5.5 2.4v4.2c0 3.4-2.2 5.6-5.5 6.6-3.3-1-5.5-3.2-5.5-6.6V5.4z"/><path d="m8.6 10.6 1.7 1.7 3.1-3.4"/>')
IC_CHAT    = svg('<path d="M3.5 6.5A2.5 2.5 0 0 1 6 4h10a2.5 2.5 0 0 1 2.5 2.5v5A2.5 2.5 0 0 1 16 14H9l-4 3v-3h-1"/>')
IC_COIN    = svg('<ellipse cx="11" cy="6.4" rx="7" ry="2.8"/><path d="M4 6.4v9.2c0 1.55 3.13 2.8 7 2.8s7-1.25 7-2.8V6.4"/><path d="M4 11c0 1.55 3.13 2.8 7 2.8s7-1.25 7-2.8"/>')
IC_USERS   = svg('<circle cx="8.2" cy="7.4" r="2.7"/><path d="M3 17.2c0-2.9 2.3-4.5 5.2-4.5s5.2 1.6 5.2 4.5"/><path d="M15 6.3a2.7 2.7 0 0 1 0 5.2M16.8 17.2c0-1.8-.5-3.1-1.5-4"/>')
IC_HOME    = svg('<path d="M3.4 9.2 11 3.2l7.6 6v8.2a1.4 1.4 0 0 1-1.4 1.4h-3.4v-5.2H8.2v5.2H4.8a1.4 1.4 0 0 1-1.4-1.4z"/>')
IC_DOCOK   = svg('<path d="M12 2H5.6A1.6 1.6 0 0 0 4 3.6v14.8A1.6 1.6 0 0 0 5.6 20h10.8a1.6 1.6 0 0 0 1.6-1.6V8z"/><path d="M12 2v6h6"/><path d="m7.8 13.6 2 2 4-4"/>')
IC_BAG     = svg('<path d="M4.5 7h13l-1 11.5H5.5z"/><path d="M8 7V5.4A3 3 0 0 1 11 2.4a3 3 0 0 1 3 3V7"/>')
IC_BRIDGE  = svg('<path d="M2.5 12a8.5 8.5 0 0 1 17 0"/><path d="M2.5 12v6M19.5 12v6M8 14.4V18M14 14.4V18M2.5 18h17"/>')
IC_DOC     = svg('<path d="M9 2H4.6A1.6 1.6 0 0 0 3 3.6v12.8A1.6 1.6 0 0 0 4.6 18h6.8a1.6 1.6 0 0 0 1.6-1.6V6z"/><path d="M9 2v4h4"/>', vb="0 0 16 20")

CARET = ('<svg class="caret" viewBox="0 0 10 10" fill="none" stroke="currentColor" '
         'stroke-width="1.6" aria-hidden="true"><path d="m2 4 3 3 3-3"/></svg>')

# --------------------------------------------------------------------------
# sidebar pieces
# --------------------------------------------------------------------------
def qlink(icon, label, href="#main"):
    return ('        <li><a href="%s">\n'
            '          <span class="qlinks__icon" aria-hidden="true">%s</span>\n'
            '          <span class="qlinks__label">%s</span></a></li>' % (href, icon, label))

QUICKLINKS_GROUP = "\n".join([
    qlink(IC_COMPASS, "UBUNTU Strategy", "ubuntu-hub.html"),
    qlink(IC_STAR,    "Success Factors"),
    qlink(IC_BADGE,   "Brand Manifesto", "ubuntu-hub.html#manifesto"),
    qlink(IC_CHAT,    "Ask John", "connect-with-john.html"),
    qlink(IC_COIN,    "Financials"),
    qlink(IC_USERS,   "Culture Page"),
])

QUICKLINKS_REGIONAL = "\n".join([
    qlink(IC_HOME,    "Group", "index.html"),
    qlink(IC_COMPASS, "UBUNTU Strategy", "ubuntu-hub.html"),
    qlink(IC_DOCOK,   "Document Approval"),
    qlink(IC_BAG,     "Merchandise Hub"),
    qlink(IC_STAR,    "Rate My Service"),
    qlink(IC_BRIDGE,  "Daraja"),
])

def widget(title, body, wid=""):
    i = ' id="%s"' % wid if wid else ""
    return ('    <section class="widget"%s>\n      <h2 class="widget__title">%s</h2>\n%s\n    </section>'
            % (i, title, body))

EVENTS = """      <ul class="events">
        <li>
          <span class="events__date"><span class="events__mon">Aug</span><span class="events__day">14</span></span>
          <span class="events__body">
            <a class="events__title" href="ubuntu-hub.html">UBUNTU Hub walkthrough</a>
            <span class="events__when">Fri, Aug 14, 10:00 AM &middot; Teams</span>
          </span>
        </li>
        <li>
          <span class="events__date"><span class="events__mon">Aug</span><span class="events__day">20</span></span>
          <span class="events__body">
            <a class="events__title" href="staff.html#new-staff">New joiners welcome session</a>
            <span class="events__when">Thu, Aug 20, 9:00 AM &middot; Auditorium</span>
          </span>
        </li>
        <li>
          <span class="events__date"><span class="events__mon">Aug</span><span class="events__day">27</span></span>
          <span class="events__body">
            <a class="events__title" href="connect-with-john.html">GMD staff town hall</a>
            <span class="events__when">Thu, Aug 27, 6:30 AM &middot; All markets</span>
          </span>
        </li>
        <li>
          <span class="events__date"><span class="events__mon">Sep</span><span class="events__day">18</span></span>
          <span class="events__body">
            <a class="events__title" href="kenya-hr.html">Wellness week opening</a>
            <span class="events__when">Fri, Sep 18, 8:30 AM &middot; Group HQ</span>
          </span>
        </li>
      </ul>"""

def feed_item(badge, meta, text, tag, seen, reacts, label):
    return """        <article class="feed__item">
          <div class="feed__head">
            <span class="feed__avatar" aria-hidden="true">NS</span>
            <span class="feed__who">
              <span class="feed__author">NCBA Staff Updates</span>
              <span class="feed__meta">%s</span>
            </span>
            <span class="feed__badge">%s</span>
          </div>
          <p class="feed__text">%s</p>
          <a class="feed__tag" href="article.html">%s</a>
          <span class="feed__react" aria-hidden="true">%s</span>
          <span class="feed__views">Seen by %s</span>
          <label class="visually-hidden" for="%s">Comment on this update</label>
          <input class="feed__comment" id="%s" type="text" placeholder="Write a comment">
        </article>""" % (meta, badge, text, tag, reacts, seen, label, label)

# Viva Engage content themes that drive weekly engagement (D-055)
FEED = ('      <div class="feed">\n' + "\n".join([
    feed_item("Monday Blues", "Mon, 8:02 AM",
              "Monday Blues, cured. Post the one small thing getting you through today — a good coffee, a colleague who covered for you, a playlist. Best three get a shout-out on Furahi Day.",
              "#MondayBlues", "&#128578; 64 &nbsp; &#128079; 28", "612", "c1"),
    feed_item("Midweek Fatigue", "Wed, 1:15 PM",
              "Midweek Fatigue is real. Take the 3pm stretch break with us — five minutes, camera optional, no agenda. Drop a &#9749; below if you are joining.",
              "#MidweekFatigue", "&#9749; 87 &nbsp; &#128170; 41", "743", "c2"),
    feed_item("Furahi Day", "Fri, 4:30 PM",
              "Furahi Day! Share your win of the week, however small. Last week Operations closed a customer issue in under an hour and nobody outside the floor heard about it. Let us fix that.",
              "#FurahiDay", "&#127881; 156 &nbsp; &#10084;&#65039; 73", "1,204", "c3"),
]) + "\n      </div>")

def sidebar(kind):
    ql = QUICKLINKS_REGIONAL if kind == "regional" else QUICKLINKS_GROUP
    return "\n".join([
        widget("Quick Links", '      <ul class="qlinks">\n%s\n      </ul>' % ql),
        widget("Upcoming events", EVENTS, wid="events"),
        widget("NCBA Staff Updates", FEED),
    ])

GROUP_SIDEBAR = sidebar("group")
REGIONAL_SIDEBAR = sidebar("regional")

# --------------------------------------------------------------------------
# chrome
# --------------------------------------------------------------------------
NCBA_GROUP_URL = "https://ncbagroup.com/"

STAFF_ITEMS = [("Existing Staff", "staff.html#existing-staff"),
               ("New Staff", "staff.html#new-staff")]
DEPT_ITEMS = [("MCC", "kenya-mcc.html"), ("Strategy", "kenya-strategy.html"),
              ("Human Resources", "kenya-hr.html"), ("UBUNTU Hub", "ubuntu-hub.html")]

def header(active, has_news=True):
    def item(label, href, cls=""):
        c = ' class="is-active"' if cls else ""
        cur = ' aria-current="page"' if cls else ""
        return '      <li><a%s href="%s"%s>%s</a></li>' % (c, href, cur, label)

    def menu(label, root, items, is_active):
        rows = "\n".join('          <li><a href="%s">%s</a></li>' % (h, l) for l, h in items)
        c = ' class="is-active"' if is_active else ""
        cur = ' aria-current="page"' if is_active else ""
        return ('      <li class="has-menu">\n'
                '        <a%s href="%s"%s>%s\n          %s\n        </a>\n'
                '        <ul class="menu">\n%s\n        </ul>\n      </li>'
                % (c, root, cur, label, CARET, rows))

    news = "#news" if has_news else "#main"
    li = [
        item("About NCBA", "#main", active == "About NCBA"),
        menu("Staff", "staff.html", STAFF_ITEMS, active == "Staff"),
        item("Culture &amp; Change", news, active == "Culture & Change"),
        menu("Departments", "kenya-mcc.html", DEPT_ITEMS, active == "Departments"),
        item("UBUNTU Hub", "ubuntu-hub.html", active == "UBUNTU Hub"),
        ('      <li><a class="is-external" href="%s" target="_blank" rel="noopener noreferrer">NCBA Group'
         '<svg class="ext" viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" '
         'aria-hidden="true"><path d="M4.5 2.5H2.5v7h7v-2M7 2.5h2.5V5M9.5 2.5 5.5 6.5"/></svg>'
         '<span class="visually-hidden"> (opens in a new tab)</span></a></li>' % NCBA_GROUP_URL),
    ]
    nav = "\n".join(li)
    return """<a class="skip" href="#main">Skip to main content</a>

<!-- ============================ SUITE BAR ============================ -->
<div class="suitebar">
  <a class="suitebar__waffle" href="#main" aria-label="App launcher">
    <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
      <rect x="1" y="1" width="5" height="5" rx="1"/><rect x="7.5" y="1" width="5" height="5" rx="1"/><rect x="14" y="1" width="5" height="5" rx="1"/>
      <rect x="1" y="7.5" width="5" height="5" rx="1"/><rect x="7.5" y="7.5" width="5" height="5" rx="1"/><rect x="14" y="7.5" width="5" height="5" rx="1"/>
      <rect x="1" y="14" width="5" height="5" rx="1"/><rect x="7.5" y="14" width="5" height="5" rx="1"/><rect x="14" y="14" width="5" height="5" rx="1"/>
    </svg>
  </a>
  <a class="suitebar__app" href="index.html">SharePoint</a>
  <div class="suitebar__search">
    <svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
      <circle cx="8.5" cy="8.5" r="5.5"/><path d="M12.8 12.8 17 17"/>
    </svg>
    <label class="visually-hidden" for="q">Search this site</label>
    <input id="q" type="search" placeholder="Search this site">
  </div>
  <div class="suitebar__right">
    <a class="suitebar__icon" href="#main" aria-label="Notifications">
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
        <path d="M5 8a5 5 0 0 1 10 0c0 4 1.5 5 1.5 5h-13S5 12 5 8Z"/><path d="M8.5 16a1.8 1.8 0 0 0 3 0"/>
      </svg>
    </a>
    <a class="suitebar__icon" href="#main" aria-label="Settings">
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
        <circle cx="10" cy="10" r="2.6"/><path d="M10 2.6v2M10 15.4v2M2.6 10h2M15.4 10h2M4.8 4.8l1.4 1.4M13.8 13.8l1.4 1.4M15.2 4.8l-1.4 1.4M6.2 13.8l-1.4 1.4"/>
      </svg>
    </a>
    <a class="suitebar__icon" href="#help" aria-label="Help">
      <svg width="18" height="18" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
        <circle cx="10" cy="10" r="7.4"/><path d="M8 7.8a2.1 2.1 0 1 1 2.8 2c-.6.3-.8.8-.8 1.4v.4"/><circle cx="10" cy="14.4" r=".8" fill="currentColor" stroke="none"/>
      </svg>
    </a>
    <span class="suitebar__avatar" aria-hidden="true">NK</span>
  </div>
</div>

<!-- ============================ SITE HEADER ============================ -->
<header class="sitehead">
  <a class="sitehead__brand" href="index.html">
    <img src="assets/img/ncba-logo-white.png" alt="NCBA" width="71" height="26">
    <span class="sitehead__title">UBUNTU Hub</span>
  </a>
  <nav class="sitehead__nav" aria-label="Main">
    <ul>
%s
    </ul>
  </nav>
</header>""" % nav


def subnav_depts(active):
    """Department strip on the four department pages."""
    rows = []
    for lbl, href in DEPT_ITEMS:
        cls = ' class="is-active"' if lbl == active else ""
        cur = ' aria-current="page"' if lbl == active else ""
        rows.append('      <div class="subnav__item"><a%s href="%s"%s>%s</a></div>'
                    % (cls, href, cur, lbl))
    return ('\n<nav class="subnav" aria-label="Departments">\n'
            '  <div class="subnav__inner">\n%s\n  </div>\n</nav>' % "\n".join(rows))


def subnav_region(active):
    """Country strip retained on region-kenya.html."""
    countries = ["Kenya", "Uganda", "Tanzania", "Rwanda"]
    rows = []
    for c in countries:
        cls = ' class="is-active"' if c == active else ""
        cur = ' aria-current="page"' if c == active else ""
        sub = "\n".join('          <li><a href="%s">%s</a></li>' % (h, l) for l, h in DEPT_ITEMS)
        rows.append('      <div class="subnav__item has-submenu">\n'
                    '        <a%s href="region-kenya.html"%s>%s %s</a>\n'
                    '        <ul class="submenu">\n%s\n        </ul>\n      </div>'
                    % (cls, cur, c, CARET, sub))
    return ('\n<nav class="subnav" aria-label="Regions">\n'
            '  <div class="subnav__inner">\n%s\n  </div>\n</nav>' % "\n".join(rows))


def hero(img, alt, title, sub, flag=False):
    """Full-bleed banner. No title bar: the artwork carries its own headline."""
    fl = '  <div class="hero__flag"></div>\n' if flag else ""
    return """
<!-- ============================ HERO (full bleed) ============================ -->
<section class="hero">
  <img class="hero__img" src="assets/img/hero/%s" alt="%s" width="1920" height="310">
%s  <h1 class="visually-hidden">%s</h1>
  <p class="visually-hidden">%s</p>
</section>""" % (img, alt, fl, title, sub)


def hero_slider(slides):
    """Home-page hero rotator. No HTML text -- the artwork carries it (D-053).
    Driven by the shared [data-carousel] script."""
    figs = "\n".join(
        '      <figure class="heroslider__slide">\n'
        '        <img class="hero__img" src="assets/img/hero/%s" alt="%s" width="1920" height="310">\n'
        '      </figure>' % (img, alt) for img, alt in slides)
    return """
<!-- ============================ HERO SLIDER (full bleed) ============================ -->
<section class="hero heroslider" data-carousel aria-roledescription="carousel" aria-label="NCBA UBUNTU Hub banners">
  <div class="heroslider__viewport">
    <div class="heroslider__track" data-track>
%s
    </div>
    <button class="heroslider__btn heroslider__btn--prev" data-prev type="button" aria-label="Previous banner">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m10 3-5 5 5 5"/></svg>
    </button>
    <button class="heroslider__btn heroslider__btn--next" data-next type="button" aria-label="Next banner">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>
    </button>
    <div class="heroslider__dots" data-dots></div>
  </div>
  <h1 class="visually-hidden">Welcome to the NCBA UBUNTU Hub</h1>
</section>""" % figs


HELP = """    <section class="section" id="help">
      <div class="section__head">
        <h2>We&rsquo;re here to help</h2>
      </div>
      <div class="help__grid">

        <div class="help__card">
          <span class="help__icon" aria-hidden="true">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="8" cy="5" r="2.6"/><path d="M2.6 14c0-3 2.4-4.6 5.4-4.6s5.4 1.6 5.4 4.6"/></svg>
          </span>
          <span class="help__team">Ask HR</span>
          <p class="help__addr">askhr@ncbagroup.com</p>
        </div>

        <div class="help__card">
          <span class="help__icon" aria-hidden="true">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="2" y="3" width="12" height="9" rx="1.4"/><path d="M5.5 14h5"/></svg>
          </span>
          <span class="help__team">UBUNTU Hub support</span>
          <p class="help__addr">ubuntuhub@ncbagroup.com</p>
        </div>

        <div class="help__card">
          <span class="help__icon" aria-hidden="true">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M3 5.5A2.5 2.5 0 0 1 5.5 3h5A2.5 2.5 0 0 1 13 5.5v3A2.5 2.5 0 0 1 10.5 11H7l-3 2.2V11h-.5"/></svg>
          </span>
          <span class="help__team">Service desk</span>
          <p class="help__addr">servicedesk@ncbagroup.com</p>
        </div>

        <div class="help__card">
          <span class="help__icon" aria-hidden="true">
            <svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M2.6 6.5 8 3l5.4 3.5L8 10 2.6 6.5Z"/><path d="M4.6 8v3.2c0 .8 1.5 1.6 3.4 1.6s3.4-.8 3.4-1.6V8"/></svg>
          </span>
          <span class="help__team">Marketing &amp; Communications</span>
          <p class="help__addr">mcc@ncbagroup.com</p>
        </div>

      </div>
    </section>"""

FOOTER = """
<!-- ============================ FOOTER ============================ -->
<footer class="sitefoot">
  <div class="sitefoot__inner">
    <a class="sitefoot__brand" href="index.html">
      <img src="assets/img/ncba-logo-white.png" alt="NCBA" width="66" height="24">
    </a>
    <nav class="sitefoot__social" aria-label="Social">
      <a href="#main">LinkedIn</a>
      <a href="#main">Facebook</a>
      <a href="#main">Instagram</a>
    </nav>
  </div>
</footer>"""


def loop_item(img, alt, chip, title, excerpt, meta, video=False):
    v = " loop__item--video" if video else ""
    play = ('\n            <span class="media__play" aria-hidden="true"></span>' if video else "")
    return """        <article class="loop__item%s">
          <a class="loop__media" href="article.html">
            <img class="loop__img" src="assets/img/loop/%s" alt="%s" width="320" height="180">%s
          </a>
          <div class="loop__body">
            <span class="chip">%s</span>
            <h3 class="loop__title"><a href="article.html">%s</a></h3>
            <p class="loop__excerpt">%s</p>
            <a class="loop__more" href="article.html">Read article <span aria-hidden="true">&rarr;</span></a>
            <p class="loop__meta">%s</p>
          </div>
        </article>""" % (v, img, alt, play, chip, title, excerpt, meta)


def news_section(items, heading="News"):
    body = "\n\n".join(loop_item(*i) if isinstance(i, tuple) else i for i in items)
    return """    <section class="section" id="news">
      <div class="section__head">
        <h2>%s</h2>
        <a class="section__all" href="article.html">See all</a>
      </div>
      <div class="loop">

%s

      </div>
    </section>""" % (heading, body)


def page(fname, title, active, hero_html, main_html, sidebar_html, sub=None,
         script="", rail_label="Group resources"):
    scr = "\n\n" + script if script else ""
    has_news = 'id="news"' in main_html
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<link rel="stylesheet" href="assets/css/ncba.css">
</head>
<body>

%s
%s%s

<!-- ============================ PAGE ============================ -->
<div class="canvas">
  <div class="grid">

  <!-- ------------------------- MAIN COLUMN ------------------------- -->
  <main class="col-main" id="main">

%s

  </main>

  <!-- ------------------------- RIGHT RAIL ------------------------- -->
  <aside class="col-rail" aria-label="%s">

%s

  </aside>
  </div>
</div>
%s%s

</body>
</html>
""" % (title, header(active, has_news), sub or "", hero_html, main_html,
       rail_label, sidebar_html, FOOTER, scr)
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote %s  (%s bytes)" % (fname, format(len(html), ",")))
