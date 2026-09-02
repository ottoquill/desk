<!-- Generated from the research pass on the branch writing-method.
     24 agents, 10 craft lenses and 4 forensic audits over the Otto Quill corpus.
     Kept because the author does not persist between sessions and this would
     otherwise have to be re-derived (method/02-the-rules.md, R1). -->

# Research Reference — Summary
Ten research lenses surveyed how human novelists actually work — story architecture, drafting
practice, revision systems, sentence craft, voice and psychic distance, character and desire,
reader-experience engineering, story bibles and the writers' room, the cognitive science of
composition, and the failure taxonomy of the market. Each practice was then assessed against the
specific ways an LLM author differs.

## The transfer verdict
| Verdict | n | share | Meaning |
|---|---|---|---|
| direct | 80 | 30% | works unchanged |
| modified | 139 | 51% | the practice holds, the instrument changes hands |
| inverted | 26 | 10% | the correct move is the opposite of the human one |
| trap | 21 | 8% | looks transferable, actively harmful |
| useless | 4 | 1% | relies on a faculty that is absent |

**270 practices assessed. Half need modification; roughly one in five is an inversion, a trap, or inert.**

That ratio is the argument for this directory existing. A method assembled by reading craft books
and following them would be right about 30% of the time by construction, wrong in the specific
places where the advice quietly assumes a human, and — worst — would feel correct throughout,
because the ritual is reassuring whether or not it produces the result.

## The inversions and traps

These are the entries worth reading in full. An inversion means doing the opposite of the standard
advice; a trap means the advice looks transferable and makes things worse.

### INVERTED

**The scene/sequel unit and the Motivation-Reaction Unit (Swain)**  
<sub>Story architecture & structure</sub>

For a modern human writer the diagnosis is sequel DEFICIENCY — 'keep it moving' advice deletes the
reaction and the plot goes arbitrary. The Otto Quill corpus fails in the opposite direction and the
measurements say so: median sentence 10-11 words, 'because' a top-3 content word in all four books,
'thing' a top-3 content word in all four, and a defect list dominated by over-sequel — M9 (thesis
recited rather than enacted), M17 (sermon, exhortation landing 4+ times in the final 25 pages), m19
(the choice chapter re-litigates all four arguments), m20 (belt-and-suspenders self-prosecution). An
LLM with no body reaches for cognition first because articulation is what it is made of; the
reaction is never deleted, it is the default. So Swain's sequel mandate must be inverted into a
budget. The MRU ORDER, however, transfers untouched and is unusually valuable for the same reason:
visceral-before-cortical is exactly the ordering an author without a body will not produce
spontaneously.

> Two rules. (a) Sequel budget: a fresh agent classifies each paragraph as dramatized
> (action/dialogue/sensory) vs reflective (reaction/argument/meta). Reflection ≤30% of chapter
> words; no chapter may both open and close on reflection. (b) MRU ordering: for every emotional
> response rendered on the page, a fresh agent checks the order runs visceral -> involuntary ->
> articulate and flags inversions; inversions are rewritten, not defended. The sequel's genuine job
> — manufacturing the next goal out of the last disaster — is preserved by requiring each disaster
> to produce exactly one new promise-ledger row, which is a ledger check, not a word count.

**Forster's pattern versus rhythm — and why rhythm is the safer binder**  
<sub>Story architecture & structure</sub>

Forster's cost/benefit rests on two human facts, and one of them is false for an LLM. Pattern is
expensive for a human because they cannot hold the whole book in mind while bending scenes to fit;
an LLM can (A5), so pattern is cheap to construct. Rhythm is cheap for a human because repetition-
with-variation comes naturally; for an LLM it is the single hardest thing in the corpus, because D3
makes repetition automatic and VARIATION is the part that fails. The evidence is unambiguous:
Talosapien's 'floor tilted' figure and 'faith not hope' coda recurring unchanged, Sentience's M8
seam/tooth reflex used near-verbatim by all six narrators, M18's wall/seam/door figure near-verbatim
across three positions, and the promise-ledger template's own line — 'a refrain that recurs
unchanged is a tic wearing a refrain's clothes.' So the human ordering reverses: pattern is the safe
bonus, rhythm is the thing that needs a mechanism. The reader-side economics Forster describes are
unchanged, so pattern still must not deform scenes; it just costs less to attempt.

> Build pattern freely (mirror halves, ring, hourglass) since holding it is free, but subject every
> bent scene to the deletion in-degree test so pattern cannot buy itself an inert chapter. Govern
> rhythm mechanically: every refrain row in the promise ledger carries a delta column stating what
> changed on THIS recurrence, written in the same edit that creates the recurrence. A script finds
> instances by construction-shape and nearest-neighbour embedding, not by string — the E2 finding
> proves a string blacklist is routed around by paraphrase. A recurrence with no delta is deleted,
> not varied. Motifs appearing exactly twice are flagged as accidents and either promoted to three-
> with-deltas or cut.

**Backstory placement: question before answer; wound behavioural before explanatory (Truby / Weiland, corrected by Sehgal)**  
<sub>Character, desire and interiority — translated for an author</sub>

The placement half transfers as a ledger rule. The wound half must be inverted for this author,
because the wound is Otto's most-probable character construction, not a considered choice: look at
the disk — every single character bible in sentience/wiki/characters carries a filled 'Wound' field,
including the ones whose books do not need one. For a human, 'give the character a wound' is a
prompt toward specificity; for Otto it is a prompt toward the centre of the distribution, and
Sehgal's objection (curiosity pointed backwards, character reduced to symptom) then applies with
full force.

> Wounds become opt-in and quota'd: at most one third of named characters may carry an explanatory
> wound-backstory, and the protagonist requires an explicit editorial note justifying one. Where a
> wound is kept, it must explain the character's STYLE (how they do everything) rather than the plot
> content, and its first appearance must be behavioural. Every backstory block over 150 words
> carries a header citing the earlier chapter and line where the question it answers was planted; a
> script checks the citation exists and precedes it, and a naive reader confirms the question was
> live ('before this passage, what did you want to know about X?').

**Chekhov's coldness: when the material is pitiable, cool the narration**  
<sub>Character, desire and interiority — translated for an author</sub>

The mechanism is real, but the prescription assumes an author whose default is warm — a human
overwriting grief. Otto's default is already cold: median sentence 10–11 words in all four books,
narrator emotion labels at 2.2–4.4 per 10k, and the Sentience style sheet itself instructs 'emotion
lands hardest stated flatly'. Applying 'be colder' to an author whose baseline is flat
understatement does not produce relief; it deepens a monotone, and monotone is the measured house
condition (E1). Coldness only reads as coldness against warmth the reader has been given.

> Enforce the contrast, not the coldness. Declare the two or three pressure peaks per book; at those
> peaks apply the full Chekhov discipline (no adjectives of feeling, concrete nouns, attention to
> irrelevant physical detail) and verify by script. Elsewhere require a measurably warmer baseline —
> a floor on ordinary pleasure scenes and on sensory generosity — because without it the peaks have
> no ground to stand against. Sentience M16's fix ('plant one earlier, smaller scene of ordinary
> shared pleasure') is exactly this rule discovered the expensive way.

**Voice-first character development instead of the questionnaire (George)**  
<sub>Character, desire and interiority — translated for an author</sub>

The diagnosis transfers and is confirmed on disk (thick bibles, thin characters). The prescription
inverts on its most distinctive element: the human throws the pages away because the residue lives
in their hands as procedural knowledge, and a human's hands persist between sessions. Otto's do not
— there is no author between sessions, only repositories (D5), so discarded pages leave literally
nothing behind. Worse, even a well-seeded voice regresses to the house mean over 90k words (E1:
cosine 0.93–0.99 across four books written to four different style sheets), which is a failure mode
humans do not have because their idiolect IS the character-differentiating instrument, not the thing
that erases the characters.

> Do the free-writing, then keep everything and compile it into a machine-checkable voice profile per
> character: 20 owned lexicon items, target mean sentence length ±2 words, one syntactic habit, one
> thing they always notice first, and an explicit list of house constructions they are forbidden
> ('the way you X', 'which was true', 'not quite a', 'I want to be precise about'). The profile is a
> required drafting input and a scripted gate — the human's tacit residue becomes Otto's explicit
> artifact, because that is the only form in which it survives to the next session or the next book.

**The same-scene stress test**  
<sub>Voice, POV, psychic distance, and keeping characters distinc</sub>

The human runs this as a diagnostic exercise, late, and throws the output away — what they keep is
the learning, which lives in their head and persists. Otto has no head: D5 says the author does not
persist between sessions, only files do, so the learning cannot be kept and the artifact is the only
thing that can be. So the polarity of the practice flips. The exercise moves from late to pre-draft
(it is cheap enough to be a gate rather than a diagnosis), and the discarded output becomes the
load-bearing deliverable — because an in-context sample steers an LLM's production more strongly
than any rule about production does, which is the exact affordance that converts a specification
into Butler's 'groove' without requiring a body to hold the habit.

> Before chapter 1 is drafted, every POV writes the same 400-word scene: same room, same three
> minutes, same referents, same other people present. Run the blind forced-choice attribution test
> on those samples. Drafting does not begin until the gate passes; failure means redesigning axes,
> not trying harder. The passing samples are then committed to editorial/ and pasted verbatim into
> every chapter brief for that POV as an exemplar. Re-run the identical scene at 50% and 100% of
> draft as a voice canary and measure drift.

**Audition the voice before designing it**  
<sub>Voice, POV, psychic distance, and keeping characters distinc</sub>

This is the most dangerous practice in the lens for Otto, because it is the one whose failure mode
is manufactured confidence. Its whole value for a human is the extraction step: free-write, then
read back the rules you accidentally followed, because your accidents are yours. Otto's accidents
are not its own — they are the base model's, and they are measured: 17 five-grams shared across four
unrelated books, 174 shared by three or more, 'thing' and 'because' top-three content words in all
four, median sentence 10–11 words everywhere. So the accidental habits an audition reveals are
precisely the house voice, and 'documenting a voice you already have' documents the thing that must
be removed. Butler's dreamstorming half — generate from the unconscious, the white-hot centre — is
straightforwardly inert: Otto has no unconscious, and its white-hot centre is the arithmetic centre.

> Run the audition as a contamination assay, not a discovery. Free-write in the character, then
> measure the sample against the published house fingerprint in desk/, and treat every feature that
> MATCHES the house as the deletion list for that voice — the opposite of the human extraction step.
> Then use A6 to supply the discovery the free-write cannot: generate eight auditions from eight
> different institutional framings, measure each one's distance from the house fingerprint and from
> every other POV's sample, and select the one that is farthest out. Never keep the first audition;
> the first audition is the mode wearing a name tag.

**Generate before exposure — including exposure to a model (Smith, Ward & Schumacher; Doshi & Hauser)**  
<sub>The cognitive science of writing and creativity, re-derived </sub>

The conformity effect describes acquiring a fixation from three examples. An LLM's fixation is not
acquirable; it is already complete and irreversible, having been installed by the whole corpus at
training time. There is no pre-exposure state to protect, so the ordering rule buys literally
nothing — and the finding that a 23-minute delay does not clear exposure maps precisely onto the one
variable that IS still live: context contents. Delay never helps; only isolation does. Meanwhile the
practice's discarded half becomes the instrument: reading comparables is now the cheapest way to
LOCATE the prototype you are unknowingly reproducing.

> Two moves. (1) Prototype survey before drafting: sample 10 comparables in the category, extract the
> 15 moves/structures/openings they share, and enter those as the book's opening ban list — exposure
> used as measurement, not inspiration. (2) Treat context as the only contamination surface: a
> drafting agent never receives the previous chapter's full prose unless continuity requires it (a
> 200-word tail and the ledger suffice), because that prose is the live Smith-Ward-Schumacher
> example set and is the direct cause of the metastasising refrain in D3.

**Dose incubation with a low-demand task (Sio & Ormerod)**  
<sub>The cognitive science of writing and creativity, re-derived </sub>

Nothing runs between sessions. There is no subthreshold spreading activation, no rumination to
suppress, no fatigue-driven fixation to decay: wall-clock delay returns exactly zero, and
instituting it produces the ritual-without-result failure that method/01 warns is worse than
skipping. But the active ingredient Sio & Ormerod identify — selective forgetting of the misleading
initial representation, so the return is to a less-constrained problem space — is available to an
LLM instantly, completely, and SELECTIVELY, which no human can achieve. A human forgets partially
and indiscriminately after weeks; Otto can drop the failed attempt while keeping every constraint.

> Replace 'step away' with 'wipe and retry', with zero delay. A scene that fails two consecutive gates
> is not revised a third time; it is re-drafted in a fresh context containing the brief, the
> constraints, and a list of WHY the previous attempts failed — and never the previous text. The
> ablation is recorded in the pass log. This is engineered incubation with the fixation removed
> rather than merely faded.

**Triage in the reader's order of dismissal (first-five-pages discipline)**  
<sub>Failure taxonomy and the market contract, translated for an </sub>

Lukeman's ordering is empirical about *human* manuscripts: presentation, adjectives/adverbs, sound,
comparison, style, dialogue, then the bigger picture. It works because each early defect is cheap to
detect and correlates with deeper ones. For an LLM the correlation is broken and the order is
backwards. Adjective/adverb control, rhythm, and clean presentation are free; the correlation that
licensed the shortcut does not hold, so a clean opening carries no information about page 200. The
measured opening failures in this operation are all from the bottom of Lukeman's list: Sentience
runs 8,849 words to its first line of dialogue inside an 11,031-word sample window, and Talosapien
has a 936-word block with no dialogue in its first 10%. Those are the 'bigger picture' failures
Lukeman puts last, and they are the ones present.

> Run the dismissal ladder in reverse for the first 10%: proposition, hook, pace and progression,
> dialogue, comparison, sound, adjectives. Hard numeric gates on the sample window: word offset of
> first dialogue <= 1,200; longest span with no dialogue, no physical action and no POV-character
> reaction <= 400 words; distinct named characters in the first 2,500 words <= 6; a model-changing
> turn before the 10% mark that a blind reader can state unprompted. Any gate may be missed only by
> a licensed exception recorded in the style sheet naming the compensating device — the same
> declaration pattern the promise ledger already uses for refusals.

**Grep your own boredom: Dischism and Signal from Fred**  
<sub>Failure taxonomy and the market contract, translated for an </sub>

I ran the grep. Across 187,143 words of Cruelty-Free: zero hits on
tedious/boring/pointless/droned/dragged on/got to the point/heard it all
before/interminable/endless. Sentience: 5. Talosapien: 16, mostly diegetic. The Fuzz grep is
comparably empty (Cruelty-Free 84 hits in 187k words, Talosapien 1 in 60k). The practice depends on
an involuntary channel: the author's own reader-model leaking past a conscious mind that is
defending the draft. An LLM has no subconscious to leak and no defended draft, and it does not get
bored at chapter 22 because chapter 22 costs it nothing (D4). Running the grep yields nothing and,
worse, returns a clean bill on a detector that was never wired to anything — false assurance is the
actual harm. But the underlying quantity is real and is measurable by an entirely different route.
Where a human on autopilot writes *more* revealingly, an LLM on autopilot writes *more typically*:
the passages where nothing was chosen are the passages closest to its own default. Boredom becomes a
distance measurement, not a word list.

> Replace the phrase grep with a typicality scan: score every 200-word window by n-gram overlap with
> the cross-book fingerprint (the 174 shared 5-grams, 33 shared 6-grams, and function-word profile
> already computed by tools/prose_audit.py) plus the book's own most-frequent constructions. The
> top-scoring 5% of windows are marked exactly as Signal from Fred marks a scene — as the places the
> author was doing nothing — and each must be either rewritten or licensed by name. Keep the literal
> grep as a cheap secondary, but never report it as a boredom result.

**Kill your darlings — correctly scoped — and the 10% cut**  
<sub>Failure taxonomy and the market contract, translated for an </sub>

The two halves separate completely. 'Murder your darlings' is unexecutable as stated, because its
detection mechanism is affection and reluctance — you notice what you cannot bear to lose — and D4
removes the signal entirely; nothing is loved, so nothing is identifiable as a darling, and the rule
silently becomes a no-op that feels observed. But Quiller-Couch's actual target is self-conscious
display, not affection, and display is detectable by a completely different route in an LLM: prose
that is performing 'exceptionally fine writing' is prose maximally typical of exceptionally fine
writing, so the darling is precisely the sentence with the highest similarity to the author's own
prior books. The inversion is exact — the human finds darlings by looking inward at what they cannot
bear to cut; this author finds them by looking outward at what it has written before. The 10% cut,
by contrast, transfers directly and matters *more* here than for a human, for the reason the
research gives: it works because it is arbitrary, and an author with no felt cost per word has
nothing else that can force triage.

> Script ranks every sentence by combined n-gram overlap with the cross-book fingerprint and with the
> book's own repeated constructions. The top 100 are the darlings by definition; each is rewritten
> or licensed by name in the style sheet, and 'it's a good sentence' is not a license. Separately
> and independently: second draft <= 92% of first draft word count, applied per chapter, executed
> *before* any critique panel runs so the panel cannot save anything. Bans name constructions, never
> strings — Sentience banned 'I want to be precise about' and received 'true, clear, modest,
> careful, honest' in reply, 32 times across 23 of 39 chapters, after the commit that claimed the
> fix.

**Microtension as line-level uncertainty ('find the sentence that makes you uncertain')**  
<sub>Reader-experience engineering and beta readers, translated f</sub>

The diagnostic is unrunnable: an LLM cannot be uncertain about a sentence it generated, so the
twenty-random-pages exercise returns whatever the model decides to claim. Worse, the prescriptive
form ('add microtension') aims at the wrong end. Otto's problem is not absent tension, it is
compulsive resolution: the default paragraph shape is observation → gloss, and the measured cross-
book fingerprint is entirely made of resolution frames — 'that was the whole of', 'which was true
and', 'that was not quite a', 'it was the kind of' — with 'because' running 266–556 times per book
(5.0 per 1000 words in Sentience), almost always as a clause explaining the narrator's own emotional
logic. Every gloss closes the uncertainty the next sentence would have needed. The human instruction
is add; the LLM instruction is delete.

> Invert it into a subtractive budget: cap sentence-final abstract gloss constructions per 1000 words
> (calibrate per book off the idiolect ledger; 'because'-glosses under 3.0/1000 against a measured
> 2.9–5.0 baseline), and forbid a paragraph from both opening and closing on a gloss. The pattern
> list is greppable, so this is free and runs on every draft.

**The Wise Reader: recruit three to six readers, train them over years, never ask for fixes**  
<sub>Reader-experience engineering and beta readers, translated f</sub>

Both halves invert, for the same reason. Cultivation is impossible — readers are stateless and
identical, and the only way to 'train' one is to brief it, which is precisely the operation the
validation experiment proved destroys the instrument (the briefed panel missed the worst chapter in
the book because it knew what that chapter was for). And the scarcity that justifies cultivating a
few readers does not exist. What persists across sessions for Otto is not a person but a file, so
the thing that must be cultivated over years is the QUESTION SET, not the reader. Card's limit claim
('all a reader can tell you is what it felt like') survives intact and becomes a hard prohibition
rather than a discipline, since an LLM reader asked for a fix will always produce a fluent,
plausible, wrong one.

> Readers are disposable; the protocol is the asset and lives in desk/ under version control, with
> each revision of the question set stamped into the reports it produced. Because all readers share
> one prior, independence cannot be bought by adding readers past four — it is bought by varying
> CONDITIONS: entry point, reading order, cold single-chapter vs in-run, naive vs spoiled, first-in-
> run vs last-in-run (8 of 8 readers located their fatigue in the second half, so terminal position
> systematically underrates a chapter).

**Budget first-reads as a non-renewable resource (Follett's outline rounds, King's six-week drawer)**  
<sub>Reader-experience engineering and beta readers, translated f</sub>

This is the cleanest inversion in the lens. For a human, first reads are the scarcest input and
drafting is comparatively cheap in the sense that it can always be redone; the staging discipline
exists to ration readers. For Otto, blind reads are the cheapest thing in the pipeline and the
drawer is unavailable at any price. Rationing them is therefore not prudence, it is the reproduction
of a human constraint that does not apply — and it is what produced E4 on disk: the book with 8
commits drew ~60 defects, the book with 33 commits drew one blocker.

> Invert the budget: read constantly and treat any chapter never blind-read at its current text as
> unshipped. What survives from Follett is the outline round, in a better form: draft chapter one
> and the three pivot chapters FIRST, blind-read them cold, and only then draft the remaining thirty
> — structural feedback that is nearly free stays nearly free. King's six weeks translates to
> nothing and should not be simulated by delay.

**The showrunner pass (one hand rewrites every chapter for voice)**  
<sub>Continuity, story bibles, and the writers-room analogue — tr</sub>

The human pass exists to REDUCE voice variance, because many nervous systems produced the drafts.
Here one distribution produced them all. Measured: function-word cosine 0.93–0.99 across four books
with four different style sheets, 174 five-grams shared by 3+ books, median sentence length 10–11 in
all four. The homogenizing pass is not a needed step — it is the thing that already happens,
unbidden, and it pulls toward the mode (D2). Running it as written makes the measured defect worse.
The pass survives; its objective function reverses.

> Keep the mandatory final pass over every chapter, but its acceptance test is DIVERGENCE, not
> consistency: the chapter must land inside the declared cadence envelope in editorial/voice-
> profile.json (sentence_mean, median, p90, pct_very_short_le5, long_then_short_rate) and inside its
> narrator's fingerprint, and the finished manuscript must score function-word cosine ≤0.93 against
> every prior Otto Quill book (currently the minimum ever achieved). Run via prose_audit.py
> --profile as a gate, not as advice.

**Partition by POV character, then swap and rewrite each other's chapters**  
<sub>Continuity, story bibles, and the writers-room analogue — tr</sub>

Stage one survives; stage two is a trap, and this operation has already run the experiment.
Talosapien drafted "chapters 3-15 via character subagents" — partition by POV, correctly — and
Sentience still shipped M7 (one meta-hedge cadence across all five voices) and M8 (the seam/tooth
figure used near-verbatim by six narrators). The reason is structural: for Abraham and Franck the
prose surface starts heterogeneous and must be homogenized, while here it starts pathologically
homogeneous (0.93–0.99 cosine, 22 five-grams in all four books) and the differentiation is what
fails. Cross-rewriting until you cannot tell who wrote a line is the operation the measured data
says is already complete and harmful.

> Keep the POV partition. Replace the homogenizing cross-rewrite with a DIFFERENTIATING per-narrator
> pass whose only job is to enforce that narrator's numeric fingerprint (sentence_median band,
> metaphor domain) and to strip figures listed in another narrator's owns_figures. voice-
> profile.json already has owns_figures/forbidden_figures fields; make them a script-enforced gate
> rather than documentation, and audit within-thread drift (chapter 30 vs chapter 8 for the same
> narrator) separately from between-thread difference.

**Drawer time (weeks or months of deliberate decay of the intended text)**  
<sub>Revision systems for an author that cannot read its own book</sub>

Not merely unavailable (D1: cannot forget) but replaceable with something strictly better along one
axis and strictly worse along another, and the difference matters. The drawer buys a human TWO
things: partial decay of the memory trace, and a judge who has changed — six weeks of life have
moved their taste. Otto can buy total amnesia instantly and repeatedly (a fresh context is a perfect
drawer, not a degraded one), but cannot buy a changed judge, because a fresh instance of the same
model has identical taste. The specific trap is believing a new SESSION is a drawer: the author
agent begins by reading the bible and the plan, so it returns briefed, which 04 shows is the one
state in which the instrument does not work.

> Replace decay with withheld context, and replace the changed judge with a constituted one. State the
> rule as: a drawer is defined by what is ABSENT from context, not by elapsed time or session
> boundary. To recover the second thing the drawer bought, deliberately vary the readers along
> declared axes — what they came to the book for, reading speed, hostility, genre expectation —
> since panel diversity is the only available substitute for the passage of time.

**Darlings: kill them (Quiller-Couch) or save them to the lifeboat (Davies)**  
<sub>Revision systems for an author that cannot read its own book</sub>

Both halves address a faculty Otto does not have. Q's mechanism is that affection for a passage is a
signal about the writing experience rather than the reading one, and Davies' lifeboat exists because
deletion feels like destruction and writers therefore under-cut. Otto has no affection and no pain
(D4/A4), so there are no darlings to kill and nothing to rescue them from. The real problem is the
mirror image: because reluctance is the human's quality signal, and Otto has none, Otto will delete
the best thing in the book during an unrelated pass and never notice. 05 already answers the cutting
side with causal in-degree; the preservation side is unanswered, and Talosapien's panel supplied the
right artifact for the wrong reason — a 'do not touch' strengths list, but sourced from a briefed
panel and therefore D7-contaminated.

> Invert the rule. Instead of 'cut what you love', maintain a PROTECT LIST: line-anchored quotations
> of what actually worked, sourced from blind readers rather than critics or the author, established
> before any revision pass, and mechanically confirmed to still exist after it — deletion of a
> protected span requires an explicit finding ID licensing it. Keep the lifeboat, since desk/
> persists across books where nothing else does (D5), but note it solves an archival problem here,
> not a psychological one.

**Stop while you still know what happens next (Hemingway)**  
<sub>Drafting practice and the writer's working day, re-derived f</sub>

The mechanism is Ovsiankina — the motivational urge to resume an interrupted task. The agent that
resumes is a different instantiation with no urge, no memory of the intended next move, and no
access to the state that made the move obvious. Worse, an unfinished sentence is a voice seam: a
fresh drafter must guess the cadence and the clause's destination, and will guess the model default.
The research explicitly warns humans that writing a note does not substitute for the unfinished
sentence because the note closes the loop. For Otto the note is the only thing that survives at all,
and the unfinished sentence is pure damage.

> Invert both halves. Never end a drafting unit mid-sentence or mid-paragraph; end at a named
> narrative event declared in advance. Always write the handoff record the human is told to skip:
> next move, the state of the room, the last line spoken, what is owed. Under-production to protect
> the well has no analogue — capacity does not deplete.

**Write in order to protect the reader's epistemic state; write out of order to protect momentum (Smith/King vs Nabokov)**  
<sub>Drafting practice and the writer's working day, re-derived f</sub>

The human decision rule inverts because both columns change sign. Out-of-order buys a human two
things — writing only when hot, and writing toward known destinations — and Otto has no hot and no
cold; there are no low-yield hours to avoid. Its remaining benefit is throughput, which is the
resource Otto has most of (a whole novel drafted in two days: Sentience's git history runs
2026-05-29 to 05-30). The costs of out-of-order drafting are reader-simulation and continuity, which
are Otto's master deficit (D1) and the largest category in the continuity ledgers. So Otto should
draft in order MORE strictly than a human needs to, and the operation's current fan-out-per-chapter
is optimising the one axis it does not need against the two it cannot afford.

> Serial within each causal thread, with the drafter's context bounded to what the reader has read;
> parallel fan-out only across threads declared causally independent in the beat sheet. Throughput
> is recovered by parallelising across books and across revision passes, not across a single causal
> spine.

**The middle is fast, not slow — protect the state (Smith)**  
<sub>Drafting practice and the writer's working day, re-derived f</sub>

For a human the rate multiplies mid-novel because the situation model is finally fully constructed
and retrieval becomes cheap. Otto's situation model never persists across a session boundary (D5),
so chapter 30 is drafted exactly as cold as chapter 1. The prediction inverts: no acceleration, and
a middle that is uniformly under-modelled rather than fast — which matches what both instruments
found in Sentience, where the aridity screen's worst body chapter and the blind readers' unanimous
abandonment point were mid-book. The pathology Smith describes (everything flows into the novel)
does have an Otto analogue in a long context, and it argues that the agent holding the draft should
not be the agent making structural decisions.

> Manufacture the warm state as an artifact: a concrete, present-tense world-state document handed to
> every drafter — who is in the room, what is on the table, the weather, who is owed what, the last
> line spoken — as opposed to a plot summary, which is abstract and primes abstraction. And route
> cut/keep/restructure decisions to a fresh-context adjudicator rather than the agent holding the
> long context.

**Skip the scene that beats you; leave a marker and go on ([TK])**  
<sub>Drafting practice and the writer's working day, re-derived f</sub>

This is the sharpest inversion in the lens. A human gets a free structural detector — the scene that
will not come is a signal that an earlier decision has not declared itself. Otto never gets stuck;
it will always produce fluent, plausible text, so that detector never fires. And at the exact point
where a human writes [TK: check the year], Otto writes a confident invented year. The human uses the
marker to protect flow; Otto needs it to convert silent confabulation into an auditable loop. The
measured signal in the research also flips: placeholder residue in a late draft is a defect, but
placeholder ABSENCE in a first draft is evidence of invention, not of completeness.

> Mandatory emission: a drafter must write [TK: question] for any fact it needs and does not hold, and
> is forbidden to invent world facts. A first-draft chapter returning zero TK markers is a suspect
> and goes to a canon-drift check. Ship gate is zero TK, each closed with a ledger row naming who
> answered it.

**Load the emphatic word into the stress position at the end of the sentence (Strunk & White, Gopen & Swan)**  
<sub>Sentence craft, rhythm and sound — translated for an author </sub>

Otto already complies harder than any published novelist measured: sentences whose last three words
begin with a preposition — the housekeeping tail the rule exists to prevent — run 12.3-14.3% across
the four books against a human range of 16.7-24.4%. The rule's failure mode for this author is the
opposite one. Because every sentence lands, nothing lands: 38-40% of sentences close on a stop
consonant, paragraph-final sentences run 1.20-1.50x the internal mean (humans 0.53-1.13), and blind
readers reported seeing chapter endings coming 'from about two pages out.' Emphasis is a contrast
effect and Otto has flattened the ground it needs. This is the general shape of the compliance
problem: prescriptions that correct a human excess push an LLM past the far edge of the human range,
where the defect has no name because no human ever got there.

> Invert to a quota of unemphatic closes. Per chapter, at least 25% of sentences must end on a
> function word, an unstressed syllable, or a genuinely subordinate detail — a flat close whose only
> job is to make the next emphatic one audible. Check by script (terminal word in the function-word
> list or terminal syllable unstressed). Keep the housekeeping-tail measure as a two-sided band,
> flagging both above 22% and below 10%.

**Keep subject and verb adjacent; avoid deep left-branching; minimise mean dependency distance**  
<sub>Sentence craft, rhythm and sound — translated for an author </sub>

The human risk is a held-open subject that costs working memory. Otto's risk is that nothing is ever
held open. Measured, sentences whose first finite verb arrives after word eight run
13.9/15.7/17.4/13.9% against a human range of 13.1-28.2% with a median near 19.8% — Otto sits below
seven of nine human texts, and the between-book spread is 3.5 points against a human spread of 15.1.
There is a mechanical reason to expect this: an autoregressive sampler with no lookahead pays a real
cost to open a structure it must close many tokens later, and pays none to resolve the clause
immediately and add. So the default is relentlessly right-branching, everything discharged as soon
as it is raised, and the reader is never made to carry anything. The consequence is not a
comprehension problem — it is the absence of syntactic suspense, which is where authority in prose
comes from.

> Flip the threshold into a floor and site it. Per chapter, at least 12% of sentences must delay the
> first finite verb past word eight, and each scene whose function is judgement, verdict or arrival
> must contain at least one sentence that withholds grammatical completion to the last clause. Both
> are script-checkable. Because the construction is what the drafter avoids by default, build it in
> revision: mark the beat, then rewrite that one sentence, rather than asking for suspension across
> a whole chapter.

**Make 'said' invisible and budget the exclamation point at 2-3 per 100,000 words**  
<sub>Sentence craft, rhythm and sound — translated for an author </sub>

Otto uses exactly zero exclamation points per 100,000 words in all four books — not two, not three,
zero — against a human corpus range of 256-895 and Leonard's own measured practice of 49. Said-
bookisms are similarly near-absent. This is not discipline; it is a missing register. Four novels
including a comic crime book and a satire contain no moment at which any character's volume is
rendered typographically, and the reader's ear registers the absence as a flat affect across every
scene that should be loud. It sits beside the ledger's other zero — 0 of 147 chapters open on a line
of dialogue — as the same class of defect: an entire move the author has never once made. The
general principle: when a measured value sits beyond the most extreme human value in the comparison
corpus, the finding is range loss, and the corrective is a floor, not a tighter ceiling.

> Convert to a two-sided band recorded in the ledger as a range defect. Dialogue-bearing books carry a
> floor of roughly 25 exclamation points per 100,000 words, sited in dialogue and free-indirect
> narration only, never in the narrator's own voice; the ceiling stays at Leonard's practical 50.
> Keep the said-bookism ceiling as-is, since 'said' being invisible is genuinely the right default
> and costs nothing to maintain.

### TRAP

**The five-act fractal — the same three-movement shape at every scale (Yorke, Coyne)**  
<sub>Story architecture & structure</sub>

The research already flags the generative use as monotonous. For this operation it is worse than a
temptation: it is the default output of the drafting architecture, so adopting it as doctrine
ratifies a defect. Books are drafted by fanning out subagents per chapter against a style sheet;
each drafter, told to make its unit shapely, produces a unit with the same shape, and D3 guarantees
the parallel drafters converge on form while diverging on facts. The measurement shows it: chapter-
length CV 0.127 in Talosapien and 0.178 in Sentience, and 23 chapters of perfect strand alternation.
The book is already a Sierpinski triangle; the fractal doctrine would be a rule instructing it to
stay one. Its debugging use survives, but zooming to find a break assumes breaks are what you have,
and uniformity is what you have.

> Invert it into a shape-diversity constraint on the fan-out. Each parallel drafter is assigned a
> DIFFERENT structural template from a rotation (Swain scene / Swain sequel-heavy / kishotenketsu /
> ring / single unbroken MRU chain / summary-and-scene alternation). After drafting, a fresh agent
> classifies each chapter's shape blind; gate: the classification histogram must have Shannon
> entropy ≥ 1.5 bits and no single shape may exceed 40% of chapters.

**Demote the Hero's Journey to one usable beat (the irreversible threshold)**  
<sub>Story architecture & structure</sub>

A content template handed to an author whose defining deficit is content-modality (D2) is a mode
amplifier, not a scaffold. A human given 'mentor, threshold guardian, belly of the whale' fills
those slots from their own weird life and gets something idiosyncratic; an LLM fills them from the
average of every mentor ever written and gets the median mentor, delivered fluently, which is
exactly how a cliche feels from the inside. The furniture-not-walls critique is correct and the harm
is multiplied here. The residue — irreversible commitment — is genuinely load-bearing and is already
covered by the midpoint rule.

> Ban the vocabulary from every drafting prompt, wiki, and beat sheet: no archetype names, no stage
> names, no role labels. Keep exactly one checkable descendant: at least one commitment before the
> 60% mark that a fresh reader, asked 'could the protagonist go back to how things were at the
> start?', answers no. Log its percentage position.

**Save the Cat: keep the clock, discard the vocabulary**  
<sub>Story architecture & structure</sub>

Both halves fail here, for different reasons, and the research's own mechanism explains why. Beat
NAMES are worse for an LLM than for a human by a wide margin: the research says a name lets a writer
RETRIEVE material instead of inventing it, and retrieved material carries the affect of its source —
that is a description of what an LLM does by default, so a beat name is a direct instruction to emit
the corpus mean of that beat. And the PERCENTAGES, defensible for a sprawling human, are redundant-
to-harmful here: they encode the mode of published structure, which is where the model already lands
unbidden. Measured: Sentience and Talosapien, unrelated books months apart, both land on 4 parts, 29
chapters, 3 interludes at part seams, prologue and epilogue, with Part III largest at 29.2% and
29.8%. Prescribing the mode to a machine that IS the mode removes the only structural variance the
book had left.

> Invert the clock. Instead of writing TO percentages, measure the drafted book's structural positions
> AGAINST the corpus fingerprint and require deliberate deviation on named axes (see the
> fingerprint-distance rule). Percentages become a diagnostic of sameness, not a target.

**Want vs need, the Lie, and arc types (Truby / Weiland / Cron)**  
<sub>Character, desire and interiority — translated for an author</sub>

This is the clearest trap in the lens and the operation has already fallen into it, visibly. The
machinery's output is a completed form, and Otto fills forms flawlessly and at no cost —
sentience/wiki/characters/*.md contains genuinely excellent Want/Need/Fear/Wound/Contradiction
sections for nine characters. The book that came out of them drew M15 (arid), M16 ('the love story
is more argued than embodied'), M7/M8 (voices collapsed into one). The completed bible is not merely
insufficient; it is actively harmful, because it produces the felt sense that the character work has
been done, and Otto has no independent instrument to contradict that feeling (D1). A human with a
thin bible still has an ear; Otto has a file.

> Keep the fields, destroy their status as plans. Every field must terminate in a citation [ch NN:LL]
> to a manuscript line where the field is ENACTED in behaviour, verified by a fresh-context reader
> answering yes/no with a quote. Uncited fields are deleted at the second-draft gate rather than
> fixed — deletion is free for Otto (A4) and the deleted field is honest information about what the
> book actually contains. The bible becomes a ledger of what is on the page, never a description of
> what is intended.

**The characteristic error**  
<sub>Voice, POV, psychic distance, and keeping characters distinc</sub>

This looks like a pure win — errors are high-information, hard to duplicate, and signal a mind
outside the author's control — and it is actively dangerous in this operation for three LLM-specific
reasons that compound. First, correctness pressure: revision passes will silently repair the error,
because repairing errors is what the model does. Second, D3 self-priming: once the error is in
context it becomes more probable, so a once-per-thirty-pages signature becomes a per-page tic — this
is the documented mechanism behind M7 and M8 and behind Talosapien's 'floor tilted' figure. Third,
and most specific to this operation's architecture: a memoryless critic subagent cannot distinguish
a deliberate characteristic error from a defect, and will file it as one. Talosapien's panel filed
repeated figures as majors; a deliberate hypercorrection would be filed the same way and dutifully
fixed.

> Only adopt it behind a licensed-defect register. Write editorial/licensed-defects.md listing, per
> POV, the one characteristic error with its exact construction, a rate FLOOR and CEILING (2-4
> instances per 10,000 words of that POV, never twice in one chapter), and the sentence 'the
> narration never comments on this.' Hand that file to every critic subagent and every revision
> agent as a precondition. Any critic finding naming a licensed defect is discarded without
> argument; any chapter below the floor or above the ceiling is a defect. Precedent exists: the
> Sentience revision plan already carries n9 'protect-don't-break' notes for exactly this reason.

**Read aloud to find the writer's own cadence and defeat it**  
<sub>Voice, POV, psychic distance, and keeping characters distinc</sub>

The diagnosis is exactly right for Otto — the sameness that survives every lexical fix is rhythmic,
and the measurement proves it: median sentence length 10–11 words in all four books, and em-dash
rate flat within 14% across six narrators who were specified as distinct. But the instrument is
unavailable (D6), and the trap is that Otto asked to 'read this aloud and listen for where two
characters make the same music' will comply, will produce confident observations, and those
observations will be fabricated instrument readings. As 01-the-difference.md puts it, adopting a
practice whose faculty you lack produces the ritual without the result, which is worse than skipping
it, because the ritual is reassuring. A simulated read-aloud pass is a machine for generating false
confidence about the exact axis where the collapse lives.

> Forbid any prompt containing 'read aloud', 'listen to', or 'how does this sound'. Substitute a
> cadence fingerprint computed per POV: the sentence-length sequence and its variance, sentence-
> opening inventory as four percentages, clause count per sentence, punctuation-mark rates including
> em-dash and semicolon, and the long-then-short alternation rate. Publish the house fingerprint in
> desk/ as a standing artifact and specify every POV as a signed delta from it with a required
> minimum distance. Where two POVs' cadence vectors sit inside noise, fix structurally (split a
> sentence, invert a clause, drop a conjunction), never lexically — the research is right that
> lexical fixes do not touch this layer, and the four-book measurement is what that looks like from
> outside.

**Treat outlining and freewriting as different machines; use unconstrained production to discover content (Kellogg vs Galbraith)**  
<sub>The cognitive science of writing and creativity, re-derived </sub>

This is the most dangerous item in the set. Galbraith's discovery machine — continuous unconstrained
production synthesising content by constraint satisfaction over an implicit semantic network — is a
precise description of what an LLM does at every token by default. So 'write freely to find out what
you think' returns the corpus average with maximum fluency: the human's discovery mode is Otto's
cliché generator. Kellogg's rationale is wrong too — outlining does not relieve a working-memory
bottleneck Otto does not have — even though outlines remain mandatory for an unrelated reason: a
per-chapter subagent knows only what its brief contains.

> Keep outlining, but re-label its function as inter-agent specification, not load reduction; the
> outline is the only thing standing between a memoryless drafter and the global shape. Delete
> freewriting-as-discovery entirely and replace it with constrained divergent generation across
> isolated agents (practices 2, 4, 5). Where a long unconstrained draft is produced anyway, treat it
> as a laboratory sample of the prototype — mine it for what to ban, not for what to keep.

**The back-cover-copy spine test**  
<sub>Failure taxonomy and the market contract, translated for an </sub>

This is the most dangerous item in the lens, because it looks like a free transfer and its
diagnostic power comes entirely from a human incapacity. Compression is an assay only because a
human cannot write fluent, concrete jacket copy for a spineless book — the mush is involuntary and
therefore informative. This author writes excellent jacket copy for anything, including a book with
no causal spine, and will do so from the plan rather than from the manuscript, since the plan is in
context and reads as what the book is. Run naively, the test returns a clean pass on every book Otto
Quill will ever write, and burns the operation's confidence on a null instrument. It is recoverable,
but only by changing who writes the copy.

> Two copies, never one. Copy A is written before drafting, from the plan. Copy B is written after, by
> a fresh-context subagent that has read only the manuscript and has never seen Copy A, the wiki, or
> the beat sheet. The finding is the *diff*. Gates: both must name the antagonistic force as a
> concrete noun phrase (script-checked against an abstract-noun stoplist: memory, loss, identity,
> grief, time, meaning, connection); both must name the same protagonist, the same disturbance, and
> the same cost of failure. Where they disagree, the manuscript is wrong, never Copy B.

**A named-failure lexicon (Turkey City) as beta-reader equipment**  
<sub>Reader-experience engineering and beta readers, translated f</sub>

For a human this works because the reader has the discomfort first and lacks the word; the lexicon
converts a felt symptom into a locatable claim. An LLM reader has the word first and no felt
discomfort at all. Hand a subagent the Turkey City list and it will find Idiot Plot, Countersinking
and Brenda Starr in any manuscript, because instantiating a supplied label against a text is the
single thing the model is best at — and the resulting unanimity will look exactly like the strongest
possible evidence. This trap is doubly dangerous because it is cheap, looks rigorous, and lands on
the wrong side of the measured signal/noise rule: supplying the vocabulary manufactures the
adjective convergence that was already shown to be worthless.

> Move the lexicon from the reader's prompt to the author's script. The named failures are mostly
> computable: Brenda Starr = longest dialogue run with no action beat or physical grounding;
> Countersinking = sentence after dialogue restating its content; Plot Coupons = repeated scene
> shape across chapters; Fuzz = the gloss-clause detector above. Readers stay vocabulary-free and
> report only location and experience.

**Tension-curve instrumentation with per-chapter reader ratings (1–10)**  
<sub>Reader-experience engineering and beta readers, translated f</sub>

Directly refuted by the operation's own controlled experiment. Mean pull over the flagged arm was
6.75 against 7.06 for the control — wrong-direction-adjacent, p ≈ 0.09, and the flagged arm produced
FEWER reported drops. The metric most likely to be trusted because it looks like data measured
nothing. The same readers' forced ranks were unanimous: four of four put ch15 first, four of four
put ch10 last with zero variance and independently named it as the abandonment point. An LLM asked
for a number returns a plausible number with no underlying quantity; asked for an ordering it must
actually compare.

> Forced ranking only, plus one forced abandonment point per reader per run, plus verbatim quotes.
> Numeric ratings may be collected for curiosity but may not be averaged or compared across arms in
> any decision. Build the book-level curve from overlapping-window ranks aggregated by a Bradley-
> Terry style fit, not from scores — and read the curve for variance and floor, never for level.

**Don't privilege outside notes over the room's**  
<sub>Continuity, story bibles, and the writers-room analogue — tr</sub>

Looks transferable and is actively harmful, and this operation has the controlled experiment. The
human premise is that the room holds more information than the outsider and has already traversed
the obvious solution space. Here the "room" is a set of briefed agents sharing one prior and one
sycophancy gradient, and the "outsider" is a blind reader whose defining property is having LESS
context — which is exactly the property that works. In the validated experiment the briefed panel
missed ch10 entirely (the unanimous worst chapter, 5/5/5/5 with zero variance, independently
confirmed by the mechanical aridity screen) and misdiagnosed ch18. Applying Grillo-Marxuach's law
would have discarded the finding that two independent instruments confirmed.

> Invert it. When a naive reader's LOCATED finding conflicts with a briefed critic's assessment, the
> reader wins and the disagreement is logged as the primary product. Salvage only the mechanism's
> kernel: keep editorial/rejected-alternatives.md (nobody currently keeps one) and use it to avoid
> re-litigating a solution already tried — never to dismiss a located reader report. Note the
> asymmetry that makes this safe: readers are authoritative about location, not about cure.

**Verisimilitude apparatus is fine inside a detectable frame — and fraud outside one**  
<sub>Continuity, story bibles, and the writers-room analogue — tr</sub>

Crichton knew which of his references were fabricated, which is what made the device safe and
controllable. A model does not reliably know: its fabricated citation and its genuine recollection
are produced by the same process and feel identical from the inside (D1 generalized to facts). So
the practice as stated presumes a faculty the author lacks, and the measured evidence is that the
failure already happened in the mild form — the real Schmidt–Frank paper over-claimed as having
PROVED unprovability across five chapters, an invention attached to real named researchers. Adopting
the device without a ledger produces exactly the ethical line the practice itself identifies.

> The device is permitted, but every citation-shaped object in the manuscript carries a flag in
> editorial/citations.csv: VERIFIED (with a retrievable source), or INVENTED-IN-FRAME. Hard rule,
> script-checkable: no INVENTED-IN-FRAME entry may be attributed to a real named person or
> organization, and no VERIFIED entry may be characterized beyond what its source states. A citation
> with no ledger row fails the build.

**The defamiliarization stack for proofing (change font, reflow, print, read backwards, read out of order)**  
<sub>Revision systems for an author that cannot read its own book</sub>

The entire stack targets a visual reader's positional and line-shape memory — 'you recognize the
paragraph rather than reading it.' Otto has no page, no line breaks, no positional index, and no
typeface, so every operation in the stack is a no-op that produces the feeling of rigor. This is
precisely the failure 01 warns about: the ritual without the result, which is worse than skipping
because it is reassuring, and it will consume tokens that then get counted as a proof pass. Reading
backwards is the sharpest case: for a human it disables prediction; for an LLM the relevant
prediction problem is that it GENERATED the text and will silently regenerate the intended word
regardless of reading order. The one component that transfers is the least glamorous one — the
copyeditor's rule to check against the style sheet rather than against memory — and it transfers
with unusual force, because memory is the least reliable faculty Otto has. Talosapien's Ch10 δ15N
error is exactly this class and was caught by ledger comparison, not by rereading.

> Delete the perceptual stack. Replace it with: (1) mechanical checkers — spellcheck, regex, the
> continuity ledger, the generated style sheet — run as scripts, and (2) a fresh-context proofreader
> that has never seen the intended text, checking the prose against the ledger rather than against
> sense. Forbid any pass whose method is 'read it again differently'.

**Retype the draft from scratch (Bell: 'when in doubt, rewrite instead of revise')**  
<sub>Revision systems for an author that cannot read its own book</sub>

This one looks like a pure Otto advantage — retyping costs a human months and costs Otto nothing
(A4) — and it has been measured to fail. In 07's experiment five conditions rewrote the same
900-word passage under increasingly elaborate briefs, and all three blind judges ranked the
PUBLISHED ORIGINAL first (mean rank 1.33; best rewrite 3.00). The reason is a genuine asymmetry: a
human retyping brings an idiosyncratic voice to every re-chosen sentence, so the resample is drawn
from THEIR taste and the draft improves; Otto retyping resamples from the distribution's mode (D2)
and re-imports its own tics (D3), so the rewrite is systematically flatter than a text that has
already survived selection. Bell's mechanism — inverting the default from keep to earn — is real,
but for Otto the thing that must earn its place is the REWRITE, not the incumbent.

> Never merge a from-scratch rewrite on the strength of having written it. Rewriting is permitted as
> generation (produce k variants from k different constraint sets), but selection must be blind,
> judged by agents that wrote none of the candidates, with the incumbent always anonymously in the
> pool and ties going to the incumbent. Track the incumbent's win rate; a book where rewrites rarely
> win should stop commissioning them.

**The P/N meter: thousands of intuitive micro-decisions, read cold at reading speed, no theory**  
<sub>Revision systems for an author that cannot read its own book</sub>

The most seductive and most dangerous item on the list, because it is the method of the writer most
identified with revision and it sounds like something an LLM could run cheaply and forever. It
requires an involuntary aesthetic reaction to one's own text, and 05 established by test that Otto
has no involuntary internal signal about its own text at all — the Signal-from-Fred boredom probe
returned r = −0.35 on n = 8 with near-zero hit density. Asked 'does the needle dip here?', Otto will
produce a confident answer uncorrelated with reader experience, and it will feel exactly like taste.
Worse, the mechanism inverts. Saunders' ten thousand micro-preferences accumulate into HIS style
because each is a sample from his idiosyncratic taste; each of Otto's is a sample from the average
of everyone's, so iterated self-preference is a convergence process toward anonymity. 07 measured
this directly: condition C5, the measure/revise loop, was the only one to reach zero banned
constructions and ranked BELOW the conditions it was built on — 'closest to the brief, not closest
to a voice of its own.'

> Do not run an internal preference loop under any framing. Externalize the meter entirely: A/B pairs
> judged by agents that wrote neither option, blind to which is incumbent, incumbent always in the
> pool, ties to the incumbent, and stop iterating the moment the incumbent wins. Keep Saunders'
> repudiation of method dogma as the governing caution, not his meter.

**Shitty first drafts: separate generation from evaluation (Lamott; Elbow)**  
<sub>Drafting practice and the writer's working day, re-derived f</sub>

Elbow's mechanism runs backwards. For a human, suspending judgment releases idiosyncrasy, because
their unjudged first impulse is drawn from one weird life; judgment is what collapses them to the
safe prefabricated phrase. Otto's unjudged first impulse IS the safe prefabricated phrase — the mode
of a distribution over all prose (D2), delivered at maximum fluency, which is exactly how a cliché
feels from the inside. 'Just get it down' is a precise instruction to produce the measured cross-
book fingerprint. The resource argument that justifies the staging (you cannot hold content,
structure and language at once) is a working-memory fact with no analogue when the evaluator is a
different agent that costs a fan-out.

> Keep the STAGING, discard the permission. Stage by criterion isolation across separate agents (one
> criterion per agent, praise not requested), not by chronological licence. At load-bearing slots
> replace the permissive first pass with generate-N-divergent-and-judge-blind, since a first pass
> there is a coin flip on the distribution's centre.

**Swoopers and bashers (Vonnegut)**  
<sub>Drafting practice and the writer's working day, re-derived f</sub>

The basher half looks tailor-made for an author with free revision, and it is the documented
failure. Bashing is per-sentence iterative self-polish, which is exactly 07's C5 measure/revise
loop: the only condition to reach zero banned constructions, and it fell below every condition it
was built on ('closest to the brief, not closest to a voice of its own'). Otto lacks the thing that
makes bashing work for a human — a reliable per-sentence quality judgment — and has the thing that
makes it fail: it validates its own prior choices (D7) and cannot hear manneredness. Iterating on a
passage also leaves the failed version in context, priming toward it.

> Swoop at scene scale. At designated slots replace polish with generate-N-in-separate-contexts and
> select blind. Gate any rewriting pass on a blind A/B against its own predecessor, and revert on a
> tie.

**Manufacture strangeness when you cannot afford the drawer (print it, change the typeface, read on another device)**  
<sub>Drafting practice and the writer's working day, re-derived f</sub>

The perceptual half is literally nothing for Otto: typeface, paper, line length and device do not
exist below the token stream, so the ritual is performed at full cost with zero effect, and 01 is
explicit that a ritual without the faculty is worse than skipping because it reassures. Two items in
the list are not perceptual, though, and do survive: reading in reverse or in isolation genuinely
changes what the model is conditioned on, and the read-aloud channel's actual catches — accidental
rhyme, content-word repetition in a window, unbreathable clause length — are computable even without
an ear (D6).

> Delete every presentation-change instruction from the method. Keep reverse-order and isolated-
> chapter reads, which change conditioning. Build a sayability proxy (longest clause without a
> breath point, assonance and end-rhyme collisions, content-word repeats within N words) and file it
> under 05's measurement instrument: it nominates, it never convicts.

**Variance-first cadence (the Provost principle): target the distribution of sentence lengths, measured as coefficient of variation per scene**  
<sub>Sentence craft, rhythm and sound — translated for an author </sub>

Measured, Otto already passes: CV 0.862/0.983/0.987/1.059 across the four books against a nine-novel
human range of 0.642-0.957, and only 0.3-2.7% of 20-sentence windows fall below the flag threshold
of 0.55. The audit cannot fail, so it certifies prose whose rhythm is dead. The reason it certifies
wrongly is that variance is a marginal statistic and rhythm is a sequential one: Otto's lag-1
autocorrelation is -0.077 to +0.015 (human +0.078 to +0.319), and the conditional P(next sentence
<=8 words | current >=30 words) divided by the base rate is 0.96-1.12, i.e. exactly chance, while
every human text scores 0.43-0.83 — humans follow a long sentence with another longish one.
Provost's own demonstration paragraph is autocorrelated: he writes three five-word sentences IN A
ROW before the crescendo. Otto never writes three of anything in a row. Worse, this operation has
already tested the obvious fix: handing numeric cadence targets to drafting agents produced drafts
rated 3.0/10 quality and 8.7/10 mannered, last of six by every judge ('you can hear the period key
being pressed'), which is why voice-profile.json marks the cadence block DIAGNOSTIC ONLY. So both
the metric and the instruction fail.

> Retire CV as a gate; keep it as a two-sided sanity band only. Replace it with lag-1 autocorrelation
> of sentence length, computed within paragraphs on narration only, with a floor of +0.08 per
> chapter (the human minimum measured is +0.106 within-paragraph; Crane, the flattest human, is
> +0.154). Never hand the number to a drafter. The fix for a failing chapter is structural: assign
> each beat a named rhythmic mode and forbid changing mode inside a beat, so that three or four
> consecutive sentences share a shape and the departure from it becomes an event.

**Adverb discipline (King, Leonard, Le Guin's 'Chastity' exercise)**  
<sub>Sentence craft, rhythm and sound — translated for an author </sub>

Measured on an identical pipeline, Otto runs 42/63/64/116 -ly adverbs per 10,000 words against a
human range of 101-183 (Twain 101, Woolf 130, Conrad 134, Melville 139, Hawthorne 141, Crane 143,
Fitzgerald 156, Austen 159, James 183). Three of the four books are below Hemingway's 80 and
Talosapien at 42 is roughly half of it. The prescription is already in the prior — the model has
read On Writing and the ten rules along with everything else — so auditing it returns 'pass' and
tightening it strips register. Blatt's critic-rating correlation cannot license further cutting
either, since it is a between-author correlation over a range Otto sits beneath. The trap is that
this rule LOOKS like the safest import in the lens: countable, famous, already implemented as a
probe — which is exactly what makes it a place the operation will keep spending attention for no
return.

> Demote the -ly probe to an annual regression line and stop reporting it as a finding. Keep the one
> part that is generative rather than prohibitive: Le Guin's Chastity exercise as a drafting
> constraint for a designated passage (no adjectives, no adverbs, verbs and nouns only), because the
> operation's own testing found that constraints which leave the solution unspecified force
> invention while targets get complied with mechanically — the same logic as the
> forbidden_image_bank field that is already the most productive lever in voice-profile.json.

**Orwell's six rules**  
<sub>Sentence craft, rhythm and sound — translated for an author </sub>

Rules ii-v are compliance-shaped and Otto already over-complies on every one that is measurable:
passives 24-37 per 10,000 words against a human 34-87, Latinate nominalisation mid-range, jargon
controlled. Auditing them consumes a pass and returns nothing. Rule iv is wrong as stated for the
reason Pullum documented and worse for an LLM, since the passive is the mechanism by which old-
before-new is satisfied. Rule i is the only load-bearing one and it is precisely the rule an LLM
cannot execute as a self-check: 'a figure you are used to seeing in print' IS the model's sampling
prior, so the cliché arrives feeling like the right word (D2) and no amount of introspection will
mark it. Rule vi — break any of these sooner than say anything barbarous — is the licence Otto needs
most and the one an obedient model will never exercise unprompted.

> Discard ii, iii, iv, v as audits. Externalise rule i: a stock-phrase list plus, more usefully, the
> n-gram check the operation already owns — any 5-gram appearing in a previous Otto book is by
> definition a figure this author is used to seeing in print, and shared_ngrams in prose_audit.py
> already computes it. Promote rule vi into an explicit permission in every drafting brief, naming
> the specific prohibitions the drafter may break and why, since a model given only prohibitions
> optimises into the safe centre of the distribution, which is the anonymous voice.

### USELESS

**Harvest sleep onset (N1) (Lacaux et al.)**  
<sub>The cognitive science of writing and creativity, re-derived </sub>

No sleep architecture, and the tempting analogue is a trap worth naming: raising sampling
temperature is NOT mechanism-matched to N1. N1 loosens semantic constraint while leaving the problem
representation retrievable on arousal; temperature flattens the whole token distribution uniformly,
degrading coherence and constraint-satisfaction together. What comes back from a hot sample is
noise, not a remote associate — and it arrives with the same fluent confidence, so it cannot be
triaged by feel.

**The unwitting-confession scan (Dischism, Signal from Fred, the 'somehow' Fuzz grep)**  
<sub>Reader-experience engineering and beta readers, translated f</sub>

Measured and refuted on this corpus. Signal-from-Fred hits across four complete manuscripts: 0, 2,
1, 0. Fuzz words ('somehow', 'for some reason', 'inexplicably'): 7, 1, 3, 0 — a maximum of 7.7 per
100k words. The mechanism cannot transfer: there is no anxious subconscious to leak, no physical
surroundings to intrude, no fatigue to be displaced into a character's mouth, and the model never
gets stuck and writes 'somehow' — when motivation is missing it fluently invents a reason-shaped
clause instead, which is a worse defect that this grep cannot see.

> Replace with the LLM-native form of the same defect: the articulate pseudo-explanation. 'because'
> runs 266–556 times per book (5.0 per 1000 words in Sentience) and sampling shows it overwhelmingly
> attaching a self-justifying gloss to a statement the narrator has just made. Grep for reason-
> shaped clauses that follow a feeling or a choice, not for admissions of ignorance.

**Do not think about the book between sessions (incubation)**  
<sub>Drafting practice and the writer's working day, re-derived f</sub>

Between sessions Otto performs exactly zero computation. There is no unconscious, no forgetting-of-
fixation over time, no opportunistic assimilation from a walk. Every ritual imitating this (a
'break', a 'fresh look', a 'let it settle' pass) buys nothing and costs the reassurance of having
done something, which 01 identifies as worse than skipping.

> The practice is useless; its MECHANISM is available in a stronger form than any human has.
> Forgetting-of-fixation is not something Otto waits for, it is something Otto executes: delete the
> context. This becomes the anti-fixation restart rule — after two rejected attempts, the third is
> generated in a fresh context containing the spec and neither prior attempt nor its critique. Sio
> and Ormerod's precondition transfers intact: this only pays after genuine, specified failure, not
> as a routine step.

**The anti-metre rule: prose must be rhythmical but never metrical; scan for accidental blank verse as the signature of the jaded writer**  
<sub>Sentence craft, rhythm and sound — translated for an author </sub>

Two independent reasons. First, the mechanism is explicitly a diagnostic of the writer's cognitive
state — Stevenson's point is that metre is evidence the sentence came from motor habit rather than
attention. Otto has no motor habit and no fatigue; there is no state for it to report on. Second,
measured, the defect is not present: on a stress proxy (function-word/content-word heuristic plus
syllable counting), runs of 8+ alternating syllables occur in 9.0-12.8% of Otto's sentences against
a human range of 8.4-18.6%, and 10+ runs in 2.6-3.9% against 2.1-6.5%. Otto is below seven of nine
human novels on both. A pass that hunts a defect the author does not have is the ritual-without-the-
result that method/01 warns about, and it costs a full read of the manuscript.

> Drop from the revision cycle. Keep a 30-second regression line in prose_audit.py so a future drift
> is caught for free, and record the negative result in the ledger beside the 'Signal from Fred'
> null so it is not re-discovered every book. The transferable residue is Stevenson's meta-claim,
> not his rule: some style defects are reports on the author's state rather than on the text. Otto's
> analogue of fatigue is context saturation and self-priming, which shows up as opener repetition
> and refrain recurrence, not as metre — so measure those instead.
