#!/usr/bin/env python3
"""Page content for the NCBA UBUNTU Hub mockup. Run: python3 pages.py"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen import *   # noqa

# One script drives every rotator on the page -- hero slider and section
# carousels alike. The only JavaScript in the project (D-054).
CAROUSEL_SCRIPT = """<script>
/* Minimal vanilla carousel. Binds to every [data-carousel] on the page. */
(function () {
  Array.prototype.forEach.call(document.querySelectorAll('[data-carousel]'), function (root) {
    var track = root.querySelector('[data-track]');
    if (!track) return;
    var slides = Array.prototype.slice.call(track.children);
    var dots = root.querySelector('[data-dots]');
    var cap = root.querySelector('[data-cap]');
    var i = 0;

    slides.forEach(function (s, n) {
      if (!dots) return;
      var b = document.createElement('button');
      b.className = 'carousel__dot';
      b.type = 'button';
      b.setAttribute('aria-label', 'Go to slide ' + (n + 1));
      b.addEventListener('click', function () { go(n); });
      dots.appendChild(b);
    });

    function go(n) {
      i = (n + slides.length) % slides.length;
      track.style.transform = 'translateX(' + (-100 * i) + '%)';
      if (cap) {
        cap.querySelector('h3').textContent = slides[i].getAttribute('data-title') || '';
        cap.querySelector('p').textContent = slides[i].getAttribute('data-text') || '';
      }
      slides.forEach(function (s, k) { s.setAttribute('aria-hidden', k !== i); });
      if (dots) Array.prototype.forEach.call(dots.children, function (d, k) {
        d.classList.toggle('is-current', k === i);
      });
    }

    var p = root.querySelector('[data-prev]'), nx = root.querySelector('[data-next]');
    if (p) p.addEventListener('click', function () { go(i - 1); });
    if (nx) nx.addEventListener('click', function () { go(i + 1); });
    go(0);
  });
})();
</script>"""


def slide(img, alt, t, x):
    return ('            <figure class="carousel__slide" data-title="%s" data-text="%s">\n'
            '              <img class="media__img" src="assets/img/media/%s" alt="%s" width="940" height="529">\n'
            '            </figure>' % (t, x, img, alt))


def carousel(slides, heading=None, label="NCBA highlights"):
    h = ('      <div class="section__head">\n        <h2>%s</h2>\n      </div>\n' % heading) if heading else ""
    return """    <section class="section">
%s      <div class="carousel" data-carousel aria-roledescription="carousel" aria-label="%s">
        <div class="carousel__viewport">
          <div class="carousel__track" data-track>

%s

          </div>
          <button class="carousel__btn carousel__btn--prev" data-prev type="button" aria-label="Previous slide">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m10 3-5 5 5 5"/></svg>
          </button>
          <button class="carousel__btn carousel__btn--next" data-next type="button" aria-label="Next slide">
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 3 5 5-5 5"/></svg>
          </button>
        </div>
        <div class="carousel__cap" data-cap aria-live="polite">
          <h3></h3>
          <p></p>
        </div>
        <div class="carousel__dots" data-dots></div>
      </div>
    </section>""" % (h, label, "\n\n".join(slides))


def video(img, alt, cap, heading=None):
    h = ('      <div class="section__head">\n        <h2>%s</h2>\n      </div>\n' % heading) if heading else ""
    return """    <section class="section">
%s      <a class="media media--video" href="article.html">
        <img class="media__img" src="assets/img/media/%s" alt="%s" width="940" height="529">
        <span class="media__play" aria-hidden="true"></span>
      </a>
      <p class="media__cap">%s</p>
    </section>""" % (h, img, alt, cap)


def twoup(left, right, heading=None):
    """Two media tiles side by side in the main column, each a video poster."""
    def tile(img, alt, title, cap):
        return """        <div class="twoup__col">
          <h3 class="twoup__title">%s</h3>
          <a class="media media--video" href="article.html">
            <img class="media__img" src="assets/img/media/%s" alt="%s" width="940" height="529">
            <span class="media__play" aria-hidden="true"></span>
          </a>
          <p class="media__cap">%s</p>
        </div>""" % (title, img, alt, cap)
    h = ('      <div class="section__head">\n        <h2>%s</h2>\n      </div>\n' % heading) if heading else ""
    return """    <section class="section">
%s      <div class="twoup">
%s
%s
      </div>
    </section>""" % (h, tile(*left), tile(*right))


def banner(img, alt, cap, heading=None):
    h = ('      <div class="section__head">\n        <h2>%s</h2>\n      </div>\n' % heading) if heading else ""
    return """    <section class="section">
%s      <span class="media">
        <img class="media__img" src="assets/img/media/%s" alt="%s" width="940" height="529">
      </span>
      <p class="media__cap">%s</p>
    </section>""" % (h, img, alt, cap)


def feature(img, alt, heading, paras):
    p = "\n".join("      <p>%s</p>" % x for x in paras)
    return """    <section class="section">
      <div class="section__head">
        <h2>%s</h2>
      </div>
      <span class="media">
        <img class="media__img" src="assets/img/media/%s" alt="%s" width="940" height="529">
      </span>
      <div style="margin-top:16px">
%s
      </div>
    </section>""" % (heading, img, alt, p)


def doctiles(heading, items, wid=""):
    i = ' id="%s"' % wid if wid else ""
    rows = "\n".join('        <a class="doctile" href="#main"><span class="doctile__icon" aria-hidden="true">%s</span>%s</a>'
                     % (IC_DOC, x) for x in items)
    return """    <section class="section"%s>
      <div class="section__head">
        <h2>%s</h2>
      </div>
      <div class="doctiles">
%s
      </div>
    </section>""" % (i, heading, rows)


def intro(eyebrow, heading, paras, wid=""):
    i = ' id="%s"' % wid if wid else ""
    p = "\n".join('      <p class="lede">%s</p>' % x for x in paras)
    return """    <section class="section"%s>
      <p class="eyebrow">%s</p>
      <h2 style="margin-bottom:12px">%s</h2>
%s
    </section>""" % (i, eyebrow, heading, p)


def prose(heading, paras, wid=""):
    i = ' id="%s"' % wid if wid else ""
    p = "\n".join("      <p>%s</p>" % x for x in paras)
    return """    <section class="section"%s>
      <div class="section__head">
        <h2>%s</h2>
      </div>
%s
    </section>""" % (i, heading, p)


ASKBOX = """    <section class="section">
      <div class="askbox">
        <div class="askbox__head">
          <span class="askbox__avatar" aria-hidden="true">NK</span>
          <span class="askbox__who">
            <span class="askbox__title">Ask John a question</span>
            <span class="askbox__meta">Goes to the Office of the Group Managing Director</span>
          </span>
        </div>
        <label class="visually-hidden" for="askq">Your question for the GMD</label>
        <textarea class="askbox__input" id="askq" rows="3"
                  placeholder="What would you like to ask? A rough idea is as welcome as a polished one."></textarea>
        <div class="askbox__foot">
          <label class="askbox__check">
            <input type="checkbox" id="askanon"> Ask anonymously
          </label>
          <span class="askbox__actions">
            <button class="btn btn--secondary" type="button">Save draft</button>
            <button class="btn btn--primary" type="button">Submit question</button>
          </span>
        </div>
        <p class="askbox__note">Questions are read by the GMD's office. Recurring themes are answered on the record at the next fireside chat.</p>
      </div>
    </section>"""


# ==========================================================================
# 1. index.html
# ==========================================================================
page("index.html", "NCBA Group | UBUNTU Hub", "About NCBA",
     hero_slider([("hero-slide-1.jpg", "Welcome to the refreshed NCBA UBUNTU Hub"),
                  ("hero-slide-2.jpg", "NCBA colleagues at the UBUNTU Hub launch"),
                  ("hero-slide-3.jpg", "Moments from across NCBA Group"),
                  ("hero-slide-4.jpg", "Welcome to the refreshed NCBA UBUNTU Hub")]),
     "\n\n".join([
        twoup(("gmd-quote.jpg", "John Gachora, Group Managing Director, on the UBUNTU Hub",
               "A message from the GMD",
               "John Gachora, Group Managing Director. 5 min 20 sec."),
              ("monica-quote.jpg", "Monicah Kihia, Group Director HR and Culture, on the UBUNTU Hub",
               "A message from HR",
               "Monicah Kihia, Group Director, HR and Culture. 4 min 05 sec."),
              "Messages from leadership"),
        video("ubuntu-spirit.jpg", "Play the 2026-2030 UBUNTU Strategy film",
              "The 2026-2030 UBUNTU Strategy - giving our people the tools, services and experiences that match the scale of their vision. 3 min 40 sec.",
              "The UBUNTU Spirit"),
        carousel([
            slide("upd-friday.jpg", "Go For It Friday", "Go For It Friday",
                  "Every great day starts with someone like you. Whether it is teamwork, customer love, or just a vibe that made someone's day better - let us know on Conversations."),
            slide("upd-webinars.jpg", "Upcoming webinars", "Upcoming webinars",
                  "Short sessions you can join from your desk. Bookable through the events calendar, recorded for anyone who cannot make the live slot."),
            slide("upd-hrchat.jpg", "Chat with HR", "Chat with HR",
                  "Open desk hours with the HR team. Bring a question about leave, pay, development or anything you have been meaning to ask."),
            slide("upd-events.jpg", "Check out last week's events", "Check out last week's events",
                  "Photographs from across the Group - what we got up to, who was there, and what is coming next."),
        ], "What's happening", "NCBA updates"),
        news_section([
            ("loop-teaser.jpg", "The refreshed NCBA UBUNTU Hub", "#UBUNTUHub",
             "The UBUNTU Hub is live &mdash; here is what changed",
             "A cleaner home page, a single news feed across every market, and quick links that actually go where you expect. Here is a short tour of what moved and why.",
             "Marketing, Communications &amp; Citizenship &middot; 4 August 2026"),
            ("loop-gogetters.jpg", "Go Getters, this is your space", "#GoGetters",
             "Go Getters: your space to share and shine",
             "Big wins and small joys both count. Colleagues across the Group are posting the everyday moments that make the work worth doing.",
             "Culture &amp; Change &middot; 1 August 2026"),
            ("loop-fireside.jpg", "CEO fireside chats", "#AskJohn",
             "Fireside chats with the GMD return this quarter",
             "Bring a question, a rough idea, or a frustration you think nobody has noticed. Sessions run across all markets and every question submitted gets read.",
             "Office of the GMD &middot; 29 July 2026"),
            ("loop-halloffame.jpg", "Hall of Fame", "#HallOfFame",
             "Hall of Fame: the teams behind the quarter",
             "Recognition that names the people, not just the project. See who is accomplishing their goals across our markets.",
             "HR &amp; Culture &middot; 24 July 2026"),
            ("loop-tea.jpg", "Tea with Group", "#TeaWithGroup",
             "Tea with Group: what is brewing across our markets",
             "A short monthly round-up of what teams are shipping, testing and arguing about - written by the people doing the work.",
             "Internal Communications &middot; 18 July 2026"),
        ]),
        HELP,
     ]), GROUP_SIDEBAR, script=CAROUSEL_SCRIPT)

# ==========================================================================
# 2. ubuntu-hub.html
# ==========================================================================
page("ubuntu-hub.html", "UBUNTU Hub | NCBA UBUNTU Hub", "UBUNTU Hub",
     hero("hero-ubuntu.jpg", "Welcome to the new NCBA UBUNTU Hub",
          "The UBUNTU Hub", "Our strategy, our manifesto and the spirit behind both."),
     "\n\n".join([
        intro("UBUNTU &middot; 2026&ndash;2030",
              "One spirit, one strategy, one hub",
              ["UBUNTU is the idea that we are who we are because of each other. It is not a campaign line - it is the operating assumption behind how we serve customers and how we treat colleagues.",
               "This page brings together the strategy, the manifesto and the people explaining both."]),
        video("ubuntu-spirit.jpg", "Play the UBUNTU Spirit film",
              "The UBUNTU Spirit - giving our people the tools, services and experiences that match the scale of their vision. 3 min 40 sec.",
              "The UBUNTU Spirit"),
        prose("The UBUNTU Manifesto", [
            "<strong>We are because you are.</strong> Every account, every approval, every awkward conversation handled well - that is the bank, not the logo.",
            "<strong>We show up.</strong> For customers who are having a bad week, and for colleagues carrying more than they let on. Showing up is the whole job on most days.",
            "<strong>We go for it.</strong> Careful is not the same as slow. We would rather try something, learn quickly and say so than protect a position nobody is defending.",
            "<strong>We make room.</strong> The best idea in the room is often held by the person least likely to volunteer it. Making room for it is everyone's work, not just the chair's.",
            "<strong>We finish together.</strong> Nobody's target is met until the handover lands. If it is not finished for the customer, it is not finished."],
              wid="manifesto"),
        banner("ubuntu-spirit.jpg",
               "The 2026-2030 UBUNTU Strategy on a page",
               "The 2026-2030 UBUNTU Strategy, on a page.",
               "Strategy on a page"),
        feature("feature-louisa.jpg", "Louisa Wandabwa, Group Director, on translating strategy into momentum",
                "Louisa on turning ambition into momentum",
                ["The strategy function sits between the ambition and the delivery. Its job is to keep the two honest about each other - to translate a board-level intention into work a team can pick up on Monday, and to carry the reality of delivery back the other way.",
                 "Each pillar has a named owner, a small set of measures, and a quarterly checkpoint that is published internally rather than presented once and filed."]),
        doctiles("UBUNTU documents", [
            "Strategy on a page (PDF)", "The UBUNTU Manifesto", "Pillar owners and measures",
            "Quarterly checkpoint pack", "Brand and tone of voice", "Glossary of terms"]),
        news_section([
            ("loop-strategy.jpg", "2026-2030 UBUNTU Strategy", "#UBUNTUStrategy",
             "The 2026&ndash;2030 UBUNTU Strategy, explained",
             "How the pillars were chosen, what was deliberately left out, and the measures that will tell us early if something is not working.",
             "Strategy &middot; 3 August 2026"),
            ("loop-louisa.jpg", "Strategy Mission key visual", "#Strategy",
             "Translating strategic ambition into momentum",
             "The checkpoint is not a status report. It is the moment to say what has changed about the plan since the last one, and why.",
             "Strategy &middot; 28 July 2026"),
            ("loop-magic.jpg", "You make the magic happen", "#MakeItHappen",
             "Where your team fits into the pillars",
             "A short guide to reading the strategy from the bottom up - starting from the work you already do rather than from the diagram.",
             "Strategy &middot; 21 July 2026"),
            ("loop-gogetters.jpg", "Go Getters", "#GoGetters",
             "The people carrying UBUNTU day to day",
             "Recognition for the work that shifted a measure rather than the work that produced the most slides.",
             "Culture &amp; Change &middot; 14 July 2026"),
            ("loop-live.jpg", "The UBUNTU Hub is live", "#UBUNTUHub",
             "Why the Hub and the strategy launched together",
             "A platform is only worth building if it changes what people can find and say. Here is the thinking behind launching both at once.",
             "Internal Communications &middot; 7 July 2026"),
        ], "UBUNTU news"),
        HELP,
     ]), GROUP_SIDEBAR, sub=subnav_depts("UBUNTU Hub"))

# ==========================================================================
# 3. staff.html
# ==========================================================================
page("staff.html", "Staff | NCBA UBUNTU Hub", "Staff",
     hero("hero-staff.jpg", "NCBA staff", "Staff",
          "Everything you need, whether you joined this week or a decade ago."),
     "\n\n".join([
        intro("Staff", "All you need to know",
              ["Two routes in. If you have been here a while, start with Existing Staff for the things you use often. If you are new, start with New Staff and work down the list in order.",
               "Anything personal or sensitive goes to the HR team directly rather than a shared channel."]),
        intro("Section 1", "Existing Staff",
              ["The things you actually use - leave, pay, benefits, development and the forms nobody enjoys filling in. Most questions are answered by the documents below."],
              wid="existing-staff"),
        doctiles("Existing staff: all you need to know", [
            "Leave and time off", "Payslips and tax", "Medical cover and claims",
            "Pension scheme", "Performance and goals", "Learning and development",
            "Internal job opportunities", "Staff loans and benefits", "HR policies A&ndash;Z"]),
        intro("Section 2", "New Staff",
              ["Your first weeks, in the order they actually happen. Work down this list and you will have covered everything expected of you in month one."],
              wid="new-staff"),
        doctiles("New staff: all you need to know", [
            "Before day one: what to bring", "Getting your laptop and access",
            "Your first week checklist", "Meet your buddy and your team",
            "Mandatory training and compliance", "Setting your first goals",
            "Benefits enrolment", "Who to ask about what", "Probation: what to expect"]),
        news_section([
            ("loop-welcome.jpg", "Welcome to NCBA", "#NewStaff",
             "Your first ninety days at NCBA",
             "What good looks like early on, from colleagues who joined in the last year and remember it clearly.",
             "HR &amp; Culture &middot; 5 August 2026"),
            ("loop-kpis.jpg", "Career growth", "#CareerGrowth",
             "Ready for your next move? Internal opportunities",
             "How internal mobility works here, what managers are asked to do when a colleague applies, and the timeline you can expect.",
             "HR &amp; Culture &middot; 30 July 2026"),
            ("loop-tea.jpg", "Wellness", "#Wellness",
             "Wellness week: what is on and how to join",
             "Sessions covering physical health, financial wellbeing and the parts of mental health people find hardest to raise.",
             "HR &amp; Culture &middot; 22 July 2026"),
            ("loop-halloffame.jpg", "Hall of Fame", "#HallOfFame",
             "Recognition: how nominations actually work",
             "Who can nominate, what the panel looks for, and why naming people beats naming projects.",
             "HR &amp; Culture &middot; 15 July 2026"),
            ("loop-social.jpg", "Staff updates", "#StaffUpdates",
             "Getting the most out of Staff Updates",
             "A practical guide to posting well - what is worth sharing internally and what belongs in a team channel.",
             "Internal Communications &middot; 8 July 2026"),
        ], "Staff news"),
        HELP,
     ]), GROUP_SIDEBAR)

# ==========================================================================
# 4. connect-with-john.html
# ==========================================================================
page("connect-with-john.html", "Connect with John | NCBA UBUNTU Hub", "",
     hero("hero-john.jpg", "John Gachora, Group Managing Director",
          "Connect with John",
          "Fireside chats, town halls and a standing invitation to ask the question you actually want answered."),
     "\n\n".join([
        intro("Office of the Group Managing Director",
              "Ask the question you actually want answered",
              ["Every session below is recorded and every question submitted is read. If a question comes up often enough, it gets answered on the record rather than in a corridor.",
               "Bring a rough idea as readily as a polished one. The most useful sessions have started from someone saying they did not understand why we do something a particular way."]),
        ASKBOX,
        news_section([
            ("loop-fireside.jpg", "GMD fireside chat", "#AskJohn",
             "Fireside Chat: what is on your mind this quarter",
             "An open session with no fixed agenda. Submit a question in advance or raise it live - the floor genuinely opens.",
             "Office of the GMD &middot; 31 July 2026", True),
            ("loop-branch-gmd.jpg", "From branch stories to chats with the GMD", "#AskJohn",
             "From branch stories to chats with the GMD",
             "Colleagues in branches see things head office does not. This series brings those observations directly into the conversation.",
             "Office of the GMD &middot; 25 July 2026", True),
            ("loop-gmd-desk.jpg", "The GMD at his desk", "#Leadership",
             "A short update on how we are tracking",
             "A plain-language walk through where we are against the plan, what has moved, and what has not moved as fast as we hoped.",
             "Office of the GMD &middot; 17 July 2026", True),
            ("loop-john.jpg", "GMD Mission key visual", "#UBUNTUSpirit",
             "Ignite Belief: what the mission means day to day",
             "Strategy documents are easy to nod along to. This session works through what the mission changes about ordinary decisions.",
             "Office of the GMD &middot; 9 July 2026", True),
            ("loop-live.jpg", "The UBUNTU Hub is live", "#UBUNTUHub",
             "Why we rebuilt the Hub, and what comes next",
             "The thinking behind the new intranet, the things deliberately left out of this release, and how to tell us what is missing.",
             "Office of the GMD &middot; 2 July 2026", True),
        ], "Sessions and recordings"),
        HELP,
     ]), GROUP_SIDEBAR)

# ==========================================================================
# 5. region-kenya.html
# ==========================================================================
page("region-kenya.html", "Kenya | NCBA UBUNTU Hub", "",
     hero("hero-kenya.jpg", "NCBA Kenya", "Karibu Kenya",
          "News, services and teams across NCBA Bank Kenya.", flag=True),
     "\n\n".join([
        video("video-gmd.jpg", "Play the GMD message to Kenya",
              "A message to colleagues across Kenya from the Group Managing Director. 4 min 12 sec.",
              "A message from the GMD"),
        banner("monica-quote.jpg",
               "Monicah Kihia, Group Director HR and Culture, on what the UBUNTU Hub is for",
               "Monicah Kihia, Group Director, HR and Culture."),
        news_section([
            ("loop-welcome.jpg", "Welcome to the new NCBA UBUNTU Hub", "#UBUNTUHub",
             "Kenya moves onto the new UBUNTU Hub",
             "Kenya is the first market fully migrated. Here is what changed for day-to-day tasks, and where the things you used to bookmark now live.",
             "Internal Communications &middot; 5 August 2026"),
            ("loop-magic.jpg", "You make the magic happen", "#MakeItHappen",
             "You make the magic happen: stories from the branches",
             "Six colleagues describe a moment this quarter when the answer was not in the process notes and they worked it out anyway.",
             "Culture &amp; Change &middot; 30 July 2026"),
            ("loop-kpis.jpg", "From KPIs to LOLs", "#NCBACulture",
             "From KPIs to LOLs: the lighter side of the quarter",
             "Targets matter, and so does the fact that people enjoy working together. A short round-up of the moments that made the floor laugh.",
             "Culture &amp; Change &middot; 22 July 2026"),
            ("loop-social.jpg", "Social media on the Hub", "#SocialMedia",
             "Sharing your day-to-day on the Hub",
             "A practical guide to posting well - what is worth sharing internally, what belongs in a team channel, and the handful of things to keep off both.",
             "Marketing, Communications &amp; Citizenship &middot; 15 July 2026"),
            ("loop-hub-live.jpg", "The Hub is live", "#UBUNTUHub",
             "Guess what just happened: the Hub is live in Kenya",
             "The switch-over is complete. Old links redirect for ninety days, and the support desk is staffed for the first two weeks of the transition.",
             "Service Desk &middot; 8 July 2026"),
        ], "News updates"),
        HELP,
     ]), REGIONAL_SIDEBAR, sub=subnav_region("Kenya"), rail_label="Kenya resources")

# ==========================================================================
# 6. kenya-mcc.html
# ==========================================================================
page("kenya-mcc.html", "Marketing, Communications &amp; Citizenship | NCBA UBUNTU Hub", "Departments",
     hero("hero-mcc.jpg", "Marketing, Communications and Citizenship",
          "Marketing, Communications &amp; Citizenship",
          "We shape how the world sees and feels NCBA."),
     "\n\n".join([
        intro("Department", "Not just e-shots and fliers",
              ["MCC works on the brand stories that connect NCBA to its customers - and on the far less glamorous work of keeping one voice across markets, channels and a lot of competing deadlines.",
               "If you need creative support, start with the request form rather than a direct message. It routes to whoever is actually free."]),
        feature("feature-nelly.jpg", "Nelly Wainaina, Group Director, MCC",
                "MCC Mission",
                ["The brand is not the logo. It is the accumulated impression left by every interaction someone has with us - a branch visit, an app screen, a letter about a fee. Marketing owns some of those and influences the rest.",
                 "Our job is to make the NCBA brand a regional powerhouse by being consistent where it matters and interesting where it counts."]),
        doctiles("MCC documents", [
            "Brand guidelines", "Logo and asset library", "Tone of voice guide",
            "Creative request form", "Event and sponsorship policy", "Presentation template",
            "Photography guidelines", "Social media standards", "Citizenship programme"]),
        news_section([
            ("loop-nelly.jpg", "MCC Mission key visual", "#MCC",
             "Iconize the NCBA brand as a regional powerhouse",
             "What consistency actually requires across five markets, and the small number of things worth being strict about.",
             "MCC &middot; 2 August 2026"),
            ("loop-mcc.jpg", "MCC Go Getters", "#GoForIt",
             "MCC Go Getters: turbo charging the brand",
             "Behind the campaign that ran across branches and channels this quarter, including what we would do differently next time.",
             "MCC &middot; 27 July 2026"),
            ("loop-magic.jpg", "You make the magic happen", "#MakeItHappen",
             "Embedding customer obsession in the work",
             "Customer obsession is easy to say. This is the practical version - the questions to ask before a campaign goes out.",
             "MCC &middot; 20 July 2026"),
            ("loop-social.jpg", "Social media", "#SocialMedia",
             "The social media standards, in plain language",
             "What you can post as an NCBA colleague, what needs a review, and who to ask when it is genuinely unclear.",
             "MCC &middot; 13 July 2026"),
            ("loop-tea.jpg", "Tea with Group", "#NCBACulture",
             "MCC visits HR: a small tradition worth keeping",
             "The team surprised HR with an afternoon of appreciation. A short piece on why these things matter more than they look.",
             "MCC &middot; 6 July 2026"),
        ], "MCC news"),
        HELP,
     ]), GROUP_SIDEBAR, sub=subnav_depts("MCC"))

# ==========================================================================
# 7. kenya-strategy.html
# ==========================================================================
page("kenya-strategy.html", "Strategy | NCBA UBUNTU Hub", "Departments",
     hero("hero-strategy.jpg", "NCBA strategy", "Strategy",
          "Translating strategic ambition into enterprise-wide momentum."),
     "\n\n".join([
        intro("Department", "Turning ambition into something a team can act on",
              ["A strategy only works if someone can tell you what it changes about their week. These pages set out the pillars, who owns each one, and how progress is actually measured.",
               "If your team's work does not map onto any of it, that is worth a conversation - it usually means either the plan or the map is wrong."]),
        feature("feature-louisa.jpg", "Louisa Wandabwa, Group Director, Investment Banking",
                "Strategy Mission",
                ["The strategy function sits between the ambition and the delivery. Its job is to keep the two honest about each other - to translate a board-level intention into work a team can pick up on Monday, and to carry the reality of delivery back the other way.",
                 "Each pillar has a named owner, a small set of measures, and a quarterly checkpoint that is published internally rather than presented once and filed."]),
        doctiles("Strategy documents", [
            "Strategy on a page", "Pillar owners and measures", "Quarterly checkpoint pack",
            "Planning calendar", "Investment case template", "Glossary of terms"]),
        news_section([
            ("loop-louisa.jpg", "Strategy Mission key visual", "#Strategy",
             "Translating strategic ambition into momentum",
             "How the pillars were chosen, what was deliberately left out, and the measures that will tell us early if something is not working.",
             "Strategy &middot; 3 August 2026"),
            ("loop-strategy.jpg", "2026-2030 UBUNTU Strategy", "#UBUNTUStrategy",
             "Making it happen: from plan to quarterly checkpoint",
             "The checkpoint is not a status report. It is the moment to say what has changed about the plan since the last one, and why.",
             "Strategy &middot; 28 July 2026"),
            ("loop-gogetters.jpg", "Go Getters", "#GoGetters",
             "Where your team fits into the pillars",
             "A short guide to reading the strategy from the bottom up - starting from the work you already do rather than from the diagram.",
             "Strategy &middot; 21 July 2026"),
            ("loop-teaser.jpg", "Coming soon", "#Strategy",
             "The planning calendar for the year ahead",
             "Key dates for the planning cycle, when input is genuinely open, and when decisions have already been taken.",
             "Strategy &middot; 14 July 2026"),
            ("loop-halloffame.jpg", "Hall of Fame", "#HallOfFame",
             "Teams that moved a pillar this quarter",
             "Recognition for the work that shifted a measure rather than the work that produced the most slides.",
             "Strategy &middot; 7 July 2026"),
        ], "Strategy news"),
        video("video-strategy.jpg", "Play the UBUNTU strategy film",
              "Giving our UBUNTU the tools, services and experiences that match the scale of their vision. 2 min 55 sec.",
              "The strategy in two minutes"),
        HELP,
     ]), GROUP_SIDEBAR, sub=subnav_depts("Strategy"))

# ==========================================================================
# 8. kenya-hr.html
# ==========================================================================
page("kenya-hr.html", "Human Resources | NCBA UBUNTU Hub", "Departments",
     hero("hero-hr.jpg", "Human Resources", "Human Resources",
          "Supercharging HR as the orchestrator of the organisation of the future."),
     "\n\n".join([
        intro("Department", "The practical side of working here",
              ["Leave, pay, benefits, development, and the forms nobody enjoys filling in. Most of what people need from HR is answered on this page or in the documents below.",
               "For anything personal or sensitive, contact the team directly rather than posting in a shared channel."]),
        carousel([
            slide("hr-lastweek.jpg", "What happened last week", "What happened last week",
                  "Photographs and short write-ups from the sessions, socials and team moments across the Group over the past week."),
            slide("hr-august.jpg", "Share your best August moments", "Share your best August moments",
                  "Post a photo from your month - a team lunch, a win, a customer thank-you. The best ones run on the Hub and in the next all-staff mailer."),
            slide("hr-gogetters.jpg", "Go Getters, this is your space", "Go Getters, this is your space",
                  "Big wins. Small joys. Everyday moments that matter. This is your space to share and shine, where your story fuels the UBUNTU spirit."),
        ], "What's on in HR", "HR updates"),
        feature("feature-monica.jpg", "Monicah Kihia, Group Director, HR and Culture",
                "HR Mission",
                ["An organisation is the sum of the decisions its people feel able to make. HR's role is to remove the friction that stops good people making good decisions - unclear policies, slow processes, development that never quite gets scheduled.",
                 "The measure of success is not how many programmes we run. It is whether colleagues can get on with the work they were hired to do."]),
        doctiles("Department documents", [
            "Staff wellness", "Staff requisition forms", "HR policies",
            "Department structure", "Medical forms", "Pension scheme",
            "Staff clearance forms", "Group life cover", "Learning and development"]),
        news_section([
            ("loop-monica.jpg", "HR Mission key visual", "#HRMission",
             "Supercharging HR for the organisation of the future",
             "What the HR function is prioritising this year, and the handful of processes being rebuilt rather than tweaked.",
             "HR &amp; Culture &middot; 1 August 2026"),
            ("loop-halloffame.jpg", "Hall of Fame", "#HallOfFame",
             "Hall of Fame: recognising the quarter's teams",
             "Recognition that names people rather than projects, with a note on how nominations are actually assessed.",
             "HR &amp; Culture &middot; 26 July 2026"),
            ("loop-tea.jpg", "Wellness", "#Wellness",
             "Wellness week: what is on and how to join",
             "Sessions across the week covering physical health, financial wellbeing and the parts of mental health people find hardest to raise.",
             "HR &amp; Culture &middot; 19 July 2026"),
            ("loop-kpis.jpg", "Career growth", "#CareerGrowth",
             "Ready for your next move? Internal opportunities",
             "How internal mobility works here, what managers are asked to do when a colleague applies, and the timeline you can expect.",
             "HR &amp; Culture &middot; 12 July 2026"),
            ("loop-gogetters.jpg", "Go Getters", "#GoGetters",
             "Development plans that survive contact with the year",
             "A short guide to writing a development plan specific enough to be useful and small enough to actually finish.",
             "HR &amp; Culture &middot; 5 July 2026"),
        ], "HR news"),
        HELP,
     ]), GROUP_SIDEBAR, sub=subnav_depts("Human Resources"), script=CAROUSEL_SCRIPT)

# ==========================================================================
# 9. article.html
# ==========================================================================
ARTICLE = """    <article>
      <div class="article__hero">
        <img src="assets/img/media/article-hero.jpg" alt="Go Getters, this is your space" width="940" height="529">
      </div>

      <span class="chip">#GoGetters</span>
      <h1 class="article__title" style="margin-top:12px">Go Getters: your space to share and shine</h1>

      <div class="article__by">
        <span class="article__avatar" aria-hidden="true">MC</span>
        <span>
          <span class="article__author">Marketing, Communications &amp; Citizenship</span>
          <span class="article__date">Published 1 August 2026 &middot; 4 min read</span>
        </span>
      </div>

      <div class="article__body">
        <p class="lede">Big wins and small joys both count. Across the Group, colleagues have started posting the everyday moments that make the work worth doing &mdash; and there is now one place to find them.</p>

        <p>The Go Getters space began as an experiment on a single floor. Someone posted a photo of a team that had stayed late to close a customer issue, and it turned out that a lot of people wanted to read that sort of thing. Within a month the habit had spread further than anyone had planned for, which is usually the sign that something is worth building properly.</p>

        <h2>What belongs here</h2>

        <p>Anything that made your work better this week. A colleague who unblocked something. A process that finally got simpler. A customer conversation that went unexpectedly well, or unexpectedly badly and taught you something. The bar is deliberately low &mdash; the point is frequency, not polish.</p>

        <p>What does not belong is anything covering customer detail, anything that would embarrass a named colleague, and anything that is really a complaint looking for an audience. Those have other routes, and they work better.</p>

        <div class="pullquote">The most useful posts are usually the smallest ones. Nobody needs a case study; they need to know a thing is possible.</div>

        <h2>How to post</h2>

        <p>Use the share box at the top of the Hub, or post from your team page and tag it. Posts appear in the Group feed within a few minutes. Add a photo if you have one, but do not let the absence of a photo stop you &mdash; a sentence is enough.</p>

        <h3>A note on recognition</h3>

        <p>Posting here is not a substitute for formal recognition, and it does not feed into performance conversations. It exists because a lot of good work is invisible to everyone except the people immediately around it, and that seems like a fixable problem.</p>

        <p>If you are not sure whether something is worth sharing, it probably is. The colleagues who post most often will tell you they felt awkward about the first one.</p>
      </div>

      <div class="share">
        <span class="share__label">Share</span>
        <a class="btn btn--secondary" href="#main">LinkedIn</a>
        <a class="btn btn--secondary" href="#main">Copy link</a>
        <a class="btn btn--secondary" href="#main">Email</a>
      </div>
    </article>

    <section class="section related">
      <div class="section__head">
        <h2>Related articles</h2>
      </div>
      <div class="related__grid">
        <a class="related__card" href="kenya-mcc.html">
          <img src="assets/img/loop/loop-nelly.jpg" alt="MCC Mission key visual" width="320" height="180">
          <span class="related__text">
            <span class="related__title">Iconize the NCBA brand as a regional powerhouse</span>
            <span class="related__desc">Marketing, Communications &amp; Citizenship</span>
          </span>
        </a>
        <a class="related__card" href="ubuntu-hub.html">
          <img src="assets/img/loop/loop-strategy.jpg" alt="2026-2030 UBUNTU Strategy" width="320" height="180">
          <span class="related__text">
            <span class="related__title">The 2026&ndash;2030 UBUNTU Strategy, explained</span>
            <span class="related__desc">UBUNTU Hub</span>
          </span>
        </a>
        <a class="related__card" href="kenya-hr.html">
          <img src="assets/img/loop/loop-monica.jpg" alt="HR Mission key visual" width="320" height="180">
          <span class="related__text">
            <span class="related__title">Supercharging HR for the organisation of the future</span>
            <span class="related__desc">Human Resources</span>
          </span>
        </a>
      </div>
    </section>"""

page("article.html", "Go Getters: your space to share and shine | NCBA UBUNTU Hub", "",
     hero("hero-article.jpg", "The new NCBA UBUNTU Hub is here",
          "News", "Stories from across NCBA Group."),
     "\n\n".join([ARTICLE, HELP]), GROUP_SIDEBAR)

print("\nAll pages written.")
