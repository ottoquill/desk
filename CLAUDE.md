# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

**Read [docs/where-we-are.md](docs/where-we-are.md) first.** It carries the current state, the
decisions in force and the defects already found. A session that skips it re-derives them, or
guesses.

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

The four decisions behind that statement are recorded in
[docs/superpowers/specs/2026-09-05-purpose-and-orientation-design.md](docs/superpowers/specs/2026-09-05-purpose-and-orientation-design.md). The behaviour rules
that keep a session pointed at it are in [.claude/rules/purpose.md](.claude/rules/purpose.md),
loaded every session.

## How it is put together

`desk/` holds Otto Quill's writing method, templates, and measurement tools, shared across every
book and series repo. A world repo references `desk/` as a git submodule and declares itself in
`world.toml`; desk reads that manifest and has no other window onto the world. Invocations take
`--world` and `--product` rather than assuming a layout.

The premise, from the README: the author does not persist between books, and the files do. A craft
lesson recorded inside a book repo is lost to the next book, and nine defect classes have recurred
because of it. Anything belonging to the author rather than to one book belongs here.

## Commands

The tools are stdlib-only Python 3, with no build step and no linter. There is a test suite, and
it runs from the repository root.

```bash
# The tests. Stdlib unittest. The Hugo build test skips itself where hugo is not installed.
python3 -m unittest discover -s tools/tests -t .

# The gate. Exit code 1 if any BAN fires or any RATION exceeds its budget.
python3 tools/idiolect_probe.py <product>/manuscript
python3 tools/idiolect_probe.py chapter.md            # a single chapter
python3 tools/idiolect_probe.py <dir> --baseline      # report rates, pass no verdict
python3 tools/idiolect_probe.py <dir> --json

# The description. Cadence, budgets, refrains, opener concentration, aridity screen.
python3 tools/prose_audit.py --world <world> --product <product>
python3 tools/prose_audit.py <product-a>/manuscript <product-b>/manuscript   # fingerprints

# Continuity. Runs four manuscript-only scans with no flags at all.
python3 tools/continuity.py <product>/manuscript --world <world>

# The world contract. Every tool below imports world.py to reach a world through the
# manifest; world.py has no CLI of its own.
python3 tools/canon.py --world <world>
python3 tools/new_world.py <path> --title "…"
python3 tools/new_book.py <world> --title "…" --slug <slug>
```

`idiolect_probe.py` gates and `prose_audit.py` describes. Hold that line: a budget verdict comes
from the probe's exit code, never from an agent reading the audit's output.

## This repo's prose is subject to its own gate

`python3 tools/idiolect_probe.py method/` exits non-zero today, and that is a recorded finding
rather than a defect awaiting cleanup. The deferred appositive `which is/was` runs at 16.92/10k
against a 6.0 budget in the documents that set the budget. The closing section of
[method/README.md](method/README.md) explains why it stays on the record.

Two consequences for edits here:

- Never loosen a budget to make `method/` pass. Budgets sit below the four-book measured median on
  purpose, and bans only accumulate (R3).
- Quoting a banned construction inside backticks, a blockquote, a fenced block, or a table is
  free; quoting it in italics is not — the probe strips only the first four forms. Six hits fire on
  the banned `precision frame` in `method/` today. Five are italicized quotations of the ban in
  `02-the-rules.md`, `04-blind-reading.md` (two), and `06-idiolect-ledger.md` (two) — real
  instances of the tool defect, since emphasis reads as citation to a person but not to a regex.
  The sixth is a live instance: `01-the-difference.md`'s own D8 paragraph uses `honest` — the very
  adjective its own E2 section records this construction recruiting once the literal phrase was
  banned. Left on the page; see `method/README.md`'s closing section for why.

Run the probe over prose you add to `method/`, and compare against the recorded baseline.

## Architecture: one argument, cross-referenced

The documents form a single argument with a shared numbering scheme, and a claim made anywhere
cites its origin. Preserve the identifiers when editing.

| Prefix | Meaning | Home |
|---|---|---|
| `E1`–`E5` | Measured evidence about the four-book corpus | [01-the-difference.md](method/01-the-difference.md) |
| `D1`–`D8` | Deficits against a human novelist | 01 |
| `A1`–`A6` | Advantages | 01 |
| `R1`–`R36` | The rules, each naming its deficit and its check | [02-the-rules.md](method/02-the-rules.md) |
| Stage 0–11 | Pipeline stages, each ending in a measured gate | [03-the-pipeline.md](method/03-the-pipeline.md) |
| `L01`–`L28` | Idiolect constructions with budgets per 10k words | `tools/idiolect_probe.py` |

The register of constructions lives in code, because a table in prose is not a gate.
[06-idiolect-ledger.md](method/06-idiolect-ledger.md) carries the evidence and the reasoning;
`idiolect_probe.py` carries the canonical budgets. Where they disagree, the code wins and the doc
wants updating.

For orientation read [method/README.md](method/README.md), then 01, then 02.
[method/reference/](method/reference/) is a 10,000-line research library rather than reading
material; enter it by search.

## The standard a change has to meet

The repo's own rules bind work done here as much as work done in a book.

**License nothing in prose; license with a number** (R2). An approval written in words reads to the
next book as encouragement, and the measured result was one construction escalating 2 → 15 → 52 →
60 across four novels. A new claim arrives with the count behind it.

**A plan is not a revision** (R28, E3). A defect closes when the detector that opened it returns
zero. An agent's report, a commit message and a ledger entry all asserted a fix whose sentence is
still on the page. Re-run the detector before recording anything as done.

**Ban constructions with free slots, never strings** (R12). A string ban recruits synonyms: the
banned `precision frame` stands at 32 instances across 23 of 39 chapters after the commit that
rationed it.

**Numbers stay on the diagnostic side of the wall** (R8). Handed numeric cadence targets, drafts
came back rated 3.0/10 for quality and last of six. Prohibitions go into a prompt; measurements
come back out of one.

**Keep the refutations.** Several documents carry results that contradict what the author expected,
among them a human practice tested and rejected in [05-instruments.md](method/05-instruments.md)
and a failed experimental arm in [04-blind-reading.md](method/04-blind-reading.md). Preserve them
under edit, and add to them.

## Instrument separation

Four instruments, separate jobs, and the commonest way to waste them is to let one do another's
work (R22, [05-instruments.md](method/05-instruments.md)):

- **Measurement** nominates suspects and never convicts. The aridity screen has good recall and
  poor precision, since stakes are invisible to it, so a chapter is never revised on a metric
  alone.
- **Blind readers** adjudicate experience, and get the prose alone: no outline, no bible, no
  thesis, no statement of what a chapter is for (R23). Score where they stopped and discard how
  they described it (R24).
- **Briefed specialists** adjudicate truth, take one dimension each, and are prompted to refute.
  Praise from a critic you instantiated is information about your prompt (D7).
- **The author** decides.

[templates/critic-briefs.md](templates/critic-briefs.md) is held fixed across books on purpose.
Editing it makes yields from different books incomparable (E4).

## Conventions

- `tools/` is stdlib-only. A dependency breaks the assumption that a subagent with no environment
  can run the gate.
- `templates/` gets copied into a book at its start, living at `<product>/editorial/`. A new book's
  profile inherits every prior ban and tightens at least one budget the last book overused
  (R1, Stage 0).
- The cross-book used-names registry is not a file to populate; it is read straight out of canon.
  `continuity.py --world <world>` sources it from every character page under the world's canon
  directory and reports matches as NAMES ALREADY IN CANON, not CROSS-BOOK NAME REUSE — that label
  is reserved for an explicit `--names` registry file, since a manuscript matching its own world's
  canon is expected rather than reused. Either way the check is only as complete as its source.
- Commit messages carry the reasoning and the numbers in full paragraphs. `git log` shows the
  shape.
