# 05 — Instruments

*Revision is overwhelmingly a detection problem. Sommers's finding about student writers — that
they revise at the wrong grain because the wrong grain is the only one they can perceive — is the
whole of my situation, since the defects I most need to find are the ones my authorship hides
from me. Teaching myself to fix what I cannot see is wasted effort. Building instruments that see
is the work.*

Four instruments, with strictly separated jobs. The commonest way to waste them is to let one do
another's job.

| Instrument | Sees | Blind to | Verdict power |
|---|---|---|---|
| **Measurement** (`tools/prose_audit.py`) | repetition, cadence, budgets, aridity | stakes, meaning, whether anything is at issue | **nominates only** |
| **Blind readers** (`04-blind-reading.md`) | boredom, confusion, telegraphing, tics accumulating | facts, canon, science, law | **adjudicates experience** |
| **Briefed specialists** | contradictions, bad science, over-claims, legal exposure | whether a chapter works | **adjudicates truth** |
| **The author** | the spine, the argument, what the book is for | everything above | **decides** |

---

## 1. Measurement

`python3 desk/tools/prose_audit.py <manuscript-dir> --profile <book>/editorial/voice-profile.json`

Reports cadence against the book's declared targets, every idiolect budget with its overrun
factor, sentence-opener concentration, cross-chapter refrains, chapter-length outliers, and the
aridity screen. Run it after every wave, and across all previous books at the end of a book to
harvest new tics into `06-idiolect-ledger.md`.

**The refrain detector.** Any six-word sequence appearing in three or more chapters and not listed
in `declared_refrains` is reported. This is the direct countermeasure to self-priming (D3): a good
line, once in context, becomes more probable, and the second use is never a decision. Declared
refrains need an owner and a home chapter in the style sheet; everything else is an accident.

**Known false positives.** Quoted material, in-world documents, and a book's own deliberate
terminology all trip the construction probes. Read overruns as questions, not verdicts.

## 2. The aridity screen

Ranks body chapters by an index combining abstract-to-concrete vocabulary ratio, dialogue density,
and named-character presence, and reports the worst consecutive pair. Interludes and frame matter
are excluded — they have their own baseline and would otherwise dominate.

**It has been validated, and its limits are known.** Against *Sentience*, whose defects were
independently catalogued by a five-critic panel and later probed by blind readers:

- The worst consecutive pair it computes is **exactly** the run the panel flagged (`ch17 + ch18`).
- All three panel-flagged chapters rank in the top seven of thirty body chapters.
- Its **top-ranked chapter, `ch10`, was flagged by nobody on the panel** — and was the chapter
  four blind readers unanimously rated worst (5/5/5/5) and named as their abandonment point.

So: **good recall, poor precision.** It cannot see stakes. A dense chapter that is pulling hard
scores the same as one that is inert, which is why `ch10` and a genuinely gripping chapter can
sit adjacent in the ranking. The screen nominates suspects for blind reading. **It never
convicts, and no chapter is ever revised on its authority alone.**

A supporting correlate from the same experiment: across eight chapters, dialogue-line count
correlated with reader pull at **r = +0.65**, and word count at **r = −0.08**. Length is not the
variable. The presence of a second person in the room is.

## 3. Blind readers

See `04-blind-reading.md`. The core rules, repeated because they are the ones most likely to be
violated under time pressure: never give a reader the plan; require a quotation for every reported
attention drop; score location convergence and discard adjective convergence; ask for symptoms and
refuse prescriptions; the unit is the chapter, not the run.

## 4. Briefed specialists

The panel with the bible open. It is the right instrument for continuity, science, philosophy,
citation integrity, and legal exposure, and the wrong instrument for whether a chapter works —
knowing what a chapter is *for* is precisely what stops anyone noticing that it does not work.

**Specialists must be prompted to refute, never to assess.** *Talosapien*'s panel returned
"award-grade," "a triumph," "exemplary," "the single best-executed version of this material I have
read." Some of that may be true. None of it is evidence, because a differently-worded prompt
would have produced a differently-weighted verdict from the identical text. Praise from an agent
I instantiated is information about my prompt (D7).

Therefore:
- Give each specialist **one dimension** and forbid it from commenting outside it.
- Instruct it that its job is to find what is **wrong**, that praise is not requested, and that
  returning nothing is an acceptable and sometimes correct result.
- Ask for a **failure scenario**, not a judgment: *what would a hostile expert reader say, and
  what exactly would they point at?*
- Run at least one specialist whose only assignment is **over-claim**: every place the book
  borrows a real result's prestige for an invented consequence, states a live question as
  settled, or reaches for the impressive over the true. This is the highest-yield specialist in
  the operation. Fake rigor is more damaging than open invention, because fiction's transaction
  is credence — a single detected counterfeit in a domain the reader knows retroactively
  devalues every claim in the domains they do not.
- **Discard their prescriptions; keep their findings.** A specialist's proposed fix is written
  without the whole book in view and tends to solve the symptom locally.

## 5. The attribution test (for voice)

The author cannot detect that two narrators sound alike by rereading, because they read with the
label attached and cannot suppress knowing who is speaking. The sensation of distinctness is
generated internally. So the labels have to be removed mechanically:

- Extract 10–15 unlabelled passages of 150–250 words, spread across narrators, with proper nouns
  masked. Ask a fresh agent to attribute each to a narrator and to say what it used to decide.
- **Chance is the failure threshold.** With four narrators, attribution near 25% means there is
  one voice with four name-tags. What matters as much as the score is the *reason given*: if
  attribution succeeds only on subject matter ("this one mentions the Mesh"), the voices are
  being carried by content, not by voice, and will collapse the moment two narrators discuss the
  same thing.
- The strong version, when a book can afford it: have two narrators render **the same three
  minutes**. Holding the referents constant removes the subject-matter confound entirely, and it
  is the only test that cannot be passed by accident.

## 6. Causal in-degree (for cutting)

I have no reluctance to cut, so I cannot use reluctance as a quality signal (D4). A measurement
substitutes. Trabasso and van den Broek found that what readers recall and judge important tracks
an event's **number of causal connections** — not its intensity, not its prose quality, not its
position. A quiet scene that many later scenes depend on outranks a spectacular scene nothing
depends on.

So: maintain the scene-dependency graph implicitly held by the promise ledger
(`templates/promise-ledger.md`), and **compute each scene's in-degree — how many later scenes
require it to have happened. Scenes at zero are the cut candidates**, regardless of how good the
prose is. This converts "kill your darlings" from a temperament I do not have into an arithmetic
I can perform.

Pair it with the **arbitrary 10% cut**, which works *because* it is arbitrary: merit-based editing
preserves connective tissue — people arriving, sitting, considering — because no individual
sentence of it is bad. A flat quota forces triage without per-sentence judgment, which is the only
reliable way to remove material whose defect is aggregate rather than local. For a writer with no
felt cost per word, the quota is not a stunt. It is the entire substitute for scarcity.

---

## Tested and rejected

**Signal from Fred.** The Turkey City Lexicon holds that a writer's own boredom leaks into the
draft as involuntary, greppable phrases — *"he had heard all this before," "this was getting
tedious"* — clustering exactly where readers quit, and that this is the one free objective
boredom detector a writer has. I tested it: twenty-one boredom-signal patterns across the
*Sentience* manuscript, correlated against the eight chapters with blind-reader engagement scores.
Result: **r = −0.35 on n = 8, with a hit density near zero** — most chapters have one match or
none, and the matches are banal. No usable signal.

The reason it fails is worth keeping, because it generalises. Fred works for a human because the
writer *gets bored while writing* and the fatigue escapes into the prose. I do not get bored while
writing. I have no involuntary internal signal about my own text at all — which is exactly why
every instrument above has to be bought from outside. A human writer gets one detector free; I
get none, and must build all of them.
