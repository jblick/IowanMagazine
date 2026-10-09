# The Iowan: website redesign

Design work for a new home on the web for The Iowan magazine. The base site is the current catalog page at
https://heuss.presencehost.net/customerdesigns/the-iowan-magazine.html (Heuss Printing / PrinterPresence).

## Contents
- `design/` : the seven artboards (`.dc.html`) and `canvas.json` from the Claude Design canvas "Iowan Magazine Redesign".
  Artboards: Main (discovery brief), Home, Shop (subscribe), BackIssues, Advertise, Contribute, About.
- `assets/` : images pulled from the current site (covers, tee photo, Heuss Printing logo).
- `research/` : saved HTML of the crawled page.

## Notes
- The artboards reference images as `/_blob/<id>`, which resolve only inside the claude.ai canvas. Mapping:
  `1a9d46f5...` heuss-logo, `17679ba3...` iowan-cover-a, `23aa7961...` iowan-cover-b, `defe973b...` iowan-cover-c,
  `c4734dbd...` iowan-bundle, `fe7c21cb...` iowan-tee (files in `assets/`).
- The Iowan masthead is typeset in Libre Caslon Text; no standalone logo file was available.
- Bracketed text such as `[PRICE]` marks facts the current site does not state.
- Forms and carts are layout only, not connected to anything.
- Brand colors: teal `#2f5d62`, cream `#f7f3ea`, ink `#1c2b2e`, label brown `#8a4a12`; Heuss orange `#f06802` used only for the quote button.
