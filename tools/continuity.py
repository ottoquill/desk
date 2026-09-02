#!/usr/bin/env python3
"""
continuity.py — the cheapest detector in the operation.

Continuity contradiction is the largest defect class in the Otto Quill corpus (28 of 88
documented defects, 32%) and the ONLY class that has ever produced a declared blocker — all three
blockers across four books were a single fact asserted two incompatible ways by chapters drafted
in the same parallel wave. Parallel drafting agents diverge on facts and converge on phrasing;
this script is the defense against the first half.

    python3 tools/continuity.py MANUSCRIPT_DIR [--facts facts.json] [--names names.json]

--facts   a typed fact store: [{"entity","attribute","value","unit","chapter"}, ...]
          Drafting agents already return an `invented` array of details other chapters must
          honour. Merge those arrays into this file after every wave and run this BEFORE the next
          wave drafts. Any (entity, attribute) key carrying two values is a defect, not a nuance.
--names   the cross-book used-names registry from desk/, so book N+1 does not reuse a name that
          book N deliberately renamed away from.

With neither flag it still runs four manuscript-only scans that need no configuration at all.

PRECISION. The fact-store, spelling and surname checks are near-exact. The pronoun scan is a
heuristic and will produce false positives on entities whose nearby objects attract pronouns
(a "Pool", a "Mesh"); treat its output as a list to look at, not a list to fix. It earns its
place anyway: run against the shipped Sentience manuscript it locates ch25's "Sable warned you,
I know she did" — defect M12, which the revision plan named by line number, the commit message
claimed to have normalised, and the continuity ledger recorded as locked canon. All three
artifacts assert a fix that is not in the text. Nothing but a detector reading the manuscript
catches that.

Stdlib only.
"""
import argparse, json, os, re, sys, unicodedata
from collections import Counter, defaultdict

FRONTMATTER = re.compile(r'\A---\s*\n.*?\n---\s*\n', re.S)

# Words that are capitalised for reasons other than being a name.
STOP = set('''The A An And But Or So If When While Then There Here That This These Those It He She
They We I You His Her Their Our Your My Not No Yes What Which Who Whom Whose How Why Where After
Before Because Although Though Since Until Once Every Each All Some Many Most One Two Three Four
Five Six Seven Eight Nine Ten First Second Third Last Next Now Later Even Only Just Still Yet Of
In On At To For With From By As Was Were Is Are Be Been Being Had Have Has Do Did Does Will Would
Could Should May Might Must Can God Sir Madam Mr Mrs Ms Dr Part Chapter Prologue Epilogue Monday
Tuesday Wednesday Thursday Friday Saturday Sunday January February March April May June July
August September October November December North South East West Earth Sun Moon'''.split())

PRONOUNS = {'he': 'he/him', 'him': 'he/him', 'his': 'he/him',
            'she': 'she/her', 'her': 'she/her', 'hers': 'she/her',
            'they': 'they/them', 'them': 'they/them', 'their': 'they/them',
            'it': 'it/its', 'its': 'it/its'}

def load(d):
    out = []
    for f in sorted(os.listdir(d)):
        if not f.endswith('.md') or f.upper().startswith('README'):
            continue
        t = open(os.path.join(d, f), encoding='utf-8').read()
        out.append((f, FRONTMATTER.sub('', t)))
    return out

def fold(s):
    """Strip accents and case so 'Sólveig' and 'Solveig' collide."""
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn').lower()

def proper_nouns(text):
    """Capitalised tokens not at a sentence start, which is where names hide."""
    out = []
    for m in re.finditer(r'(?<![.!?"“]\s)(?<!^)\b([A-Z][a-zà-öø-ÿĀ-ſ]{2,})\b', text, re.M):
        w = m.group(1)
        if w not in STOP:
            out.append(w)
    return out

# ---------------------------------------------------------------- the four scans

def scan_spelling(chapters):
    """Same name, two spellings — the m12 'Solveig' / 'Sólveig' class."""
    forms = defaultdict(Counter)
    where = defaultdict(set)
    for f, t in chapters:
        for w in proper_nouns(t):
            forms[fold(w)][w] += 1
            where[fold(w)].add(f)
    out = []
    for key, variants in forms.items():
        if len(variants) > 1 and sum(variants.values()) >= 3:
            out.append((key, dict(variants), sorted(where[key])))
    return sorted(out, key=lambda x: -sum(x[1].values()))

def scan_pronouns(chapters, min_hits=6):
    """One named entity carrying two pronoun regimes — the M11/M12 class.

    Strict heuristic, because a loose one is useless: count a pronoun only when it is the FIRST
    pronoun after the name, within a short window, with no other proper noun intervening. That
    still misses most references, but what it counts is nearly always bound to the name, and a
    detector that cries wolf on every abstract noun in the book gets switched off."""
    WINDOW = 7
    names = Counter()
    for f, t in chapters:
        for w in proper_nouns(t):
            names[w] += 1
    common = {n for n, c in names.items() if c >= min_hits}
    regimes = defaultdict(lambda: defaultdict(list))

    for f, t in chapters:
        toks = re.findall(r"[A-Za-zà-öø-ÿĀ-ſ']+|[.!?;]", t)
        for i, tok in enumerate(toks):
            if tok not in common:
                continue
            for j in range(i + 1, min(i + 1 + WINDOW, len(toks))):
                nxt = toks[j]
                if nxt in '.!?;':
                    break                                   # do not cross a sentence boundary
                if nxt in common or (nxt[:1].isupper() and nxt not in STOP):
                    break                                   # a competing antecedent appeared
                low = nxt.lower()
                if low in PRONOUNS:
                    regimes[tok][PRONOUNS[low]].append(f)
                    break                                   # first pronoun only
    out = []
    for n, r in regimes.items():
        tot = sum(len(v) for v in r.values())
        if tot < 10 or len(r) < 2:
            continue
        ranked = sorted(r.items(), key=lambda kv: -len(kv[1]))
        minority = sum(len(v) for _, v in ranked[1:])
        if minority / tot >= 0.15 and minority >= 3:
            out.append((n, tot, {k: len(v) for k, v in ranked},
                        sorted({f for _, v in ranked[1:] for f in v})))
    return sorted(out, key=lambda x: -x[1])


def scan_surnames(chapters, registry=None, families=()):
    """One surname doing duty for two characters — the Believer Okonkwo/Ferris class —
    and reuse of a name across books."""
    full = Counter()
    for _, t in chapters:
        for m in re.finditer(r'\b([A-Z][a-z]{2,})\s+([A-Z][a-z]{2,})\b', t):
            a, b = m.group(1), m.group(2)
            if a not in STOP and b not in STOP:
                full[(a, b)] += 1
    by_last = defaultdict(set)
    for (a, b), c in full.items():
        if c >= 2:
            by_last[b].add(a)
    collisions = {b: sorted(v) for b, v in by_last.items()
                  if len(v) > 1 and b not in families}
    reused = {}
    if registry:
        here = {n for pair in full for n in pair}
        for name, books in registry.items():
            if name in here:
                reused[name] = books
    return collisions, reused

def scan_facts(path):
    """A typed fact store: any (entity, attribute) with two values is a contradiction."""
    facts = json.load(open(path))
    keyed = defaultdict(list)
    for f in facts:
        keyed[(str(f['entity']).strip().lower(), str(f['attribute']).strip().lower())].append(f)
    out = []
    for (e, a), rows in keyed.items():
        vals = {f"{str(r.get('value')).strip().lower()} {str(r.get('unit', '')).strip().lower()}".strip()
                for r in rows}
        if len(vals) > 1:
            out.append((e, a, sorted(vals), [r.get('chapter', '?') for r in rows]))
    return out

# ------------------------------------------------------------------------ report

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('manuscript')
    ap.add_argument('--facts', help='typed fact store JSON (merged `invented` arrays)')
    ap.add_argument('--names', help='cross-book used-names registry JSON: {"Name": ["book", ...]}')
    ap.add_argument('--families', nargs='*', default=[],
                    help='surnames legitimately shared by related characters (suppresses the collision check)')
    a = ap.parse_args()

    chapters = load(a.manuscript)
    if not chapters:
        sys.exit(f'no chapters in {a.manuscript}')
    registry = json.load(open(a.names)) if a.names else None
    fail = 0

    print(f"\n{'='*78}\n  CONTINUITY SCAN — {a.manuscript}  ({len(chapters)} chapters)\n{'='*78}")

    if a.facts:
        conflicts = scan_facts(a.facts)
        print(f"\n  FACT STORE  ({'CONFLICTS' if conflicts else 'clean'})")
        for e, at, vals, chs in conflicts:
            fail += 1
            print(f"    ✗ {e} · {at}: {' vs '.join(vals)}   [{', '.join(map(str, chs))}]")
        if not conflicts:
            print("    no key carries two values")
    else:
        print("\n  FACT STORE  (not supplied — this is the highest-yield check; see --facts)")

    sp = scan_spelling(chapters)
    print(f"\n  SPELLING VARIANTS  ({len(sp)} found)")
    for key, variants, files in sp[:12]:
        fail += 1
        v = ', '.join(f'{k}×{n}' for k, n in sorted(variants.items(), key=lambda kv: -kv[1]))
        print(f"    ✗ {v}")
        print(f"        {', '.join(files[:5])}{' …' if len(files) > 5 else ''}")
    if not sp:
        print("    all proper nouns spelled consistently")

    pr = scan_pronouns(chapters)
    print(f"\n  PRONOUN REGIMES  ({len(pr)} entities with a mixed regime)")
    for n, tot, counts, files in pr[:12]:
        fail += 1
        print(f"    ✗ {n}: {', '.join(f'{k}×{v}' for k, v in counts.items())}  (n={tot})")
        print(f"        minority regime in: {', '.join(files[:5])}{' …' if len(files) > 5 else ''}")
    if not pr:
        print("    every named entity carries one pronoun regime")

    col, reused = scan_surnames(chapters, registry, set(a.families))
    print(f"\n  NAME COLLISIONS  ({len(col)} surnames shared by two characters)")
    if col:
        print("    (related characters legitimately share a surname — pass --families to whitelist)")
    for last, firsts in col.items():
        fail += 1
        print(f"    ✗ {last}: {', '.join(firsts)}")
    if not col:
        print("    no surname does duty for two characters")
    if registry is not None:
        print(f"\n  CROSS-BOOK NAME REUSE  ({len(reused)} names already used elsewhere)")
        for n, books in reused.items():
            print(f"    ! {n} — previously used in: {', '.join(books)}")
        if not reused:
            print("    no name reused from a previous book")

    print(f"\n  {'FAIL' if fail else 'PASS'} — {fail} finding(s)\n")
    sys.exit(1 if fail else 0)

if __name__ == '__main__':
    main()
