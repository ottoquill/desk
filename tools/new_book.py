#!/usr/bin/env python3
"""
new_book.py — add a book product to an existing world.

Copies desk's templates into the product's editorial directory, creates the manuscript directory,
and APPENDS a [[products]] table to world.toml. Appending at end of file is a text operation that
preserves every comment, which is how this respects the rule that no tool rewrites a config file.

The copied editorial/voice-profile.toml has its `book = "TITLE"` placeholder replaced with the
title passed in — the templates/ copy itself is never touched.

    python3 tools/new_book.py WORLD --title "Title" --slug book-one

Stdlib only. Requires Python 3.11+ for tomllib (via world.py).
"""
import argparse
import pathlib
import shutil
import sys

# desk's tools live in one directory and import each other by name.
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import world as world_mod
from world import MANIFEST  # the manifest's filename, so the two spellings cannot drift

TEMPLATES = pathlib.Path(__file__).resolve().parent.parent / 'templates'
COPY = ('voice-profile.toml', 'style-sheet.md', 'promise-ledger.md', 'critic-briefs.md')
BOOK_PLACEHOLDER = 'book = "TITLE"'

STANZA = '''
[[products]]
id   = "{slug}"
kind = "book"
path = "{path}"
'''


class NewBookError(Exception):
    """A world manifest is missing, a slug collides, or a template is missing."""


def _escape(value):
    """Escape a value for interpolation into a double-quoted TOML string. Backslashes first, then
    quotes — escaping quotes first would double-escape the backslashes just introduced."""
    return value.replace('\\', '\\\\').replace('"', '\\"')


def add(world_path, title, slug):
    root = pathlib.Path(world_path)
    manifest = root / MANIFEST
    try:
        existing = world_mod.load(root).products
    except world_mod.WorldError as e:
        raise NewBookError(str(e)) from None
    if any(p.id == slug for p in existing):
        raise NewBookError(f"{slug!r} is already declared in {manifest}")

    rel = f"books/{slug}"
    product = root / rel
    (product / 'manuscript').mkdir(parents=True, exist_ok=True)
    editorial = product / 'editorial'
    editorial.mkdir(parents=True, exist_ok=True)
    for name in COPY:
        src = TEMPLATES / name
        if not src.is_file():
            raise NewBookError(f"missing template {src}")
        shutil.copyfile(src, editorial / name)

    profile = editorial / 'voice-profile.toml'
    text = profile.read_text(encoding='utf-8')
    if BOOK_PLACEHOLDER not in text:
        raise NewBookError(f"{profile}: missing placeholder {BOOK_PLACEHOLDER!r}")
    safe_title = _escape(title)
    profile.write_text(
        text.replace(BOOK_PLACEHOLDER, f'book = "{safe_title}"', 1), encoding='utf-8'
    )

    safe_slug = _escape(slug)
    safe_path = _escape(rel)
    with open(manifest, 'a', encoding='utf-8') as fh:
        fh.write(STANZA.format(slug=safe_slug, path=safe_path))
    return product


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('world', help='world root, or the world.toml itself')
    ap.add_argument('--title', required=True)
    ap.add_argument('--slug', required=True)
    a = ap.parse_args()

    root = pathlib.Path(a.world)
    if root.name == MANIFEST:
        root = root.parent

    try:
        product = add(root, a.title, a.slug)
    except NewBookError as e:
        sys.exit(f"new_book: {e}")

    print(f"""
created {product}/
  editorial/voice-profile.toml   set the cadence targets and inherit the budgets
  editorial/style-sheet.md       R9a, R10, R11: sentences and prohibitions, never moods
  editorial/promise-ledger.md
  editorial/critic-briefs.md     held fixed across products; editing it makes yields incomparable
  manuscript/

declared in {root / MANIFEST}

next:
  cd {root}
  1. Stage 1, the spine. Never delegated. Gate: back-cover copy and last line exist.
  2. python3 desk/tools/canon.py --world .
""")


if __name__ == '__main__':
    main()
