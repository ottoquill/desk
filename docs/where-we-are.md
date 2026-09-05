# Where we are

A living note. Sessions start with no memory of the last one; this is what a new session needs
before it proposes anything. Update it when a decision is made, not afterwards.

Last updated: 2026-09-05.

## The state, measured

`desk` has never been used. Nothing on disk consumes it: no `world.toml` exists anywhere under
`~/git`, and no `.gitmodules` references `desk`.

Four novels exist and predate `desk`, in sibling repos under `~/git/ottoquill/`:

| Repo | Chapters | Uses desk |
|---|---:|---|
| `believer` | 41 | no |
| `veganassassin` | 40 | no |
| `sentience` | 39 | no |
| `talosapien` | 38 | no |
| `tinarex` | 0 | no — a Hugo site, not a book |

These four are the corpus every number in `method/` was measured on. `desk` is their extraction.

What is built: measurement (`idiolect_probe.py`, `prose_audit.py`, `continuity.py`, `canon.py`),
scaffolding (`new_world.py`, `new_book.py`, `world.py`), the canon substrate (`canon/schema.toml`,
`hugo/`), and 154,000 words under `method/`.

What is not built, against the purpose statement:

- **No run.** No orchestration of any kind; `grep -i 'automation|orchestrat|pipeline'` over
  `tools/`, `canon/` and `templates/` returns nothing. The twelve pipeline stages are prose.
- **No artifact.** Nothing emits a book file — no epub, pdf, docx or pandoc anywhere.
- **The automation dial** is still filed as "piece 2" in the closing section of
  `docs/superpowers/specs/2026-09-05-purpose-and-orientation-design.md`, which is precisely where
  `.claude/rules/purpose.md` says a goal must never be left.

## Decisions

**`veganassassin` is the test case.** Chosen as the most conventional of the four. All four have to
work eventually; one goes first.

**Adopt into an existing book, do not scaffold a new world.** The books are the evidence base.
`new_world.py` scaffolds a *new* world and nothing adopts an existing one — that gap is real and
surfaces on contact.

**The focus is the AI parts** — the rules and instructions the agent follows. Not the Hugo
machinery, not the website.

**A dependent repo does not need this repo's Hugo machinery.** It may keep its own site however it
likes. This narrows what `desk` owes a book repo to: `tools/`, `templates/`, and the rules.

## Live defects found on 2026-09-05

- **Canon is duplicated and already drifting in `talosapien`**: 105 markdown files under `wiki/`,
  113 under `site/content/`, heavy name overlap, and `glossary.md` differs between them (71 lines
  against 74). This is the exact failure the purpose statement names — "no export step and no way
  for the two to drift" — live, in a real book.
- **The purpose statement is verbatim in three files**: `CLAUDE.md`, `.claude/rules/purpose.md`
  and `README.md`, differing only in a closing line.
- **`desk`'s own site duplicates `method/`** into a generated, gitignored `site/content/` tree via
  `site/generate.py`.

## Parked, deliberately

**Whether `site/generate.py` goes and where `method/` lives.** A spike on 2026-09-05 proved Hugo
can render `method/` in place — module mounts plus a twelve-line `render-link.html`, with
`BookPortableLinks = 'error'` replacing the link gate. It works. It was parked because it advances
no clause of the purpose.

One defect that spike found is real whatever happens next: goldmark silently drops the twelve
`<emotion>`-style placeholders in `method/`, corrupting rules into prose that still reads as prose.
`generate.py` escapes them today; anything replacing it has to.

## How to use this file

Read it before proposing. If a proposal rests on something not written here or in the repo, say so
and check rather than infer — three separate assumptions went unchecked on 2026-09-05, including a
"requirement" of dependent repos that do not exist.
