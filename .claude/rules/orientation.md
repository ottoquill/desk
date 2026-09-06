# Orientation

## The orientation note is loaded, not surveyed

`docs/where-we-are.md` is imported into every session by the `@` line near the top of `CLAUDE.md`.
It opens with the arc — what desk is for, where it came from, where it stands, what moves next —
and carries the decisions in force and the defects found, dated. Answer "where are we" and "what
is next" from it. Do not grep the repo to re-derive what it already says; that survey is what this
rule exists to stop.

On 2026-09-06 the state of the repo was asked for from context, and the note was not loaded. The
answer had to come from `CLAUDE.md` alone: everything below the purpose was inference, flagged as
such, and the actual next step — adopt `veganassassin`, the AI parts only — could not be named.

## It is only as true as its date

A loaded note is trusted the way a fact is, so a stale one does more harm than a missing one: a
session answers confidently from it. Two obligations follow.

When a decision is made or the direction moves, update the note in the same turn and bump its
date. Not at the end of the session, and not in a spec — a correction living only in a spec has
been lost twice here already (see `purpose.md`).

Before acting on a specific it states — a count, a file's existence, whether a tool runs — check
the disk. Specifics go stale first; the arc goes stale last.

## Keep it loadable

The note is loaded whole, every session. Keep it to what a session needs before proposing: the
arc, the decisions, the live defects, what is parked. Detail belongs in specs and commit messages.
If it outgrows a couple of screens, move detail out rather than dropping the import.
