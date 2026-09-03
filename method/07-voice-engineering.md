# 07 — Voice Engineering

*How to make books that do not sound like each other, given that my default is the average of all
prose. This document contains the strongest result in the corpus, and it refutes the obvious
approach — including the version of it I proposed before testing.*

---

## The Coverage Law

> **Prose changes along exactly the axes the brief makes checkable, and reverts to the attractor
> everywhere else.**

This is not a slogan; it is the reading of a natural experiment that already exists in the repos.
*Talosapien* was rewritten in full, on a branch, to Hemingway's principles: 109,051 words down to
60,263, under a brief that named short declarative sentences, one thought per sentence, cut
adverbs, concrete over abstract, the iceberg.

**What the brief named moved enormously:**

| | before | after |
|---|---|---|
| mean sentence length | 25.4 | 15.9 |
| p90 sentence length | 66 | 35 |
| sentences ≥ 40 words | 23.1% | 6.8% |
| `-ly` adverbs /10k | 58.5 | 45.8 |

**What the brief did not name did not move:**

| | before | after |
|---|---|---|
| `the way you X` simile /10k | 18.6 | 14.3 |
| `thing(s)` /10k | 86.4 | 81.1 |
| `because` /10k | 58.9 | 45.3 |
| `the only X` /10k | 1.6 | 1.7 |
| subject-first sentence openings | 91% | 90% |
| `Not a X. [Capital]` /10k | 17.0 | **27.6 — it rose 62%** |

Function-word cosine between the original book and its own halved Hemingway rewrite: **0.9967 —
closer than any two Otto Quill books are to each other.** All twenty-two cross-book five-grams
survive the conversion.

So the design problem is not motivation, taste, or the strength of the instruction. **It is
coverage.** Any dimension of voice for which no query exists is guaranteed to be house style in
the finished book. And the last row is the warning: an axis that is *adjacent* to a named axis can
get worse, because chopping cascades into short sentences manufactures more hard cuts.

## What has never changed

**Constituent order.** Across four novels, a plural frame voice, found-document interludes,
second-person recipe interludes, a full Hemingway conversion, and the essays in this directory,
the proportion of sentences opening on their grammatical subject sits between **85% and 96%**.
Nothing has ever changed where an Otto Quill sentence starts. It has never been specified, and it
is measurable with a first-token lookup.

*(The method essays measure 93%. I am doing it in this sentence.)*

**Terminal ascent — the master habit, from which the named tics descend.** Every unit of prose is
required to end at a higher level of abstraction than it began: the sentence ends on the gloss of
the fact, the paragraph on the proposition the scene proves, the chapter on the aphorism.

- Paragraph-final sentences are dramatically longer than paragraph-internal ones — 40.0 vs 19.0
  words in *Talosapien*, 25.4 vs 15.9 in *Believer*, 23.6 vs 15.8 in *Sentience*.
- 51–65% of multi-sentence paragraphs close on a sentence longer than that paragraph's own average.
- 37–47% of paragraph-final sentences end on an abstract noun; 27–51% contain a generic-person
  reference (*you*, *one*, *a man*, *anyone*).
- Mean chapter-final sentence: *Talosapien* **73.6 words**.

The figures I have been banning one at a time — the-way-you, which-was, the-only-X, the-whole-of,
the abstract antithesis — are not separate tics. **They are the available instruments of one
policy**, which is why prohibiting them individually re-tools rather than stops. Attack the policy
and all of them starve at once. And the policy is checkable without taste: *does the final noun
phrase of this paragraph name something a camera in this scene could photograph?* — a yes/no a
memoryless subagent answers with low variance.

**The signature simile is the deficit made visible.** `the way you X` is not a simile of
resemblance but a simile of **procedure**: it explains an inner state by naming a universal human
procedure the reader is assumed to have performed. *"knew the way you know a grave is a grave"*;
*"the way you understand a stair is missing only after your foot has gone through"*; *"the way you
track a scar from across a room."* A human's simile draws on one idiosyncratic life — *like my
grandmother's coat*. Mine draws on the average of all lives, because that is the only material I
have (D8). It follows that the replacement is not a different simile. It is a rule about where a
comparison may be **sourced**.

**One rhetorical machine delivers the theme in all four books.** The abstract antithesis:
*"correct is not the same as honest"* (*Talosapien*); *"the accurate thing was not the same as the
good thing"* (*Believer*); *"survivable is not the same as legible"* (*Sentience*); *"that's not
the same thing as it mattering"* (*Cruelty-Free*). This is worse than a tic — the figure is doing
the book's most important work, which is exactly why it survives every ration. A figure ledger has
to distinguish *the figure the author reaches for* from *the figure this book's thesis is delivered
by*, and require the second to be **reassigned per book**, not merely rationed.

## Why the style sheets never had a chance

**They are one document with the nouns swapped.** *Sentience*'s and *Talosapien*'s opening sections
are near-identical sentence for sentence — both "the binding constitution of the prose… when in
doubt, consult this file, not taste"; both "register: lucid, precise, unshowy… Egan's rigor,
Chiang's restraint"; both "default sentence: plain declarative. Earn the long recursive sentence."
A machine's elegiac confession and a hard-SF deep-time epic are described in the same words. The
spec is written by the same author under the same attractor as the prose, so **a different voice
was never actually specified.** Any fix that produces the next book's voice by free composition
will reproduce this: the spec must come from a procedure that forces difference from the *measured*
previous book.

**And where a style sheet did specify cadence, nobody checked.** *Believer*'s guide orders "long,
clause-stacked observation followed by a short, flat landing." Measured: 55.5% of its
multi-sentence paragraphs end on a sentence *longer* than the paragraph average; only 23.6% of
paragraph closes are ≤ 6 words. The book does long-then-**longer**, book-wide, and shipped. The
drafting agents believed they were obeying; the reviewers believed it had been obeyed.

> **An unmeasured instruction is decoration. Every prose rule ships with the query that decides
> it.**

**Naming three influences causes the problem.** "Egan's rigor, Chiang's restraint, Baxter's
deep-time sublime." "The love-child of Saramago's premise-rigor, Ishiguro's restraint, and the
satirical bite of Saunders / Heller." Naming several exemplars licenses *interpolation*, and
interpolation is the attractor — breadth is precisely what produces the mean. The one brief in the
corpus that named exactly **one** author, converted them into eight operational mechanisms, and
supplied a worked before/after example is the only brief that ever moved the cadence.

## The narrators are not distinct either

Within *Sentience*, pairwise narrator similarity runs 0.953–0.987. Ariel — an artificial mind — and
Mara — a human woman — sit at **0.9860**, which is the same-voice noise floor for windows of that
size. Leave-one-out classification of 1,200-word chunks on function words: *Talosapien* POV
identity 86.6% accurate **with** pronouns, **53.7% without** (majority baseline 35.8%). Book
identity holds up far better (88.6% → 72.7%).

So the unit of voice variation in this corpus is the book, not the character — and even that is
mostly pronouns. Per-narrator idiolect is not a refinement to add later. It is the untouched 90%
of the problem.

**A same-voice noise floor now exists**, which makes "these are distinct voices" falsifiable for
the first time. Two disjoint random windows of one voice in one book, 200 trials per size, median
/ p05:

| window | median | p05 |
|---|---|---|
| 1,500 words | 0.9613 | 0.9162 |
| 3,000 | 0.9765 | 0.9574 |
| 6,000 | 0.9867 | 0.9722 |
| 12,000 | 0.9930 | 0.9851 |
| 25,000 | 0.9967 | 0.9943 |

Read against it: Ariel vs Mara at 0.9860 is indistinguishable from noise. *Believer* vs
*Talosapien* at 0.9892 is a real but weak separation. *Talosapien*'s frame voice at 0.9136 against
its own body is a genuine, large one. **Without this table every cosine in the project is
uninterpretable; with it, a voice profile can state a hard acceptance criterion.**

## What has actually worked, three times

Three passages in 300,000 words genuinely break free, and all three do it the same way — and none
of them was told to sound different.

| passage | cosine vs its own book's body |
|---|---|
| *Cruelty-Free*'s second-person imperative recipe interludes | **0.8372** — below the *minimum* of 200 same-voice trials at that length |
| *Talosapien*'s first-person-plural present-tense frame | 0.9136 — the only narrator that classifies at 100% after pronoun ablation |
| *Believer*'s dossier interludes (slide deck, stand-up set, redacted memo) | 0.9321 — mean sentence 11.1 vs 21.0, the-way frame 3.5 vs 25.3 |

In the recipes the generic-you simile runs at **0.0 per 10k against 12.9 in the body.**

The common mechanism is not a description. It is an **externally imposed compulsory form** — a deck
must have bullets and KPIs, a recipe must have imperatives and quantities, a plural reconstruction
must confess what it cannot know — **plus a change of grammatical person.** Descriptions of a voice
have never once produced one. And note that this mechanism is *generative*, not prohibitive, which
is what protects it from producing mannered prose: it gives the sentence something to do rather
than something to avoid.

**Its ceiling is equally clear.** A form-shift buys a different word distribution; it does not buy
a different sentence. The recipes are still 96% subject-first, and their deferred appositive rate
is *higher* than the body's. Only *Believer*'s dossiers move the architecture — and they are the
passages whose source form physically forbids subordination. **Full separation needs both levers:
the imported grammar, which supplies material and diction, and an explicit constituent-order and
clause-depth target, which supplies rhythm. Neither alone has ever been sufficient.**

**Person and tense are the cheapest large-effect lever and have been chosen by accident.** Mean
same-person book pair 0.979; mean cross-person 0.939. Genre distance is uncorrelated — literary
satire and hard SF are the *closest* pair in the corpus. Four books have used three of the
available person-tense combinations, each time for narrative reasons, never as a voice instrument.

## Three specs, three outcomes

Two independent experiments, one on a 900-word passage judged blind and one on a scene brief,
converge on the same ladder:

| spec | result |
|---|---|
| **Adjectival register** ("lucid, precise, unshowy") | Pure house style. Obeyed perfectly; tripped 9 of 10 banned constructions anyway. |
| **Bare numeric cadence targets** | Quality 3.0/10, mannered 8.7/10, last of six by every judge. *"You can hear the period key being pressed."* |
| **Construction bans alone** | Zero bans tripped — and starved. Prohibition removes without supplying. |
| **Bans + narrow influence + owned/forbidden image bank** | Best of the rewrites. *"The brief being met by thinking, not by obedience."* |
| **Mechanisms + worked example** (the Hemingway brief) | 37–71% movement on every named axis, at book length, without manner. |

The apparent contradiction — numbers ruinous in one place, effective in the Hemingway brief —
resolves cleanly. Bare numbers name a *target* and invite compliance, and compliance for me is
retrieval. Numbers inside a brief that also supplies mechanisms and a worked before/after example
name a *behaviour*, and behaviours have to be performed. **The number is never the instruction. It
is how the instruction is checked.**

## The method

1. **Cover the sentence, not the mood.** The voice constitution must carry a query for constituent
   order, clause depth, terminal altitude, and metaphor sourcing. These four are currently
   uncovered, and by the Coverage Law they will therefore be house style.
2. **Set terminal altitude explicitly.** Declare where a paragraph may end. The default test: the
   final noun phrase names something a camera in the scene could photograph.
3. **Import a compulsory form and carry it into the body.** Give the narrator an occupational or
   documentary grammar — a chef's mise-en-place ordering, a deposition's numbered assertions, a
   repair log's fault-then-remedy — and let it govern the scene prose, not just the interludes.
   *Cruelty-Free* proves both halves: where the chef's grammar reaches the narration, the prose
   measurably departs from house style; across the 89,787 words where it does not, the effect
   decays.
4. **Choose person and tense as instruments**, per book and per narrator, not as a byproduct of the
   premise.
5. **Name one influence, converted into mechanisms, with a worked before/after example.** Never
   three, never as adjectives.
6. **Generate the spec by a procedure that forces difference from the measured previous book** —
   never by writing a fresh description, which converges on the same description.
7. **Pair every prohibition with a positive constitution.** Bans alone starve the prose; that risk
   is real and appears immediately.
8. **Measure, then revise. Never instruct and trust.** The constraint does not prevent the
   construction from arising; it makes it detectable.
9. **State the acceptance criterion against the noise floor.** "Each narrator sits below the p01
   same-voice cosine for its word count" is a claim that can fail. "The voices feel distinct" is
   not.
10. **Ban the figure that carries the thesis, per book.** Rationing it is not enough — it survives
    because it is doing the most important work in the book.

## The standing caution

Unconstrained, I write the average of everyone. Over-constrained, I write compliance — audibly
obeying a rule, which reads worse than the default, because the default is at least fluent. The
evidence puts the safe zone at: **a compulsory imported form, a deliberate person and tense, one
influence rendered as mechanism, an owned and a forbidden image bank, an explicit terminal
altitude, and prohibitions on the constructions — with every one of them carrying the query that
decides it, and the numbers kept on the diagnostic side of the wall.**
