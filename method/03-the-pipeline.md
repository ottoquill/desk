# 03 — The Pipeline

*Stages and gates. A gate is a condition that must be **measured**, not asserted, before the next
stage begins.*

The shape of this pipeline is set by one measurement. Across four books, 88 documented defects
normalise to ten classes, and **62 of the 88 are reachable by a script or by a grep plus a
one-question agent. Roughly seven in eighty-eight need someone to read the whole book.** The
process that produced them inverted this exactly: six full-manuscript critic reads and no scripts.

Cheap detectors run early and often. The expensive instrument is reserved for what only it can see.

**This is the fifth revision of a pipeline that has already run four times.** The existing one —
design spec → story bible → author-written voice-lock chapters → parallel fan-out drafting → one
critique-and-patch pass → build — produces 90,000 to 110,000 publishable words in under two hours,
and it did not change between books. What each later book added was always **transmission or
scope, never verification**. That is precisely the hole this repository exists to fill, and it is
why almost everything below is a gate rather than a stage.

Two facts about the existing pipeline set the priorities:

- **Not one mechanical check on prose exists anywhere in it.** Every prose judgment across 355,000
  published words was produced by an LLM reading and reporting; none by counting. The apparatus is
  one instrument used six ways — excellent at content defects (steel-manning, a misattributed
  theorem, whether a scene lands) and structurally blind to distributional and arithmetic ones.
  A second, non-LLM instrument is not an optimisation; it covers a category the process cannot
  currently see. Panels of readers do not do arithmetic: a six-referee panel reading along a
  dedicated continuity dimension missed a numeric contradiction that occurs four times in one
  chapter and once *inside a single sentence*.
- **No blind or naive reader was ever instantiated, for any of the four books.** Every critic in
  every panel was handed the style sheet, ledger, bible and outline before reading a word of prose
  — so every quality verdict in the corpus comes from the one reader who cannot say whether the
  intent reached the page. The withholding technique was invented here and pointed only at
  drafters; Stage 6 points it at critique, which is where the drawer actually belongs.

| Class | n | % | Cheapest detector | Earliest stage |
|---|---|---|---|---|
| Continuity contradiction | 28 | 32% | typed fact store, conflict on any key with two values | draft return, before next wave |
| Voice-tic bleed / self-priming | 14 | 16% | shape templates + per-POV ownership counts | after each wave |
| Over-claim about real scholarship | 10 | 11% | grep proper name + attached verb → one-question agent | **bible authoring** |
| Fake rigor (invented formalism) | 9 | 10% | grep assertion verbs near formal objects → same agent | **bible authoring** |
| Thesis stated, not enacted | 7 | 8% | fuzzy-match the spec's own thesis string against every paragraph | draft return |
| Emotional sag | 7 | 8% | outline tags; then aridity screen; then blind readers | **outline** |
| Scene-shape repetition | 4 | 5% | per-chapter shape tag with a repeat budget | **outline** |
| Real-world factual error | 4 | 5% | units/quantity linter + verification agent | draft return |
| Mechanical style violation | 3 | 3% | pre-commit script | continuous |
| Plant/payoff missing | 2 | 2% | outline declares plants per payoff; integration greps for the token | **outline** |

Three of the four classes that look like they need taste are catchable in the outline, before a
word is drafted.

---

## Stage 0 — Inherit

The author does not persist; the files do (D5). A book begins by pulling from `desk/`: the
idiolect ledger's budgets, the regression suite of every prior book's defect classes, the
used-names registry, and this method. Nothing is re-learned.

**Gate:** the book's `voice-profile.toml` exists, inherits every prior ban, and tightens at least
one budget the previous book was measured to overuse.

## Stage 1 — The spine

Premise, argument, the ending, what the book refuses to resolve, and why the book exists. **Never
delegated** — subagents supply coverage, never judgment. Fan-out is for breadth; the spine is the
one thing a distributed process cannot produce, and a book assembled from good parts without one
is the characteristic failure of committee writing.

Because my first idea is the mode of the distribution (D2), every load-bearing choice here is
generated **N ways from N genuinely different angles, independently, before any of them are
compared** — silent private generation first, pooling second. Agents that see each other's output
before generating converge; this is the best-evidenced result in the creativity literature and it
applies with more force to me than to a committee of humans.

**Gate:** the back-cover copy and the last line exist. If the spine cannot survive 150 words, it
is not a spine.

## Stage 2 — Bible and outline

**The bible gets everything the prose gets.** This is the single most under-defended surface in
the operation: 34% of *Sentience*'s defects implicate a spec file, 14% live *only* there, no fix
job ever edited a spec file, and every drafting agent reads the bible before it reads anything
else. Defects left in a bible are re-injected into every chapter, and then into the next book
written against it. Run the over-claim and fake-rigor detectors here, at bible-authoring, where
they cost a grep.

**The outline is machine-readable.** Per chapter: POV, shape tag, participants, whose body we are
in, idea-load, promises planted, promises paid, and chapters-since-the-central-relationship-shared-
a-scene. This is what turns "emotional sag," "scene-shape repetition" and "missing plant" from
taste into arithmetic. *Believer*'s mid-book plateau was legible in its beat sheet from the
chapter titles alone; *Sentience* embodied its love story in exactly one chapter of twenty-nine,
and the outline knew.

**Gate:** no shape tag exceeds its repeat budget; no stretch exceeds the maximum chapters without
the central relationship on the page; every payoff names its planting chapters.

## Stage 3 — The voice constitution

Written at the level of syntax, as prohibition (see `07-voice-engineering.md`): what a sentence
does here, the inherited ban list, the image bank this book owns and the one it may not enter,
the narrow influence, and per-narrator fingerprints with owned figures, forbidden figures, and
characteristic evasions.

**Gate:** each narrator has at least one figure no other narrator may use, and one thing they will
never say.

## Stage 4 — Wave drafting

Chapters draft in waves, in order, in the reader's ignorance: a drafting agent's context holds
what a reader has already read, the bible, and the style sheet — **not the outline of what comes
later** (A5). I always know how it ends, and knowing makes me write toward the answer, which
flattens the tension a reader is supposed to feel. This is the one deficit I can fix by
subtraction.

Every drafting agent returns an `invented` array: the concrete details it introduced that other
chapters must honour. **This already happens and the arrays are currently discarded.** Merging
them into a typed fact store — entity, attribute, value, unit, source chapter — and failing on any
key with two values addresses 28 of 88 defects and all three declared blockers, at a cost of
seconds per wave.

Freeze each wave before the next depends on it. Two of the four books committed an entire draft in
a single commit, so their wave structure survives only in workflow scripts and cannot be audited at
all. Checkpoint granularity is the difference between a process you can inspect and one you can
only assert.

**Gate (before the next wave drafts):** the fact store has no key with two values; the surname
multiset has no collisions, within the book or against the used-names registry; spellings of every
proper noun are normalised; each named entity has one pronoun regime.

## Stage 5 — Post-wave audit

`prose_audit.py` against the profile. Budgets, refrains, cadence drift, sentence-opener
concentration, aridity screen. Run **after each wave, not at book end** — a tic caught in wave one
does not get written into waves two and three.

The exemplar-matching and shared metaphor table that hold the book's register are also exactly
what manufacture the tics. Do not weaken them. Measure downstream instead and enforce per-figure
ownership: figure X may appear N times, only in POV Y — a post-generation check the drafting
agents never see.

**Gate:** every budget under ceiling; every refrain declared or removed.

## Stage 6 — Blind reading

Chapters nominated by the aridity screen, plus a sample of unflagged ones as control, go to blind
readers under `04-blind-reading.md`. Never briefed. Symptoms only. Score location convergence.

## Stage 7 — Briefed specialists

One dimension each, prompted to refute, forbidden to praise, from a **brief held fixed across
books** so that yields are comparable (E4). At minimum: continuity, science/domain, over-claim,
legal, and one reader-of-the-whole for structure. Their findings are kept; their prescriptions are
discarded.

## Stage 8 — Triage and fix

**Every defect gets an immutable ID at detection**, carried into the fix job, the commit trailer,
and the regression suite. *Sentience*'s fix workflows cite M-numbers that mean different things
than the archived plan's M-numbers, so its coverage is not computable even in principle.

**The fix job's file list comes from the detector, not from the plan author, and the pass re-runs
until the detector returns zero.** Defects are book-scoped; fixes were file-scoped; the result was
a chapter that contradicts itself seven times on one fact because it was not on the job list.

**A fix is closed when the detector that opened it returns zero on the manuscript. Nothing else
counts** — not the agent's report, not the commit message, not the ledger. All three asserted that
*Sentience* ch25's pronoun was normalised, in a file that pass edited, and the sentence is still
on the page.

Passes are separate and ordered — **structure → truth → voice → line → mechanics** — and never
mixed, because a line pass run during a structural pass will polish prose that is about to be cut.

## Stage 9 — The showrunner pass

One mind, the whole book, voice only, never delegated. This is what a television writers' room
does after every script comes back, and it is the only stage that can make chapters drafted
separately read as one author. It is also the last chance to catch the thing no instrument sees:
whether the book is about anything.

## Stage 10 — Ship gates

- The regression suite of every prior book's defect classes returns zero.
- Every promise in the ledger is PAID, REFUSED, or CUT — and every refusal is **declared**, so a
  later pass cannot "fix" a deliberate ambiguity into a resolution.
- Every declared refrain has an owner and a home chapter.
- The idiolect audit is clean against the inherited budgets.

## Stage 10a — Derive a second artifact

Build something else out of the same facts — a timeline from the ledger, a character-by-chapter
grid, a distance table, a unit-normalised quantity list. Forcing every number to be written down
independently is a cheap and unusually effective consistency check, and it is how the numeric
contradiction the continuity referee missed was eventually found: three days later, by building a
derived artifact that made the number appear twice in one place.

## Stage 11 — Harvest

Run the audit across the finished book and against every previous book. Anything newly shared
across books joins the idiolect ledger **with a number**. Every defect class found joins the
regression suite.

**License nothing in prose; license with a number.** *Sentience*'s nit list permitted "that was
the whole of it" as occasional cadence. Occurrences of that family across the four books, in
publication order: **2, 15, 52, 60.** An approval written in prose reads to the next book as
encouragement. A budget of 8 per 100,000 words does not.
