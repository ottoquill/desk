# The World Contract

*Design spec. Makes `desk/` world-independent infrastructure, and gives it an entry point.*

**Status:** approved in discussion 2026-09-02, not yet implemented.
**Scope:** piece 1 of 3. Pieces 2 and 3 are named at the end and not designed here.

---

## The problem

Two defects, reported together.

**desk knows about dependent books.** Path coupling to `<book>/manuscript` and `<book>/editorial/`
runs through thirteen files, including all four templates. `names.json` is worse: a registry keyed
by
which book used which name, holding per-book state inside shared infrastructure.

**There is no entry point.** The repo carries 39 rules, 12 pipeline stages and a 10,000-line
research library, and never says how to start. Grepping for a creation path returns three
incidental phrases. Stage 0 says a book "begins by pulling from `desk/`" and lists what it pulls,
yet no procedure anywhere follows it.

Citing the four existing novels as measured evidence stays untouched; what changes is the
structural coupling to books that have yet to be written.

## What desk is for

A world contains all material relevant to that world and all of its media: canon, lore, timeline,
multiple books, a wiki, a game. `desk/` contains only what is world-independent and reusable, and
is referenced from a world.

The intended range of use runs from a single prompt outlining a concept that produces an entire
publishable book, through to fully interactive authoring. Both ends consume the same instruments
and the same gates.

## Principles

**desk knows product kinds; the world names instances.** desk ships what a book is, which
instruments apply to one, and what any product needs from canon. The world supplies names, paths and
content. Names belonging to a world never appear anywhere inside desk.

**Backward-looking derived data stays; forward-looking state leaves.** The `L01`–`L28` budgets are
constants measured on a past corpus, and they describe the model's attractor rather than one
author's quirks: any world drafted by the same model family lands in the same place. They stay.
Anything that accumulates as new work is produced belongs to the world.

**Config is human-owned and machine-read. State is machine-owned and machine-read.** Config is
TOML, state is JSON, and no tool ever rewrites a config file.

## The contract

### Referencing desk

A world adds desk as a **git submodule**, pinned to a commit. A book built two years later against
different budgets is then reproducible, and the question "which desk version gated this book" has
an answer. A sibling checkout by convention, the arrangement the current docs imply, cannot answer
it.

### The manifest

`world.toml` at the world root is the whole interface. desk reads it and learns how any world is
assembled, without learning which world it has been handed.

```toml
title = "…"
desk   = "desk"                  # submodule path

[canon]
facts = "data/canon/facts.json"  # typed fact store
names = "data/canon/names.json"  # used-names registry

[[products]]
id   = "…"
kind = "book"                    # a kind desk ships
path = "books/…"

[[products]]
id   = "…"
kind = "wiki"
path = "wiki"
```

Every path has a default, so a conventional world declares its products and little else. Products
are declared rather than discovered: letting desk guess what counts as a product is the failure of
the pure-convention alternative, and it would put a world's shape back inside desk.

A world that renders its
wiki with Hugo points `canon` under `data/` and Hugo reads the same files the gate reads, with no
export step and no way for the wiki to drift from what the books were gated against. desk neither
knows nor cares that Hugo exists; placement is the world's business, and that is why paths
are declared rather than assumed.

### Conventional layout

```
world/
  world.toml
  desk/                        submodule
  data/canon/facts.json        machine state
  data/canon/names.json        machine state
  books/<slug>/
    editorial/voice-profile.toml
    editorial/style-sheet.md
    editorial/promise-ledger.md
    editorial/critic-briefs.md
    manuscript/
  wiki/
```

### What each side owns

| | desk | world |
|---|---|---|
| Method, rules, pipeline | yes | |
| Instruments and budgets | yes | |
| Templates | yes | |
| Defect **classes**, regression suite | yes | |
| Canon, facts, names, timeline | | yes |
| Bibles, outlines, spines | | yes |
| Manuscripts and other media | | yes |
| Voice profile for a product | template only | filled copy |
| Defect **instances** | | yes |

The regression split is the subtle one. A defect class (over-claim, fake rigor, self-priming) is a
failure mode of the author and ratchets in desk. A defect instance belongs to the work that
carried it and ratchets in the world.

## Changes to desk

1. **Delete `names.json`.** World state. `new_world.py` creates an empty one inside a world.
2. **`tools/world.py`** — a stdlib module that loads `world.toml`, applies defaults, and resolves
   product and canon paths. Every other tool takes `--world PATH` through it.
3. **`tools/continuity.py`** learns `--world`, which supplies `--facts` and `--names` from the
   manifest. The existing explicit flags stay and win when both are given.
4. **`tools/prose_audit.py`** learns `--world` plus a product id, and reads a **TOML** profile via
   `tomllib`. `templates/voice-profile.json` becomes `voice-profile.toml`, losing nine `_comment`
      keys and a 431-character line to real comments. No book consumes the JSON form yet, so the
   change breaks no
   existing consumer.
5. **`tools/new_world.py`** — scaffolds a world: `world.toml`, empty canon, directory skeleton, and
   the submodule command printed rather than run.
6. **`tools/new_book.py`** — adds a book product to an existing world: copies the four templates
   into `editorial/`, creates `manuscript/`, and **appends** a `[[products]]` table to `world.toml`.
   Appending at end of file is a text operation that preserves every comment, so the rule that no
   tool rewrites config holds.
7. **`method/00-starting-a-world.md`** — the missing entry point. Submodule, manifest, first
   product, then the ordered path from concept to draft with the gate command at each stage. This
   is the manual path; piece 2 automates it.
8. **Decouple the docs.** `<book>/manuscript` and `desk/tools/...` become world-relative
   throughout `method/` and `templates/`. `CLAUDE.md` stops saying desk is checked out alongside a
   book.

## Testing

The repo has no tests. This spec adds the first ones, as stdlib `unittest` under `tools/tests/`,
run by `python3 -m unittest discover tools/tests`:

- **`world.py`** — defaults applied to a minimal manifest; explicit paths override; a product id
  that does not exist fails loudly; a malformed manifest reports the file and the reason.
- **`new_world.py`** and **`new_book.py`** — scaffold into a temp directory, then assert the result
  loads through `world.py` and that the appended manifest still parses. Round-trip, not shape.
- **`prose_audit.py`** — a TOML profile yields the budget map the audit expects, asserted against
  literal values rather than against the removed JSON template.

Backfilling tests for the three existing tools is out of scope here and worth doing separately.

Prose added to the repo runs `python3 tools/idiolect_probe.py` before commit, per `CLAUDE.md`. This
spec clears every construction budget and holds one cadence finding, `pct_le5 = 20.7` against a
20.0 ceiling, that is a probe artifact: the markers of an ordered list parse as sentences, so `1.`
through `8.` above count as eight one-word sentences, and the figure without them is 13%. Stripping
ordered-list markers the way headings are already stripped is a small fix, a no-op on a manuscript,
and out of scope here.

## Non-goals, stated plainly

**`wiki` and `game` kinds are declared but ungated.** Every instrument in desk is prose-shaped:
cadence, sentence openers, 28 syntactic constructions, blind readers. A wiki has no cadence and a
game has no chapters. This spec lets a world *declare* those products so the manifest records what
exists; it applies instruments to `kind = "book"` only. Pulling the product-agnostic
layer out from under the prose craft is piece 3, and until it lands, declaring a game buys little
beyond a name.

**No orchestration.** `new_world.py` and `new_book.py` do mechanical setup and print what to run
next. Neither script drafts, and neither drives a stage. That is piece 2.

## The other two pieces

**Piece 2 — the runner.** Stages, gates, and the automation dial from one prompt to interactive.
Needs the contract in this spec to know what work exists.

**Piece 3 — the layering.** Separating world and story concerns (continuity, promise and payoff,
causal structure) from prose craft, so a wiki or a game can use the lower half. `continuity.py` is
already on the right side of that line and is the model for it.
