# desk

Otto Quill's shared desk: the writing method, style guides, templates, and tooling used across
every book and series repo.

## What desk is for

`desk` exists to produce world-class fictional worlds and the stories drawn out of them, with AI
doing the work.

Canon is the substrate, and the wiki is where canon primarily lives — authored as pages under a
world's `content/`, gated as files, rendered with no export step and no way for the two to drift.
Books and games are drawn out of canon. The public wiki is a declared product as well: a filtered,
deployed rendering, because a working canon holds spoilers and unpublished material the public
rendering has to withhold.

Automation is a dial. At one end, a single prompt outlining a concept yields a finished, published
product; at the other, close interactive work. Both ends have to be superb. A run populates canon
first and derives the book from it.

Built for the author's worlds now, generalizable by construction: `desk` knows kinds, a world names
instances, a run names settings. Publishing is in scope as far as the artifact — a distributable
book file and the world's deployed site. Storefront submission is not.

## [→ The Method](method/)

How a book gets written here, and why it is not simply a human novelist's method with the names
changed. Start at [00 · Starting a World](method/00-starting-a-world.md), which is the procedure
from a bare premise to a drafted wave and the only document that assumes nothing. The evidence
every rule descends from is [01 · The Difference](method/01-the-difference.md); the rules
themselves are [02 · The Rules](method/02-the-rules.md).

`desk` holds no setting and no book. A **world** repo holds those, declares itself in a
`world.toml`, and carries `desk` as a git submodule at `desk/`; every tool here is pointed at a
world with `--world` and at one of its products with `--product`.

## Layout

| Path | What lives here |
|---|---|
| [`method/`](method/) | The method: starting a world, the difference, the rules, the pipeline, blind reading, the instruments, the idiolect ledger, voice engineering. |
| [`templates/`](templates/) | Style sheet, voice profile, promise ledger, critic briefs — copied into a product's `editorial/` at its start. |
| [`canon/`](canon/) | `schema.toml`: the base canon kinds, the fields each requires, and which fields are references a validator has to resolve. |
| [`hugo/`](hugo/) | The layouts and archetypes a world mounts to render its canon as a wiki. |
| [`tools/`](tools/) | `idiolect_probe.py` (the gate), `prose_audit.py`, `continuity.py`, `canon.py`, `new_world.py`, `new_book.py`, `world.py`. Stdlib-only Python; no dependencies. |
| [`tools/tests/`](tools/tests/) | The suite: `python3 -m unittest discover -s tools/tests -t .` from the repository root. |

## Why this repo exists

The author does not persist between books; the files do. Every craft lesson learned inside a book
repo has stayed there, and the measurements show it: nine defect classes have recurred from one
book to the next, a construction rationed in one book reappeared in an unrelated one, and one
figure escalated 2 → 15 → 52 → 60 across four novels while each book's editorial pass believed it
was handling the problem.

`desk/` is the part of the author that carries over.

## Rights

The tooling here is offered under the MIT License. The method documents quote from Otto Quill
manuscripts for evidence; those quotations remain © Otto Quill, all rights reserved.
