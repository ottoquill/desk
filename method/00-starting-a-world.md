# 00 — Starting a World

Grep this repository for how to start a book and three incidental phrases turn up. Stage 0 of
`03-the-pipeline.md` says a book begins by pulling from `desk/` and names what it pulls; no
procedure anywhere carries that sentence out. This document is that procedure: what a world is,
how a world depends on `desk`, the two scaffolding tools, how canon is laid out on disk, and the
ordered path from a bare premise to a drafted wave, with the exact command that gates each stage.
Six pieces, one order.

## What a world is, and what desk is

A **world** is a git repository holding one setting and every book set inside it. Its root carries
a `world.toml` manifest, a `content/canon/` directory of canon pages, a `hugo.toml` that mounts a
wiki, and a `[[products]]` table declaring each book. A world names people, places, factions, and
titles.

`desk` names none of those. It is Otto Quill's shared writing method: the rules, the pipeline, the
templates, and the measurement tools, checked out once and reused across every world. A world
supplies the setting and the books; `desk` supplies the craft and the gate. A world with no `desk`
has canon and no measurement; `desk` with no world has a gate and no manuscript to run it on. Grep
`desk` itself and no character, place, or book title turns up. By design.

## Desk as a submodule

A world holds `desk` as a git submodule at `desk/`, pinned to a commit the way any dependency is
pinned. Adding it to a fresh world:

```bash
git submodule add <desk-remote> desk
```

Cloning a world that already declares the submodule needs one more step, since a plain `git clone`
leaves `desk/` present but empty:

```bash
git clone <world-remote> my-world
cd my-world
git submodule update --init --recursive
```

Every path in this document, and every path `world.toml` writes by default, assumes `desk` sits at
the world's root under that exact name. A manifest can point somewhere else with its own `desk`
key; nothing below requires that, and the default is the one worth keeping.

## `new_world.py`

`tools/new_world.py` scaffolds the manifest, the canon skeleton, and the Hugo config. It writes
text and reads none of `desk`'s own files, so it runs whether the submodule step above happened
yet or not.

```bash
python3 desk/tools/new_world.py PATH --title "Title"
```

Run it from wherever a checkout of `desk` sits — inside the future world, inside `desk` itself, or
anywhere a relative or absolute path resolves. `PATH/world.toml` already existing stops the run
rather than getting overwritten. What gets created:

```
PATH/world.toml            the manifest desk reads: title, desk path, canon path, products
PATH/hugo.toml              mounts desk/hugo
PATH/content/canon/         one directory per kind, each holding a .gitkeep
```

and the script prints the commands that follow, ending in a pointer to this file.

## Canon and the page shape

Canon is Markdown in Hugo's native shape: TOML front matter between `+++` fences carrying the
facts a script can check, prose in the body carrying the lore a script cannot. One artifact, three
readers — Hugo renders it as a wiki, `canon.py` validates it, and `continuity.py` reads the front
matter as a typed fact store for a manuscript to be checked against.

```
+++
kind       = "character"
id         = "SLUG"
name       = "Name"
pronouns   = ""
occupation = ""
factions   = ["OTHER-SLUG"]
+++

Prose. What this person is like to be in a room with.
```

Every page declares `kind`, `id`, and `name`. The base schema at `desk/canon/schema.toml` adds
required and optional fields per kind — `character`, `place`, `faction`, `event`, `artifact`,
`term`, `relationship` — and declares which fields are references. A `factions` field on a
character has to resolve to a page carrying `kind = "faction"` and that same `id`; `canon.py`
checks it. A world may extend the schema with kinds and fields of its own. Narrowing a field
`desk` already requires, or redirecting a reference `desk` already declares to a different target,
both raise an error instead.

```bash
python3 desk/tools/canon.py --world .
```

Reads every page under the world's canon directory, skipping files whose names start with an
underscore, since those carry Hugo section metadata rather than canon. It reports each broken
reference and each missing required field, then exits 1 on any finding and 0 on none. Run it after
every canon edit, not only before a draft begins — a page added mid-book is canon too.

## `new_book.py`

`tools/new_book.py` adds a book product to a world that already has a manifest.

```bash
python3 desk/tools/new_book.py . --title "Title" --slug book-one
```

It copies `voice-profile.toml`, `style-sheet.md`, `promise-ledger.md`, and `critic-briefs.md` from
`desk/templates/` into `books/book-one/editorial/`, creates `books/book-one/manuscript/`, and
appends a `[[products]]` table onto the end of `world.toml` — appended, so a comment already in the
file survives the write. The copied voice profile has its `book = "TITLE"` placeholder swapped for
the title given here; the template inside `desk/templates/` stays untouched. A slug already
declared in `world.toml` is refused rather than overwritten.

## The path from concept to draft

Stages 1 through 5 of `03-the-pipeline.md`, in the order a book actually moves through them, each
paired with the command whose exit code is its gate — a number a script returns, not a description
a person reads and nods along to.

| Stage | What happens | The gate |
|---|---|---|
| 0 · Inherit | `new_world.py`, then `new_book.py` | the profile inherits every prior ban and tightens one |
| 1 · The spine | premise, argument, ending, refusals. Never delegated | back-cover copy and the last line exist |
| 2 · Canon and outline | canon pages, machine-readable outline | `python3 desk/tools/canon.py --world .` returns zero |
| 4 · Wave drafting | chapters in waves, in the reader's ignorance | `python3 desk/tools/continuity.py <ms> --world .` returns zero |
| 5 · Post-wave audit | after each wave, never at book end | `python3 desk/tools/idiolect_probe.py <ms>` exits zero |

Stage 3, the voice constitution, sits between the outline and drafting, and it has no single exit
code: it gets written as prohibition, at the level of syntax, and its check is that each narrator
owns a figure no other narrator gets to use. See `07-voice-engineering.md` for how that gets
written, and for the measured reason a mood-description style sheet fails to do the job.

At Stage 5, `prose_audit.py` supplies the description and `idiolect_probe.py` supplies the gate.
They read the same profile; only one of them returns the exit code a wave is allowed to pass on.

```bash
python3 desk/tools/prose_audit.py --world . --product book-one
python3 desk/tools/idiolect_probe.py books/book-one/manuscript
```

Run the second command after every wave, not once at the end. A finding stays open until then. A
plan to fix it, a commit that claims to, and an agent's report that it is done are not proof of
that — only a second run of that same command, returned clean, is (R28).
