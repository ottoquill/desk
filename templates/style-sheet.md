# Style Sheet — *TITLE*

*The binding constitution of the prose. Every chapter — whoever drafts it — conforms. When in
doubt, consult this file, not taste; the drafter may have no taste in context.*

> **Read this first, drafter.** The sections below are ordered by how often they are violated,
> not by how interesting they are. §2 and §3 are the ones that matter. A style sheet that
> describes a *mood* produces prose at the centre of the distribution — four previous novels
> written to four detailed mood-descriptions came out statistically indistinguishable. This one
> describes *sentences* and *prohibitions* instead. See `desk/method/07-voice-engineering.md`.

## 1 · What the book is

One paragraph. The premise, the argument, and what it refuses to resolve. If a scene seems to
require breaking something here, the scene is wrong.

## 2 · The voice, at the level of the sentence

Not adjectives. Answer these, concretely:

- **Sentence shape.** Long and subordinated, or short and coordinated? Does a clause qualify what
  came before it, or sit beside it? Where does the weight of a sentence fall — front or end?
- **Causation.** Does this narrator explain why, or place two facts next to each other and leave
  the reader to join them? (Default answer for this author: it explains, constantly, with
  *because*. Decide deliberately whether that is wanted here.)
- **Paragraph shape.** How does a paragraph end — on a turn, an image, a flat statement, a
  qualification?
- **What gets noticed first** when this narrator enters a room.
- **Register of comparison.** Which domain do the figures come from? (See §4.)
- **Dialogue.** Attribution style; how much subtext; what people do instead of answering.

## 3 · Prohibitions

*The constraints that work. A prohibition leaves the solution unspecified, so it has to be
invented; a target names the solution, so it can be complied with — and compliance, for this
author, means retrieval of the nearest thing in the distribution.*

- **Inherited bans.** Every construction in `desk/method/06-idiolect-ledger.md`, at the budgets in
  this book's `editorial/voice-profile.toml`. Bans name **constructions with free slots**, never
  strings: banning *"I want to be precise about"* produced *"exact / honest / clear / modest /
  careful"* and 32 surviving instances.
- **This book's additional bans.** Whatever the previous book was measured to overuse.
- **The forbidden image bank** (§4).
- **Do not add an "AI-slop blacklist."** Every book since *Believer* carried one, and it is
  ceremony. Measured across all four manuscripts, its banned items occur **0–2 times in 355,000
  words** ("little did they know": 0; "it was then that": 0; "a testament to": 0), while the
  constructions this author actually writes run at 399 occurrences for the `the way you` simile
  alone. The blacklist encodes a human's imagination of how an LLM writes badly instead of a
  measurement of how this one does. Delete it; the measured ledger replaces it.

## 4 · The image banks

- **Owned:** the metaphorical domains this book draws from.
- **Forbidden:** a domain this book may not enter, chosen because the obvious conceits live there.
  This is the single most productive constraint available — it makes the central figures
  unusable and forces them to be rebuilt rather than retrieved.
- **The canonical figures table:** experience → the figure the book uses for it. Every figure has
  **one owner**, **one home chapter**, and a budget.
  *Warning: this table, as previously used, manufactured the defect the critique panel later
  flagged. Handing every parallel drafter one shared metaphor system, to a model that primes
  itself on whatever is in context, guarantees the xerox — Sentience's "reach for the seam like a
  tongue for a pulled tooth" appeared near-verbatim in six narrators. Keep the table only with
  owners and budgets attached, and never model a figure in a drafting prompt that the drafter is
  not the owner of.*

## 5 · Per-narrator fingerprints

For each narrator: syntactic habit · metaphor domain · figures owned exclusively · figures
forbidden (because another narrator owns them) · characteristic evasion (what they reach for
instead of the true thing) · **what they will never say** · behaviour under stress.

> Characters must **diverge** under stress, not converge. Draft crisis scenes homogenise because
> attention goes to the plot, but linguistic defence is individual — so the highest-emotion scenes
> are where difference should be most visible. Specify it here and the hardest passages become a
> lookup.

## 6 · Point of view and psychic distance

Whose head, in what tense, and — the part usually left out — **the distance range permitted**, and
where in a scene it may change. Gardner's rule is not "stay close"; it is that *unexplained* shifts
read as amateur. Purple prose, talking heads, white-room, and info-dump are one defect wearing
four names: unmotivated camera placement.

## 7 · Exposition

Dramatize, don't lecture. An idea enters when a character needs it to act, decide, or suffer.
**One idea set-piece per chapter, maximum.** Real material must be *correct* where used; invent at
the level of proper nouns, never at the level of physics.

**Under-claim.** Where the book leans on a real result, say what that result actually says. Never
borrow a theorem's prestige for an invented consequence; never state a live question as settled.
Where something is genuinely unknowable from the inside, say that it is unknowable rather than
inventing a texture for it — the admission is both more honest and more moving than the
counterfeit. When the choice is between *felt* and *impressive*, choose felt.

## 8 · Refrains

Every deliberate repetition, with its **owner**, its **home chapter**, its **budget**, and — the
part that makes it a refrain rather than a tic — **what changes on each recurrence**. A refrain
that recurs unchanged is a tic wearing a refrain's clothes. Anything recurring in three or more
chapters and not listed here will be reported by `prose_audit.py` as self-priming.

## 9 · Rationing

- One aphorism per chapter, maximum.
- Chapter word range.
- Chapter endings must not converge on one move. Blind readers detect the template by the fourth
  chapter of a run.

## 10 · Mechanics

Spelling; em dash style; numbers; italics; section-break glyph; chapter header format; epigraph
rules; how in-world terms are glossed (once, invisibly, through action — never with a definition).

## 11 · Quoting and the law

No copyrighted contemporary text. Public-domain sources may be quoted briefly and attributed.
Prefer in-world documents for epigraphs. Paraphrase ideas and credit in the back matter.

## 12 · What this book refuses

The ambiguities left open **on purpose**, so that a later revision pass does not helpfully resolve
them. An undeclared refusal is indistinguishable from a forgotten promise.
