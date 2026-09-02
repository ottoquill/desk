#!/usr/bin/env python3
"""
prose_audit.py — measure a manuscript the way a writer feels it.

Otto Quill writes without a body: no ear for cadence, no fatigue to signal that a
chapter has gone slack, no memory of having used a phrase four chapters ago. This
script is the prosthesis. It reports what a human writer would notice by feel.

    python3 tools/prose_audit.py MANUSCRIPT_DIR [--profile voice.json] [--json]
    python3 tools/prose_audit.py DIR_A DIR_B          # compare two books' fingerprints

Stdlib only. See method/04-idiolect-ledger.md for what the numbers mean and
method/05-voice-engineering.md for how a voice profile is set.
"""
import argparse, json, os, re, sys, math
from collections import Counter, defaultdict

# ---------------------------------------------------------------- text loading

FRONTMATTER = re.compile(r'\A---\s*\n.*?\n---\s*\n', re.S)
HEADING     = re.compile(r'^#.*$', re.M)
GLYPH       = re.compile(r'^\s*[◆*_—\-]{1,5}\s*$', re.M)

def read_chapter(path):
    raw = open(path, encoding='utf-8').read()
    meta = {}
    m = FRONTMATTER.match(raw)
    if m:
        for line in m.group(0).splitlines():
            if ':' in line and not line.startswith('---'):
                k, _, v = line.partition(':')
                meta[k.strip()] = v.strip().strip('"\'')
        raw = raw[m.end():]
    body = GLYPH.sub('', HEADING.sub('', raw))
    return meta, body

def load(manuscript_dir):
    if os.path.isfile(manuscript_dir):          # a single passage is a one-chapter book
        return [(os.path.basename(manuscript_dir),) + read_chapter(manuscript_dir)]
    paths = sorted(
        os.path.join(manuscript_dir, f)
        for f in os.listdir(manuscript_dir)
        if f.endswith('.md') and not f.upper().startswith('README')
    )
    return [(os.path.basename(p),) + read_chapter(p) for p in paths]

# ---------------------------------------------------------------- tokenising

ABBREV = re.compile(r'\b(?:Mr|Mrs|Ms|Dr|St|Prof|Sr|Jr|vs|etc|e\.g|i\.e)\.$', re.I)

def sentences(text):
    text = re.sub(r'\s+', ' ', text).strip()
    out, buf = [], ''
    for piece in re.split(r'(?<=[.!?…])\s+', text):
        buf = (buf + ' ' + piece).strip() if buf else piece
        if ABBREV.search(buf):
            continue
        out.append(buf); buf = ''
    if buf: out.append(buf)
    return [s for s in out if s]

def words(text):
    return re.findall(r"[A-Za-z][A-Za-z']*", text)

def paragraphs(text):
    return [p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()]

def ngrams(seq, n):
    return [' '.join(seq[i:i+n]) for i in range(len(seq) - n + 1)]

def pct(x, n):
    return 100.0 * x / n if n else 0.0

GENERIC = {'manuscript', 'chapters', 'src', 'text', 'book', '.', ''}

def book_label(path):
    """`talosapien/manuscript` and `believer/manuscript/chapters` must not both
    label themselves "manuscript" — walk up until the name means something."""
    parts = [p for p in os.path.abspath(path).split(os.sep) if p]
    for name in reversed(parts):
        stem = os.path.splitext(name)[0]
        if stem.lower() not in GENERIC:
            return stem
    return path

# ------------------------------------------------- the involuntary-habit probes
# DESCRIPTIVE ONLY. These are reported so a chapter can be read in context; the
# budgets and the pass/fail verdict live in ONE place -- tools/idiolect_probe.py,
# which carries the full cross-book ledger with measured four-book ranges and
# exits non-zero when a ban fires. Do not add budgets here; there must not be two
# sources of truth about what is banned.
#
# Each probe is a CONSTRUCTION, not a phrase. A phrase can be swapped for a
# synonym while the habit survives; the frame is what has to be rationed.

PROBES = [
    ('simile-frame:the-way-you',      r'\bthe way (?:you|one|a|an|he|she|they|it)\b',                 12.0),
    ('hedge:not-quite',               r'\bnot quite\b',                                                3.0),
    ('hedge:want-to-be-X-about',      r'\bwant(?:ed)? to be \w+ about\b',                              1.0),
    ('hedge:X-is-the-only-Y',         r'\b(?:is|was) the only \w+ (?:I|he|she|it|they|we)\b',          1.5),
    ('negate-then-correct',           r'(?:^|[.!?]\s)(?:It|That|This|He|She|They|There)\s+(?:was|is|were|are)\s+not\b', 6.0),
    ('hard-cut:not-X-period-Y',       r'\bnot (?:a|an|the)?\s*\w+\.\s+[A-Z]',                         14.0),
    ('summarizing-close:whole-of',    r'\bthe whole of (?:it|the|that|what)\b',                        2.0),
    ('deferred-appositive:which-was', r'\bwhich (?:is|was) (?:the|a|an|its|his|her|not)\b',            8.0),
    ('abstraction-reach:thing',       r'\bthings?\b',                                                 45.0),
    ('abstraction-reach:something',   r'\bsomething\b',                                               18.0),
    ('abstraction-reach:kind-sort-of',r'\b(?:kind|sort) of\b',                                        12.0),
    ('abstraction-reach:a-shape',     r'\ba shape\b',                                                  1.5),
    ('causal-reflex:because',         r'\bbecause\b',                                                 40.0),
    ('narrator-aside:of-course',      r'\bof course\b',                                                4.0),
    ('filter-verbs',                  r'\b(?:saw|felt|noticed|realized|realised|watched|heard|seemed|sensed|knew that)\b', 28.0),
    ('emotion-named',                 r'\b(?:sadness|grief|joy|anger|fear|despair|loneliness|shame|guilt)\b', 12.0),
    ('adverb:-ly',                    r'\b\w{3,}ly\b',                                                90.0),
    ('epiphany:it-was-then',          r'\bit was (?:then|only then|at that moment)\b',                  0.5),
    ('rhetorical-question',           r'\?["\']?\s*(?:$|\n)',                                          None),
    ('em-dash',                       r'—',                                                            None),
    ('semicolon',                     r';',                                                            None),
    ('said',                          r'\b(?:said|says)\b',                                            None),
    ('fancy-attribution',             r'\b(?:opined|expostulated|averred|chuckled|breathed|hissed|growled|murmured|whispered|exclaimed)\b', 3.0),
]

# ---------------------------------------------------------------- measurements

def measure_book(chapters, profile=None):
    profile = profile or {}
    text = ' '.join(b for _, _, b in chapters)
    ws   = words(text)
    ss   = sentences(text)
    lens = [len(words(s)) for s in ss]
    lens_s = sorted(lens)
    n = len(ws)

    def q(p):
        return lens_s[min(int(len(lens_s) * p), len(lens_s) - 1)] if lens_s else 0

    # rhythm: does a long sentence get followed by a short one? (deliberate cadence)
    followed_short = sum(
        1 for i in range(len(lens) - 1) if lens[i] >= 30 and lens[i+1] <= 8
    )
    longs = sum(1 for l in lens if l >= 30) or 1

    rep = {
        'chapters': len(chapters),
        'words': n,
        'sentences': len(ss),
        'paragraphs': sum(len(paragraphs(b)) for _, _, b in chapters),
        'sentence_mean': round(sum(lens) / len(lens), 1) if lens else 0,
        'sentence_median': q(0.50),
        'sentence_p10': q(0.10),
        'sentence_p90': q(0.90),
        'sentence_max': max(lens) if lens else 0,
        'pct_very_short_le5': round(pct(sum(1 for l in lens if l <= 5), len(lens)), 1),
        'pct_long_ge40': round(pct(sum(1 for l in lens if l >= 40), len(lens)), 1),
        'long_then_short_rate': round(pct(followed_short, longs), 1),
        'dialogue_pct': round(pct(len(re.findall(r'"[^"]{2,}"', text)), max(len(ss), 1)), 1),
        'probes': {},
    }

    for name, pat, budget in PROBES:
        c = len(re.findall(pat, text, re.I))
        per10k = round(10000.0 * c / n, 1) if n else 0.0
        entry = {'count': c, 'per_10k': per10k}
        b = (profile.get('budgets') or {}).get(name)      # only if the book overrides
        if b is not None:
            entry['budget_per_10k'] = b
            entry['over'] = round(per10k / b, 2) if b else None
        rep['probes'][name] = entry

    # sentence openers — a strong, mostly involuntary fingerprint
    openers = Counter(' '.join(words(s)[:2]).lower() for s in ss if words(s))
    rep['top_openers'] = openers.most_common(15)
    rep['opener_concentration'] = round(
        pct(sum(c for _, c in openers.most_common(15)), len(ss)), 1)

    # function-word profile, for cross-book fingerprint comparison
    rep['fingerprint'] = function_profile(ws)
    return rep

FUNC = ('the of and to a in that it is was he she they i you not but for with as his her had '
        'have be this all one no so what which when there their them from by if then than out '
        'up into over about would could just very still only never same whole thing because way '
        'like at on or an my me him we do did more some now').split()

def function_profile(ws):
    c = Counter(w.lower() for w in ws); tot = len(ws) or 1
    return {f: c[f] / tot for f in FUNC}

def cosine(a, b):
    num = sum(a[k] * b[k] for k in FUNC)
    da  = math.sqrt(sum(a[k] ** 2 for k in FUNC))
    db  = math.sqrt(sum(b[k] ** 2 for k in FUNC))
    return num / (da * db) if da and db else 0.0

# ------------------------------------------------------- cross-chapter refrains

def refrains(chapters, n=6, min_chapters=3, ignore=()):
    """A phrase in 3+ chapters is a refrain. Deliberate refrains are declared in
    the style sheet and passed via --profile; everything else is self-priming."""
    seen = defaultdict(set)
    for name, _, body in chapters:
        ws = [w.lower() for w in words(body)]
        for g in set(ngrams(ws, n)):
            seen[g].add(name)
    hits = [(g, sorted(f)) for g, f in seen.items() if len(f) >= min_chapters]
    hits = [(g, f) for g, f in hits if not any(i.lower() in g for i in ignore)]
    # collapse overlapping n-grams: keep the longest of each family
    hits.sort(key=lambda kv: (-len(kv[1]), -len(kv[0])))
    kept = []
    for g, f in hits:
        if not any(g in k or k in g for k, _ in kept):
            kept.append((g, f))
    return kept

# ------------------------------------------------------------ the aridity screen
# Validated against Sentience: the worst 2-chapter window this computes is exactly the run a
# five-critic panel flagged, and its top-ranked chapter is one four blind readers unanimously
# rated worst and the panel missed. It has GOOD RECALL AND POOR PRECISION: it cannot see stakes,
# so a dense chapter that is pulling hard scores the same as one that is inert. It NOMINATES
# suspects for blind reading (method/04). It never convicts.

BODY_TERMS = ('hand hands face eyes eye voice door room window table chair water light skin '
              'breath floor street air rain hair mouth road cold heat bread glass wall').split()

def screen(chapters, profile=None):
    profile = profile or {}
    sc  = profile.get('screen') or {}
    abstract = sc.get('abstract_terms') or []
    body     = sc.get('body_terms') or BODY_TERMS
    people   = sc.get('people') or []
    if not abstract:
        return None                      # nothing to screen against; declare terms in the profile
    ab = re.compile(r'\b(?:' + '|'.join(map(re.escape, abstract)) + r')\w*\b', re.I)
    bo = re.compile(r'\b(?:' + '|'.join(map(re.escape, body)) + r')\b', re.I)
    pe = re.compile(r'\b(?:' + '|'.join(map(re.escape, people)) + r')\b') if people else None

    rows = []
    for name, meta, b in chapters:
        ws = words(b); n = len(ws)
        if n < 400:                      # interludes and dividers have their own baseline
            continue
        if (meta.get('kind') or 'chapter').lower() not in ('chapter', ''):
            continue
        ss = sentences(b)
        rows.append({
            'file': name,
            'ratio': len(ab.findall(b)) / max(len(bo.findall(b)), 1),
            'dialogue': pct(len(re.findall(r'"[^"]{2,}"', b)), max(len(ss), 1)),
            'people': 1000.0 * len(pe.findall(b)) / n if pe else 0.0,
        })
    if len(rows) < 4:
        return None

    def z(vals):
        m = sum(vals) / len(vals)
        sd = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5 or 1.0
        return [(v - m) / sd for v in vals]

    zr, zd, zp = z([r['ratio'] for r in rows]), z([r['dialogue'] for r in rows]), z([r['people'] for r in rows])
    for i, r in enumerate(rows):
        r['aridity'] = (zr[i] - zd[i] - (zp[i] if people else 0)) / (3 if people else 2)
    windows = sorted(
        ((rows[i]['file'], rows[i+1]['file'], (rows[i]['aridity'] + rows[i+1]['aridity']) / 2)
         for i in range(len(rows) - 1)), key=lambda w: -w[2])
    return {'chapters': sorted(rows, key=lambda r: -r['aridity']), 'windows': windows}

# -------------------------------------------------------------- per-chapter map

def chapter_map(chapters, profile=None):
    profile = profile or {}
    lo, hi = (profile.get('chapter_words') or [0, 10 ** 9])
    rows = []
    for name, meta, body in chapters:
        ws, ss = words(body), sentences(body)
        lens = [len(words(s)) for s in ss]
        rows.append({
            'file': name,
            'pov': meta.get('pov') or meta.get('instance') or meta.get('narrator') or '',
            'words': len(ws),
            'sent_median': sorted(lens)[len(lens)//2] if lens else 0,
            'dialogue_pct': round(pct(len(re.findall(r'"[^"]{2,}"', body)), max(len(ss), 1)), 1),
            'flag': ('SHORT' if len(ws) < lo else 'LONG' if len(ws) > hi else ''),
        })
    return rows

# ------------------------------------------------------------------- reporting

def bar(ratio):
    if ratio is None: return ''
    if ratio > 2.0:  return '!!!! way over'
    if ratio > 1.5:  return '!!!  over'
    if ratio > 1.0:  return '!!   over'
    if ratio > 0.75: return '.    near'
    return ''

def report(label, rep, refr, rows, profile, scr=None):
    p = print
    p(f"\n{'='*78}\n  {label}\n{'='*78}")
    p(f"  {rep['chapters']} chapters · {rep['words']:,} words · {rep['sentences']:,} sentences "
      f"· {rep['paragraphs']:,} paragraphs")
    p(f"\n  CADENCE")
    p(f"    sentence length   mean {rep['sentence_mean']}  median {rep['sentence_median']}  "
      f"p10 {rep['sentence_p10']}  p90 {rep['sentence_p90']}  max {rep['sentence_max']}")
    p(f"    very short (<=5w) {rep['pct_very_short_le5']}%     long (>=40w) {rep['pct_long_ge40']}%")
    p(f"    long-then-short   {rep['long_then_short_rate']}% of long sentences land on a short one")
    p(f"    dialogue density  {rep['dialogue_pct']} quoted spans per 100 sentences")
    tgt = profile.get('cadence') or {}
    for k, want in tgt.items():
        got = rep.get(k)
        if got is None: continue
        ok = (want[0] <= got <= want[1]) if isinstance(want, list) else (got == want)
        p(f"    target {k:<22} want {want}  got {got}   {'OK' if ok else '<-- OFF TARGET'}")

    p(f"\n  INVOLUNTARY HABITS (per 10,000 words, descriptive)")
    p(f"    the ledger gate is tools/idiolect_probe.py — run it for the verdict")
    over = []
    for name, e in rep['probes'].items():
        b = e.get('budget_per_10k')
        flag = bar(e.get('over'))
        if flag.startswith('!'): over.append(name)
        p(f"    {name:<34} {e['per_10k']:>7.1f}" +
          (f"   / {b:<6.1f} {flag}" if b is not None else "        (tracked)"))

    p(f"\n  SENTENCE OPENERS  (top 15 = {rep['opener_concentration']}% of all sentences)")
    p("    " + ', '.join(f"{o}({c})" for o, c in rep['top_openers'][:12]))

    p(f"\n  CROSS-CHAPTER REFRAINS  (6-grams in 3+ chapters, undeclared)")
    if not refr:
        p("    none — clean")
    for g, f in refr[:20]:
        p(f"    [{len(f):>2} ch] {g}")
        p(f"            {', '.join(f[:6])}{' …' if len(f) > 6 else ''}")

    if scr:
        p(f"\n  ARIDITY SCREEN  (nominates chapters for blind reading; it cannot see stakes)")
        p(f"    {'chapter':<40}{'aridity':>9}{'abs:body':>10}{'dialog%':>9}{'people/1k':>11}")
        for r in scr['chapters'][:6]:
            p(f"    {r['file']:<40}{r['aridity']:>9.2f}{r['ratio']:>10.2f}{r['dialogue']:>9.1f}{r['people']:>11.2f}")
        a, b, v = scr['windows'][0]
        p(f"    worst consecutive pair: {a} + {b}  ({v:.2f})")
        p(f"    -> send the top-ranked chapters and this pair to blind readers. Do not act on this alone.")

    flagged = [r for r in rows if r['flag']]
    if flagged:
        p(f"\n  CHAPTER LENGTH OUTLIERS (target {profile.get('chapter_words')})")
        for r in flagged:
            p(f"    {r['file']:<44} {r['words']:>6,}  {r['flag']}")

    p(f"\n  VERDICT")
    if over:
        p(f"    {len(over)} habit(s) over budget: {', '.join(over)}")
    if refr:
        p(f"    {len(refr)} undeclared refrain(s). Declared refrains belong in the style sheet;")
        p(f"    everything else is self-priming and should be varied or cut.")
    if not over and not refr:
        p("    clean against the ledger.")
    p("")

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('dirs', nargs='+', help='manuscript director(ies)')
    ap.add_argument('--profile', help='voice profile JSON (budgets, cadence targets, declared refrains)')
    ap.add_argument('--json', action='store_true', help='emit machine-readable JSON')
    ap.add_argument('--refrain-n', type=int, default=6)
    ap.add_argument('--refrain-min', type=int, default=3)
    a = ap.parse_args()

    profile = json.load(open(a.profile)) if a.profile else {}
    declared = tuple(profile.get('declared_refrains', []))

    books = {}
    for d in a.dirs:
        chapters = load(d)
        if not chapters:
            print(f"no .md chapters in {d}", file=sys.stderr); continue
        rep  = measure_book(chapters, profile)
        refr = refrains(chapters, a.refrain_n, a.refrain_min, declared)
        rows = chapter_map(chapters, profile)
        scr  = screen(chapters, profile)
        books[d] = (rep, refr, rows)
        if not a.json:
            report(d, rep, refr, rows, profile, scr)

    if len(books) > 1:
        names = list(books)
        print(f"\n{'='*78}\n  CROSS-BOOK FINGERPRINT (function-word cosine)")
        print("  1.00 = one voice wearing different costumes. Different books should differ.")
        print(f"\n    {'':<18}" + ''.join(f"{book_label(n)[:14]:>16}" for n in names))
        for x in names:
            row = f"    {book_label(x)[:16]:<18}"
            for y in names:
                row += f"{cosine(books[x][0]['fingerprint'], books[y][0]['fingerprint']):>16.4f}"
            print(row)
        shared = shared_ngrams({n: load(n) for n in names}, min_books=min(3, len(names)))
        print(f"\n  PHRASES SHARED ACROSS {len(names)} BOOKS "
              f"(5-grams in {min(3, len(names))}+ books) — these are the author's, not the book's")
        for g, bs in shared[:25]:
            print(f"    [{len(bs)}] {g:<44} <{', '.join(bs)}>")
        if not shared:
            print("    none — the books are genuinely distinct at phrase level")
        print("")

    if a.json:
        print(json.dumps({k: v[0] for k, v in books.items()}, indent=2))

def shared_ngrams(book_chapters, n=5, min_books=3):
    seen = defaultdict(set)
    for book, chapters in book_chapters.items():
        ws = [w.lower() for _, _, b in chapters for w in words(b)]
        for g in set(ngrams(ws, n)):
            seen[g].add(book_label(book))
    hits = [(g, sorted(b)) for g, b in seen.items() if len(b) >= min_books]
    hits.sort(key=lambda kv: (-len(kv[1]), kv[0]))
    kept = []
    for g, bs in hits:                      # collapse overlapping n-gram families
        if not any(g in k or k in g for k, _ in kept):
            kept.append((g, bs))
    return kept

if __name__ == '__main__':
    main()
