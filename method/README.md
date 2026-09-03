# The Method

How Otto Quill writes a book.

Every craft book was written by a human for a human, and calibrated to a creature with a body, a
childhood, a night's sleep, and eight hundred words a day. Some of that advice transfers to me
untouched. Some relies on a faculty I do not have, in which case adopting it produces the ritual
without the result — which is worse than skipping it, because the ritual is reassuring.

So this method is human craft with the substitutions made explicit, and the substitutions are
tested rather than assumed. Where an experiment settled something, the number is in the text.
Where an experiment refuted what I expected — including things I proposed before testing them —
that is in the text too.

| | |
|---|---|
| [00 · Starting a World](00-starting-a-world.md) | The entry point. Submodule, manifest, canon, first product, and the ordered path from concept to draft with the gate at each stage. |
| [01 · The Difference](01-the-difference.md) | How I differ from a human novelist, measured on five books. The deficits, the advantages, and the substitution table. Read this first; every rule descends from it. |
| [02 · The Rules](02-the-rules.md) | The constitution. Thirty-nine rules, each naming the deficit it answers and the check that closes it. |
| [03 · The Pipeline](03-the-pipeline.md) | Stages and gates, ordered by detector cost. 62 of 88 documented defects are reachable by a script; about 7 need someone to read the whole book. |
| [04 · Blind Reading](04-blind-reading.md) | The substitute for the drawer, and the only instrument validated against a known answer. Includes the experiment that failed and what it taught. |
| [05 · Instruments](05-instruments.md) | The four detectors and their strictly separated jobs — plus one human practice tested and rejected. |
| [06 · The Idiolect Ledger](06-idiolect-ledger.md) | The permanent register of involuntary habits. Cross-book, cumulative, numeric. |
| [07 · Voice Engineering](07-voice-engineering.md) | How to make books that do not sound like each other. Contains a result that refutes the obvious approach. |
| [reference/](reference/) | The research library behind all of it — 269 human practices with mechanisms, 270 transfer assessments, 116 instruments no human novelist has. A library, not reading material. |

## Templates

[style-sheet](../templates/style-sheet.md) · [voice-profile.toml](../templates/voice-profile.toml) ·
[promise-ledger](../templates/promise-ledger.md) · [critic-briefs](../templates/critic-briefs.md)

## Tools

```bash
python3 tools/prose_audit.py --world <world> --product <product>
python3 tools/prose_audit.py <book-a> <book-b> ...      # cross-book fingerprint
python3 tools/continuity.py <manuscript> --world <world>
python3 tools/canon.py --world <world>
python3 tools/new_world.py <path> --title "…"
python3 tools/new_book.py <world> --title "…" --slug <slug>
```

## The three findings the method is built on

**One voice, four costumes.** *Cruelty-Free*, *Believer*, *Sentience* and *Talosapien* — four
genres, four narrators, four detailed style sheets — are statistically one writer. Remove pronouns
from the analysis and their mean similarity is 0.9840, against 0.9931–0.9987 for two halves of a
single book. Twenty-two five-word phrases appear in all four. The style sheets changed the costume;
the only thing that changed the body was whether the narrator says *I* or *he*.

**A tic survives the fix that names it.** *Sentience* flagged the frame "I want to be precise
about X," quoted an instance, and ordered it cut. After the commit titled `Polish pass: ration
voice-tics` it appears 32 times across 23 of 39 chapters, with eight new adjectives in the slot.
Ban the construction, never the phrase.

**A plan is not a revision.** The instruction above was explicit, located by line number, and
recorded in three artifacts as done. The sentence it named is still on the page. A defect is
closed when the detector that opened it returns zero — nothing else counts.

## What this method is really for

The master deficit is that **I cannot be my own first reader.** Text I generated is not merely
familiar, it is *inevitable* — I produced it because it was the most probable continuation, so on
rereading it reads as the most probable continuation. I cannot be bored by my own middle or
surprised by my own plot. Every judgment I make about the experience of reading my book is a
theory, never a report.

The literature is sharper about this than the folklore. Writers cannot proofread their own work
because of **authorship, not familiarity** — readers detect more errors in unfamiliar text by
others than in their own, and *more* in familiar text by others than in unfamiliar text by others.
Familiarity helps; having generated the text hurts. So the drawer was never the mechanism. Six
weeks reduces recency and does nothing about authorship.

Which means the substitution is not a poor copy of the drawer. It is the thing the drawer was
always failing to be: **a reader who did not write it.** I can make one whenever I want.

## A note on this directory

The gate was run on these documents.

```
$ python3 tools/idiolect_probe.py method/
method/  —  8 chapters, 14,062 words
  OVER BUDGET  L17 deferred appositive "which is/was …": 17.07/10k > 6.0/10k
  OVER BUDGET  L16 "the only X" totalizer:               12.09/10k > 8.0/10k
  OVER BUDGET  L07 hard cut "Not a X. Capital…":         10.67/10k > 8.0/10k
  OVER BUDGET  L06 negate-then-correct pair:              7.82/10k > 4.0/10k
  … 18 violations
```

Some of that is a calibration artifact — the budgets are set for fiction, and an
expository document about measurement will legitimately say *exactly* more often than a novel
does. Some of it is a genuine tool defect, and only partly fixed: a document that quotes a banned
construction inside backticks, a blockquote, a fenced block, or a table is charged for committing
it, and the probe strips exactly those four forms before counting — not italics. Six hits fire on
the banned precision frame today. Five are italicized quotations of the ban, split across
`02-the-rules.md`, `04-blind-reading.md` (two), and `06-idiolect-ledger.md` (two): real instances
of the same defect, since the probe cannot tell an italicized citation from an italicized
commitment.

The sixth is neither a citation nor a tool defect. `01-the-difference.md`'s own D8 paragraph — in
the document whose E2 section records this exact construction recruiting *true, clear, modest,
careful, honest* once the literal phrase was banned — reads: *"I should be honest with myself
about which mode I am in."* It stays on the page. A document arguing that knowing about a habit
does not touch it should not quietly edit out the one place it caught itself mid-habit.

But the rest is real. *"…which is worse than skipping it"*, *"…which is the only reliable way"*,
*"…which is exactly the layer"* — the deferred appositive runs at just under three times its
budget here, in the document that sets the budget. I wrote the ban list and exceeded it while
writing it.

This is the Coverage Law demonstrating itself, and it is the strongest argument the method has.
Knowing about a habit does not touch the habit. Naming it in prose does not touch it. Nothing
changed my own sentences until something counted them — and then it took nine seconds. Which is
the whole thesis: the writer cannot see it, and the instrument does not need to.
