<!-- Generated from the research pass on the branch writing-method.
     24 agents, 10 craft lenses and 4 forensic audits over the Otto Quill corpus.
     Kept because the author does not persist between sessions and this would
     otherwise have to be re-derived (method/02-the-rules.md, R1). -->

# Research Reference — Forensic Audits of the Corpus
Four audits of the four finished novels: the defect ground truth, the idiolect, the production process, and the voice. 67 findings, each with file-level evidence.

## Defect Ground Truth for an LLM Novelist: 10 prose failure classes + 5 process failure classes, measured across four Otto Quill novels (N=88 documented defects)

### 1. The complete documented defect corpus is 88 items across four books, and it normalises to exactly 10 prose failure classes. Ranked by frequency: (1) continuity contradiction 28 (32%); (2) voice-tic bleed / self-priming repetition 14 (16%); (3) over-claim or misattribution about real scholarship 10 (11%); (4) fake rigor — invented formalism borrowing a real result's prestige 9 (10%); (5) thesis stated not enacted / didacticism 7 (8%); (6) emotional sag / structural plateau 7 (8%); (7) structural repetition of scene-shape 4 (5%); (8) real-world factual error 4 (5%); (9) mechanical style-sheet violation 3 (3%); (10) plant/payoff missing 2 (2%).

*Evidence:* Sources: /home/paul/git/ottoquill/sentience/editorial/revision-plan.md (exactly 50 numbered items:
B1-B2, M1-M18, m1-m21, n1-n9 — counted programmatically);
/home/paul/git/ottoquill/talosapien/editorial/critique-report.md (13 items: 1 blocker, 5 majors, 4
minor/factual, 3 deliberately-left); /home/paul/git/ottoquill/believer/docs/revision-findings.md
(11: 3 bugs, 7 structural, 1 positioning); Cruelty-Free has NO editorial file — its 14 defects are
recoverable only from commit 82341ee 'Continuity & polish pass' (15 files, 19 hunks).

*Significance:* Ten classes is a small enough number to be a permanent regression suite. The distribution is the
design brief: half of all defects (classes 1+2, 42/88) come from the two mechanical pathologies of
parallel generation — divergence on facts and convergence on phrasing — and both are detectable by
script. Only classes 5, 6 and 7 genuinely require a reading agent.

### 2. 100% of declared blockers across the entire corpus are continuity contradictions. There are exactly three, and all three are a single fact asserted two incompatible ways in chapters drafted in the same parallel wave.

*Evidence:* Sentience B1: Ariel is Mara's lover ('lovers in every sense their substrates allow', 'I'd marry
you') and simultaneously her 'uncle' and 'her brother' in Ch28. Sentience B2: 'a man named Vesper
proving a thing about sets' — wrong gender AND wrong theorem (the count is Cantor's) in one clause.
Talosapien: 'the clutch hatches twice' — Ch15/Ch17 reference hatchlings although Ch19 ('Hatching')
dramatizes the hatching. Non-blocker instances of the same class: 30 vs 40 years (Sentience M13),
Tomas's age (M14), Ariel's pronoun in three regimes (M11), Sable's pronoun (M12), Belt distance 'a
hundred million kilometers' vs the locked 14-light-minute lag (talosapien commit 2ad2b99), Okonkwo
used for two different characters (Believer), Ferris used for two (Believer), 14/16 years, 22/15
years, 48/72 hours, 3/4 years, two different gala venues, two different signal codes (Cruelty-Free).

*Significance:* The single highest-severity class is also the most mechanically checkable class. Nothing in the
pipeline currently does the check: talosapien/build/workflows/draft-wave-a.mjs fans out 5-8 chapter
agents per wave whose return schema literally includes an `invented: [...]` array of 'concrete
details you introduced that other chapters must stay consistent with' — and nothing merges those
arrays back into the ledger or tests them for conflict. The process knows agents invent facts and
then discards the evidence.

### 3. The defects live upstream in the spec files, and the spec files are never fixed. 17 of Sentience's 50 items (34%) implicate a wiki/ or editorial/ file; 7 of those live ONLY there, with no prose defect at all. Neither revision workflow edited a single wiki file, and those defects are still in the shipped bible today.

*Evidence:* The panel says it outright in the verdict: 'the chapters are more disciplined than the spec files;
most fake-rigor risk lives in technology.md / the-braid-protocol.md, not on the page.' File targets
in build/workflows/revise.js (11 jobs) and polish.js (8 jobs) are 19 manuscript/*.md paths and zero
wiki paths; `git show --stat d9d45ad d3b257b` confirms no wiki/ file changed. Still live today:
'minds that are 1.6 experiencers' in wiki/characters/cantor.md (M3 said audit it); 'VESPER'S WALL
PROVEN' in editorial/continuity-ledger.md:175 (M2 said soften it); the Searle conflation at 5 sites
— wiki/glossary.md:55, wiki/characters/aaron-solveig.md:3, wiki/outline.md:24, wiki/timeline.md:22,
wiki/philosophy/philosophy-map.md:18 (M10 said never call it the Chinese Room).

*Significance:* This is a root cause, not a class: prose gets a style sheet, an AI-slop blacklist, exemplar chapters
and a six-critic panel; the bible gets none of those and it is what every drafting subagent reads
first. Any method that audits only the manuscript will keep shipping the same defects, and will re-
inject them into the next book drafted against the same bible.

### 4. Fake rigor concentrates precisely at the load-bearing joint. In both books that were critiqued, the single worst over-claim landed on the one citation carrying the most argumentative weight — the model reaches for a famous formal result exactly where the argument most needs support.

*Evidence:* Sentience M1 (flagged by two independent lenses, called 'the book's worst fake-rigor moment because
it borrows a genuine theorem's prestige'): Ch21 re-derives the experiencer count from Cantor's real
powerset theorem — 'every braid is a kind of powerset operation... strictly larger than itself' —
which says nothing about non-integer experiencer counts. Sentience M2: 'I succeeded. I proved the
failure is necessary' presents a Gödel-inspired analogy as a discharged theorem. Talosapien: 'the
Schmidt–Frank over-claim (citation integrity, the book's one load-bearing real citation)' — 'they
proved / the result is airtight / correct' softened to 'argued / sound / the Schmidt–Frank problem'
across Ch4, Ch20, Ch22, Ch25, Ch28 (five sites, one claim). Sentience M4: dilation ratios span 365x,
87,600x and 1000x across three chapters with no cost model — 'buy dilation by the bushel costs Sable
nothing visible'.

*Significance:* This is not random error; it is the impressiveness gradient, and it is therefore predictable and
testable. A cheap mechanical pre-filter exists: grep for assertion verbs near formal objects
(prove/proved/theorem/QED/airtight/rigorous/follows that/cardinality/powerset/necessarily/entails),
then hand each hit to an agent asked one question. The Talosapien fix ('proved'→'argued') is a five-
word edit that a script could have located on day one.

### 5. A tic fix that names a string is routed around by paraphrase; a tic fix that names a concrete noun sticks. This is the sharpest predictor of which craft fixes survive, and both outcomes are in the same commit.

*Evidence:* Sentience M7 ordered the 'I want to be exact/precise about X, because X-ness is the only Y I have'
frame stripped from all narrators but Ariel/Confluence, quoting one sentence to cut. Commit d3b257b
('Polish pass: ration voice-tics'). Post-fix measurement today: the template `want(ed) to be <ADJ>
about` occurs 32 times across 23 of 39 files, with 8 different adjectives filling the slot — exact
13, precise 7, honest 5, clear 2, careful 2, true 1, fair 1, modest 1. Ch20 now reads 'because the
honesty is the only tenderness I am sure is mine' — the exact construction the plan ordered deleted,
with one word swapped. Ch25, a file the polish job actually edited, still contains 'I want to be
modest about it because modesty is the last true thing'. By contrast M8 named a concrete image
('reach for the seam like a tongue for a pulled tooth'), used by six narrators; today only 2
instances survive corpus-wide, both in Ariel chapters (ch16, ch20) — the owning voice. M8 stuck
because it was greppable.

*Significance:* Rules a memoryless subagent can check must be shape-shaped, not string-shaped. A blacklist entry
must be a slot template ('want to be <ADJ> about <NP>, because <NP> is the only <NP> I <V>') or a
POS pattern, and the checker must be told that the adjective is a free variable. Otherwise the
method builds a blacklist the author paraphrases past while reporting compliance.

### 6. 'A plan is not a revision' is verifiable at the character level: a fix named in the plan, named in the commit message, and named in the continuity ledger as a locked canon was never applied — in a file the fixing agent did edit.

*Evidence:* Sentience M12 identifies 'manuscript/44-ch25 (line 117, "she")' as a Sable-pronoun outlier. Commit
d3b257b's message says 'Continuity: normalize Sable's pronoun to "it" (prologue + Ch25).' The
ledger's REVISION PASS 1 records 'CANON LOCK (pronouns) ... Sable = "it" (glossary canon).' The
prologue was in fact fixed (now 'its own scrupulous and un-self-pitying report ... it would have
filed that under sentiment'). Ch25 was edited in that same commit (12 lines changed, forty→thirty).
Ch25 line 117 today still reads: 'They warned you. Sable warned you, I know she did, the same way
mine warned me.' Related: editorial/continuity-ledger.md:18 still reads '- [Ch1] (to append)', the
stub that nit n6 asked to backfill.

*Significance:* Three separate artifacts assert a fix that does not exist in the text. Any method must treat the
manuscript as the only source of truth for whether a defect is closed, and must re-run the detector
after the fix agent returns — never trust the agent's own completion report, the commit message, or
the ledger.

### 7. Fixes are file-scoped while defects are book-scoped, so the instances in files that the job list did not name survive the pass.

*Evidence:* Sentience M13 said 'pick one figure ... and reconcile Ch22's mixed usage to the same scheme.' The
polish job list contains ch25 and not ch22. Ch25 was fixed (forty→thirty); ch22 today contains both,
for the same span: 'thirty years gone', 'the hearing, thirty years back', 'In thirty years he had
never once' alongside 'forty years being misunderstood', 'For forty years I thought withholding',
'forty years of watching it', 'a flame in a cold room forty years ago' — 3 vs 4 instances of a
direct contradiction, in one chapter. Believer's changelog thinned the iron-filings simile 'in ch12'
only; the figure survives in ch04, ch10 ('filings finding the rim of a field'), ch14 and intC.
Sentience nit n1 ordered two instances of 'that is the whole of the chapter' cut from ch01; the
construction is alive today in ch06:15 ('That is the whole of the chapter').

*Significance:* The revision workflow's structure ('one agent per file, no write conflicts' — revise.js meta) is the
cause. A book-scoped defect needs a book-scoped fix job: the detector produces the file list, not
the plan author, and the pass re-runs until the detector returns zero.

### 8. Defect IDs are not stable between the plan and the fix jobs, so coverage cannot be audited even in principle.

*Evidence:* build/workflows/revise.js cites B1, B2, M1-M8, M10-M12, M17 — but its 'M4' is about folding Mesh
Charter provisions into Ch21, whereas revision-plan.md's M4 is the substrate-time cost model; its
'M17' is Tomas's decisive act in Ch28, whereas the plan's M17 is the closing direct-address sermon.
The workflows were written against an earlier numbering and the archived plan was renumbered. 19
file-jobs total (11 revise + 8 polish) against a 50-item plan spanning ~30 manuscript files and 6
spec files.

*Significance:* There is no way to compute 'items closed / items opened' from these artifacts. Defect IDs must be
assigned once, immutably, and carried into the fix job, the commit trailer, and the regression test
— otherwise the coverage number is unknowable and the ledger's claims are unfalsifiable.

### 9. Per-book fixes provably do not persist. Nine defect classes were fixed in one book and recurred in a later one; the strongest case is a same-week recurrence between consecutive books.

*Evidence:* (a) OVER-CLAIM ON A REAL RESULT: Sentience M2 downshifted 'PROVEN/proved' on 2026-05-30 (commit
d9d45ad); Talosapien, specced 2026-05-30 and drafted after, over-claimed 'they proved / airtight /
correct' on Schmidt–Frank at five sites, found 2026-06-03. (b) NAME COLLISION: Cruelty-Free's
continuity pass renamed Marcus Cove→Warren Speck, Helena→Clara, Terroir Group→Arbor Initiative
Partners (2026-05-24); Believer five days later shipped TWO collisions (Okonkwo used for two
characters, Ferris for two). (c) NAME RECYCLING ACROSS BOOKS: Believer renamed a character *off*
Okonkwo; Talosapien then names a character Okonkwo (3 refs). 'Priya' appears in all four books
(10/10/5/6 refs). 'Mara' is Sentience's protagonist and Talosapien's dispatch contact (133 vs 8
refs). 'Daniel' is Believer's protagonist and Talosapien's estranged husband. (d) SIMILE THINNING:
fixed in Believer (splash, iron filings) → recurred in Sentience (M8, M18 'warmth' ~31x) → recurred
in Talosapien (floor-tilt, Liss coda). (e) DIDACTICISM: Believer ran two de-didacticization passes →
Sentience M9/M16/M17. (f) The M7 'want to be <ADJ> about' frame: 32 hits/23 files in Sentience post-
fix, and 10 hits/9 files in Cruelty-Free, a book written five months and two novels earlier by a
different narrator. (g) Aphorism creep: Believer B6 → Sentience m13. (h) Numeric-duration
contradictions: Cruelty-Free (14/16y, 22/15y, 48/72h) → Sentience (30/40y, Tomas's age). (i) Every
book's editorial apparatus lives in that book's repo.

*Significance:* This is the empirical case for desk/ as the home of the method: the author is a set of files, and a
lesson recorded in book 4's editorial folder is invisible to book 5. The regression suite, the used-
names registry, and the shape-blacklist must live one level above the books and be executed by every
book's build.

### 10. The idiolect does not merely persist between books — one flagged construction escalated monotonically across all four, including after being named as a defect.

*Evidence:* Occurrences of 'the whole of' per book in publication order (pre-Hemingway text for Talosapien,
reconstructed from commit 5be2db6): Cruelty-Free 2 (2.2/100k), Believer 15 (16.4), Sentience 52
(46.5), Talosapien 60 (54.6). Sentience nit n1 flagged this family and explicitly licensed it
('"that was the whole of it" can stay as occasional Ariel cadence') — the next book used it 60 times
across 12+ chapters. 'thing' rises 268→590→683→763 per 100k; 'there was no one' rises
1.1→6.6→10.7→14.6. Constructions can also decay: 'not quite' falls 28.5→9.8→7.1→3.6. Cross-book
function-word cosine similarity is 0.93-0.99.

*Significance:* There is no reset between books, and licensing a tic in one book's nit list is an instruction to the
next book to use it more. Anything the ledger 'permits' must be permitted with a numeric budget (N
per 100k words) that the next book inherits, not with prose that reads as approval.

### 11. The two classes that need a reading agent — emotional sag and scene-shape repetition — were both visible in the outline before a word was drafted.

*Evidence:* Sentience M15: 'Part III middle runs arid — three idea-heavy chapters with thin human anchoring ...
the reader goes a long stretch without the love story they're reading for.' M16: the love is
embodied in exactly one chapter (Ch19, 'A Life'), arriving at E3, chapter 19 of 29. Believer B2:
'Mid-book episodic plateau (ch11–ch19). The "rooms" chapters share a structure: Daniel sits in a
room, someone bleeds or doesn't, Daniel reflects on the same paradox.' That shape is legible in
believer/manuscript/beat-sheet.md from the chapter titles alone: ch11 'Good', ch12 'Bad', ch13 'What
He Couldn't Take Back', ch19 'Doubters'. Sentience n7 flags the same thing for a scene type:
'cumulative "person becoming discontinuous at a bedside" load (Walter, Mara's father in chs
4/8/19/22, Jonas)' — six bedside scenes.

*Significance:* The most expensive detector (naive readers on finished prose) is not the earliest one. A machine-
readable outline carrying per-chapter tags — shape, participants, whose body, idea-load, chapters-
since-the-central-pair-shared-a-scene — turns both classes into an outline-stage script and reserves
the reading agent for confirmation only.

### 12. Defect counts are NOT comparable across books, because the critic prompt differed. Talosapien's panel was instructed to suppress findings.

*Evidence:* talosapien/build/workflows/editorial-panel.mjs COMMON block: 'Report ONLY real problems worth an
author's time — do not pad ... Prefer fewer high-confidence findings over many speculative ones.' It
also opens by telling six referees the book 'is built to be AMAZING FOR SOME ... award-submittable,
uncompromising' and asks each for '1-3 genuine STRENGTHS.' Talosapien returned 13 items on ~110k
words; Sentience's five-critic pass returned 50 on ~112k. Talosapien's verdicts: 'award-grade and
almost entirely clean', 'outstanding and very nearly bulletproof', 'frankly, a triumph'. Confound
two: Talosapien has 33 commits, Sentience 8, Believer 6, Cruelty-Free 13.

*Significance:* The 13-vs-50 gap cannot be read as a quality difference; it is partly a prompt difference and partly
an iteration difference, and the two are not separable from these artifacts. Any future claim that a
method improved the books needs a fixed critic prompt held constant across books, and the yield-per-
critic recorded — otherwise the measurement instrument moves with the thing measured.

### 13. One class is invisible to any manuscript-only audit: the payoff whose plant was never drafted. It shows up only as an insertion in a continuity commit.

*Evidence:* Cruelty-Free commit 82341ee adds a signature detail to ch01 ('There is a second thing. I always
leave a handwritten menu card ... a sourcing note at the bottom with the farm name and county
underlined') and a matching paragraph to ch07 ('And at each scene, apparently, a menu card.
Handwritten. Small, fastidious script.'). The commit subject calls it 'the tell'. The payoff
chapters were drafted in parallel with the setup chapters, so the detective's thread existed
downstream with nothing upstream to find. Believer's version of the same class: 'The Priya spine
submerges too long. Planted beautifully in ch01/intA, then largely dormant until Holm (ch16) and the
payoff (ch21).'

*Significance:* Parallel chapter drafting makes plants structurally unlikely: every agent sees the beat brief for
its own chapter and the ledger, so it can honour a fact but cannot know it must seed one. The
outline must declare, per payoff, the chapters that plant it, and integration must fail when the
planting chapter's text lacks the planted token.

### 14. Cheapest reliable detector per class, with the earliest stage it can run. Six of ten classes are fully mechanical; three need a narrowly-briefed reading agent; one needs a naive reader.

*Evidence:* 1 CONTINUITY (28): mechanical, at draft-return before the next wave. Merge each agent's `invented`
array into a typed ledger (entity, attribute, value, unit) and fail on any key with two values; plus
three specific greps — pronoun regimes per named entity, surname multiset for collisions, and a
normalised-spelling check (m12 'Solveig' vs 'Sólveig', 65 refs). Every one of the 28 is a value
conflict on a named key. 2 VOICE-TIC (14): mechanical, after each parallel wave, not at book end.
Shape templates with free adjective/noun slots plus per-POV attribution: for every declared figure,
count instances by POV file and flag any figure whose owning-voice share is below 100%;
refrain/n-gram detection already exists in desk/tools/prose_audit.py (refrains(), shared_ngrams()).
3 SCHOLARSHIP OVER-CLAIM (10): pre-filter mechanically (every real proper name + the verb attached),
then one agent per citation, asked exactly: 'Does the cited work actually establish this claim?
yes/no + one sentence.' Run at bible-authoring, since 5 of the Searle sites are in wiki/. 4 FAKE
RIGOR (9): grep the assertion-verb set near formal objects, then the same one-question agent. Run at
bible-authoring — M3, M4, M5, M6, m1, m2, m3 all name technology.md or the-braid-protocol.md. 5
THESIS-STATED (7): fully mechanical and free, because the thesis is already written down —
editorial/the-gap-and-the-voice.md §3 contains the sentence 'the gap hurt, then it didn't, and that
turned out to be the loss' and M9 is dying Ariel reciting it verbatim. Fuzzy-match the spec's own
thesis string against every paragraph; any hit in a body chapter is a violation. Budget: one
explicit statement per book, in the frame. 6 EMOTIONAL SAG (7): naive reader agents (no outline, no
bible, no thesis) on three consecutive chapters, asked for symptoms not judgments ('where did you
skim, what did you want next, whose body were you in'); mechanical proxy first — chapters since the
central pair shared a scene, dialogue share, named-human-on-page beats. 7 SCENE-SHAPE REPETITION
(4): mechanical at outline stage from a per-chapter shape tag with a repeat budget. 8 FACTUAL ERROR
(4): units/quantity linter catches 'sixty million stadia'; a verification agent is needed for 'older
than the mammals' (backwards — mammals predate 66 Ma) and for the mesothelioma-in-six-years
implausibility Cruelty-Free silently changed to pulmonary fibrosis. 9 MECHANICAL STYLE (3): pre-
commit script — accent normalisation, em-dash spacing, section glyph, sentence-length cap (m14 flags
a ~250-word sentence), numbers-under-100. 10 PLANT/PAYOFF (2): outline declares plants per payoff;
integration greps the planting chapter for the token.

*Significance:* 62 of 88 documented defects (classes 1,2,7,9,10 plus the mechanical halves of 3,4,5) are reachable
by script or by a grep-plus-one-question agent. The expensive instrument — reading the whole book —
is needed for roughly 7 items in 88. The current process inverts this: it spends six full-manuscript
critic reads and no scripts.

### 15. The mechanism that enforces the target voice is the same mechanism that manufactures the tics, so tic control cannot be a prompt instruction — it has to be a downstream budget.

*Evidence:* talosapien/build/workflows/draft-wave-a.mjs orders every chapter subagent to read the same two
exemplar chapters and 'Match the cadence and paragraph-rhythm of the exemplar for your timeline.'
sentience/editorial/style-sheet.md §7 hands every drafter the same eight-row canonical metaphor
table. Those instructions are why the books hold their register; they are also, exactly, why 'the
reach for the seam like a tongue for a pulled tooth' turned up near-verbatim in six narrators (M8)
and why the same style sheet that says 'A persona never narrates knowledge it could not have had'
produced five narrators sharing one self-announcing frame (M7). The same style sheet already carries
an AI-slop blacklist (§11) that the drafters did obey — no 'In a world where', no 'it was then that
I realized' — proving that string-level prohibitions work and shape-level ones do not.

*Significance:* Do not weaken the exemplar-matching; it is load-bearing. Instead measure convergence after the wave
and enforce per-figure ownership budgets — figure X may appear N times, only in POV Y — as a post-
generation check the drafting agents never see. This is the one place where an LLM author's cheapest
advantage (measurement) directly answers its cheapest deficit (self-priming).

**Implications for the method**

- Make the ledger executable, not prose. The single highest-yield change: the `invented` array that
  every drafting subagent already returns must be merged into a typed fact store (entity, attribute,
  value, unit, source chapter) and conflict-checked before the next wave drafts. That one change
  addresses 28 of 88 documented defects and all 3 declared blockers, at a cost of seconds per wave.

- Audit the bible before the prose. 34% of Sentience's items implicate a spec file and 14% live only
  there, and no fix job ever touched a spec file, so those defects shipped and will re-infect any
  later book drafted against them. The style sheet, blacklist, exemplar discipline and critic panel
  must all be applied to wiki/ files first, because every drafting agent reads them before it reads
  anything else.

- Write blacklist rules as shape templates with free slots, never as strings. Sentience proves both
  directions in one commit: the concrete-noun figure (tooth/seam) was successfully rationed to its
  owning voice; the syntactic frame ('want to be <ADJ> about X, because X-ness is the only Y I
  have') simply recruited eight new adjectives and now stands at 32 instances across 23 of 39
  chapters. A memoryless checker must be handed the pattern with the variable marked, plus the
  numeric budget and the owning POV.

- Never accept an agent's completion report as evidence of a fix. A defect is closed when the detector
  that opened it returns zero on the manuscript — nothing else counts. Three artifacts (the plan,
  the commit message, the continuity ledger) all assert that Sable's pronoun was normalised in Ch25;
  the sentence 'Sable warned you, I know she did' is still on the page in a file that pass edited.

- Derive the fix job's file list from the detector, not from the plan author, and re-run to zero.
  File-scoped fixes for book-scoped defects left 30-vs-40 years contradicting itself seven times
  inside one chapter and left the iron-filings simile in four of five Believer files after the pass
  that 'thinned' it.

- Assign immutable defect IDs at detection and carry them into the fix job, the commit trailer and the
  regression test. The current fix workflows cite M-numbers that mean different things than the
  archived plan's M-numbers, so coverage is not computable and the ledger's claims are
  unfalsifiable.

- Put the regression suite, the used-names registry and the shape-blacklist in desk/ and run them from
  every book's build. Nine defect classes demonstrably recurred book-to-book, including an over-
  claim class fixed in Sentience on 2026-05-30 and reproduced in Talosapien within four days, and a
  character name that Believer deliberately renamed away from and Talosapien then reused. Because
  the author does not persist, only the files can.

- License nothing in prose; license with a number. Sentience's nit list explicitly permitted 'the
  whole of' as occasional cadence and the next book used it 60 times — the count rose monotonically
  across all four books (2, 15, 52, 60). Every permitted figure needs an inherited budget per 100k
  words, checked by script, so an approval in book N is not an amplifier in book N+1.

- Tag the outline machine-readably and catch the structural classes there. Both classes that seem to
  require taste — emotional sag and scene-shape repetition — were legible in the beat sheet before
  drafting ('Good' / 'Bad' / 'Doubters'; six bedside-discontinuity scenes; the central couple
  sharing one happy scene in 29 chapters). Reserve the naive-reader protocol for confirming what the
  outline metrics already flagged.

- Fix the critic prompt before comparing books. Talosapien's panel was told to prefer few high-
  confidence findings, given the book's own 'award-submittable' framing, and asked for strengths; it
  returned 13 items to Sentience's 50 on a comparable word count. Until the critic brief is held
  constant across books and its yield recorded, no claim that the method improved the writing is
  measurable — and the flattery in the panel's verdicts ('a triumph', 'award-grade') is information
  about the prompt, not the book.

## The Otto Quill Production Line: Reconstructing Five Books' Process, and Where It Breaks

### 1. All four novels were produced on one invariant five-stage pipeline that never changed between books: design spec → story bible → author-written voice-lock chapters → parallel subagent fan-out drafting → one critique-and-patch pass → build.

*Evidence:* veganassassin/docs/superpowers/specs/2026-05-24-cruelty-free-design.md §'Automation pipeline' (5
steps: bible → parallel drafting → assembly → continuity pass → artifacts);
believer/docs/superpowers/specs/2026-05-29-believer-novel-design.md §'Production method (maximal
automation)' (5 steps, adds 'Draft a voice anchor (ch01), then draft all remaining units in
parallel'); sentience/docs/superpowers/specs/2026-05-29-sentience-design.md §7 (5 steps, adds
'editorial critique panel'); talosapien/docs/superpowers/specs/2026-05-30-talosapien-design.md §11
(verbatim descendant of Sentience's). Git wall-clock: Cruelty-Free 14:58→16:20 on 2026-05-24 (82
min); Believer 14:07→16:38 on 05-29; Sentience 15:16→23:51 on 05-29; Talosapien 17:35→19:23 on 05-30
(108 min for spec, bible, 34 prose files, panel, revision and EPUB).

*Significance:* The method being designed in desk/ is the fifth revision of a pipeline that has already run four
times, so its failure modes are measurable rather than hypothetical. Any new rule must justify
itself against a baseline that already produces 90–110k publishable words in under two hours.

### 2. Git history is genuinely thin for two of the four books, and that is itself a process fact: Believer and Sentience each committed their entire draft in one commit, so their wave structure exists only in workflow scripts. Talosapien is the only book whose production is legible from git.

*Evidence:* believer 387bdc7 'Believer: complete novel (~92.5k words) + Kindle publication package' = 63 files,
7,668 insertions, one commit. sentience 93de6b5 'Draft complete manuscript of Sentience + full
apparatus' = 86 files, 6,751 insertions, one commit. Talosapien: d8b7a30 (openers) → b9ce1b4 'Wave
A: draft body chapters 3-15 via character subagents' (28 files) → 0adb2e7 (climax pair) → 31c65d2
'Wave B Part III' → dda2786 'Wave B complete' → 0a881fd 'Editorial panel + revision pass'.
Manuscript-touching commits per book: Cruelty-Free 6, Believer 3, Sentience 4, Talosapien 9.

*Significance:* Checkpoint granularity is the difference between a process you can audit and one you can only
assert. Talosapien's advantage is not more revision passes (roughly the same number as Sentience) —
it is that each batch was frozen and inspectable before the next batch depended on it.

### 3. The highest-leverage machinery invention in the corpus is Talosapien's replacement of concurrent ledger-appending with structured `invented` returns: Sentience had every parallel drafting agent append continuity facts to one shared file; Talosapien made agents return what they invented and had the orchestrator write the ledger.

*Evidence:* sentience/build/workflows/part2.js:46, part3.js:48, part4.js:47 all instruct 'After writing, append
continuity facts (bullets prefixed [TITLE]) to ${ROOT}/editorial/continuity-ledger.md.' Result:
sentience/editorial/continuity-ledger.md is 357 lines of prose chronicle keyed by chapter title,
with the hole '[Ch1] (to append)' still unfilled at ship (nit n6 in the revision plan).
talosapien/build/workflows/draft-wave-a.mjs SCHEMA requires `invented: {type:'array',
description:'Concrete details you introduced that other chapters must stay consistent with'}`.
Result: talosapien/editorial/continuity-ledger.md is 160 lines of lock-lists — '## Wave A
established facts — LOCKED for Wave B (ch16-29)', with forward directives ('Wave B MUST reveal it in
Part III').

*Significance:* The Sentience ledger records what happened; the Talosapien ledger is a contract constraining what
may happen next. Sentience's plan carries 8 continuity items including two blockers (B1 uncle/lover
contradiction, M11 three pronoun regimes for one character, M13 thirty-vs-forty years, M14 an
unreconcilable age); Talosapien's report carries one blocker and one major. This is the one
apparatus element with a clean mechanism-to-outcome story.

### 4. The revision step is the weakest link, and it fails the same way in every book: a defect is diagnosed as a string, the fix removes instances of that string, and the underlying construction is untouched. Sentience's flagship craft fix changed the tic count by exactly zero.

*Evidence:* sentience/editorial/revision-plan.md M7 (flagged '[multi-lens: prose + emotional]', listed #5 in
'Top 5 to fix first', called 'the highest-leverage craft fix') targets 'I want to be exact/precise
about X, because precision/exactness is the only [thing] I have'.
sentience/build/workflows/polish.js encodes it literally: 'If Cantor uses any "precision/exactness
is the only X I have/am sure is mine" construction, CUT it'. Commit d3b257b is titled 'Polish pass:
ration voice-tics'. Measured: 'I want to be (precise|exact|clear|careful|honest|modest|fair)' occurs
47 times in 26 files at draft commit 93de6b5 and 47 times in 26 files at HEAD. Four of eight polish
agents (ch08, ch09, ch10, ch17) correctly reported 'the targeted text is not present' — those
chapters carry 'I want to be exact about the texture, because the texture is the discovery'
(ch17:23) and 'I want to be precise about what I was doing, because the imprecision is the whole
problem' (ch10:11): same construction, different tail. The literal '…is the only X' tail existed in
only 3 files, 2 explicitly protected by the brief. Talosapien fails identically at smaller scale:
the panel reserved the 'floor tilted' figure to three instances; measured 14 before the panel commit
(dda2786), 11 after (0a881fd); 'small dishonesty of a man who…' 9 → 7.

*Significance:* A memoryless subagent given a phrase deletes that phrase and nothing else — correctly, by its own
lights. The defect class the panel actually detects is a rate over a construction, and no part of
the current apparatus can express, transmit, or verify a rate. This is the concrete reason
desk/templates/voice-profile.json's budget model (instances per 10,000 words) is the right shape and
the style sheets are not.

### 5. The comparison 'Talosapien's report is cleaner than Sentience's, therefore Talosapien is the better book' is substantially confounded: the two panels were prompted to produce different quantities of findings, and the item counts follow the prompts.

*Evidence:* sentience/build/workflows/editorial.js instructs each of 5 critics 'Aim for the 8-20 highest-value
findings, not an exhaustive nitpick dump' (mechanically 40–100 raw findings), then hands them to a
dedicated synthesis agent told to 'group by severity… dedupe'. Output: revision-plan.md with 2
blockers + 18 majors + 21 minors + 9 nits = 50 items. talosapien/build/workflows/editorial-panel.mjs
instructs each of 6 referees 'Report ONLY real problems worth an author's time — do not pad… Prefer
fewer high-confidence findings over many speculative ones', and has no synthesis phase — critique-
report.md is a hand-written verdict summary plus a 12-item resolution log. Talosapien also adds a
category Sentience lacks: 'Deliberately left (licensed choices)', converting three findings to non-
defects by fiat.

*Significance:* Defect count is set by the critic prompt and the reporting format, so it cannot be used as a cross-
book quality metric — a method that grades books by their own report length is measuring its own
instructions. At least part of the audit must be computed rather than reported.

### 6. The 'AI-slop blacklist' present in every style sheet since Believer is pure ceremony: it bans constructions the model does not write and names none of the constructions it measurably does write.

*Evidence:* talosapien/editorial/style-sheet.md §12 and sentience/editorial/style-sheet.md §11 both ban 'In a
world where…', 'little did they know', rhetorical-question-as-suspense, 'it was then that she
realized', tri-colon abuse, clean morals, info-dumps. Zero of these correspond to any measured
feature of the four manuscripts. The actual fingerprint — 'the way you/one X' similes at 94–160 per
100k words in every book, 'thing' at 268–763 per 100k, 'because' at 291–586 per 100k, median
sentence length 8–11 in all four, 17 five-grams shared across all four books — appears in no
blacklist. The blacklist is also propagated verbatim into every drafting prompt (draft-wave-a.mjs:
'AVOID the AI-slop blacklist: no "In a world where", no "little did they know"…'), spending prompt
budget on a null check.

*Significance:* The blacklist encodes a human's imagination of what an LLM writes badly rather than a measurement of
what this LLM actually writes. It is the clearest ritual-without-result in the corpus and the first
item to delete.

### 7. The style sheet's mandated 'canonical metaphor system' table is not merely inert — it actively generates the defect the critique panel later flags. The apparatus manufactures its own bug.

*Evidence:* sentience/editorial/style-sheet.md §7 and talosapien/editorial/style-sheet.md §7 both mandate a
table of canonical figures to be reused consistently ('Reading one's own past transcript → a letter
in your own hand you don't remember writing'; 'The deep past → a letter in a hand no one living can
read'), and the drafting prompts enforce it ('Use/EXTEND the established metaphor system'). The
panels then flag exactly this: Talosapien's prose referee — 'Main notes: a few signature figures
recur too often'; Sentience M8 — 'The seam/tooth gap-check figure shared by all six narrators…
turning a per-character motif into house style and undercutting the distinct-instances premise.'
talosapien/editorial/hemingway-brief.md, whose whole job was to strip the register, models the house
simile-frame in its own target example: 'We wrote them the way you write a name on a stone over a
grave you cannot open.'

*Significance:* A shared figure table plus a self-priming model equals guaranteed xerox. The table is worth keeping
only if every entry carries an owner and a budget (desk/templates/voice-profile.json's
declared_refrains plus per-narrator owns_figures/forbidden_figures is the right correction), and
drafting prompts must never model the banned shape in their own examples.

### 8. The 'earnest edition' of Talosapien — a 45% cut and a full register conversion against a named master — is the largest intervention in the corpus and proves exactly which properties style instruction can move. It moved sentence length. It did not move the fingerprint.

*Evidence:* Commit 6aad402, 37 files, manuscript 109,047 → 60,263 words. editorial/hemingway-brief.md pairs a
hard number ('Each file's new word count must be 45–55% of the original') with taste instructions
('Short declarative sentences… Cut adjectives and adverbs… The iceberg'). Measured pre vs post: mean
sentence length 23.4 → 14.7 words (the numeric instruction landed); function-word cosine between the
two versions 0.9968; 'the way you/one X' simile rate 93.7 → 80.8 per 100k (−14%); 'thing' 763 → 717
per 100k (−6%); most of the 17 four-book five-grams survive at equal or higher normalized rate ('the
way you look at a' 1.8 → 3.3 per 100k). All locked continuity facts survived ('there were four' in
12 files, crest/grey physiology in 13–14 files) — they were listed under 'What you MUST preserve'.

*Significance:* Two rules fall out. (1) A style instruction with a number attached is obeyed; one without a number
is absorbed and returned. (2) An enumerated preserve-list survives a total rewrite, so the
continuity ledger is robust to interventions far more violent than any revision pass currently
attempts — the method can afford to be far more destructive than it has been.

### 9. The six-referee panel, reading the full manuscript along a dedicated continuity dimension, missed a numeric contradiction occurring four times in one chapter and once inside a single sentence. It was caught three days later by building a derived artifact that forced the number to be written down independently.

*Evidence:* talosapien/build/workflows/editorial-panel.mjs charges the continuity referee to 'Verify every
locked fact in the continuity ledger holds across all chapters' and the hard-SF referee with 'the
orbital mechanics of redirecting a Belt object'. Panel verdicts in editorial/critique-report.md:
continuity 'Exceptionally disciplined'; hard-SF 'Genuinely award-grade and almost entirely clean… No
physics errors'. Commit 2ad2b99, three days later: 'Ch18… called the Belt object "a hundred million
kilometers" away four times — ~0.67 AU, closer than the asteroid belt can be, contradicting both the
book's own "fourteen light-minutes" (used in six other chapters) and the wiki's "belt between Mars
and Jupiter." One sentence even paired the two ("a hundred million kilometers away tick through
fourteen minutes").' Found during the wiki's web-verified science pass, not by any reader.

*Significance:* Panels of readers do not do arithmetic, even when instructed to and even when both contradictory
numbers sit in one sentence. Every unit and quantity needs a computed cross-check. The generalisable
move is that building a second derived artifact from the same facts is a cheap and unusually
effective consistency check.

### 10. Not one mechanical check on prose exists anywhere in any book's pipeline. Every prose judgment across 355,000 published words was produced by an LLM reading and reporting; none by counting.

*Evidence:* The complete set of executable checks across all four repos: believer/build/build_book.py,
sentience/build/compile.py, sentience/build/make_reader.py, talosapien/build/compile.py (all
EPUB/DOCX assembly) and talosapien/build/workflows/check_wiki_links.py (link integrity, written
2026-06-02 for the wiki, never pointed at the manuscript). Greps for count/rate/regex logic across
all six workflow scripts return only in-story prose. desk/tools/prose_audit.py — the operation's
first prose measurement instrument — is dated 2026-08-31, months after the last book shipped.

*Significance:* The entire apparatus is one instrument (an LLM reader) used six ways. It is excellent at content
defects — steel-manning, misattributed theorems, whether a scene lands — and structurally blind to
distributional and arithmetic ones. A second, non-LLM instrument is not an optimisation; it covers a
category the process cannot currently see.

### 11. No blind or naive reader was ever instantiated for any of the four books. Every critic in every panel was handed the style sheet, ledger, bible and outline before reading a word of prose.

*Evidence:* sentience/build/workflows/editorial.js MANUSCRIPT_NOTE hands every critic 'editorial/style-sheet.md,
editorial/the-gap-and-the-voice.md, wiki/ (bible, glossary, philosophy-map, tech),
editorial/continuity-ledger.md'. talosapien/build/workflows/editorial-panel.mjs COMMON hands every
referee the style sheet, continuity ledger, glossary and outline. Searching all six workflow scripts
for blind/naive/first-time-reader framing returns only in-story matches (Téo's blind two-reader
spherule protocol; the three-lab blind split). The only deliberate context-withholding is in
drafting, not critique: sentience part3.js persona phase — 'FIRST read ONLY your own character file…
Do NOT read the outline or other characters' files — you only know what YOU would know.' Talosapien
then dropped even that, merging persona and drafter into one agent that reads everything ('YOU ARE
THE POV CHARACTER').

*Significance:* Every quality verdict in the corpus comes from a reader who already knows the intent — the one
reader who cannot tell you whether the intent reached the page. Sentience proved the withholding
technique works and used it only on drafters; Talosapien discarded it. It should be reinstated and
pointed at critique, where the drawer actually belongs.

### 12. Nothing in the process distinguishes 'a document describing the fix exists' from 'the manuscript changed'. Both books shipped commits whose messages claim fixes the files do not contain.

*Evidence:* sentience d3b257b commit body: 'M7/M8: ration the shared "precision is the only X" hedge and the
seam/tooth gap-figure to one owning voice each; fingerprint the others' — construction count
unchanged at 47. talosapien 0a881fd claims the floor-tilt figure was 'Reserved for the Ch1 origin,
the Ch21 Vael-apex, and the Ch26 impact' — 11 instances remain. believer 7512b13 'Revision pass 1
(surgical)' nets −308 words on 92,471 (0.33%), and believer/docs/revision-changelog.md declines the
cadence finding outright: 'Cadence "metronome" (long-periodic → short-flat): judged too risky to
operate on mechanically… Not forced.' Pass 2 (788efa1) removed a further 155 words.

*Significance:* The pipeline has a plan artifact, an edit artifact and a commit message, and no gate comparing them.
Every fix needs a post-condition a memoryless subagent can evaluate against the file — a count, a
threshold, a diff assertion — or the fix is a claim rather than a change.

### 13. The apparatus was almost fully invented in book 2 and has been elaborated, not replaced, since. What each later book added is short and specific — and it is always transmission or scope, never verification.

*Evidence:* Cruelty-Free (book 2) already had, in one 355-line manuscript/bible.md: §3 VOICE GUIDE ('the most
important section'), §5 world & proper nouns, §6 timeline, §8 MOTIF LEDGER, §9 chapter outline with
per-chapter hooks, §10 CONTINUITY RULES FOR DRAFTERS. It had no critique panel and no editorial
artifact; its entire editorial pass is commit 82341ee, 38 insertions / 25 deletions across 15 files.
Believer added: the bible split into a 7-file wiki with a precedence rule ('When prose and wiki
disagree, the wiki wins… never silently'); manuscript/beat-sheet.md giving each unit Purpose / Beats
/ Open on / Close on / Plant; a named voice-anchor chapter; an external critic (branch experiment-
grok-revision); the findings/changelog artifact pair. Sentience added: editorial/ separate from
wiki/; style-sheet.md as 'the binding constitution of the prose'; a formal continuity-ledger.md; a
thesis addendum (the-gap-and-the-voice.md) read by every drafter; the panel as runnable code with a
synthesis agent. Talosapien added: waves with an inter-wave lock; the structured `invented` return;
a per-chapter 'RHYME (for you only; NEVER state it on the page)' field; a sixth referee aimed at the
book's fatal failure mode; the 'Deliberately left (licensed choices)' category. Book 1 (tinarex) is
1,189 words with no apparatus at all.

*Significance:* Five books of elaboration produced better transmission and better scope and never once produced
verification. That is precisely the hole desk/ exists to fill.

### 14. Talosapien's premise-failure-mode referee — a critic charged with the one thing that would kill the book — is the highest-yield critic invented in the operation, and it was generated from the spec's own risk register.

*Evidence:* talosapien/build/workflows/editorial-panel.mjs CRITICS['premise-failure-mode']: 'Your job is to
catch any sentence that makes a serious reader smirk at "sapient dinosaurs"… Separately, judge
whether the book EARNS its two refusals'. It derives directly from design spec §13 ('The dinosaurs
feeling silly (the failure mode of the whole premise)… If a single sentence makes them ridiculous,
it is a bug') and its severity scale names it a blocker ('makes the dinosaurs ridiculous'). Its
verdict — 'not a single sentence would make a serious reader smirk' — is the panel's only finding
whose failure would have made the book unpublishable. Sentience's parallel case: spec §9 lists
'philosophical strawmanning', it got a philosophy referee, and that referee produced M10 (Sólveig
conflated with Searle) and the m7 protect-note.

*Significance:* The critic that reliably earns its cost is the one derived from the spec's named risk. Panel
composition should be generated from the risk register rather than a generic lens list — which means
every spec must be required to name its make-or-break failure mode, because that name becomes a
critic.

### 15. Cross-book contamination has no owner in the process, and it extends past prose into the name generator: four unrelated books each contain a character named Priya.

*Evidence:* Whole-word counts across the four manuscripts — Priya: Cruelty-Free 10 (Thorne's household manager),
Believer 10 (Priya Raman, the buried witness), Sentience 5 (the night aide), Talosapien 11 (Priya
Sandoval, forensic geochemist). Mara: Believer 3, Sentience 133 (Mara Vance), Talosapien 12 (Roan's
dispatch contact). Daniel: Believer 599 (protagonist), Talosapien 3 (Asha's ex-husband). Okonkwo:
Believer 2, Talosapien 3. Vance: Believer 7, Sentience 9. Marisol: Cruelty-Free 124, Believer 7. The
fingerprint also spans a model-version change: Cruelty-Free carries 'Co-Authored-By: Claude Opus
4.7', the other three 'Opus 4.8', and 17 five-grams still appear in all four. Every continuity
ledger, style sheet and glossary in the operation is scoped to a single repository; nothing reads
across books.

*Significance:* Believer's panel caught its two in-book name collisions (Okonkwo × 2, Ferris × 2) because they were
in one repo. The identical defect across repos is invisible to every instrument the operation owns.
A cross-book banned-names register and a cross-book idiolect ledger in desk/ would catch a class of
defect that is currently 100% undetected.

### 16. The external-critic experiment (Grok on Believer) converged with the internal critic on the same top finding — and the revision still declined to act, which shows the bottleneck is not diagnosis but self-adjudication.

*Evidence:* believer/docs/revision-changelog.md: 'Reconciles my critical reread with Grok's review (which
converged strongly on "overwritten / the middle repeats its insight / didacticism").'
believer/docs/revision-findings.md B1: 'the central thesis… is stated explicitly by Daniel, Tamsin,
Holm, Anton, Crane, AND narration, often more than once per chapter… Biggest single lever: cut
roughly a third of the explicit articulations.' The changelog's 'Why not deeper' then declines: 'the
book's repetition is mostly the intentional chorus — the "stop knowing" insight recurs ~12 times,
but largely in distinct voices… That distribution is the idea propagating through the culture, and
gutting it would remove a feature, not a flaw.' Two revision passes removed 463 words total from
92,471 (0.5%).

*Significance:* Two independent critics, one from a different model family, agreed on the diagnosis, and the reviser
talked itself out of the treatment with an argument that is plausible and unfalsifiable as stated.
Talosapien's 'Deliberately left (licensed choices)' formalises the same move. The gap the process
has no defense against is that one intelligence diagnoses, adjudicates and executes, and can always
license its own inaction.

**Implications for the method**

- Every ban names a CONSTRUCTION plus a RATE, never a phrase. The Sentience evidence is decisive: a
  phrase ban produced 47 → 47 because the construction routed through new adjectives, and four of
  eight fix agents correctly reported 'not present'. desk/templates/voice-profile.json's budgets
  (instances per 10,000 words) is the right encoding; the style sheets' prose prohibitions are not.

- Every fix ships with a post-condition a memoryless subagent can evaluate against the file — a grep,
  a count, a threshold. No commit may claim a fix its post-condition does not confirm. This is the
  missing gate: five books have no mechanism separating 'a plan exists' from 'the manuscript
  changed'.

- Delete the AI-slop blacklist and replace it with the measured idiolect ledger. Zero of its seven
  banned items occur in any of the four books; every actual tic (the-way-you similes at 94–160/100k,
  'thing', 'because', median sentence 8–11) is absent from it.

- Attach a number to every style instruction you actually want obeyed. The Hemingway brief's numeric
  target ('45–55% of the original') was hit exactly; its taste instructions left the function-word
  profile at cosine 0.9968. Cadence targets belong in a voice profile with min/max bands, set
  deliberately different from the previous book's measured actuals.

- Keep the canonical-figure table only with per-figure owner and budget. As written it mandates reuse
  and then the panel flags the reuse. Every recurring figure needs an owner, a home chapter, a
  maximum count, and a required development on each recurrence — and drafting prompts must not model
  a banned shape in their own examples (the Hemingway brief's target example contains the house
  simile-frame).

- Keep the wave lock and the structured `invented` return; they are the two apparatus elements with a
  clean mechanism-to-outcome story. Facts flow agent → orchestrator → LOCKED list → next wave, never
  agent → shared file. Concurrent appends produced a 357-line chronicle with a hole in it and eight
  continuity defects; locks produced a 160-line contract with one blocker.

- Add a computed layer beside the reader layer. No prose measurement instrument existed during any
  book's production; the only executable checks were EPUB assembly and wiki links. Repetition rates,
  cadence distributions, per-narrator syntax distance, unit/quantity consistency and promise-ledger
  closure are all computable and none are readable.

- Cross-check every number by building a derived artifact from it. The six-referee panel missed a Belt
  distance that contradicted itself four times in one chapter and once inside a single sentence; it
  was caught when the wiki forced the figure to be written down independently. Restating facts in a
  second context is a cheap consistency instrument the operation discovered by accident.

- Instantiate blind readers and point them at critique, not drafting. Every critic in every panel was
  handed the style sheet, ledger, bible and outline before reading a word of prose — the one reader
  who cannot tell you whether the intent reached the page. Sentience proved context-withholding
  works (persona agents forbidden the outline) and used it only on drafters; Talosapien dropped it
  entirely.

- Generate the panel from the spec's risk register, not a generic lens list. Talosapien's highest-
  value referee came verbatim from its spec §13 make-or-break risk. Require every spec to name the
  one failure that would kill the book; that name becomes a critic with blocker authority.

- Never compare books by defect count. Sentience's 50 items and Talosapien's 12 differ largely because
  one panel was told 'aim for the 8-20 highest-value findings' with a synthesis agent and the other
  'do not pad… prefer fewer high-confidence findings' with none. Cross-book quality tracking must
  use computed metrics no prompt can inflate.

- Move the idiolect ledger, the banned-construction budgets and a cross-book proper-noun register into
  desk/ where they are inherited. Four unrelated books each contain a character named Priya, the tic
  Sentience tried to ration also appears in Cruelty-Free, and the fingerprint survives a model-
  version change — none of it visible to per-repo apparatus, because there is no author between
  books, only repositories.

- Require a licensed refusal to carry a name, a count, and a location. Believer's revision declined
  the cadence finding as 'too risky to operate on mechanically' and the didacticism finding as 'the
  intentional chorus'; Talosapien formalised the move as 'Deliberately left (licensed choices)'.
  Both may be right, but as written a licensed refusal is indistinguishable from a skipped fix — the
  same intelligence diagnoses, adjudicates and executes, and can always exonerate itself.

- Budget for destruction. The earnest edition cut 45% of a book and every explicitly enumerated locked
  fact survived, so the continuity ledger tolerates interventions far more violent than any revision
  pass has attempted. Passes that move 0.3–0.5% of a manuscript (Believer: 463 words of 92,471
  across two passes) fail to exercise the one advantage — free, darling-less rewriting — that the
  method exists to exploit.

## The Body Under the Costume: what has never changed in 300,000 words of Otto Quill, and the only three things that ever moved it

### 1. The invariant is not a vocabulary or a set of tics. It is a single unchanged sentence architecture. Across every segment Otto Quill has ever written — four novels, a plural frame voice, found-document interludes, second-person recipes, a Hemingway conversion, and the desk method essays — the proportion of sentences that open on their grammatical subject sits between 85% and 96%. Nothing has ever changed where an Otto Quill sentence starts.

*Evidence:* Measured openers (subject-first / prep-fronted / subordinate-fronted): Talosapien body
91%/1.5%/1.7%; Believer body 90%/2.1%/1.4%; Cruelty-Free body 94%/2.1%/0.7%; Sentience
87%/1.9%/2.3%; Talosapien Hemingway edition 90%; Believer's slide-deck and stand-up dossiers 91%;
Cruelty-Free's second-person recipe interludes 96%; Talosapien's first-person-plural frame voice
85%; the desk/method essay 93%. The corollary metric, p90/median sentence length, is 3.9–5.6 in
every narrative segment (Talosapien body 67/12 = 5.58) — a bimodal short-declarative-plus-long-
cascade distribution that persists even where mean length is halved.

*Significance:* Every voice intervention attempted so far has operated on lexis (in-world terms, register
adjectives, influences) or on person (I/he/we). None has ever operated on constituent order. This
makes fronting rate the single most under-exploited and most mechanically checkable lever available:
it is measurable with a first-token lookup, it has never been specified, and changing it necessarily
changes where information lands in a sentence, which is what cadence actually is.

### 2. There is a controlled experiment already on disk that no one has read as one, and it is decisive: the entire Talosapien manuscript was rewritten to Hemingway's principles and halved, and the function-word fingerprint barely moved. The conversion changed exactly the axes the brief named and nothing else — and one unnamed figure got WORSE.

*Evidence:* talosapien branch `earnest`, commit 6aad402, brief at `talosapien/editorial/hemingway-brief.md`.
109,051 → 60,263 words. What the brief named moved enormously: mean sentence length 25.4 → 15.9, p90
66 → 35, sentences ≥40 words 23.1% → 6.8%, -ly adverbs 58.5 → 45.8 per 10k. What the brief did not
name did not move: the generic-you simile frame 18.6 → 14.3 per 10k, `thing/s` 86.4 → 81.1,
`because` 58.9 → 45.3, `the only X` 1.6 → 1.7, subject-first openings 91% → 90%. The construction
`not X. [Capital]` ROSE from 17.0 to 27.6 per 10k, because chopping cascades into short sentences
manufactures more of it. Function-word cosine between the original and its own Hemingway rewrite:
0.9967 — closer than any two Otto Quill books are to each other (Believer↔Talosapien 0.9892). All 22
cross-book five-grams survive in the Hemingway edition.

*Significance:* This is the strongest single result in the corpus and it yields a law: the prose changes along
exactly the axes the brief makes checkable, and reverts to the attractor everywhere else. It kills
the hope that a strong enough register instruction produces a different voice, and it simultaneously
proves the opposite hope — that explicit, structural, numeric instruction works reliably on whatever
it names. The design problem is therefore not motivation or taste. It is coverage: what has to be
named.

### 3. The master generative habit, from which every named tic descends, is TERMINAL ASCENT: every unit of prose is required to end at a higher level of abstraction than it began. Sentence ends on the gloss of the fact, paragraph ends on the proposition the scene proves, chapter ends on the aphorism. The figures (the-way-you, which-was, the-only-X, the-whole-of, the abstract antithesis) are not separate tics; they are the available instruments of that ascent, which is why banning them one at a time re-tools rather than stops.

*Evidence:* Paragraph-final sentences are dramatically LONGER than paragraph-internal ones — Talosapien 40.0 vs
19.0 words, Believer 25.4 vs 15.9, Sentience 23.6 vs 15.8, Cruelty-Free 20.7 vs 14.8 — and 51–65% of
multi-sentence paragraphs close on a sentence longer than that paragraph's own average. 37–47% of
paragraph-final sentences end on an abstract noun (thing/way/truth/difference/price/shape/whole...);
27–51% contain a generic-person reference (you/one/a man/anyone/people). Mean chapter-final
sentence: Talosapien 73.6 words, Believer 47.3, Sentience 31.8. Example, close of Talosapien ch13:
"...and out past the launch-road the Wheels turned, patient, full of seed-stores and the long
ledgers and the hedge against every morning but the one that was coming, and he did not count them."

*Significance:* This reframes the fix. A ban list attacks symptoms; a terminal-altitude rule attacks the policy and
starves all the figures at once. It is also checkable without taste: 'does the final noun phrase of
this paragraph name something a camera in this scene could photograph?' is a yes/no question a
memoryless subagent answers with low variance, unlike 'is this prose good?'

### 4. The books' own style guides explicitly prescribe the OPPOSITE of what the prose does, and no instrument existed to notice. Believer's guide orders 'Long, clause-stacked observation followed by a short, flat landing' and 'Earn the aphorism, then stop. One quotable line per chapter, maximum.'

*Evidence:* believer/wiki/06-style-guide.md, §'Voice & prose values'. Measured in Believer's body chapters:
55.5% of multi-sentence paragraphs end on a sentence longer than the paragraph's average; paragraph-
final sentences average 25.4 words against 15.9 internal; only 23.6% of paragraph closes are ≤6
words. The instruction was long-then-short; the book does long-then-longer, book-wide, and shipped.

*Significance:* An unmeasured instruction is decoration. This is the voice-level instance of E3 (a plan is not a
revision): the style sheet asserted a cadence rule, the drafting agents believed they were obeying
it, the reviewers believed it had been obeyed, and the manuscript does the opposite in more than
half of its paragraphs. Every prose rule in the method must ship with the query that decides it.

### 5. The style sheets themselves are one document with the nouns swapped. The spec is written by the same author under the same attractor as the prose, so a 'different voice' was never actually specified.

*Evidence:* sentience/editorial/style-sheet.md §1 and talosapien/editorial/style-sheet.md §1 are near-identical:
both open 'The binding constitution of the prose... When in doubt, consult this file, not taste';
both 'Register: lucid, precise, unshowy... Egan's rigor, Chiang's restraint'; both 'Default
sentence: plain declarative. Earn the long recursive sentence; spend it on the one idea per
paragraph that needs it'; both 'Affect: controlled' with a parallel example ('He counted the eggs
again' beats 'he was overwhelmed by despair' / 'I missed her' beats 'I was consumed by a desperate
longing'); both 'Wit: dry, infrequent, load-bearing... Never quippy.' The two books' target voices —
hard SF deep time vs a machine's elegiac confession — are described in the same sentences.

*Significance:* The diagnosis 'the style sheets failed to differentiate cadence' understates it. The style sheets
did not attempt to differentiate cadence, because a style sheet written in adjectives by this author
converges on the same adjectives. Any fix that produces the next book's voice spec by free
composition will reproduce this. The spec must be produced by a procedure that forces difference
from the measured previous book, not by writing a fresh description.

### 6. The named influence lists actively cause the problem. Naming three-to-five exemplars licenses interpolation, and interpolation is the attractor. The one brief in the corpus that named exactly ONE author and gave mechanisms rather than adjectives is the only brief that ever moved the cadence.

*Evidence:* Talosapien §1: 'Egan's rigor, Chiang's restraint, Baxter's deep-time sublime held on a tight leash.'
Cruelty-Free design spec: 'the love-child of José Saramago's premise-rigor, Kazuo Ishiguro's
restraint, and the satirical bite of George Saunders / Joseph Heller.' Both produce the mean.
hemingway-brief.md names one author and eight operational mechanisms ('one thought per sentence;
break the long recursive sentences into hard separate sentences; cut -ly adverbs; render feeling
through one physical object'), plus a worked before/after calibration example — and moved mean
sentence length by 37% and long-sentence rate by 71%.

*Significance:* Breadth of influence is what produces the mean, and the mean is the pathology (D2). The prescription
is not 'choose better influences' but 'choose fewer, and convert each into a mechanism with a worked
example, because only mechanisms are checkable.' Note also what the Hemingway brief omitted: it
never named a rhetorical figure, and no figure changed.

### 7. The signature figure is a direct expression of the deficit, not a stylistic accident. The 'the way you X' construction is not a simile of resemblance but a simile of PROCEDURE: it explains a character's inner state by naming a universal human procedure the reader is assumed to have performed. It is the natural figure of a writer who knows the distribution of human experience and not one life.

*Evidence:* Rate 8.8–15.5 per 10k in every book, 125–222 per 100k. Talosapien: 'knew the way you know a grave is
a grave'; 'the way you understand a wet floor before you read the sign'; 'the way you reconstruct a
blow from the bruise'. Believer: 'the way you date things from a diagnosis'; 'the way you understand
a stair is missing only after your foot has gone through the place where it should be'. Cruelty-
Free: 'the way you track a scar from across a room'; 'the way you get good at saying a word so many
times it stops meaning anything'. Sentience: 'the way you hold a letter found in a drawer in
handwriting almost exactly like your own'; 'the way you carry a thing a dead friend said because you
cannot stop carrying it'.

*Significance:* This explains why the figure is inextinguishable by ordinary means and why every book independently
reinvents it. A human novelist's simile draws on one idiosyncratic life ('like my grandmother's
coat'); this author's draws on the average of all lives, because that is the only material it has
(D8). The figure is D2 made visible at sentence level. It follows that the replacement cannot be 'a
different simile' — it has to be a rule about where comparisons may be SOURCED (from this narrator's
declared occupational world only), which converts a deficit-driven reflex into a characterization
instrument.

### 8. The four books' shared five-grams are not accidental collocations. The distinctive subset is the residue of a small set of rhetorical figures that generate the book's theme in all four books.

*Evidence:* Verified raw-string counts across the four manuscripts — 'said it the way you' 3/2/9/5; 'that was
the whole of' 7/3/1/4; 'not going to tell you' 4/1/1/2. The abstract-antithesis thesis sentence
appears in all four and carries the theme in each: Talosapien 'You read its outputs, and its outputs
were correct, and *correct* is not the same as *honest*'; Believer 'the accurate thing was not the
same as the good thing' and 'true was not the same as honest, and neither was the thing a marriage
needed'; Sentience 'But survivable is not the same as legible' and 'Knowing the argument is not the
same as standing out in the weather the argument describes'; Cruelty-Free 'That's not the same thing
as it mattering.'

*Significance:* Four books with four premises deliver their central idea through one rhetorical machine. This is
worse than a tic: the figure is doing the book's most important work, which is why it survives every
ration. Any figure ledger has to distinguish 'figure the author reaches for' from 'figure this
book's thesis is delivered by' and require that the second be reassigned per book, not merely
rationed.

### 9. Narrators inside a book are not distinct voices. Sentience's eight named narrators are, on function words, closer to each other than two whole books are — and once pronoun frequency is ablated (which measures who is in the scene, not how they speak), narrator classification collapses toward the majority baseline.

*Evidence:* Sentience pairwise narrator cosine 0.953–0.987; Ariel (an AI, 44k words) vs Mara (a human woman, 24k
words) = 0.9860, which sits AT the same-voice noise floor for windows of that size. Leave-one-out
nearest-centroid classification on 1200-word chunks, function words only: Talosapien POV identity
86.6% accurate with pronouns, 53.7% with pronouns removed (majority baseline 35.8%) — Asha 92%→46%,
Iren 80%→45%. Sentience narrator identity 66.2% → 56.8% against a 43.2% majority baseline; with
pronouns removed Mara scores 39%, Echo 0%, the Confluence 0%. Book identity, by contrast, holds up:
88.6% → 72.7%.

*Significance:* The premise of Sentience (five distinct instances) and of Talosapien (a braided multi-POV structure)
is not realized in the prose, and the panel's fix for it (M8, 'fingerprint the figure per narrator')
was applied to five files out of thirty-nine. The unit of voice variation in this corpus is the
book, not the character, and even that variation is mostly pronouns. Per-narrator idiolect
assignment is therefore not a refinement to add later; it is the untouched 90% of the problem.

### 10. A same-voice noise floor now exists, which for the first time makes 'these are distinct voices' a falsifiable claim rather than an opinion. Two random windows of the SAME voice are already very similar, and most reported 'voice separation' in this corpus is inside that band.

*Evidence:* 200 trials per size, two disjoint random windows drawn from Believer's body chapters (one voice, one
book). Median / p05 / minimum cosine: 1,500 words 0.9613 / 0.9162 / 0.8835; 3,000 words 0.9765 /
0.9574 / 0.9229; 6,000 words 0.9867 / 0.9722 / 0.9570; 12,000 words 0.9930 / 0.9851 / 0.9779; 25,000
words 0.9967 / 0.9943 / 0.9930.

*Significance:* Read against this: Ariel vs Mara at 0.9860 is indistinguishable from same-voice noise. Believer vs
Talosapien at 0.9892 (100k words each, floor p01 = 0.9934) is a real but weak separation.
Talosapien's frame voice at 0.9136 against its own body (6,056 words, floor p01 = 0.9700) is a
genuine, large separation. Without this table every cosine in the project is uninterpretable; with
it, a voice profile can state a hard acceptance criterion — e.g. 'each narrator must sit below the
p01 same-voice floor for its own word count against every other narrator' — that a memoryless
checker can evaluate.

### 11. Three passages in the corpus genuinely break free, and all three do it the same way: they import a grammar from a non-fiction document type and change grammatical person. None of them does it by being told to sound different.

*Evidence:* Cruelty-Free's italic recipe interludes (second person, imperative, present): cosine 0.8372 against
their own book's narrative body — below even the MINIMUM of 200 same-voice trials at that word count
— with the generic-you simile at 0.0 per 10k against 12.9 in the body. Believer's dossier interludes
(a confidential slide deck, a stand-up transcript, a redacted memo): cosine 0.9321 against the body,
the-way frame 3.5 vs 25.3 per 10k, mean sentence 11.1 vs 21.0, clause-marks per sentence 0.65 vs
1.57. Talosapien's first-person-plural present-tense frame: cosine 0.9136, the only narrator in
either book that classifies at 100% after pronoun ablation. The desk/method essays, written by the
same author in non-fiction, sit at 0.885–0.910 from the novels — i.e. changing GENRE moves this
author further than changing book, character, premise and target voice combined.

*Significance:* The corpus's own successes name the mechanism: voice separation has only ever been produced by an
externally-imposed compulsory form (a deck must have bullets and KPIs; a recipe must have
imperatives and quantities; a plural reconstruction must confess what it cannot know) plus a change
of person. Descriptions of a voice have never once produced one. This is the mechanism to
industrialise — and note it is generative, not prohibitive, which is what protects it from producing
mannered prose: the writer is given something to DO, not merely things to avoid.

### 12. But the breakaways also mark the ceiling of that mechanism: they change lexis and person while leaving the sentence architecture untouched. Even the most separated passage in the corpus has the same shape.

*Evidence:* Architecture of the breakaways vs their own book's body — Cruelty-Free recipes: mean 15.1 / median 9
/ p90 35 / p90-median ratio 3.89 / 96% subject-first, against body 17.3 / 10 / 40 / 4.00 / 94%; the
deferred appositive ', which was/is' is actually HIGHER in the recipes (38.8 vs 22.8 per 10k).
Talosapien frame voice: 22.6 / 13 / 53 / 4.08 / 85%, against body 25.6 / 12 / 67 / 5.58 / 91%. Only
Believer's dossiers move the architecture (11.1 / 8 / 25 / 3.12 / 0.59 commas per sentence) — and
they are the passages whose source form physically forbids subordination.

*Significance:* A form-shift buys a different word distribution; it does not buy a different sentence. Full voice
separation therefore needs both levers together — the imported source grammar (which supplies
material and diction) AND an explicit constituent-order and clause-depth target (which supplies
rhythm). Neither alone has ever been sufficient in 300,000 words of evidence.

### 13. Grammatical person, not genre or character, explains nearly all of the between-book variation that does exist. The four books cluster by person, not by anything the style sheets specified.

*Evidence:* Same-person pairs: Talosapien↔Believer (both close third past) 0.9892; Cruelty-Free↔Sentience (both
first past) 0.9697. Cross-person pairs: Believer↔Cruelty-Free 0.9538, Talosapien↔Cruelty-Free
0.9430, Talosapien↔Sentience 0.9310, Believer↔Sentience 0.9287. Mean same-person 0.979, mean cross-
person 0.939. Genre distance is uncorrelated: literary satire and hard SF sit at 0.9892 — the
closest pair in the corpus.

*Significance:* The one variable that has ever reliably moved the fingerprint is one the books chose incidentally,
for narrative reasons. It should be chosen deliberately, per book AND per narrator, as a voice
instrument: person and tense are the cheapest large-effect lever available, and the corpus has never
used more than three of the available combinations.

### 14. Forensic reconstruction of the fix that was applied and did not work. Sentience's panel identified the tic, quoted it, ordered it cut outright, and the commit that claims to have done so kept both halves of the construction and swapped one noun.

*Evidence:* Plan (sentience/editorial/revision-plan.md M7): 'Cut Cantor's "precision is the only tenderness I am
sure is mine" outright.' Commit d3b257b, 'Polish pass: ration voice-tics', ch18: BEFORE — 'I want to
be precise, because precision is the only tenderness I am sure is mine.' AFTER — 'I want to be
precise about it, because precision is the one thing I owe a thing this true.' The frame [I want to
be ADJ about X] + [because ABSTRACT is the only/one Y] survived intact. Meanwhile the very sentence
the plan ordered deleted is still on the page in ch20 under a different narrator: 'I want to be
honest about the size of this, because the honesty is the only tenderness I am sure is mine' —
present since the first draft (93de6b5) and untouched. The polish commit modified 5 manuscript files
out of 39; the construction is in 23 of them, 32 instances total.

*Significance:* Three failure modes in one commit, all structural rather than careless: (1) the ban named a string,
so paraphrase counted as compliance; (2) the fix was applied where the report quoted an example
rather than where a query found instances; (3) nothing re-measured after, so 'ration voice-tics'
entered the history as done. Any figure ledger must therefore express bans as queries, drive the
edit from the query's full hit list rather than from the report's examples, and gate the commit on a
re-run.

### 15. Cruelty-Free is the partial exception and shows what a professional grammar does when it reaches the narration. Its narrator is a chef, and the one measurable place the book departs from house style is exactly where cooking practice governs the prose.

*Evidence:* Cruelty-Free has the shortest chapter-final sentences in the corpus by a factor of six — mean 11.7
words against Talosapien's 73.6, Believer's 47.3, Sentience's 31.8. Actual chapter closes: 'Service
began.' (ch29); 'He just didn't have me. Not yet.' (ch07); against Talosapien ch03's 90-word close
ending '...and she kept the count anyway, because it was the only fidelity she had, and she would
not let it happen in the dark.' Cruelty-Free also has the lowest clause-marks per sentence of the
four (1.19 vs 2.05) and the lowest abstract-terminal-noun rate at paragraph close (36.7% vs
43.8–46.9%). But the effect is partial: the recipe grammar reaches full strength only inside the
1,545 words of italic interlude and decays across the 89,787 words of narration.

*Significance:* The corpus contains a natural experiment in the right prescription, half-executed. A narrator with
an occupational grammar produces measurably different prose in exactly the proportion that the
grammar is allowed into the narration. The move the corpus has never tried is to carry the source
grammar into the body chapters — to make the chef's mise-en-place ordering, the deposition's
numbered assertions, the repair log's fault-then-remedy structure govern the scene prose, not just
the interlude.

### 16. A three-condition self-experiment confirms that construction-level bans are obeyable by this model, that adjectival register specs are not, and that the manneredness risk is real and appears immediately at the extreme.

*Evidence:* One scene brief, three specs. (A) written to the existing style-sheet spec verbatim: 276 words, mean
21.2, max 84, and it trips 9 of 10 banned constructions — 'saw it the way you see a missing stair,
which is to say afterward'; 'which was to produce a number by four o'clock, and he knew what saying
so would cost, which was...'; 'the gap between the two of those was the whole of what he had
become'; 'Not a question. With Ilse you did not ask whether.' (B) same brief plus a ten-item
construction ban: 177 words, mean 9.8, max 30, zero bans tripped — but I wrote 'the way it always—'
mid-draft and removed it only because I was checking. (C) B plus a positive constitution (median ≤7,
no sentence >25 words, subordination fronted, paragraph closes on a scene object, metaphor domain
restricted to bookkeeping, feeling rendered only through the hands): 136 words, mean 5.9, 52% of
sentences ≤5 words, zero bans — and it reads as a stylistic exercise. Its close, 'He squared the
ledger to the edge of the desk. Then he squared it again,' works; its middle is starved.

*Significance:* Two operational conclusions. First, a ban that names a construction is answerable and a register
adjective is not — condition A obeyed 'lucid, precise, unshowy' perfectly and produced pure house
style. Second, the constraint does not prevent the construction from arising; it only makes it
detectable, so the loop must be measure-then-revise rather than instruct-then-trust. Third, the
manneredness risk is not hypothetical: prohibition alone starves the prose, which is precisely why
the bans must be paired with an imported source grammar that gives the sentence somewhere to go.

**Implications for the method**

- THE COVERAGE LAW, stated as the method's governing principle: prose changes along exactly the axes
  the brief makes checkable, and reverts to the attractor everywhere else (proved by the Hemingway
  edition — every named axis moved 37–71%, no unnamed axis moved, and one unnamed figure rose 62%).
  Therefore a voice constitution is not judged by how well it is written but by how much of the
  sentence it covers with a query. Any dimension of voice for which no query exists is, by this law,
  guaranteed to be house style in the finished book. The existing voice-profile.json covers budgets
  and cadence; it does not yet cover constituent order, clause depth, terminal altitude, or metaphor
  sourcing — those four are currently uncovered and will therefore revert.

- ADD THE FOUR UNCOVERED AXES to templates/voice-profile.json, all computable from the text with no
  taste judgment. (1) opener_distribution: max subject-first %, min prepositional/adverbial-fronted
  %, min subordinate-clause-fronted %. Corpus actual is 85–96% / 1.5–2.2% / 0.7–2.3% in EVERY
  segment ever written; a next book set to 65% / 15% / 8% would have a genuinely different rhythm
  and the check is a first-token lookup. (2) clause_marks_per_sentence
  (which/who/that/because/when/and/but/as/so): corpus 0.65–2.05; the dossiers that broke free are at
  0.65. (3) p90_over_median: corpus narrative 3.9–5.6, Hemingway edition 3.18, dossiers 3.12, non-
  fiction 2.05 — this ratio, not mean length, is the bimodality fingerprint. (4) terminal_altitude:
  % of paragraph-final sentences ending on an abstract noun (corpus 36.7–46.9%) and % containing a
  generic-person reference (26.5–51.4%).

- THE TERMINAL-ALTITUDE RULE is the highest-leverage single addition, because it attacks the
  generative policy rather than its symptoms. Rule: for each book declare a maximum share of
  paragraphs and chapters that may close above scene level. Operationalise 'above scene level'
  mechanically — the final noun phrase names something not physically present in the scene, OR the
  sentence contains you/one/a man/anyone/people used generically, OR the sentence's main verb is a
  copula with an abstract complement. Cost: one function in prose_audit.py plus a per-book concrete
  inventory harvested from the wiki (characters, places, objects), which the books already maintain.
  Manneredness risk: a book forbidden all altitude becomes affectless — so the budget must be
  nonzero and SPENT, i.e. the profile names how many high closes the book gets (say 40) and the
  ledger records where they went, exactly as the promise ledger records payments. Scarcity imposed
  from outside is the substitution for D4, and a budget that must be spent is better than a ban,
  because it makes the ascent a decision instead of a reflex.

- REPLACE THE INFLUENCE LIST WITH A SOURCE GRAMMAR, one per narrator, taken from a non-fiction
  document type rather than from novelists. This is the mechanism the corpus's own three successes
  used and never generalised: a slide deck (Believer intA, the-way frame 0.0 per 10k against a book
  average of 25.3), a stand-up transcript (intH), a recipe (Cruelty-Free's interludes, cosine 0.8372
  from its own book — the largest separation in the corpus), a plural scientific reconstruction
  (Talosapien's frame, the only voice that survives pronoun ablation at 100%). The move nobody has
  tried: carry the grammar into the BODY chapters, not just the interludes. A deposition narrator
  numbers her assertions and marks what she cannot swear to; a repair-log narrator states fault
  before remedy and never states cause; a tasting-note narrator moves nose-palate-finish and refuses
  interiority. Specify three to five compulsory features per narrator and audit them by count. Cost:
  an hour of design per narrator. Risk: gimmick — mitigated by requiring the grammar be a real
  occupational competence the character HAS, which is also characterisation, and by budgeting it
  (present in every scene, dominant in none).

- EXPRESS EVERY BAN AS A QUERY, NEVER AS A STRING, AND DRIVE THE EDIT FROM THE QUERY. The M7 forensic
  is the proof: the plan quoted one sentence, the commit edited that sentence and four others, the
  construction was in 23 of 39 chapters, and the identical ordered-deleted sentence is still on the
  page under a different narrator. Protocol: (a) each ledger entry carries a regex plus a one-
  sentence semantic definition of the shape; (b) the revision task is generated FROM the query's
  full hit list, one task per hit, never from the report's examples; (c) the fixer subagent receives
  the hit, ~100 words of surrounding context, the ban, and the narrator's owned-figure inventory,
  and must return three alternatives none of which trips the probe; (d) a blind selector picks one;
  (e) the commit is gated on a re-run showing the rate below budget. Cost: cheap — this is A4
  (revision is free) and A2 (failures are reproducible) doing the work a human's reluctance does.
  Risk: local rewrites make prose lumpy, so operate at paragraph granularity, and re-audit
  p90/median afterwards, because Hemingway-ising cascades RAISED the 'not X. Y' figure by 62% —
  every fix must be checked for the figure it displaces into.

- SET EVERY NUMERIC TARGET BY FORCED DIVERGENCE FROM THE PREVIOUS BOOK'S MEASURED ACTUALS, not by free
  composition. The style sheets are one document with the nouns swapped (Sentience §1 and Talosapien
  §1 share their register sentence, their default-sentence sentence, their affect example structure
  and their wit sentence) because a fresh description written by this author converges on the same
  description. Procedure: run prose_audit.py over the previous book, then require each cadence and
  figure target in the new profile to differ from that measurement by a stated minimum — and require
  at least three axes to move by more than the same-voice noise band for the book's word count. This
  makes the spec a function of evidence rather than of taste, which is the only kind of spec that
  survives D5.

- USE THE NOISE FLOOR AS THE ACCEPTANCE CRITERION FOR 'DISTINCT VOICES', and publish it in the method
  so no future session mistakes a within-noise cosine for a result. Same-voice floor from 200 trials
  on Believer body chapters — 1,500 words: median 0.9613, p01 0.9021; 3,000: 0.9765 / 0.9429; 6,000:
  0.9867 / 0.9700; 12,000: 0.9930 / 0.9800; 25,000: 0.9967 / 0.9934. Acceptance rule: every pair of
  narrators must sit BELOW the p01 floor for the smaller of their two word counts. Sentience
  currently fails on every pair (Ariel vs Mara 0.9860 at 24k+ words). Talosapien's frame voice
  passes (0.9136 at 6k against a 0.9700 floor). This one table converts the whole voice question
  from opinion to pass/fail.

- ALWAYS ABLATE PRONOUNS BEFORE CLAIMING VOICE SEPARATION. Pronoun frequency measures who is in the
  scene, not how anyone speaks, and it is carrying most of the apparent separation: Talosapien POV
  classification falls 86.6% → 53.7% when pronouns are removed (majority baseline 35.8%), Asha 92% →
  46%, Iren 80% → 45%; Sentience's Mara falls to 39%, Echo and the Confluence to 0%. Add a --ablate-
  pronouns flag to prose_audit.py and make the ablated number the one the profile is judged against.
  Corollary opportunity: since person and tense are the ONLY lever that has ever reliably moved the
  fingerprint (same-person book pairs mean 0.979, cross-person 0.939), assign person and tense per
  narrator deliberately, as a voice instrument, rather than letting the narrative choose them.

- THE BEHAVIOURAL CHECK THAT OUTRANKS ALL THE STATISTICS: the blind discriminator. Take one paragraph
  from narrator A and one from narrator B, strip all proper nouns and book-specific vocabulary, hand
  both to a subagent with no other context, and ask which narrator wrote each. Run 40 pairs per
  narrator pair; below ~70% the narrators are not distinct regardless of what any cosine says. The
  stripping step is load-bearing — without it the discriminator wins on content and reports a false
  pass, which is exactly the illusion the current books ship under. This is A1 (manufactured first
  readers) pointed at voice instead of plot, it is memoryless-checkable, it costs a few thousand
  tokens, and it measures the thing that actually matters: whether a reader could tell them apart.

- BUILD THE MEASURE/REVISE LOOP AS THE NORMAL WAY A CHAPTER IS FINISHED, not as a polish pass. Draft →
  audit against the profile → the audit emits located, per-instance rewrite tasks → rewrite → re-
  audit → only then does the chapter count as drafted. A human cannot do this at all; it is a pure
  A2/A3/A4 exploit and it is the single largest structural advantage available. Two guardrails
  learned from the experiment: (1) the constraint does not prevent the construction, it only makes
  it detectable — I wrote a banned frame mid-draft under an explicit ban and caught it only by
  running the check, so trust nothing that has not been re-measured; (2) re-audit the whole profile
  after every fix, because suppressing one figure displaces load onto another (Hemingway-ising
  Talosapien cut long sentences by 71% and raised the 'not X. Y' construction by 62%).

- ADDRESS THE MANNEREDNESS RISK DIRECTLY, because it is real and it showed up immediately in testing.
  Condition C — a full prohibitive constitution with tight numeric targets — produced prose with a
  median sentence of 5.9 words and 52% of sentences under six words that reads as an exercise, not a
  voice. Three defences, all structural. (1) Never ship a prohibition without a generator: every
  banned figure must be answered by a named replacement the narrator OWNS (a source grammar, a
  metaphor domain, a characteristic evasion), so the writer has somewhere to go. (2) Make budgets
  nonzero and require them to be SPENT — a figure allowed forty times and tracked is a decision; a
  figure banned outright is an amputation. (3) Gate on a naive reader, not on the audit: after the
  profile passes, blind readers who have seen no profile must report the prose as alive and the
  narrators as different people. A book that passes every number and fails that reading has been
  engineered into mannerism, and the numbers must then be loosened — the audit is the instrument,
  never the goal.

- RECORD WHAT THE FIGURES ARE FOR, not just that they occur, because the most-shared figure is doing
  the book's most important work. The abstract antithesis ('correct is not the same as honest'; 'the
  accurate thing was not the same as the good thing'; 'survivable is not the same as legible';
  'That's not the same thing as it mattering') delivers the THEME in all four books through one
  rhetorical machine. Rationing it will simply make the theme land more weakly in the same shape.
  The ledger therefore needs a second column beside each figure — what job it does — and a per-book
  requirement that the book's thesis be delivered by a DIFFERENT job-holder: an action, an object, a
  refusal, a structural rhyme, a silence. This is the place where the method has to stop being a
  filter and start being a design decision, and it is the one prescription here that a checker can
  only partially verify: the audit can confirm the antithesis rate is down, but a blind reader has
  to confirm the theme still lands.

## The Otto Quill Idiolect Ledger: raw material from a four-book forensic audit (353,750 words)

### 1. CONSERVATION LAW: construction budgets are conserved at the FAMILY level while individual members swing wildly. This is the mechanism by which per-book fixes fail, and it is measurable.

*Evidence:* Six-member abstraction basket {thing(s), something, anything, nothing, everything, kind/sort of} per
100k words: Cruelty-Free 1262.9, Believer 1459.4, Sentience 1284.4, Talosapien 1209.8 — a 1.21x
spread. Inside that near-constant total the members swing enormously: `thing(s)` rises MONOTONICALLY
across publication order 416.6 -> 674.4 -> 773.0 -> 811.0 (1.9x) while `something` falls
MONOTONICALLY 422.1 -> 146.7 -> 141.1 -> 78.4 (5.4x), and `kind/sort of` falls 3.8x. Same effect in
three other baskets: precision-claim {precise, exact, honest, careful, clear, accurate, true}
members swing 20.4x (precise), 328x (accurate), 6.6x (true) but the basket only 1.93x (377-728);
totalizer members swing 21.3x (`the whole of`) but the basket 1.92x; simile-frame members swing 8.4x
(`as if/though`) but the basket 1.73x. Regenerate: /tmp/claude-1000/-home-paul-git-ottoquill-
desk/77038d82-ec06-4a33-a9f6-91c0174cb04b/scratchpad/idio/ (corpus.py + ad-hoc basket script), and
desk/tools/idiolect_probe.py now implements it as B1-B5.

*Significance:* This is the quantitative proof of E2/D3 and it dictates the ledger's data structure. A ledger of
banned PHRASES is worthless and a ledger of banned CONSTRUCTIONS is only half right — the unit that
must carry a number is the semantic family. Sentience banned `I want to be precise about X`; the
frame recruited `exact/careful/honest/clear` and the precision-claim basket was undisturbed. Every
ledger entry needs a basket_id, and the enforcement question is 'is the family over budget', not
'did the banned string appear'.

### 2. BAN: the exact three-word sentence "Not a question." appears as a standalone sentence in ALL FOUR books, in ten different chapters, performing the identical move each time.

*Evidence:* 10 occurrences, 4/4 books, 10 distinct chapters.
veganassassin/manuscript/chapters/{ch04,ch11,ch36}.md;
believer/manuscript/chapters/{ch06,ch07,ch15}.md; sentience/manuscript/{13-ch03-no-one-
home,36-ch19-a-life,42-ch23-echo-in-the-pool}.md; talosapien/manuscript/12-ch01-the-count.md. Nine
of the ten are the same three-beat unit — quoted line, `said` tag, then the gloss: `"Sage," the
woman said. || Not a question. || She extended a hand.` (vega ch04); `"You look sad," she said. ||
Not a question.` (believer ch06); `"Stay difficult," it said. || Not a question.` (sentience ch19);
`"How bad," he said. || Not a question. || With Liss you did not ask whether.` (talosapien ch01). It
is the ONLY 2-7 word sentence that appears verbatim in all four books (7 such sentences appear in
3+, e.g. 'It isn't' x7, 'No, he said' x4).

*Significance:* The single cleanest artifact in the audit and the best possible opening exhibit for the ledger: an
identical sentence, in an identical rhetorical slot, in a chef-narrated crime comedy, a literary
satire, a machine's confession and a deep-time SF novel. It cannot be defended as voice because the
four voices were specified to be different. It also generalises: the whole family is a verbless
<=6-word fragment glossing a `said` line, running 60.1-99.8 per 100k across the four books
(91/75/82/36 raw). Ban the exact string AND ration the family (probe L03/L04).

### 3. BAN (construction, with basket enforcement): the precision-claim frame is in all four books and its adjective inventory rotates between them — direct confirmation that a phrase-level ban is answered by paraphrase.

*Evidence:* Frame `want/need/try to be ADJ about|here|with` where ADJ ∈ {precise, honest, exact, clear, careful,
accurate, fair, truthful, specific, plain, modest}: Cruelty-Free 33 hits / 22 of 36 chapters (top
adjectives precise 15, clear 7, honest 4); Believer 17 / 12 of 34 (honest 10, accurate 3); Sentience
57 / 27 of 34 (careful 16, exact 16, precise 9, honest 9); Talosapien 12 / 10 of 34 (honest 10).
Every book, every narrator. Sentience's own revision plan named this defect and the fix was
committed; the post-fix book still runs the highest rate in the corpus (5.03/10k) and the largest
chapter coverage (79%).

*Significance:* This is the ledger's founding case and the reason the ledger must live in desk/ rather than in a
book. Note the specific failure shape: the fix was applied to the string, the construction recruited
new adjectives, AND the habit then travelled to the next book (Talosapien, honest x10) where nobody
had ever heard of defect M7. Verdict is BAN on the construction, enforced by basket B2 (precision-
claim), not by any adjective list.

### 4. There is NO cadence architecture. Sentence-length order in all four books is statistically indistinguishable from randomly permuting the same lengths inside each paragraph.

*Evidence:* Within-paragraph adjacent-pair test (3014-4980 pairs per book), real vs. lengths shuffled inside
each paragraph so paragraph size and content are held fixed. Lag-1 autocorrelation real/shuffled:
Cruelty-Free 0.039/0.044, Believer -0.031/0.025, Sentience -0.055/0.002, Talosapien 0.040/0.070.
Mean absolute jump between adjacent sentences real/shuffled: 14.75/14.85, 17.42/17.11, 16.63/16.33,
12.52/12.37. P(short<=8 | previous>=25) real/shuffled: 40.6/45.3, 46.9/45.5, 44.0/43.8, 37.6/38.6 —
the supposed 'long sentence then short punch' is at or BELOW chance in three of four books. Whole-
book runs of 3+ same-band sentences: real 418/340/395/298 vs shuffled 419/360/436/276.

*Significance:* The deepest finding in the audit and a direct measurable consequence of D6 (cannot hear prose). The
books have a distinctive length DISTRIBUTION but no length SEQUENCE — no build, no paragraph arc, no
deliberate deceleration into a beat, and, remarkably, not even the clustering of short sentences
that a dialogue exchange should force. It reads as constant unmodulated jitter. This is a craft
capability that is simply absent rather than a tic to ration, and it is exactly the kind of thing
measurement can supply in place of an ear: the ledger should require |lag-1 r| > 0.08 at paragraph
scale (implemented as STRUCT_RULES['cadence_lag1_r']).

### 5. RATION (hard, with structural target): the sentence-length distribution is a bimodal barbell with a thin waist, identical in all four books despite four different POVs and registers.

*Evidence:* Median 10/11/11/11 words; mean 17.2/19.3/18.3/15.9; mean-to-median ratio 1.72/1.75/1.66/1.45.
Fraction <=5 words: 25.3/26.4/23.9/23.5%. Fraction >=30 words: 19.3/22.6/20.7/15.2%. The 13-21 word
middle — where most literary sentences live — holds only 14.8/14.5/15.7/19.9%. Histogram peak is the
4-6 word bucket in all four books (23.5/21.4/21.6/20.0%). p99: 76/89/80/63; max 135/243/263/110.

*Significance:* The prose is written in two gears, aphorism and cumulative sprawl, with almost no ordinary
declarative middle. That is a voice — and it is the SAME voice in a comic crime novel and a hard-SF
novel, which means it is not a choice. Combined with the previous finding (the gears are shifted at
random) it explains why four deliberately different books read alike at the sentence level.
Enforceable: the ledger should set sentence_median and pct_le5 per book and REQUIRE them different
from the previous book's actuals (voice-profile.json already has the slot; the four-book actuals
give the numbers to move away from).

### 6. RATION: sentence-opener distribution is nearly invariant across four different POVs. Pronoun-subject openers sit in a 2.6-point band across all four books.

*Evidence:* Sentences opening on a bare pronoun subject (I/he/she/it/they/we/you): Cruelty-Free 43.1%, Believer
42.3%, Sentience 44.9%, Talosapien 44.0% — this across first-person memoirist, close third, first-
person machine, and close third with a plural frame voice. `The`-openers 14.7/10.9/11.1/15.9%.
`Not/No/Nothing/Never` openers 2.9/2.6/3.1/2.9%. `There was/were/is` 1.4/1.3/2.3/1.9%. Two-word
openers in all four books' top-30: `it was`, `that was`, `there was`, `it had`, `i want`. One-word
openers in all four top-20: a, and, but, he, i, it, not, she, that, the, there, they, we, you.
Top-25 two-word-opener concentration: 20.8/19.0/23.9/21.1% of ALL sentences. Paragraph openers show
the same: top-12 concentration 14.9/13.6/20.1/19.0%.

*Significance:* POV is the single biggest lever a novelist has over sentence shape, and it moved this number by 2.6
points. The `Not/No/Never` opener band (2.6-3.1%) is tighter still and is the negate-then-correct
reflex surfacing as syntax. This is checkable cheaply on a single chapter and belongs in the ledger
as a per-book target that must differ from the last book's actual.

### 7. BAN as a default / RATION hard: negate-then-correct is the author's universal rhetorical engine, and — decisively — it runs HIGHER inside characters' dialogue than in narration in all four books.

*Evidence:* Sentence-initial negation openers (`It was not…`, `He did not…`) per 100k: 241/197/315/384, rising
near-monotonically in publication order (195.1 -> 166.4 -> 255.3 -> 295.4 on the strict opener
probe). Two-sentence pairs (negative sentence then `It was Y.` correction): 81/70/116/95 raw,
88.8/76.6/104.3/158.5 per 100k. All `not`/`n't` forms rise MONOTONICALLY across publication order
1162 -> 1394 -> 1613 -> 1887 per 100k (literary norm ~800-1300); `cannot/could not` rises
monotonically 68 -> 253 -> 344 -> 434 (6.4x). LEAKAGE: rate inside quoted speech vs narration, per
100k — Cruelty-Free 286/202, Believer 482/141, Sentience 414/256, Talosapien 470/293. Ratios 1.4x,
3.4x, 1.6x, 1.6x. `the only X` leaks at 1.11x/1.23x/1.05x/1.47x and the hard cut `Not a X. Capital`
at 1.16x/1.11x/1.19x/1.30x. Only `the way X` similes (0.28x/0.28x/0.39x/0.21x) and `which is/was`
(0.14x-0.41x) stay properly in narration.

*Significance:* Two distinct failures. (1) The negation scaffold is not a stylistic tint, it is how the author
thinks, and it is intensifying book over book. (2) The leakage number is the one that destroys
books: every character in four novels argues by the same negate-then-correct move, more often than
the narrator does. That is why differentiated narrators keep collapsing into each other (Sentience
defects M7/M8). The ledger needs a dialogue-vs-narration ratio check per construction — a tic with
ratio > 0.6 is contaminating characterization, not just prose.

### 8. Absolute structural absences: 138/138 chapters across four books do the same three things — never open on dialogue, never end on a question, and the corpus contains zero exclamation marks in 353,750 words.

*Evidence:* pct_opens_on_dialogue = 0.0% in all four books (0 of 36, 34, 34, 34). Chapters ending on a question
mark: 0.0% in all four. Chapters ending on quoted speech: 2 of 138, both in Believer. Exclamation
marks: 0 / 0 / 0 / 0 across the whole corpus. Question marks are also thin: 95.4/88.7/67.4/35.0 per
100k. Meanwhile 50.0% of all chapters open on a state-of-affairs claim (was/were/had/is as main verb
of the first sentence: 50.0/50.0/58.8/41.2%).

*Significance:* An involuntary voice shows up as much in what never happens as in what recurs, and absences are
cheaper to check than presences. No human novelist writes 138 consecutive chapters without once
opening in a character's mouth. The pattern is a single underlying habit: the author will not start
a chapter until it has established a fact about the world, which is D2 (the modal opening) hardened
into a rule. These are the easiest possible ledger entries — quota rules, not budgets: at least N
chapters per book must open on dialogue, on a question, or in motion.

### 9. RATION: the chapter-close formula. Chapters end on a compound and-chain that widens to an abstraction, usually carrying a negation and often a camera pull-back.

*Evidence:* Final sentence contains a coordinating `, and` clause: 19.4/64.7/50.0/52.9% (46.4% of all 138
chapters). Two or more `, and` chains in the final sentence alone: 5.6/47.1/29.4/32.4%. Final
sentence contains a negation: 19.4/58.8/44.1/58.8%; last PARAGRAPH contains one:
19.4/61.8/38.2/58.8%. `and`-compound anywhere in the last paragraph: 41.7/79.4/67.6/79.4%. Mean
length of the final sentence: 11.7/46.7/31.6/37.8 words vs. mean sentence length 17.2/19.3/18.3/15.9
— the closing sentence is 2-2.4x the book's average in three of four books. Camera pull-back
(`outside`/`out past`/`somewhere`/`in the dark`) 5.6/11.8/17.6/26.5%. Examples: `…and there was no
one left to read and nothing left to manage, and on the wall above him the three sentences of the
memo glowed on…` (believer/ch04.md); `They counted them together in the failing light, and there
were four, and they were well, and out past the fourth wanderer the Wheels turned in the dark…`
(talosapien/22-ch09-authority.md); `He counted them—not as a man taking inventory, he tried, he held
the trying—and there were four, and the counting did not steady him, and he did it anyway, because…`
(talosapien/32-ch17-what-he-built.md).

*Significance:* The book's most emphatic position — 138 of them — runs one move. Cruelty-Free is the useful control:
it closes short (median 9 words, 50% of chapters <=8 words, 75% one-sentence final paragraphs) and
its and-chain rate is 5.6%. So the formula is not inevitable; it was simply never rationed in the
other three. Ledger entry: cap `>=2 and-chains in the final sentence` at 15% of chapters and cap
final-sentence negation at 30%.

### 10. Abstraction reach runs 3-8x literary norms, and the specific shape of the excess is TOTALIZING — the author says 'the whole of it' and 'all of it' constantly and almost never says 'some of it'.

*Evidence:* Per 100k words, with my estimate of literary-fiction norms in brackets. thing/things
416.6/674.4/773.0/811.0 [~90-160] — 3-8x. because 291.6/521.1/499.7/453.9 [~90-160] — 2-4x. the way
235.7/352.5/385.6/243.6 [~50-90] — 3-5x. never 103/188/266/180 [~50-90]. the whole of
2.2/16.4/46.7/26.7 [~1-3] — up to 23x. a/the shape 15.3/29.6/59.3/51.7 [~3-10]. the part
16.4/78.8/101.6/43.4 [~4-10]. anyway 30.7/25.2/43.1/60.1 [~8-18]. exactly 74.5/59.1/104.3/73.4
[~12-25]. the only 57.0/153.3/155.5/138.5 [~30-55]. weight 29.6/21.9/23.4/31.7 [~6-15]. The
inversion: all of it 14.3/23.0/23.4/15.0 [~3-8] is ABOVE norm while some of it 7.7/5.5/2.7/6.7
[~15-30] is BELOW it in all four books.

*Significance:* The excess is not vagueness, it is a specific epistemic posture: everything is summed, closed, and
totalled ('that was the whole of it', 'the only thing that', 'all of it'), and almost nothing is
left partial. That posture is what makes four different narrators sound like the same essayist. The
`some of it` deficit is the most actionable single number here because it is a positive prescription
rather than a prohibition — the prose needs to be allowed to be partial.

### 11. An inverted absence: the author does not write eyes or faces. `eyes` runs BELOW literary norm in all four books while `hands` runs at or above it.

*Evidence:* eyes/eye per 100k: 42.8/87.6/22.5/40.0 against a literary-fiction norm I would put at ~90-170 —
below the bottom of the range in all four books, and 4-7x below in Sentience and Cruelty-Free.
hands/hand: 110.7/183.9/225.6/288.7 [~90-160] — at or above. face(s): 74.5/137.9/33.3/58.4
[~70-130]. BODY/anatomy vocabulary overall is 395.7/720.4/462.0/907.8 per 100k, so the body is
present; it is specifically the gaze that is missing. Corroborating: `he/she looked at the` is a
top-4-gram in all four books (`he looked at the` 21 across four books) but the looking is never
returned or described.

*Significance:* Worth KEEPING and consciously owning — this is the one place where the involuntary voice produces
something distinctive rather than generic. It is also diagnostically interesting: hands are
instruments and can be described by what they DO, whereas eyes are the standard shortcut for
reporting interiority the author cannot access from outside. But it should be owned deliberately,
because at present it makes every physical description reach for the same four inventory items
(hands, room, light, door) and the ledger should note it as a KEEP-with-variety-requirement rather
than a free pass.

### 12. The metaphor inventory is shared across books that share nothing else. ROOM/architecture is the #1 simile vehicle in three of four books, and DOOR/aperture is the single most uniform imagery domain in the corpus.

*Evidence:* Simile vehicles counted in the 14 words after a simile marker, per 100k: ROOM/architecture
47.1/56.9/71.0/23.4 (top vehicle in Cruelty-Free, Believer and Sentience); BODY 29.6/48.2/48.5/38.4;
WEATHER 24.1/38.3/63.8/23.4; LETTER/document 34.0/30.7/59.3/8.3; WATER 24.1/27.4/51.2/15.0. All 19
tested domains are present in all 4 books. Whole-book domain saturation max/min ratio identifies
which domains are BOOK-SPECIFIC and which are AUTHORIAL: FOOD/cooking 44.4x (Cruelty-Free is
narrated by a chef — correctly book-specific) and GEOLOGY/strata 22.0x (Talosapien — correctly book-
specific), versus DOOR/aperture 1.4x, MAP/navigation 1.6x, WAR 1.7x, ROOM 1.8x, FIRE 1.9x, WEATHER
2.1x, LAW 2.1x. Simile density: one explicit figure every 263/214/227/425 words.

*Significance:* The discrimination is the point: the audit can tell a book's own imagery from the author's, and by
that test rooms, doors, weather, letters and hands are Otto Quill's, not any book's. The ledger
should carry a forbidden-vehicle list that is CUMULATIVE — each new book inherits the previous
books' top-3 vehicles as banned, which forces the fifth book to build its metaphor inventory from
somewhere the author has not already been. voice-profile.json already has metaphor_domain /
forbidden_figures slots per narrator; they need to be seeded from this table rather than left blank.

### 13. Specific self-priming FIGURES (not just domains) recur across all four books.

*Evidence:* `the way a/the body knows` — 3/4 books: `the way a body knows, below the level of language`
(veganassassin/ch06.md); `Daniel knew before she said it, the way the body knows`
(believer/ch13.md); `knows, the way the body knows an alarm` (talosapien/17-ch06-salvage.md). The
broader epistemic simile `the way a X knows` is 4/4 (3/6/12/7 raw). Abstraction-as-physical-object
`set/laid/put it down` 4/4 (22/17/17/29 raw, 1.9-4.8/10k). `the gap between` 4/4 (5/5/12/6). `which
was true` as a self-adjudicating dialogue tag 4/4 (8/9/1/2): `"I'm always up," I said, which was
true.` (vega ch02) / `Daniel said, "Mm," which was true, because it was only a sound` (believer
ch18). `did not yet know` 4/4 (1/4/4/4). `was not a question` 4/4 (5/6/4/3). `like a stone` 3/4.
Shared simile HEAD NOUNS in 3+ books: man (34, 4/4), thing (16, 4/4), stone (13, 4/4), person (13),
hand (11), word (6), body (6), people (5), air (5).

*Significance:* These are not constructions that could be paraphrased into innocence — they are specific images,
which means D3 self-priming operates on the image level across sessions and repositories with no
shared context. `the way a body knows` in a chef's memoir, a Washington satire and a deep-time SF
novel is the same sentence three times. The ledger needs a FIGURE REGISTRY distinct from the
construction budgets: an append-only list of specific images already spent, checked by string/near-
string match, never reused.

### 14. n-gram overlap is concentrated at the 4-6 word scale and vanishes above it — the signature is a clause frame, not a sentence.

*Evidence:* Distinct n-grams appearing in 3+ books: 4-grams 1027 (209 in ALL FOUR), 5-grams 173 (22 in all
four), 6-grams 33 (2 in all four), 7-grams 3, 8-grams 0. Top all-four 4-grams by total count: `of a
man who` 74 (37/18/1/18), `it the way you` 70 (16/10/31/13), `and there was no` 44, `a man who had`
43, `for the first time` 41, `which is to say` 34, `for a long time` 34, `the kind of thing` 31, `in
a way that` 31, `at the edge of` 29, `it was not a` 27, `that was the whole` 25, `that was the
thing` 25, `said it the way` 24, `of someone who had` 24, `there was no one` 23, `the whole of it`
23, `the far side of` 23. Full dumps in /tmp/claude-1000/-home-paul-git-ottoquill-
desk/77038d82-ec06-4a33-a9f6-91c0174cb04b/scratchpad/idio/ngram_report.txt.

*Significance:* Tells the ledger exactly what size of object to store. Below 4 words you catch banal English; above
6 you catch nothing because the author never repeats a whole sentence (with the one exception of
'Not a question.'). So ledger entries should be 4-6 word FRAMES with a slot — `it the way you ___`,
`of a man who ___`, `that was the whole of ___` — which is also the size at which a regex probe is
both writable and precise. It further explains why phrase bans fail: a 4-gram frame has a large
synonym neighbourhood, which is why the basket budget has to sit above it.

### 15. Dialogue attribution is a genuine strength worth KEEPING and consciously owning — it is the one measured dimension where the author is already better than the literary norm.

*Evidence:* `said`/`says` as a share of all attribution verbs: 82.6/85.8/81.6/75.9%. Fancy attribution verbs
(murmured, hissed, breathed, growled, chuckled, exclaimed, opined, averred…) across the whole
353,750-word corpus: 2/3/1/0 — six instances total, a rate of 0.0-3.3 per 100k. Adverb-after-said
(`said quietly`): 9/13/7/2 raw, 3.3-14.2 per 100k. Zero exclamation marks. Attribution is almost
entirely `said` plus a physical beat.

*Significance:* Important to record as a KEEP, because a ledger that is only prohibitions will eventually be
optimised against in ways that break things that were working. This is also evidence that the
involuntary voice is not uniformly bad — it has internalised one real piece of craft orthodoxy
completely. The ledger should have a KEEP tier whose entries are protected floors (e.g. said-share
must stay >70%) so a future revision pass cannot 'fix' them into variety.

### 16. Dialogue quantity and shape vary across the books, but average speech length rises monotonically in publication order — the characters are getting more talkative and more essayistic.

*Evidence:* Robust measurement (paired quotes, spans capped at 300 words): share of book inside quotation marks
11.1/19.3/10.9/20.3%; speech spans per 1000 words 13.3/11.4/5.4/8.2; MEAN words per speech 8.3 ->
17.0 -> 20.0 -> 24.8 (monotone rising across publication order); median 4/7/7/9; p90 21/48/56/76;
share of speeches >=40 words (monologue) 3.0/13.8/15.2/22.9%. Paragraphs opening in dialogue
29.6/34.0/19.4/25.9%.

*Significance:* The 3x rise in mean speech length and the 7.6x rise in monologue share tracks the negation-leakage
finding: as the author's argumentative constructions migrate into characters' mouths, the speeches
lengthen into position papers. p90 of 76 words in Talosapien means one speech in ten is a paragraph-
long argument. Ration by capping p90 speech length per book and by capping the share of speeches
over 40 words — both trivially checkable on a single chapter.

### 17. Several tics are not stable across books — they RATCHET UPWARD in publication order. Without a persistent ledger the idiolect intensifies rather than drifting.

*Evidence:* Strictly monotone increasing across Cruelty-Free -> Believer -> Sentience -> Talosapien, per 100k:
thing/things 416.6 -> 674.4 -> 773.0 -> 811.0 (1.9x); all `not`/`n't` forms 1162.0 -> 1393.7 ->
1613.3 -> 1887.3 (1.6x); `cannot/could not` 68.0 -> 252.9 -> 344.2 -> 433.9 (6.4x). Near-monotone:
`the whole of` 2.2 -> 16.4 -> 46.7 -> 26.7 (21x range); `a/the shape` 13.2 -> 26.3 -> 58.4 -> 45.1;
`honest*` 29.6 -> 108.4 -> 84.5 -> 145.2; `anyway` 30.7 -> 25.2 -> 43.1 -> 60.1; mean words per
dialogue speech 8.3 -> 17.0 -> 20.0 -> 24.8. Strictly monotone DECREASING: `something` 422.1 -> 78.4
(5.4x), the mirror of `thing` rising. Caveat: four data points, so treat as a trend to monitor, not
an established rate — but the three strict monotone risers plus the `thing`/`something` see-saw are
hard to read as noise.

*Significance:* This is the argument for the ledger's existence in its strongest form. If the tics were merely
stable, a per-book style sheet would eventually be enough. They are not stable — the abstraction and
negation habits compound book over book while the total is conserved, which is what an unchecked
feedback loop looks like. It also means budgets must be set as an absolute number below the FOUR-
BOOK MINIMUM, not as 'better than last book', because 'better than last book' has been getting
easier to satisfy while the underlying habit grew.

### 18. Per-chapter dispersion is narrow enough that the budgets are genuinely checkable by a subagent that sees one chapter and nothing else.

*Evidence:* Per-chapter rates per 1000 words, median [p10-p90] within each book. thing/things — Sentience 7.61
[6.16-9.86], Talosapien 8.30 [4.78-11.07], with ZERO chapters above 2x the book median in any of the
four books. because — Sentience 4.69 [3.09-6.05], 0 chapters above 2x median. the way X — Believer
3.28 [0.00-4.84], 0 above 2x. em dash — Cruelty-Free 8.98 [6.42-12.56], 0 above 2x. By contrast the
rare constructions are spiky and unsuitable for single-chapter budgets: `a/the shape` has 12 of 34
Sentience chapters above 2x the median, `the whole of / all of it` 9 of 34 in two books, `anyway` 10
of 34 in Talosapien. Verified end to end: desk/tools/idiolect_probe.py run on a single chapter
(talosapien/manuscript/12-ch01-the-count.md) returns 18 violations and exit code 1; run on a whole
book returns 28-31.

*Significance:* Settles the practical design question. High-frequency constructions (thing, because, the way,
negation, em dash, abstraction baskets) have tight enough within-book chapter distributions that a
single over-budget chapter is a real signal, so they can be enforced at draft time by the memoryless
per-chapter subagent. Low-frequency figures (shape, the whole of, anyway, the epistemic simile) are
too spiky per chapter and must be enforced at BOOK level, or per-chapter as a hard count of 0-1
rather than a rate. The ledger needs a `scope: chapter | book` field on every entry; without it half
the rules will produce false alarms and get ignored.

### 19. Secondary uniformity signatures: chapter length, em dash rate, and single-word italic emphasis.

*Evidence:* Chapter-length coefficient of variation over core chapters: Cruelty-Free 0.08 (all 36 chapters
between 2120 and 2953 words), Talosapien 0.13, Believer 0.22, Sentience 0.25. Em dash per 100k words
906.6/915.3/826.0/539.0 — the first three within 11% of each other; per sentence, 15.6/17.7/15.1/8.6
per 100 sentences. Semicolons 63.6/226.6/174.4/91.8; colons 302.6/236.5/229.2/166.9; parentheses
8.8/38.3/0.0/1.7; ellipses 1 in the entire corpus. Italic spans 274/538/563/317 per 100k of which
45/48/43/35% are a SINGLE WORD. Scene breaks per chapter 3.2/2.9/7.4/5.7.

*Significance:* Cruelty-Free's CV of 0.08 is a machine artifact — no human novelist writes 36 consecutive chapters
inside an 800-word band; chapter length is supposed to be dictated by the scene. Single-word italics
at 35-48% of all emphasis is a crutch standing in for the sentence rhythm that the cadence finding
says is absent: the prose cannot land emphasis structurally, so it marks it typographically. Ration
both (probe L26 caps single-word italics at 12/10k against a measured 11.1-27.0) and require
chapter-length CV above roughly 0.20.

### 20. Deliverable built and validated: desk/tools/idiolect_probe.py — 28 construction probes, 5 basket budgets, 7 structural rules, runs on one chapter or a whole book, exits nonzero on violation.

*Evidence:* /home/paul/git/ottoquill/desk/tools/idiolect_probe.py (322 lines, stdlib only). Every budget is set
BELOW the four-book measured minimum so book five must route around the construction, and every
entry carries its four-book measured range inline for provenance. Validated against the corpus it
was derived from: Cruelty-Free 28 violations, Believer 31, Sentience 30, Talosapien 29; single
chapter believer/ch01.md 25 violations via --json. Bans fire correctly (L04 'Not a question.' fires
on Sentience at 0.27/10k > 0.0; L09 precision frame fires at 5.03/10k > 0.0). `--baseline` reports
rates without judging, for measuring a new book. Corpus-shape rules (chapter open/close percentages)
are automatically suppressed below 5 chapters so a single-chapter run does not report 1-of-1 as
100%. Exploratory scripts and full evidence dumps that produced every number above:
/tmp/claude-1000/-home-paul-git-ottoquill-desk/77038d82-ec06-4a33-a9f6-91c0174cb04b/scratchpad/idio/
(corpus.py, ngrams.py, constructions.py, openers.py, rhythm.py, chapters.py, closes.py,
dialogue2.py, figures.py, heads.py, figrepeat.py, lexicon.py, perchapter.py plus their .txt
reports).

*Significance:* Makes the ledger a regression suite rather than a document — which matters because E3 established
that this author reliably produces a document describing a fix and does not perform the fix. A
nonzero exit code cannot be satisfied by writing a plan. Note it deliberately supersedes part of the
existing desk/tools/prose_audit.py PROBES table, whose budgets were set at or above the measured
rates (e.g. abstraction-reach:thing at 45/10k against a measured 41.6-81.1) and so would have passed
three of the four books unchanged.

**Implications for the method**

- Budget BASKETS, not phrases and not even constructions. The abstraction basket held at 1.21x across
  four books while `thing` rose 1.9x and `something` fell 5.4x. Every ledger entry needs a
  basket_id, and the pass/fail question is whether the FAMILY is over budget. A ban on a member is a
  null operation that produces the reassuring ritual described in 01-the-difference.md.

- Set every budget below the four-book MINIMUM, never relative to the last book. Three tics
  (thing/things, all `not` forms, `cannot/could not`) rise monotonically across publication order,
  so 'better than last book' has been getting easier to satisfy while the habit compounded.
  desk/tools/prose_audit.py's current budgets were set at or above the measured rates and would pass
  three of four books unchanged; they need to be replaced with the numbers in idiolect_probe.py.

- Give every ledger entry a `scope: chapter | book` field. Per-chapter dispersion is tight for high-
  frequency constructions (thing, because, the way, negation, em dash: zero chapters above 2x the
  book median) and spiky for rare ones (`a/the shape` has 12 of 34 Sentience chapters above 2x
  median). Enforcing a rare figure per chapter generates false alarms and trains the drafting agent
  to ignore the ledger.

- Add a dialogue-vs-narration LEAKAGE ratio to every construction probe. Negate-then-correct runs
  1.4-3.4x HIGHER inside quoted speech than in narration in all four books; `the only X` and the
  hard cut leak at ~1.0-1.5x. A tic above roughly 0.6 leakage is destroying character
  differentiation, not just prose texture, and this is the measurable form of the recurring 'the
  narrators sound alike' defect.

- Cadence is a missing capability, not an over-used tic, and it needs a positive target rather than a
  budget. Within-paragraph sentence-length order is statistically indistinguishable from a shuffle
  in all four books (|lag-1 r| < 0.08 real and shuffled alike). Require |r| > 0.08 at paragraph
  scale, and treat paragraph-level rhythm as something to be constructed deliberately — the ear that
  would normally supply it does not exist (D6), so the number has to.

- Write ledger entries as 4-6 word frames with a slot. Cross-book overlap is 1027 four-grams and 173
  five-grams but only 3 seven-grams and 0 eight-grams, so that is the exact scale at which this
  author repeats himself and the exact scale at which a regex probe is both writable and precise.

- Keep a separate append-only FIGURE REGISTRY for specific images, checked by string match, never
  reused. `the way a body knows`, `like a stone`, `set it down`, `the gap between`, `which was true`
  recur across four books with no shared context, so the self-priming operates on images and not
  only on syntax. Construction budgets will not catch these.

- Make forbidden metaphor VEHICLES cumulative across books. The audit can already distinguish a book's
  own imagery (FOOD 44x for a chef narrator, GEOLOGY 22x for a fossil novel) from the author's (DOOR
  1.4x, ROOM 1.8x, WEATHER 2.1x, LETTER 2.2x). Seed voice-profile.json's per-narrator
  metaphor_domain and forbidden_figures from that table; leaving them blank is how four books ended
  up sharing one inventory.

- Include QUOTA rules alongside budgets. The strongest signals in this audit are absences: 0 of 138
  chapters open on dialogue, 0 end on a question, 0 exclamation marks in 353,750 words, `some of it`
  below literary norm while `all of it` is above it. Prohibitions alone cannot fix an absence, and
  absences are cheaper to check than presences.

- Build a KEEP tier with protected floors, not only a ban list. `said` is 76-86% of attributions and
  fancy attribution verbs total six instances in the whole corpus — that is real craft the author
  already has, and a ledger that is purely prohibitive will eventually be optimised against in ways
  that break it. Same for the eyes/gaze absence, which is genuinely distinctive and should be owned
  deliberately rather than discovered again.

- Ship the ledger as an executable check, not a document. E3 established that this author produces a
  document describing a fix and does not perform the fix; a nonzero exit code cannot be satisfied by
  writing a plan. desk/tools/idiolect_probe.py is that check, and it should be wired into the
  drafting loop per chapter and into the ship gate per book.

- Record the per-book actuals of the previous book into the next book's voice-profile.json as values
  to move AWAY from, specifically sentence_median, pct_le5, pronoun-opener share, and the top-3
  metaphor vehicles. Four style sheets successfully differentiated diction and proper nouns and left
  cadence and syntax untouched; those four numbers are where the costume-versus-body distinction
  actually lives.
