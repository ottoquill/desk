# The World Contract and Canon

*Design spec. Makes `desk/` world-independent infrastructure, gives it an entry point, and makes
canon the substrate a world is built on.*

**Status:** revised 2026-09-02 after review; implementation has yet to begin.
**Scope:** piece 1 of 3. The remaining pieces are named at the end.

---

## The problem

Three defects.

**desk knows about dependent books.** Path coupling to `<book>/manuscript` and `<book>/editorial/`
runs through thirteen files, including all four templates. `names.json` is worse: a registry keyed
by which book used which name, holding per-book state inside shared infrastructure.

**There is no entry point.** The repo carries 39 rules, 12 pipeline stages and a 10,000-line
research library, and never says how to start. Grepping for a creation path returns three
incidental phrases. Stage 0 says a book "begins by pulling from `desk/`" and lists what it pulls,
yet no procedure anywhere follows it.

**The wiki was filed as an output.** The first draft of this spec treated books as the primary
product and listed a wiki as a kind that could be declared but bought little beyond a name. That
is backwards. Every world has a rich wiki and supporting material, and those underpin the world
rather than descending from it. Canon is the substrate; a book is one thing drawn out of it.

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

**desk knows kinds; the world names instances.** This holds at two levels. desk ships what a book
is and which instruments apply to one; it also ships what a character, place or faction requires.
The world supplies names, paths and content. Names belonging to a world never appear anywhere
inside desk.

**Reusable is not the same as universally needed.** A Hugo theme is world-independent — it carries
no world's nouns and every world with a wiki wants the same layouts — so it belongs in desk even
though a world that ships only a game will never mount it. The test for desk is reusability across
worlds, never necessity for all of them.

**Backward-looking derived data stays; forward-looking state leaves.** The `L01`–`L28` budgets are
constants measured on a past corpus, and they describe the model's attractor rather than one
author's quirks: any world drafted by the same model family lands in the same place. They stay.
Whatever accumulates as new work is produced belongs to the world.

**Config is human-owned and machine-read. State is machine-owned and machine-read.** Config is
TOML, state is JSON, and no tool rewrites a config file.

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
title  = "…"
desk   = "desk"                     # submodule path
canon  = "content/canon"            # canon pages, Hugo content
schema = "canon/schema.toml"        # optional: extends desk's base schema

[[products]]
id   = "…"
kind = "book"
path = "books/…"
```

Every path has a default, so a conventional world declares its products and little else. Products
are declared rather than discovered: letting desk guess what counts as a product is the failure of
the pure-convention alternative, and it would put a world's shape back inside desk.

### Conventional layout

```
world/
  world.toml
  desk/                            submodule
  content/canon/
    characters/…md                 canon pages: TOML front matter + prose
    places/…md
    factions/…md
  canon/schema.toml                optional world-specific kinds
  books/<slug>/
    editorial/voice-profile.toml
    editorial/style-sheet.md
    editorial/promise-ledger.md
    editorial/critic-briefs.md
    manuscript/
    invented.json                  per-wave machine state, pre-promotion
  hugo.toml                        mounts desk/hugo as a module
```

### What each side owns

| | desk | world |
|---|---|---|
| Method, rules, pipeline | yes | |
| Instruments and budgets | yes | |
| Templates | yes | |
| Canon **schema** — the kinds | yes | |
| Hugo module — archetypes, layouts, shortcodes | yes | |
| Defect **classes**, regression suite | yes | |
| Canon **pages** — the instances | | yes |
| Bibles, outlines, spines | | yes |
| Manuscripts and other media | | yes |
| Voice profile for a product | template only | filled copy |
| Defect **instances** | | yes |

The regression split is the subtle one. A defect class (over-claim, fake rigor, self-priming) is a
failure mode of the author and ratchets in desk. A defect instance belongs to the work that
carried it and ratchets in the world.

## Canon

### The page

A canon page is Markdown in Hugo's native shape: TOML front matter carrying the checkable facts,
prose in the body carrying the lore.

```markdown
+++
kind     = "character"
id       = "sable"
name     = "Sable"
pronouns = "she/her"
factions = ["salvagers"]
+++

Sable came up through the yards, which is where she learned …
```

One artifact, three consumers: Hugo renders it, the canon validator checks it, and
`continuity.py` reads its front matter as the typed fact store. Nobody authors lore in JSON, and
the front matter earns the gate its facts without a parallel data file to keep in step.

**Front matter is TOML, delimited `+++`.** Types are unambiguous, `tomllib` parses it from the
stdlib, and it is one of Hugo's native forms. Manuscript chapters keep their existing `---` and are
not migrated: they are not Hugo content, they carry two or three author-facing fields rather than
checkable facts, and churning the manuscript format to match would buy consistency and nothing
else. Both parsers learn to accept either delimiter so a world may unify if it wants to.

### The schema

desk ships `canon/schema.toml` declaring base kinds and their fields — **character, place,
faction, event, artifact, term, relationship** — with `id` and `name` required everywhere and `id`
unique across the world.

A world extends the base rather than replacing it, through the optional `schema` key in
`world.toml`. A hard-SF world adds `technology`; a game world adds `quest`. Without extension desk
would dictate what a world may contain, and that is this spec's own coupling problem pointing the
other way.

### Relationship is a kind, not a field

Six of the seven kinds are nodes. `relationship` is an edge, and it earns its own page because the
alternative — a list of names on each character — cannot hold what a relationship actually carries.

The rationale is Orson Scott Card's, in *Characters & Viewpoint* (1988), where the concept has a
section heading of its own in chapter 1: **network**. Card describes the self as "a kind of
network, many threads connecting us to many different people, who are always shifting," and states
the consequence directly — "we are different people in different relationships." The taciturn
fellow at work is a cut-up at the bowling alley. A character who sounds the same to everyone has no
network, and the four-book finding says that flat default is where this author reverts without
something holding it open.

Card's *network* is the graph; a page is one edge of it. Both halves live in the one file, since
two cross-referencing character pages give the same relationship two homes and let them drift.

```markdown
+++
kind    = "relationship"
id      = "sable-toro"
name    = "Sable and Toro"
between = ["sable", "toro"]

[sable_to_toro]
never_says   = "his first name"
register     = "drops contractions, sentence length falls"
routes_around = ["the yards"]

[toro_to_sable]
never_says = "that he was there"
register   = "over-explains, may be interrupted"
+++

They have not been in the same room since …
```

**The per-direction fields are behavioral, never adjectival** — R9a applied to a new kind. "Warm
but guarded" is exactly the specification four style sheets proved inert. What earns a slot is
mechanical and checkable: what A never says to B, which register A drops, who may interrupt whom,
which topic A routes around, whose sentences shorten.

Two things follow that this spec does not build. Naming the addressee is a **dropped candidate** —
[02-candidate-rules.md](../../../method/reference/02-candidate-rules.md) formalises declaring to
whom a narration is addressed, with an omission list and a gate, and it never reached
[02-the-rules.md](../../../method/02-the-rules.md). Promoting it, extended from narrator-to-reader
to character-to-character, is a change to the constitution and belongs in its own commit. And Card
names the phenomenon without measuring it, which is the usual shape here: the **interlocutor
test** — partition a character's dialogue by addressee, mask the names, and check whether the sets
separate above chance — is piece 3.

### Two fact lifecycles

Canon and invention are different and the first draft of this spec conflated them.

**Canon** is authored deliberately, curated, and durable. It is the wiki, and it exists before any
product does.

**Invented** is what drafting agents return under R16: concrete details a chapter introduced that
later chapters must honour. These merge into `invented.json` per wave, machine-written, and get
gated for contradiction before the next wave drafts.

Surviving inventions are **promoted** into canon pages at harvest. That promotion is what makes
the wiki accumulate rather than merely describe, and it is the step the first draft missed
entirely. The promotion tooling is piece 2; the page shape and the gate that admits an invention
are here.

### Validation

**`tools/canon.py`** — loads canon pages, validates front matter against the schema, checks that
ids are unique and that every cross-reference resolves, and emits the fact store `continuity.py`
consumes. Replaces the hand-maintained `facts.json` of the previous draft as canon's source of
truth.

The used-names registry dissolves into this. Every character page carries a name, so
`continuity.py --names` reads canon instead of a separate file that somebody has to remember to
update. `names.json` is deleted for a better reason than the one the first draft gave.

## What desk ships for Hugo

A Hugo module at `desk/hugo/`, mounted by a world's `hugo.toml`:

- **archetypes** — one per base kind, so a new canon page starts with its required fields present.
- **layouts** — one per kind, rendering front matter as a fact panel above the prose body.
- **shortcodes** — cross-references between canon pages, fact tables, timeline views.
- **a config fragment** — the mounts and output settings a canon wiki needs.

A world that renders no wiki mounts none of it. A world that wants its own look overrides layouts
in the usual Hugo way, since a module is overridable by design.

## Changes to desk

1. **Delete `names.json`.** Superseded by canon.
2. **`tools/world.py`** — stdlib module that loads `world.toml`, applies defaults, resolves paths.
   Every other tool reaches the world through it.
3. **`tools/canon.py`** — schema validation, id uniqueness, cross-reference integrity, fact-store
   extraction.
4. **`canon/schema.toml`** — the seven base kinds, `relationship` among them.
5. **`desk/hugo/`** — the module: archetypes, layouts, shortcodes, config fragment.
6. **`tools/continuity.py`** learns `--world`, taking facts and names from canon. The explicit
   flags stay and win when both are given. This tool and `prose_audit.py` both learn to strip
   `+++` front matter alongside `---`.
7. **`tools/prose_audit.py`** learns `--world` plus a product id, and reads a **TOML** profile via
   `tomllib`. `templates/voice-profile.json` becomes `voice-profile.toml`, losing nine `_comment`
   keys and a 431-character line to real comments. No book consumes the JSON form, so the change
   breaks no existing consumer.
8. **`tools/new_world.py`** — scaffolds a world: manifest, canon skeleton, `hugo.toml` with the
   module mounted, and the submodule command printed rather than run.
9. **`tools/new_book.py`** — adds a book product: copies templates into `editorial/`, creates
   `manuscript/`, and **appends** a `[[products]]` table to `world.toml`. Appending at end of file
   preserves every comment, so the rule that no tool rewrites config holds.
10. **`method/00-starting-a-world.md`** — the missing entry point. Submodule, manifest, canon,
    first product, then the ordered path from concept to draft with the gate at each stage.
11. **Decouple the docs.** `<book>/manuscript` and `desk/tools/...` become world-relative
    throughout `method/` and `templates/`. `CLAUDE.md` stops saying desk is checked out alongside
    a book.

## Testing

The repo has no tests. This spec adds the first ones, as stdlib `unittest` under `tools/tests/`,
run by `python3 -m unittest discover tools/tests`:

- **`world.py`** — defaults applied to a minimal manifest; explicit paths override; an unknown
  product id fails loudly; a malformed manifest reports the file and the reason.
- **`canon.py`** — a page missing a required field fails; duplicate ids fail; a dangling
  cross-reference fails; a valid set extracts the expected fact store; a world schema extends the
  base rather than replacing it; a `relationship` whose `between` names an absent character fails,
  and both directions survive extraction.
- **`new_world.py`** and **`new_book.py`** — scaffold into a temp directory, then assert the result
  loads through `world.py` and that the appended manifest still parses. Round-trip, not shape.
- **`prose_audit.py`** — a TOML profile yields the budget map the audit expects, asserted against
  literal values rather than against the removed JSON template.

Backfilling tests for the three existing tools is out of scope here and worth doing separately.

Prose added to the repo runs `python3 tools/idiolect_probe.py` before commit, per `CLAUDE.md`.

## Non-goals

**Promotion tooling.** The gate that admits an invention is specified here; the machinery that
rewrites canon pages from surviving inventions is piece 2.

**Game as a gated kind.** A world may declare one and desk will carry it in the manifest, but no
instrument here knows what a game is. Unlike the wiki, that stays a name for now.

**No orchestration.** The scaffolds do mechanical setup and print what to run next. Neither
script drafts, and neither drives a stage.

## The other pieces

**Piece 2 — the runner.** Stages, gates, promotion, and the automation dial from one prompt to
interactive. Needs this contract to know what work exists.

**Piece 3 — instruments beyond the manuscript.** Smaller than the first draft assumed. Lore pages
are prose written by the same model and carry the same 28 constructions, so `idiolect_probe.py`
and `prose_audit.py` already apply to canon bodies and mostly need pointing at them. What genuinely
needs building is structural: promise and payoff, causal in-degree, continuity across products
rather than within one, and the **interlocutor test** — partition a character's dialogue by
addressee, mask the names, and check whether the sets separate above chance. That last one reuses
the function-word cosine that found E1, pointed at a new unit, so it is a smaller build than it
sounds.
