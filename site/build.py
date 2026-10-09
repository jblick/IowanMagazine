#!/usr/bin/env python3
"""Build The Iowan static site.

Each file in pages/ starts with a settings comment, for example:

    <!-- title: Stories | nav: stories | description: Stories from every corner of Iowa. -->

The rest of the file is the page's <main> content. This script wraps it in the shared
head, header and footer and writes the finished page next to this script. Icons are
written as {{icon:name}} and replaced with inline SVG (Lucide shapes).

Run: python3 site/build.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
PAGES = ROOT / "pages"

NAV = [
    ("stories", "stories.html", "Stories"),
    ("events", "events.html", "Events"),
    ("back-issues", "back-issues.html", "Back issues"),
    ("institutions", "institutions.html", "Schools and libraries"),
    ("advertise", "advertise.html", "Advertise"),
    ("contribute", "contribute.html", "Contribute"),
    ("about", "about.html", "About"),
]

ICONS = {
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "printer": '<path d="M6 9V2h12v7"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5M12 15V3"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "book": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>',
    "school": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
}


def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="theme-color" content="#2f5d62">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&family=Oswald:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/iowan.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
"""

HEADER = """<div class="utility">
  <div class="wrap">
    <div class="text-size" role="group" aria-label="Text size">
      <span class="label">Text size</span>
      <button type="button" data-text-size="normal" aria-pressed="true" aria-label="Standard text size">A</button>
      <button type="button" data-text-size="large" aria-pressed="false" aria-label="Large text size">A</button>
      <button type="button" data-text-size="larger" aria-pressed="false" aria-label="Largest text size">A</button>
    </div>
    <div class="utility-links">
      <a href="subscribe.html#manage">My subscription</a>
      <a href="institutions.html">Schools and libraries</a>
      <a href="subscribe.html#gift">Give a gift</a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <div class="masthead-row">
      <p class="left">Iowa's original state magazine</p>
      <a class="masthead" href="index.html" aria-label="The Iowan, home">
        <span class="name">THE IOWAN</span>
        <span class="tagline">The people. The places. The stories. The life. Since 1952</span>
      </a>
      <div class="right">
        <form class="search-form" role="search" action="stories.html">
          <label class="visually-hidden" for="q-desktop">Search stories</label>
          <input id="q-desktop" name="q" type="search" placeholder="Search stories">
          <button type="submit" aria-label="Search">{search}</button>
        </form>
        <a class="btn btn-primary btn-small" href="subscribe.html">Subscribe</a>
        <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-nav">{menu}<span>Menu</span></button>
      </div>
    </div>
  </div>
  <nav class="primary-nav" id="primary-nav" aria-label="Main">
    <div class="wrap">
      <ul>
{nav}
      </ul>
      <div class="mobile-search">
        <form class="search-form" role="search" action="stories.html">
          <label class="visually-hidden" for="q-mobile">Search stories</label>
          <input id="q-mobile" name="q" type="search" placeholder="Search stories">
          <button type="submit" aria-label="Search">{search}</button>
        </form>
      </div>
    </div>
  </nav>
</header>
"""

FOOTER = """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <p class="name">THE IOWAN</p>
        <p>The people. The places. The stories. The life. Published since 1952, six issues a year.</p>
        <div class="social mt-lg">
          <a href="https://www.instagram.com/theiowanmagazine/" aria-label="The Iowan on Instagram">{instagram}</a>
          <a href="#" aria-label="The Iowan on Facebook [LINK TO CONFIRM]">{facebook}</a>
        </div>
      </div>
      <div>
        <h2>Read</h2>
        <ul>
          <li><a href="stories.html">Stories</a></li>
          <li><a href="events.html">Events calendar</a></li>
          <li><a href="back-issues.html">Back issues</a></li>
          <li><a href="index.html#newsletter">Newsletter</a></li>
        </ul>
      </div>
      <div>
        <h2>Subscribe</h2>
        <ul>
          <li><a href="subscribe.html">Subscribe or renew</a></li>
          <li><a href="subscribe.html#gift">Give a gift</a></li>
          <li><a href="institutions.html">Schools and libraries</a></li>
          <li><a href="subscribe.html#manage">My subscription</a></li>
        </ul>
      </div>
      <div>
        <h2>Printed in Ames</h2>
        <div class="printed-by">
          <img src="img/heuss-logo.jpg" alt="Heuss Printing" width="96" height="68" loading="lazy">
          <p>Printed by Heuss Printing<br><a href="about.html#heuss">Request a print quote</a></p>
        </div>
        <p class="mt-lg">903 North Second Street<br>Ames, IA 50010<br><a href="tel:+15152326710">(515) 232-6710</a></p>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 The Iowan</p>
      <p><a href="advertise.html">Advertise</a> &middot; <a href="contribute.html">Contribute</a> &middot; <a href="about.html">About and contact</a> &middot; <a href="about.html#privacy">Privacy</a></p>
    </div>
  </div>
</footer>
<script src="js/iowan.js" defer></script>
</body>
</html>
"""

SETTINGS = re.compile(r"^<!--(.*?)-->\s*", re.S)


def nav_html(active):
    items = []
    for key, href, label in NAV:
        current = ' aria-current="page"' if key == active else ""
        items.append(f'        <li><a href="{href}"{current}>{label}</a></li>')
    return "\n".join(items)


def build():
    for src in sorted(PAGES.glob("*.html")):
        text = src.read_text()
        m = SETTINGS.match(text)
        if not m:
            raise SystemExit(f"{src.name}: missing settings comment")
        settings = dict(
            (k.strip(), v.strip())
            for k, v in (part.split(":", 1) for part in m.group(1).split("|"))
        )
        body = text[m.end():]
        title = settings["title"]
        full_title = "The Iowan" if title == "Home" else f"{title} | The Iowan"
        html = (
            HEAD.format(title=full_title, description=settings.get("description", ""))
            + settings.get("banner", "")
            + HEADER.format(nav=nav_html(settings.get("nav", "")), search=icon("search"), menu=icon("menu"))
            + '<main id="main">\n' + body + "</main>\n"
            + FOOTER.format(instagram=icon("instagram"), facebook=icon("facebook"))
        )
        html = re.sub(r"\{\{icon:([a-z]+)\}\}", lambda mm: icon(mm.group(1)), html)
        (ROOT / src.name).write_text(html)
        print(f"built {src.name}")


if __name__ == "__main__":
    build()
