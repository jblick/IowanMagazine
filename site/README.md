# The Iowan: website

A static site for The Iowan, built from `docs/brand-guidelines.md` and the mockups in `design/`.
No framework and no dependencies; open `index.html` in a browser or upload the folder to any web host.

## Editing

- Page content lives in `pages/*.html`. The shared head, header and footer live in `build.py`.
- After editing, run `python3 site/build.py` to regenerate the pages in this folder.
- Styles: `css/iowan.css` (brand colors and type are CSS variables at the top). Scripts: `js/iowan.js`.

## Pages

Home, Stories, sample Story (article template with MLA/APA/Chicago citation tool), Events (filter by region),
Subscribe (self or gift), Schools and libraries (institutional quote form), Back issues, Advertise, Contribute,
About (with the Heuss Printing credit).

## Designed for The Iowan's readers

- Older readers: 19px body text (20px in articles), a text-size control in the top bar that remembers each reader's
  choice, high-contrast colors (WCAG AA or better), 44 to 48px tap targets, visible keyboard focus.
- Academics: citation tool on every story, story search, a print stylesheet.
- Schools and libraries: a dedicated page with purchase orders, invoicing, multi-copy sets and catalog details.

## Not done yet

- Text in [BRACKETS] marks facts to get from the magazine (prices for back issues, ISSN, staff, dates).
- Forms and checkout only validate and show a confirmation; they are not connected to anything.
- Event dates are placeholders; the events listed are long-running Iowa events to be confirmed.
- Story photos are placeholders except where a cover image is used.
