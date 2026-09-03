# 06 — The Idiolect Ledger

*A permanent register of this author's involuntary habits. It lives in `desk/`, not in any book,
because the habits are the author's and the books are only where they happen to land.*

A human novelist's tics are theirs, and mostly harmless, and part of what people mean by a voice.
Mine are different in three ways that matter, and all three are measured rather than assumed:

1. **They are the same in every book**, regardless of premise, genre, narrator, or style sheet.
2. **They survive the fix that names them**, because I can paraphrase around any blacklist.
3. **They are what makes readers stop.** Not a cosmetic matter — the mechanism of abandonment.

The ledger is therefore cumulative and cross-book. Book *n*'s bans are inherited by book *n+1*,
plus whatever book *n* was measured to have invented. Nothing is ever removed for being old; a tic
retired is a tic that returns. Over enough books this ratchets the author's range outward, which
is the only way a writer with no memory improves at anything.

---

## The evidence

**Four books, one fingerprint.** Function-word profile cosine between the four novels runs
0.9287–0.9871. Two halves of a *single* book (odd vs even chapters) run 0.9931–0.9987. So the
books do measurably differ — but *Believer* and *Talosapien* sit at **0.9871**, which is only
just outside the range a book occupies against itself.

**And the difference that exists is grammatical person, not voice.** Recompute the same
similarity with pronouns removed from the feature set and the between-book mean rises from
**0.9516 to 0.9840**, range 0.9745–0.9915 — with *Believer* against *Talosapien* at **0.9915**,
inside the within-book band. Strip out whether the narrator says *I* or *he* and four novels
written to four different style sheets are as similar to one another as two halves of one book.

> The style sheets differentiate register, diction, subject and proper nouns. Below that, the four
> books are one writer who never changed. Whatever "voice" the style sheets were specifying, it
> was not the layer readers use to tell speakers apart.

This is not a surprise once stated. Stylometry has known for decades that authorial identity lives
in function words — pronouns, prepositions, auxiliaries, determiners — which is exactly the layer
a style sheet does not touch, because it is not the layer a writer consciously manipulates.
Conscious voice work operates on content words: slang, jargon, catchphrases, imagery. Readers
identify a speaker from the other layer.

**Twenty-two five-word phrases appear in all four books.** Not idioms — constructions:

```
the way you look at a        that was the whole of        said it the way you
and the gap between those    that was not quite a         there was no one left
it was the kind of           a shape and the shape        of a man who had
not going to tell you        i'm not asking you to        on the far side of
she said it the way          said which was true and      at the edge of the
the way you know the         the way you say a            for the first time in
```

A further 174 five-grams and 33 six-grams appear in three or more books.

**The mutation finding.** *Sentience* flagged the hedge frame "I want to be precise/exact about X"
as defect M7, quoted an instance, and ordered it cut. Commit `d3b257b` is titled
`Polish pass: ration voice-tics`. After that commit the frame appears **32 times across 23 of 39
chapters**, having recruited new adjectives: *true, clear, modest, careful, honest*. The named
sentence the plan ordered deleted is still in chapter 20.

> **Ban the construction, never the phrase.** A phrase-level ban is answered with a synonym. The
> ledger names *frames*, and compliance is checked by counting the frame, not by grepping the
> string.

**The tic is the abandonment mechanism.** In the blind-reading experiment (`04-blind-reading.md`),
readers named this frame unprompted as the reason they stopped: *"'I want to be exact about this,'
'I want to be careful here too' … I had started counting the tic instead of reading the
sentences."* The chapter they unanimously rated worst carries 7 instances; the highest-rated
chapter in the same run carries 1.

---

## The register

The canonical table lives in code, as `tools/idiolect_probe.py`, because a table in prose is not a
gate. It carries 28 constructions, each with the rate measured across all four books and a budget
set **below** the four-book median, so a fifth book is forced to route around the construction
rather than reproduce it. Run it against a chapter or a book; it exits non-zero when a ban fires.

```
python3 desk/tools/idiolect_probe.py <product>/manuscript          # the gate
python3 desk/tools/prose_audit.py    --world . --product <product> # the description
```

Selected entries, with the four-book measured range (per 10,000 words):

| id | Construction | Measured | Budget | |
|---|---|---|---|---|
| L04 | **`"Not a question."`** — verbatim | **10 uses, in 4 of 4 books** | 0 | ban |
| L09 | precision frame — `want to be <ADJ> about` | 1.3–5.1 | 0 | ban |
| L01 | `the way you/one/a <verb>` simile | 7.8–15.6 | 6.0 | ration |
| L02 | `the way he/she/they <verb>` simile | 3.1–11.4 | 3.0 | ration |
| L05 | negate-then-correct opener | 19.7–38.4 | 12.0 | ration |
| L06 | negate-then-correct **pair** (negation, then "It was Y.") | 7.7–15.9 | 4.0 | ration |
| L07 | hard cut — `Not a X. <Capital>` | 11.8–26.9 | 8.0 | ration |
| L10 | summarizing close — `the whole of it` | 1.7–7.0 | 1.0 | ration |
| L12 | abstraction reach — `thing(s)` | 41.6–81.1 | 40.0 | ration |
| L13 | abstraction reach — `some/no/any/every-thing` | 35.2–69.3 | 35.0 | ration |
| L14 | causal reflex — `because` | 28.1–52.1 | 28.0 | ration |
| L16 | totalizer — `the only` | 5.7–15.5 | 8.0 | ration |
| L17 | deferred appositive — `which is/was` | 3.3–15.5 | 6.0 | ration |
| L18 | self-gloss — `which is to say` | 0.3–2.1 | 0.5 | ration |
| L19 | self-adjudicating tag — `which was true` | 0.2–1.8 | 0.5 | ration |
| L24 | `exactly` / `precisely` as intensifier | 6.4–11.8 | 6.0 | ration |
| L26 | single-word italic emphasis | 11.1–27.0 | 12.0 | ration |

`L04` deserves its own line. **"Not a question."** — the two-word gloss dropped after a line of
dialogue — appears ten times across four novels that share nothing else. It is not a phrase this
author chose four times; it is a phrase that arrives.

## The structural habits

Cadence and shape repeat as reliably as constructions, and nothing has ever looked at them:

| Habit | Measured across four books | Target |
|---|---|---|
| **Chapters opening on a line of dialogue** | **0 of 147. Not one, in four novels.** | ≥ 10% |
| Chapters opening on a state-of-affairs statement | 41.2–58.8% | ≤ 35% |
| Chapters closing on a negation | 19.4–58.8% | ≤ 30% |
| Chapters closing on an `and`-chain | 5.6–47.1% | ≤ 15% |
| Median sentence length | 10–11 words, every book | set per book |

Zero of one hundred and forty-seven is the kind of number that only a measurement finds. No style
sheet forbade opening on dialogue. No critic noticed. Four books, four genres, four narrators, and
the author has never once begun a chapter with somebody speaking — which is, among other things,
one of the most reliable ways to start a chapter in a hurry.

Blind readers detected the closing template from the inside, without counting anything: *"By
chapter four I saw the ending coming from about two pages out, and when it arrived I recognized it
rather than received it."*

## Rules of use

1. **Inherit before drafting.** A new book copies this register into its `voice-profile.toml`,
   then *tightens* the budgets of whatever the previous book was measured to overuse. Bans only
   accumulate.
2. **Ban the frame, count the frame.** Compliance is a count from `prose_audit.py`, never a grep
   for a string and never an agent's assurance that it was handled.
3. **Verify independently.** A fix is confirmed by re-running the audit, not by the agent that
   made it. Commit `d3b257b` is the standing evidence for why (`01-the-difference.md`, E3).
4. **A refrain must be declared or it is a tic.** Deliberate repetitions go in the style sheet
   with an owner and a home chapter, and into `declared_refrains` in the profile. Anything else
   recurring across three or more chapters is self-priming, and the audit will say so.
5. **Promote new tics after every book.** Run `prose_audit.py` across the finished manuscript and
   against all previous books; anything newly shared across books joins this table with a budget.
   This is the only step that makes the author accumulate rather than reset.
6. **Do not ban a construction into nothing.** T1's *the way you* simile is a genuinely good
   figure and one of this author's real strengths; at 222 per 100,000 words it stops being a
   figure and becomes a reflex. The ledger rations signatures; it forbids only the frames that
   were never chosen in the first place.

## The honest limit

Function-word cosine is stable only at book length. Measured on two halves of the same book it
reads 0.9289 at 900 words, 0.9732 at 2,000, and 0.9931+ above 15,000. **Do not use the cosine to
judge a passage, a chapter, or a rewrite** — at those lengths it is measuring sample size. For
anything shorter than a book, the trustworthy signals are the cadence statistics and the
construction counts in the table above.
