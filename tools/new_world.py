#!/usr/bin/env python3
"""
new_world.py — scaffold a world that references desk.

Mechanical setup only. It creates the manifest, the canon skeleton and a Hugo config that mounts
desk's module, then prints the commands to run next. It drafts nothing and drives no stage.

    python3 tools/new_world.py PATH --title "Title"

Stdlib only.
"""
import argparse
import pathlib
import sys

MANIFEST = '''# The whole interface between this world and desk.
# Paths below are defaults; declare only what differs. Products are declared, never discovered.

title = "{title}"
desk  = "desk"
canon = "content/canon"

# [[products]]
# id   = "book-one"
# kind = "book"
# path = "books/book-one"
'''

HUGO = '''# Mounts desk's canon module. A world that renders no wiki can delete this file.
baseURL = "/"
title   = "{title}"

[[module.imports]]
path = "desk/hugo"
'''

CANON_DIRS = ('characters', 'places', 'factions', 'events', 'artifacts', 'terms', 'relationships')


def scaffold(path, title):
    root = pathlib.Path(path)
    if (root / 'world.toml').exists():
        sys.exit(f"new_world: {root / 'world.toml'} already exists; refusing to overwrite")
    for sub in CANON_DIRS:
        (root / 'content' / 'canon' / sub).mkdir(parents=True, exist_ok=True)
        (root / 'content' / 'canon' / sub / '.gitkeep').write_text('', encoding='utf-8')
    (root / 'world.toml').write_text(MANIFEST.format(title=title), encoding='utf-8')
    (root / 'hugo.toml').write_text(HUGO.format(title=title), encoding='utf-8')
    return root


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('path', help='directory to create the world in')
    ap.add_argument('--title', required=True)
    a = ap.parse_args()

    root = scaffold(a.path, a.title)
    print(f"""
created {root}/
  world.toml            the manifest desk reads
  hugo.toml             mounts desk/hugo
  content/canon/        canon pages: +++ TOML front matter, prose body

next:
  cd {root}
  git init && git submodule add <desk-remote> desk
  python3 desk/tools/new_book.py . --title "…" --slug book-one
  python3 desk/tools/canon.py --world .

then Stage 1, the spine, which is never delegated. See desk/method/00-starting-a-world.md.
""")


if __name__ == '__main__':
    main()
