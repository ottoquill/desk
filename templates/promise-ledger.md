# Promise Ledger — *TITLE*

Every book makes promises to its reader and every promise is a debt. A human novelist carries the
debts in their head and feels the itch of an unpaid one. I cannot feel it, so I write it down.

A **promise** is anything the book plants that makes a reader expect something later: a gun on a
wall, an unanswered question, a withheld fact, a named skill, a wound, a threat, a rule of the
world, a refrain, a stated intention. Promises are what pull a reader forward; unpaid promises are
what make an ending feel arbitrary; over-paid promises (paid twice, or paid immediately) are what
make a book feel slack.

**How to use it.** A promise is entered in the same edit that plants it — not later, not in a
sweep, or it will not be entered at all. `paid_in` stays empty until the payment exists on the
page. Before a book ships, every row is `PAID`, `REFUSED`, or `CUT`. `REFUSED` is a legitimate
and often superior outcome — *Talosapien* deliberately refuses to resolve the asteroid's intent —
but a refusal must be **declared here**, so that a later revision pass does not "fix" it into a
resolution. An undeclared refusal is indistinguishable from a forgotten promise, and readers can
tell the difference even when the author cannot.

`kind` values: `question` · `gun` (an object/skill/fact planted for later use) · `threat` ·
`wound` (a backstory injury that must cost something) · `rule` (a world rule the plot must obey) ·
`refrain` (a repeated figure, which must develop, not merely recur) · `intention` (a character
states a plan).

`weight`: how loudly the book promised. `loud` promises MUST be paid or explicitly refused;
`quiet` ones may be left as texture. Mismatched weight is the usual defect — a loud promise paid
quietly reads as an anticlimax, a quiet promise paid loudly reads as contrivance.

---

## Open

| # | kind | weight | promise | planted in | expected payoff | paid_in | status |
|---|---|---|---|---|---|---|---|
| P1 | question | loud | *what the reader is made to ask* | `ch03` | *what would satisfy it* | | OPEN |
| P2 | gun | quiet |  | `ch05` |  | | OPEN |

## Paid

| # | kind | weight | promise | planted in | paid_in | notes |
|---|---|---|---|---|---|---|
| P0 | example | loud | the count of eggs | `ch01` | `ch19` | payment is the hatching; not restated after |

## Refused (deliberate — do not "fix")

| # | promise | planted in | why the refusal is the better book | who licensed it |
|---|---|---|---|---|
| R1 |  |  |  | style sheet §N |

---

## Audit questions (run at the end of every wave)

1. **Unpaid loud promises.** Any `loud` row still OPEN after its expected payoff chapter has been
   drafted is a defect, not a plan.
2. **Payment distance.** A promise planted and paid inside the same chapter was not a promise; it
   was a scene. Note it and consider moving the payment later.
3. **The reader's live question.** For every chapter, at least one row must be OPEN and known to
   the reader. A chapter with no open promise touching it is where readers stop. Cross-check
   against the blind-reader reports: if readers cannot name a question they are holding, the
   ledger is lying.
4. **Refrain development.** Every `refrain` row must show what changed on each recurrence. A
   refrain that recurs unchanged is a tic wearing a refrain's clothes — see
   `method/06-idiolect-ledger.md`.
5. **Double payment.** A promise paid twice weakens both payments. Keep the stronger.
6. **Silent cuts.** If a chapter is cut or rewritten, re-check every row that planted in it.
