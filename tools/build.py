# SPDX-FileCopyrightText: 2026 Brad Barnett
#
# SPDX-License-Identifier: MIT

"""Write each page from its body in _src/, with the same head and rail.

Run it from the repository root after editing a file in _src/:

    python3 tools/build.py

A body file starts with ``@title`` and ``@desc`` lines; the rest is the page's
``<main>``. ``_src/index.html`` becomes ``/index.html`` and ``_src/NAME.html``
becomes ``/NAME/index.html``.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The rail, in order: address and name.
PAGES = [
    ("/", "PyDevices"),
    ("/mcuctl/", "MCU Control"),
    ("/mpvst/", "mpvst"),
    ("/workbench/", "Workbench"),
]

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Written by tools/build.py from _src/{src}; edit that file and run it again. -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="theme-color" content="#0b2a4a">
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
  <link rel="alternate icon" href="/favicon.ico" sizes="16x16 32x32 48x48">
  <link rel="canonical" href="https://pydevices.com{path}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
  <link rel="stylesheet" href="/assets/site.css">
</head>
<body>
  <header class="rail">
    <a class="home" href="/"><img src="/assets/logo.svg" alt="" width="40" height="40">PyDevices</a>
    <nav aria-label="Pages">
      <ol>
{nav}
      </ol>
    </nav>
    <p class="foot">Free and open source.<br><a href="https://github.com/PyDevices">github.com/PyDevices</a></p>
  </header>
  <main>
"""

TAIL = """  </main>
</body>
</html>
"""


def nav(current: str) -> str:
    rows = []
    for path, name in PAGES:
        mark = ' aria-current="page"' if path == current else ""
        rows.append(f'        <li><a href="{path}"{mark}>{name}</a></li>')
    return "\n".join(rows)


def build(src: Path) -> Path:
    lines = src.read_text(encoding="utf-8").splitlines(keepends=True)
    meta = {}
    while lines and lines[0].startswith("@"):
        key, _, value = lines.pop(0)[1:].partition(" ")
        meta[key] = value.strip()
    path = "/" if src.stem == "index" else f"/{src.stem}/"
    out = ROOT / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    page = HEAD.format(src=src.name, title=meta["title"], desc=meta["desc"], path=path, nav=nav(path))
    out.write_text(page + "".join(lines) + TAIL, encoding="utf-8")
    return out


if __name__ == "__main__":
    for src in sorted((ROOT / "_src").glob("*.html")):
        print(build(src).relative_to(ROOT))
