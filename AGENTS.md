# AGENTS.md

- Edit a page in `_src/`, then run `python3 tools/build.py`; the `index.html` files are written by it, so a hand edit there is lost on the next run.
- A new page is a new `_src/NAME.html` plus a row in `PAGES` in `tools/build.py`, which puts it in the rail on every page.
- `404.html` sends a browser on to the same path on omnipython.org, where the pages that used to answer here live now.
- `CNAME` holds the custom domain. GitHub Pages reads it; don't remove it.
- The look is this site's own (`assets/site.css`): a navy rail and a light sheet in IBM Plex. Keep it apart from omnipython.org's, and keep OmniPython's mascot off it.
