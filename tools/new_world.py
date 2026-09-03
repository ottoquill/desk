#!/usr/bin/env python3
"""
new_world.py — scaffold a world that references desk.

Mechanical setup only. It creates the manifest, the canon skeleton and a Hugo config that mounts
desk's layouts and archetypes, then prints the commands to run next. It drafts nothing and drives
no stage.

    python3 tools/new_world.py PATH --title "Title"

Stdlib only.
"""
import argparse
import pathlib
import sys

# desk's tools live in one directory and import each other by name.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from world import MANIFEST  # the manifest's filename, so the two spellings cannot drift

HUGO_CONFIG = 'hugo.toml'


class NewWorldError(Exception):
    """Error creating a new world."""


MANIFEST_TEMPLATE = '''# The whole interface between this world and desk.
# Paths below are defaults; declare only what differs. Products are declared, never discovered.

title = "{title}"
desk  = "desk"
canon = "content/canon"

# [[products]]
# id   = "book-one"
# kind = "book"
# path = "books/book-one"
'''

HUGO_TEMPLATE = '''# Mounts desk's canon layouts and archetypes. A world that renders no wiki can delete
# this file. These are mounts rather than a [[module.imports]] entry because an import names a Hugo
# Module, which Hugo resolves through the Go toolchain or under themes/ — and desk is a git
# submodule at desk/, so the import fails before a single page renders. A mount needs neither.
#
# This world's own layouts/ and archetypes/ are mounted first, so anything it puts there wins over
# desk's. Neither directory has to exist.
baseURL = "/"
title   = "{title}"

[[module.mounts]]
source = "layouts"
target = "layouts"

[[module.mounts]]
source = "desk/hugo/layouts"
target = "layouts"

[[module.mounts]]
source = "archetypes"
target = "archetypes"

[[module.mounts]]
source = "desk/hugo/archetypes"
target = "archetypes"
'''

CANON_DIRS = ('characters', 'places', 'factions', 'events', 'artifacts', 'terms', 'relationships')


def scaffold(path, title):
    root = pathlib.Path(path)
    # Both files are checked before anything is written. Refusing on the manifest alone and then
    # writing hugo.toml unconditionally destroyed a pre-existing Hugo site config and exited 0.
    for name in (MANIFEST, HUGO_CONFIG):
        if (root / name).exists():
            raise NewWorldError(f"{root / name} already exists; refusing to overwrite")
    # Escape title for TOML: backslashes first, then quotes.
    safe = title.replace('\\', '\\\\').replace('"', '\\"')
    for sub in CANON_DIRS:
        (root / 'content' / 'canon' / sub).mkdir(parents=True, exist_ok=True)
        (root / 'content' / 'canon' / sub / '.gitkeep').write_text('', encoding='utf-8')
    (root / MANIFEST).write_text(MANIFEST_TEMPLATE.format(title=safe), encoding='utf-8')
    (root / HUGO_CONFIG).write_text(HUGO_TEMPLATE.format(title=safe), encoding='utf-8')
    return root


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('path', help='directory to create the world in')
    ap.add_argument('--title', required=True)
    a = ap.parse_args()

    try:
        root = scaffold(a.path, a.title)
    except NewWorldError as e:
        sys.exit(f"new_world: {e}")

    print(f"""
created {root}/
  world.toml            the manifest desk reads
  hugo.toml             mounts desk/hugo/layouts and desk/hugo/archetypes
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
