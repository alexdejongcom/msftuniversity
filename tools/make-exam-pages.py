#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the exam prep hub: exams.html plus one page per certification.

Header and footer are lifted from an existing page at build time, so the
generated pages stay in step with the rest of the site automatically.

Run:  python3 tools/make-exam-pages.py
"""
import html
import os
import re
import runpy

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = runpy.run_path(os.path.join(ROOT, "tools", "exam-data.py"))
EXAMS, FAMILIES = DATA["EXAMS"], DATA["FAMILIES"]
OUT_DIR = os.path.join(ROOT, "exam")
SITE = "https://msftuniversity.com"

TEMPLATE_PAGE = os.path.join(ROOT, "verify.html")
LEARN_SEARCH = "https://learn.microsoft.com/training/browse/?terms="
PEARSON = "https://learn.microsoft.com/credentials/certifications/schedule-through-pearson-vue"
SANDBOX = "https://go.microsoft.com/fwlink/?linkid=2226877"


def chrome():
    """Pull the shared header and footer out of an existing page."""
    src = open(TEMPLATE_PAGE, encoding="utf-8").read()
    head = re.search(r"<header class=\"site-header\">.*?</header>", src, re.S).group(0)
    foot = re.search(r"<footer class=\"site-footer\">.*?</footer>", src, re.S).group(0)
    return head, foot


def depth_fix(markup, depth):
    """Rewrite site-relative links for a page that sits `depth` folders down."""
    if not depth:
        return markup
    prefix = "../" * depth

    def sub(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http://", "https://", "mailto:", "#", "data:", "/")):
            return m.group(0)
        return '%s="%s%s"' % (attr, prefix, url)

    return re.sub(r'(href|src)="([^"]+)"', sub, markup)


def active_nav(markup, label):
    markup = markup.replace(' class="active"', "")
    return markup.replace('>%s<' % label, ' class="active">%s<' % label, 1) if label else markup


HEAD_TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect x=%272%27 y=%272%27 width=%2713%27 height=%2713%27 fill=%27%23f25022%27/%3E%3Crect x=%2717%27 y=%272%27 width=%2713%27 height=%2713%27 fill=%27%237fba00%27/%3E%3Crect x=%272%27 y=%2717%27 width=%2713%27 height=%2713%27 fill=%27%2300a4ef%27/%3E%3Crect x=%2717%27 y=%2717%27 width=%2713%27 height=%2713%27 fill=%27%23ffb900%27/%3E%3C/svg%3E">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<link rel="stylesheet" href="{css}">
{extra}</head>
<body>
"""


def page(title, desc, canonical, body, depth=0, extra="", nav_label="Exam Prep"):
    head, foot = chrome()
    head = active_nav(head, nav_label)
    css = "../" * depth + "css/style.css"
    doc = HEAD_TPL.format(title=title, desc=desc, canonical=canonical, css=css, extra=extra)
    doc += depth_fix(head, depth) + "\n"
    doc += body
    doc += "\n" + depth_fix(foot, depth) + "\n"
    scripts = ['<script src="{p}js/events.js"></script>',
               '<script src="{p}js/achievements.js" defer></script>',
               '<script src="{p}js/terminal.js" defer></script>',
               '<script src="{p}js/counter.js" defer></script>',
               '<script src="{p}js/site.js" defer></script>']
    doc += "\n".join(s.format(p="../" * depth) for s in scripts)
    doc += "\n</body>\n</html>\n"
    return doc


def fam_name(key):
    for k, label, _ in FAMILIES:
        if k == key:
            return label
    return key


def course_detail(code, e):
    """The richer 'about the course' block.

    Everything here is optional, so an exam we have not written up yet simply
    renders without this section. All copy is ours: Microsoft's objectives and
    descriptions stay behind the official links.
    """
    if not any(e.get(k) for k in ("overview", "challenges", "labs", "duration", "retired")):
        return ""

    esc = lambda s: html.escape(str(s), quote=False)

    # A retired exam says so first, before anything else on the page.
    retired = ""
    if e.get("retired"):
        retired = (
            '    <p style="background:#fff4ce;border:1px solid #f2c94c;border-radius:var(--radius);'
            'padding:14px 18px;font-size:15px;color:var(--ink);max-width:820px;margin-bottom:22px">'
            '<strong>Retired by Microsoft on %s.</strong> This exam can no longer be taken and its '
            'renewal assessments have been withdrawn. It is kept here for people who hold it and '
            'need the context.</p>\n' % esc(e["retired"]))

    facts = []
    if e.get("duration"):
        facts.append(("Course length", esc(e["duration"]) +
                      (" &middot; %s" % esc(e["course"]) if e.get("course") else "")))
    if e.get("exam_time"):
        facts.append(("Exam", esc(e["exam_time"])))
    facts.append(("Technical level", esc(e["level"])))
    labs = e.get("labs") or {}
    facts.append(("Hands-on labs", ("%d labs" % labs["count"]) if labs.get("count")
                  else ("Yes" if labs else "None published")))

    fact_html = "\n".join(
        '      <div class="road-stat is-text"><strong>%s</strong><span>%s</span></div>' % (v, k)
        for k, v in facts)

    overview = ('    <p style="font-size:17px;color:var(--ink-soft);max-width:820px">%s</p>\n'
                % esc(e["overview"]) if e.get("overview") else "")

    prereq = ('    <p style="font-size:14.5px;color:var(--ink-faint);max-width:820px;margin-top:14px">'
              '<strong>Assumed knowledge:</strong> %s</p>\n' % esc(e["prereq"])) if e.get("prereq") else ""

    challenges = ""
    if e.get("challenges"):
        items = "\n".join("          <li style=\"margin-bottom:10px\">%s</li>" % esc(c)
                          for c in e["challenges"])
        challenges = """      <div>
        <h3 style="font-family:var(--font-display);font-size:19px;margin-bottom:12px">The problems it answers</h3>
        <p class="sub" style="margin-bottom:14px">Why people in this role end up sitting %s</p>
        <ol style="padding-left:20px;color:var(--ink-soft);font-size:15px;line-height:1.55">
%s
        </ol>
      </div>
""" % (esc(code), items)

    labs_html = ""
    if labs:
        links = []
        if labs.get("repo"):
            links.append('<li><a href="%s" target="_blank" rel="noopener">Lab instructions on GitHub '
                         '<span class="desc">Official MicrosoftLearning repository</span></a></li>'
                         % labs["repo"])
        if labs.get("guide"):
            links.append('<li><a href="%s" target="_blank" rel="noopener">Hosted lab guide '
                         '<span class="desc">The same labs, rendered for reading</span></a></li>'
                         % labs["guide"])
        labs_html = """      <div class="card resource-group">
        <h3>Hands-on labs</h3>
        <p class="sub">%s</p>
        <p style="font-size:14.5px;color:var(--ink-soft)">%s</p>
        <ul class="resource-list" style="margin-top:14px">
%s
        </ul>
      </div>
""" % ("%d labs across %d learning paths" % (labs["count"], labs["paths"])
       if labs.get("count") and labs.get("paths")
       else ("%d hands-on labs" % labs["count"] if labs.get("count") else "What you actually build"),
       esc(labs.get("summary", "")), "\n".join("          " + l for l in links))

    two_col = ""
    if challenges or labs_html:
        two_col = '    <div class="grid grid-2" style="margin-top:34px">\n%s%s    </div>\n' % (
            challenges, labs_html)

    return """
<section class="section alt">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">About the course</div>
      <h2 class="section-title">What %s actually covers</h2>
    </div>
%s%s%s
    <div class="road-strip" style="margin-top:26px">
%s
    </div>
%s  </div>
</section>
""" % (esc(code), retired, overview, prereq, fact_html, two_col)


def seller_block(code, e):
    """Enablement for the partners who resell our courses.

    Written to be useful to a buyer reading over their shoulder too: the
    'common pushbacks' are answers to fair questions, not rebuttal scripts.
    """
    s = e.get("selling") or {}
    if not s:
        return ""
    esc = lambda x: html.escape(str(x), quote=False)

    def ul(items, cls=""):
        return "\n".join('          <li%s>%s</li>' % (cls, esc(i)) for i in items)

    pitch = ('    <p style="font-size:19px;font-family:var(--font-display);color:var(--ink);'
             'max-width:760px;line-height:1.45">&ldquo;%s&rdquo;</p>\n' % esc(s["pitch"])) if s.get("pitch") else ""

    left = []
    if s.get("triggers"):
        left.append('        <h3 style="font-family:var(--font-display);font-size:18px;margin-bottom:10px">'
                    'When to bring it up</h3>\n'
                    '        <ul style="padding-left:20px;color:var(--ink-soft);font-size:15px;line-height:1.55">\n%s\n        </ul>\n'
                    % ul(s["triggers"]))
    who = []
    if s.get("buyer"):
        who.append("<strong>Who signs:</strong> " + esc(s["buyer"]))
    if s.get("attendees"):
        who.append("<strong>Who attends:</strong> " + esc(s["attendees"]))
    if who:
        left.append('        <p style="margin-top:18px;font-size:14.5px;color:var(--ink-soft);line-height:1.6">%s</p>\n'
                    % "<br>".join(who))
    if s.get("next"):
        left.append('        <h3 style="font-family:var(--font-display);font-size:18px;margin:22px 0 10px">'
                    'What to sell next</h3>\n'
                    '        <ul style="padding-left:20px;color:var(--ink-soft);font-size:15px;line-height:1.55">\n%s\n        </ul>\n'
                    % ul(s["next"]))

    right = ""
    if s.get("objections"):
        rows = "\n".join(
            '          <details style="border-top:1px solid var(--border);padding:11px 0">\n'
            '            <summary style="cursor:pointer;font-weight:600;font-size:14.5px;color:var(--ink)">%s</summary>\n'
            '            <p style="margin-top:8px;font-size:14.5px;color:var(--ink-soft);line-height:1.6">%s</p>\n'
            '          </details>' % (esc(q), esc(a)) for q, a in s["objections"])
        right = ('      <div class="card resource-group">\n'
                 '        <h3>Pushbacks you will hear</h3>\n'
                 '        <p class="sub">And a straight answer for each</p>\n'
                 '%s\n      </div>\n' % rows)

    cols = ""
    if left or right:
        cols = ('    <div class="grid grid-2" style="margin-top:30px;align-items:start">\n'
                '      <div>\n%s      </div>\n%s    </div>\n' % ("".join(left), right))

    return """
<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">For training partners</div>
      <h2 class="section-title">Selling %s</h2>
      <p>Everything a partner needs to put this course in front of the right customer.
         Lift any of it straight into a proposal.</p>
    </div>
%s%s  </div>
</section>
""" % (esc(code), pitch, cols)


def exam_page(code, e):
    slug = code.lower()
    canonical = "%s/exam/%s.html" % (SITE, slug)
    title = "%s exam prep — %s | Microsoft University" % (code, html.escape(e["title"], quote=False))
    # Newly released exams have no practice assessment yet, so don't promise one.
    offer = ("Free study guide, practice assessment and official learning paths"
             if e.get("pa") else "Free study guide and official learning paths")
    desc = "%s %s for %s, plus instructor-led training with Alex de Jong." % (
        e["blurb"].split(".")[0] + ".", offer, code)
    desc = re.sub(r"\s+", " ", desc)[:300]

    related = [(c, x) for c, x in sorted(EXAMS.items()) if x["fam"] == e["fam"] and c != code]

    jsonld = """<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Course","name":"{code} — {t}",
"description":"{d}","provider":{{"@type":"Organization","name":"Microsoft University","url":"{site}"}},
"url":"{canon}","teaches":"{t}","inLanguage":"en",
"hasCourseInstance":{{"@type":"CourseInstance","courseMode":["onsite","online"],
"instructor":{{"@type":"Person","name":"Alex de Jong"}}}}}}
</script>
""".format(code=code, t=html.escape(e["title"], quote=True), d=html.escape(e["blurb"], quote=True),
           site=SITE, canon=canonical)

    res = []
    res.append(('Official exam page', e["url"], 'Skills measured, exam duration and how to book'))
    if e.get("sg"):
        res.append(('Study guide (free)', e["sg"], 'The definitive list of what is on the exam'))
    if e.get("pa"):
        res.append(('Practice assessment (free)', e["url"], 'Microsoft&rsquo;s own practice questions, no cost'))
    res.append(('Learning paths (free)', LEARN_SEARCH + code, 'Self-paced modules on Microsoft Learn'))
    res.append(('Exam sandbox', SANDBOX, 'Try the exam interface before the real thing'))
    res.append(('Schedule the exam', PEARSON, 'Book through Pearson VUE'))

    res_html = "\n".join(
        '          <li><a href="%s" target="_blank" rel="noopener">%s <span class="desc">%s</span></a></li>'
        % (u, n, d) for n, u, d in res)

    rel_html = ""
    if related:
        rel_html = """
<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">Same track</div>
      <h2 class="section-title">Related certifications</h2>
    </div>
    <div class="grid grid-3">
%s
    </div>
  </div>
</section>
""" % "\n".join(
            '      <div class="card"><h3><a href="%s.html" style="text-decoration:none">%s</a></h3>'
            '<p>%s</p><a class="card-link" href="%s.html">Exam prep &rsaquo;</a></div>'
            % (c.lower(), c, html.escape(x["title"], quote=False), c.lower()) for c, x in related)

    detail = course_detail(code, e)
    seller = seller_block(code, e)

    body = """
<section class="page-hero">
  <div class="container">
    <div class="eyebrow" style="color:rgba(255,255,255,.8)"><a href="../exams.html" style="color:inherit">Exam prep</a> &middot; {fam}</div>
    <h1>{code} &mdash; {t}</h1>
    <p>{blurb}</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2">
      <div>
        <div class="section-head">
          <div class="eyebrow">Is this exam for you?</div>
          <h2 class="section-title">Who takes {code}</h2>
          <p>{who}</p>
        </div>
        <p style="color:var(--ink-faint);font-size:14.5px">
          Level: <strong>{level}</strong> &middot; Official credential: <strong>{t}</strong>
        </p>
      </div>
      <div class="card resource-group">
        <h3>Everything free, in one place</h3>
        <p class="sub">Straight to the official sources &mdash; no sign-up, no reselling</p>
        <ul class="resource-list">
{res}
        </ul>
      </div>
    </div>
  </div>
</section>
{detail}{seller}
<section class="{cta_class}">
  <div class="container">
    <div class="cta-band">
      <div>
        <div class="eyebrow" style="color:rgba(255,255,255,.8)">Instructor-led</div>
        <h2>Train for {code} with Alex</h2>
        <p>We deliver the official Microsoft course for {code} &mdash; in person or virtual, public or in-company.
           Real demos, real stories, and the whiteboards to take home.</p>
      </div>
      <a class="btn btn-primary" href="../contact.html">Book this training</a>
    </div>
    <p style="margin-top:18px;font-size:14px;color:var(--ink-faint)">
      Prefer to browse first? See the <a href="../training.html#catalog">full course catalog</a>
      or the <a href="../events.html">upcoming dates</a>.
    </p>
  </div>
</section>
{rel}
<section class="section">
  <div class="container" style="max-width:820px">
    <p style="font-size:13px;color:var(--ink-faint)">
      Exam titles, study guides and practice assessments are published by Microsoft and linked here directly;
      the descriptions on this page are our own. Microsoft may update exam content at any time &mdash; the
      official study guide is always the authority.
    </p>
  </div>
</section>
""".format(code=code, t=html.escape(e["title"], quote=False), blurb=e["blurb"], who=e["who"],
           level=e["level"], res=res_html, fam=fam_name(e["fam"]), rel=rel_html,
           detail=detail, seller=seller,
           # keep the light/grey rhythm. detail is grey, seller is white, so
           # whichever ran last decides the shade the CTA band needs.
           cta_class=("section alt" if seller else "section") if detail else "section alt")

    return page(title, html.escape(desc, quote=True), canonical, body, depth=1, extra=jsonld)


def hub_page():
    canonical = SITE + "/exams.html"
    title = "Microsoft exam prep — free study guides for 53 certifications | Microsoft University"
    desc = ("Free prep for 53 Microsoft certifications: official study guides, practice assessments and "
            "learning paths for every AZ, SC, MS, MD, PL, DP, MB, GH and AB exam, in one place.")

    blocks = []
    for key, label, note in FAMILIES:
        rows = [(c, e) for c, e in sorted(EXAMS.items()) if e["fam"] == key]
        if not rows:
            continue
        items = "\n".join(
            '          <li><a href="exam/%s.html">%s <span class="desc">%s</span></a></li>'
            % (c.lower(), c, html.escape(e["title"], quote=False)) for c, e in rows)
        blocks.append("""      <div class="card resource-group">
        <h3>%s</h3>
        <p class="sub">%s</p>
        <ul class="resource-list">
%s
        </ul>
      </div>""" % (label, note, items))

    body = """
<section class="page-hero">
  <div class="container">
    <div class="eyebrow" style="color:rgba(255,255,255,.8)">Free exam prep</div>
    <h1>Microsoft certification exam prep</h1>
    <p>Every certification we teach, with the free official study guide, practice assessment and
       learning paths collected on one page each. No sign-up, nothing sold — just the fastest route
       from &ldquo;I should get certified&rdquo; to actually booking the exam.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">%d certifications</div>
      <h2 class="section-title">Pick your exam</h2>
      <p>Grouped by track. Every page links straight to Microsoft&rsquo;s own free resources —
         and tells you who the exam is actually for.</p>
    </div>
    <div class="grid grid-2">
%s
    </div>
  </div>
</section>

<section class="section alt">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Want the guided version?</h2>
        <p>Self-study works. Self-study with an instructor who has taught it a hundred times works faster.</p>
      </div>
      <a class="btn btn-primary" href="contact.html">Book a training</a>
    </div>
  </div>
</section>
""" % (len(EXAMS), "\n".join(blocks))

    return page(title, html.escape(desc, quote=True), canonical, body, depth=0)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    n = 0
    for code, e in sorted(EXAMS.items()):
        p = os.path.join(OUT_DIR, code.lower() + ".html")
        open(p, "w", encoding="utf-8").write(exam_page(code, e))
        n += 1
    open(os.path.join(ROOT, "exams.html"), "w", encoding="utf-8").write(hub_page())
    print("wrote exams.html + %d exam pages" % n)


if __name__ == "__main__":
    main()
