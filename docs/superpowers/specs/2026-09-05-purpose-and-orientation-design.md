# Purpose and Orientation

*Design spec. Records what `desk` is for, where that statement lives, and the rules that keep a
session pointed at it.*

**Status:** decided 2026-09-05.
**Scope:** the purpose statement, its placement, and six behaviour rules. The runner stays piece 2
and is unchanged except where the Consequences section says otherwise.

---

## The problem

The repo has never said what it is for.

`README.md`'s "Why this repo exists" gives a mechanism — the author does not persist between
books, the files do — and the founding measurement of nine defect classes recurring across four
novels. Both are true. Neither says what the repo produces, or for whom.

The purpose was stated once, in conversation. On 2026-09-02 at 17:18 local the author described it
in full: worlds and the stories drawn out of them, superb, with automation running from a single
prompt to close interactive work, and `desk` referenced from a world repo carrying multiple books,
a canon wiki, and a game. One minute later the session restated it accurately and named the gap in
the right words — *the automation dial needs a runner*. Thirty-three minutes after that, commit
`f7da1a9` shipped the infrastructure half as piece 1 and filed the remainder in a closing section
called "The other pieces".

Piece 1 completed the same night. On 2026-09-03 the work moved to ottoquill.com. Pieces 2 and 3
have no commits.

Three days later a fresh session read `README.md` and `CLAUDE.md`, described the repo as a
defect-prevention system, and had to be corrected. That same session then reintroduced a framing
the spec had already revised, listing the wiki among the things drawn out of canon. Twice, a
correction recorded only in a spec failed to reach the work.

The diagnosis is the repo's own standard turned on itself. **License nothing in prose; license
with a number** (R2). **A table in prose is not a gate.** A purpose recorded where nothing reads
it has not been recorded.

## What was decided

Four questions were put to the author on 2026-09-05. The answers are constraints rather than
preferences, and each has a testable consequence.

### 1. Audience — the author's worlds now, generalizable by construction

`desk` is built for the author's worlds today. Nothing specific to one world or one author's voice
may live in `desk`. Someone else could use it; they are owed no onboarding, docs or support yet.

The mechanism already exists as piece 1's principle and extends by one level: **`desk` knows
kinds, a world names instances, a run names settings.**

The rejected alternative was shipping a real second user as a requirement of piece 2. By the
Coverage Law that generalizes checks before the binding ones are known.

### 2. The dial — a per-run parameter, not a fixed policy

The session offered three fixed promises for the unattended end of the dial. The author rejected
the framing:

> It depends on the prompt. Factor your instructions so that the default can be easily modified.
> If there is ambiguity, ask.

So the automation level is a parameter of a run. `desk` supplies defaults, the invoking prompt
overrides them, and genuine ambiguity escalates to the author rather than resolving itself. A run at the unattended end carries no fixed promise.

This does not dissolve the underlying tension, and the tension stays on the record. R8 measured
numeric cadence targets in a generation prompt producing the worst prose in six-way blind judging,
3.0/10 for quality. D7 holds that praise from a critic you instantiated is information about your
prompt. Machine-checkable gates automate; taste has weaker evidence behind it. A run that asks for
superb output unattended is asking for the part with the least support, and should say so.

### 3. Publishing — as far as the artifact

In scope: a distributable book file, and the world's deployed site. Out of scope: storefront
submission, the last mile that touches an external account and cannot be reverted.

`desk` has no support for either today. Stage 10 "Ship gates" is entirely quality gates; nothing
in the twelve stages emits a file.

### 4. The wiki — canon's home, and still a declared product

Canon is the substrate and the wiki is where canon primarily lives. `DEFAULT_CANON` resolves to
`content/canon` in `tools/world.py`, with per-kind archetypes, `canon/single.html` and
`canon/list.html` layouts, and a `canonref` shortcode in `hugo/`. The wiki does not render *from*
canon. The wiki **is** canon, rendered, over the same files `continuity.py` gates.

The wiki stays declarable in `world.toml` regardless, for a reason the schema cannot express
today: a working canon holds spoilers and unpublished material, and the public wiki has to be a
filtered rendering of it. Theme, domain and visibility rules need somewhere to live, and a product
entry is where deployment config already goes.

## The design

Four files. The purpose lands in both orientation files, because a session auto-loads `CLAUDE.md`
and a human arrives at `README.md`, and neither reads the other.

| File | What it carries |
|---|---|
| `CLAUDE.md` | The purpose statement, ahead of the existing description of the repo |
| `README.md` | The same statement, ahead of the existing "Why this repo exists" |
| `.claude/rules/purpose.md` | Six behaviour rules, loaded every session |
| this spec | The four decisions and their reasoning |

The existing text in both orientation files stays. Both passages remain true, and they explain
why the repo took the form it did. What changes is that it stops standing alone, where it reads as the point.

`.claude/rules/` is the mechanism already used here for `commit-messages.md`, and used at ten files
deep in `bitsy-services/wiki` alongside a `Stop` hook. The six rules are derived from failures on
the record rather than invented:

1. **Before starting work**, name which part of the purpose it advances; if none, say so first.
2. **Deferral is a decision, not a filing action** — say it in conversation and get agreement.
3. **Prefer the half that does not decompose**, or name that you are not taking it.
4. **A goal stated is a goal written down that turn**, in the orientation files.
5. **Defaults are overridable**, resolved from config a run or a world can change.
6. **A correction recorded only in a spec has not landed** — it goes to the orientation files too.

## Consequences

**Idiolect budgets become world-calibrated.** Decision 1 splits what `idiolect_probe.py` carries.
The 28 constructions are the model family's attractor, measured on a convenient corpus, and they
stay in `desk` as detection. The budgets are calibrated on four novels in one register and they
belong to a world. `CLAUDE.md` today says budgets sit below the four-book measured median on
purpose; that sentence becomes a statement about a world's profile rather than about `desk`. R1's
ratchet and R3's accumulation are unaffected — they move to the world level with the numbers.

**Canon needs a visibility dimension.** `canon/schema.toml` requires `canon_kind`, `id` and `name`
and has no field a public rendering could filter on. A boolean looks wrong: a book-one reveal is
public once book one ships, and a book-three reveal is not, so visibility is likely keyed to a
product's release. Its own spec.

**Piece 3 grows rather than shrinks.** The world-contract spec judged instruments beyond the
manuscript "smaller than the first draft assumed", on the grounds that lore pages are prose by the
same model and mostly need the existing tools pointed at them. Under decision 4 canon is the
larger prose surface over a world's life, and the tools want pointing at it early rather than
late.

**Piece 2 runs wiki-first.** A run populates canon before it drafts a manuscript, and the book is
derived downstream. The deployed site is not a publish target at the end of the pipeline.

## Non-goals

**Solving canon visibility.** Named above, deferred deliberately, and said here rather than filed.

**A roadmap file.** Piece status belongs in the spec defining the pieces. A second tracking file
is one more thing to go stale.

**A structure-checking tool.** An earlier draft proposed grepping `tools/` for world-specific
constants. It checks the repo's structure rather than a session's behaviour, and the failure being fixed
here is behavioural.

**A `Stop` hook.** `bitsy-services/wiki` blocks the turn on a red check, and `desk` should
eventually do the same. It cannot yet: `idiolect_probe.py` exits non-zero on `method/` by design
and by record. A hook needs that exception written down first, as its own decision.
