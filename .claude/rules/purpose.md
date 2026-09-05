---
paths:
  - "**"
---

# Purpose

## What desk is for

`desk` exists to produce world-class fictional worlds and the stories drawn out of them, with AI
doing the work.

Canon is the substrate, and the wiki is where canon primarily lives — authored as pages under a
world's `content/`, gated as files, rendered with no export step and no way for the two to drift.
Books and games are drawn out of canon. The public wiki is a declared product as well: a filtered,
deployed rendering, because a working canon holds spoilers and unpublished material the public
rendering has to withhold.

Automation is a dial. At one end, a single prompt outlining a concept yields a finished, published
product; at the other, close interactive work. Both ends have to be superb. A run populates canon
first and derives the book from it.

Built for the author's worlds now, generalizable by construction: `desk` knows kinds, a world names
instances, a run names settings. Publishing is in scope as far as the artifact — a distributable
book file and the world's deployed site. Storefront submission is not.

The reasoning behind each of those clauses is in
`docs/superpowers/specs/2026-09-05-purpose-and-orientation-design.md`.

## Before starting work

Name which part of the purpose the work advances. If it advances none, say so before starting,
rather than afterwards.

## Deferral is a decision, not a filing action

When part of a stated goal is not being built now, say so in the conversation and get agreement.
Recording it in a document's closing section is not deferral, it is loss.

On 2026-09-02 the automation dial was restated accurately one minute after the author described
it, filed as "piece 2" in a spec's last section, and three days later no session could recover it
from the repo.

## Prefer the half that does not decompose

Work splits into a part that breaks into tasks with tests and a part that needs a judgment call
with no unit test. The decomposable half is the one an agent reaches for, and it feels like
progress. Taking it is allowed. Taking it silently is not: name the split, and say which half you
are taking and why.

## A goal stated is a goal written down that turn

When the author states or revises the purpose, it lands in `CLAUDE.md` and `README.md` in the same
turn. Specs and plans are working documents. The orientation files are what the next session
reads, and a correction living only in a spec has already failed twice here — once for the
automation dial, once for the wiki filed as an output.

## A correction recorded only in a spec has not landed

When a spec or a review revises a framing the repo's other documents state differently, carry the
revision into the documents that state it. A spec is read by whoever opens that spec.

This rule earned its place twice in one session. The world-contract spec revised the wiki from an
output to the substrate on 2026-09-02; three days later a session read `README.md`, kept the old
framing, and wrote it into a draft rule. The correction had been made, and it stayed where it was written.

## Defaults are overridable

Every default — automation level, budgets, gate thresholds, register — resolves from config a run
or a world can override, never from a literal in a tool or a sentence in prose. Where ambiguity
remains, ask rather than assume.
