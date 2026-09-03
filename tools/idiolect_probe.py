#!/usr/bin/env python3
"""
idiolect_probe.py — enforce the cross-book idiolect ledger on one chapter or one book.

The four-book audit (Cruelty-Free, Believer, Sentience, Talosapien; 353,750 words)
established that Otto Quill's involuntary constructions survive per-book fixes and
travel to the next book. This script is the regression test for those constructions.
It is designed to be run by a subagent that remembers nothing: every verdict is a
number against a budget, never a judgement.

    python3 tools/idiolect_probe.py CHAPTER.md            # one chapter
    python3 tools/idiolect_probe.py MANUSCRIPT_DIR        # whole book
    python3 tools/idiolect_probe.py DIR --baseline        # print measured rates only
    python3 tools/idiolect_probe.py DIR --json

Exit code 1 if any BAN fires or any RATION exceeds budget. Budgets are per 10,000
words. They are set BELOW the four-book measured median so a fifth book is forced
to route around the construction rather than reproduce it.

See method/06-idiolect-ledger.md for the evidence behind each entry.
"""
import argparse, json, os, re, sys, statistics
from collections import Counter

FRONTMATTER = re.compile(r'\A(?:---|\+\+\+)\s*\n.*?\n(?:---|\+\+\+)\s*\n', re.S)
HEADING     = re.compile(r'^#{1,6} .*$', re.M)
GLYPH       = re.compile(r'^\s*(?:[◆*_—\-~•·]{1,6}|\d+)\s*$', re.M)
SKIP        = re.compile(r'^(README|beat-sheet|bible|metadata|frontmatter|_body)', re.I)

# Material a document CITES is not material it COMMITS. Stripping fenced blocks,
# inline code, markdown blockquotes and tables keeps this script honest when it is
# pointed at prose that discusses constructions -- a style sheet, or these method
# documents. It is a partial fix: italics are not stripped, so an italicized
# quotation of a ban still gets charged for committing it -- five of the six current
# hits on the banned precision frame in method/ are exactly that. On a manuscript,
# which contains none of these forms, this stripping is a no-op.
CITED = [
    (re.compile(r'^```.*?^```', re.S | re.M), ''),   # fenced blocks
    (re.compile(r'`[^`\n]+`'), ' '),                 # inline code
    (re.compile(r'^\s*>.*$', re.M), ''),             # blockquotes
    (re.compile(r'^\s*\|.*$', re.M), ''),             # tables
]

def read_chapter(path, strip_cited=True):
    raw = open(path, encoding='utf-8').read()
    m = FRONTMATTER.match(raw)
    if m: raw = raw[m.end():]
    if strip_cited:
        for pat, rep in CITED:
            raw = pat.sub(rep, raw)
    body = GLYPH.sub('', HEADING.sub('', raw))
    return re.sub(r'\n{3,}', '\n\n', body).strip()

def load(target):
    if os.path.isfile(target):
        return [(os.path.basename(target), read_chapter(target))]
    out = []
    for f in sorted(os.listdir(target)):
        if not f.endswith('.md') or SKIP.match(f): continue
        b = read_chapter(os.path.join(target, f))
        if len(b.split()) >= 200: out.append((f, b))
    return out

ABBREV = re.compile(r'\b(?:Mr|Mrs|Ms|Dr|St|Prof|Sr|Jr|vs|etc|No|Lt|Capt|Sgt|e\.g|i\.e)\.$')
def sentences(text):
    text = re.sub(r'\s+', ' ', text).strip()
    out, buf = [], ''
    for piece in re.split(r'(?<=[.!?…])\s+', text):
        buf = (buf + ' ' + piece).strip() if buf else piece
        if ABBREV.search(buf): continue
        out.append(buf); buf = ''
    if buf: out.append(buf)
    return [s for s in out if s.strip()]

def words(t):      return re.findall(r"[A-Za-z][A-Za-z']*", t)
def paragraphs(t): return [p.strip() for p in re.split(r'\n\s*\n', t) if p.strip()]

# ---------------------------------------------------------------------------
# THE LEDGER. verdict: BAN (budget 0) | RATION (numeric budget) | KEEP (report only)
# `measured` is the four-book range in instances per 10k words, for provenance.
# ---------------------------------------------------------------------------
LEDGER = [
 # id, label, regex, verdict, budget/10k, measured-range-across-4-books
 ('L01','simile-frame: "the way you/one/a X"',
   r'\bthe way (?:you|one|a\b|an\b)', 'RATION', 6.0, '7.8-15.6'),
 ('L02','simile-frame: "the way he/she/they/it X"',
   r'\bthe way (?:he|she|they|it|we|i)\b', 'RATION', 3.0, '3.1-11.4'),
 ('L03','attribution-gloss fragment after a "said" line ("Not a question.")',
   None, 'RATION', 3.0, '6.0-10.0'),
 ('L04','EXACT BANNED SENTENCE: "Not a question."',
   r'(?:^|(?<=[.!?…] ))Not a question\.', 'BAN', 0.0, '10 uses, 4/4 books'),
 ('L05','negate-then-correct opener ("It was not…", "He did not…")',
   r"(?:^|(?<=[.!?…] ))(?:It|That|This|He|She|They|There|I|We|You)\s+(?:was|is|were|are|had|did|do|does|would|could|can|will)\s*n[o']?t\b",
   'RATION', 12.0, '19.7-38.4'),
 ('L06','negate-then-correct PAIR (negative sentence then "It was Y.")',
   None, 'RATION', 4.0, '7.7-15.9'),
 ('L07','hard cut "Not a X. Capital…"',
   r'\b[Nn]ot (?:a|an|the)?\s*\w+\.\s+[A-Z]', 'RATION', 8.0, '11.8-26.9'),
 ('L08','hedge "not quite a X"',
   r'\bnot quite\b', 'RATION', 1.0, '0.2-2.6'),
 ('L09','precision frame "want/try to be precise|honest|exact|careful|clear about"',
   r'\b(?:want|wanted|need|needed|try|tried|trying|am|is|was|be)\w*\s+(?:to\s+be\s+)?(?:precise|honest|exact|clear|careful|accurate|fair|truthful|specific|plain|modest)\b\s*(?:about|here|with|,|\.)',
   'BAN', 0.0, '1.3-5.1 — banned in Sentience, reappeared with new adjectives'),
 ('L10','summarizing close "the whole of it / all of it"',
   r'\bthe whole of\b|\ball of it\b', 'RATION', 1.0, '1.7-7.0'),
 ('L11','abstraction "a/the shape (of)"',
   r'\b(?:a|the|its|his|her|that|this) shapes?\b', 'RATION', 2.0, '1.5-6.2'),
 ('L12','abstraction-reach "thing/things"',
   r'\bthings?\b', 'RATION', 40.0, '41.6-81.1'),
 ('L13','abstraction-reach "something/nothing/anything/everything"',
   r'\b(?:some|no|any|every)thing\b', 'RATION', 35.0, '35.2-69.3'),
 ('L14','causal reflex "because"',
   r'\bbecause\b', 'RATION', 28.0, '28.1-52.1'),
 ('L15','superlative-abstract "the only/most X thing"',
   r'\bthe (?:only|most \w+|first|last|one|other|whole|real|true|worst|best) thing\b',
   'RATION', 4.0, '4.1-11.9'),
 ('L16','"the only X" totalizer',
   r'\bthe only\b', 'RATION', 8.0, '5.7-15.5'),
 ('L17','deferred appositive "which is/was …"',
   r'\bwhich (?:is|was|were|are)\b', 'RATION', 6.0, '3.3-15.5'),
 ('L18','self-gloss "which is to say"',
   r'\bwhich (?:is|was) to say\b', 'RATION', 0.5, '0.3-2.1'),
 ('L19','self-adjudicating tag "which was true"',
   r'\b(?:which|and it) was (?:true|a lie|not true)\b', 'RATION', 0.5, '0.2-1.8'),
 ('L20','the-distinction "the difference/gap between"',
   r'\bthe (?:difference|gap|distance|space|distinction) between\b', 'RATION', 1.0, '1.2-2.2'),
 ('L21','epistemic simile "the way a body/hand/person knows"',
   r'\bthe way (?:a|an|the|you|one|he|she|they|we|i|his|her|some\w*)\s*\w*\s*(?:know|knew|knows)\b',
   'RATION', 0.5, '0.3-1.2'),
 ('L22','abstraction-as-object "set/laid/put it down"',
   r'\b(?:set|lay|laid|put) (?:it|them|that|the \w+) down\b', 'RATION', 2.0, '1.9-4.8'),
 ('L23','resolve marker "…anyway"',
   r'\banyway\b', 'RATION', 2.0, '2.5-6.0'),
 ('L24','"exactly/precisely" as intensifier',
   r'\b(?:exactly|precisely)\b', 'RATION', 6.0, '6.4-11.8'),
 ('L25','sentence-initial "Not/No/Never/Nothing" fragment',
   r'(?:^|(?<=[.!?…] ))(?:Not|No|Never|Nothing|Nobody)\b[^.!?]{0,50}\.', 'RATION', 6.0, '7.8-10.9'),
 ('L26','single-word italic emphasis',
   r'(?<!\*)\*\w+[.,!?]?\*(?!\*)', 'RATION', 12.0, '11.1-27.0'),
 ('L27','em dash',
   r'—', 'KEEP', None, '53.9-91.5'),
 ('L28','"said" as attribution',
   r'\b(?:said|says)\b', 'KEEP', None, '41.0-71.4'),
]

# ---------------------------------------------------------------------------
# BASKETS. The load-bearing discovery of the four-book audit: individual members
# of a construction family swing 2-20x between books while the FAMILY TOTAL is
# near-constant. `thing` rose 1.9x across the four books while `something` fell
# 5.4x and the six-member abstraction basket held at 1210-1459/100k (1.21x).
# Banning a member does not remove the habit; it moves the habit to a synonym.
# Therefore the budget that matters is the basket budget. Set below the four-book
# minimum so the fifth book has to reach for something that is not in the basket.
# ---------------------------------------------------------------------------
BASKETS = [
 ('B1', 'abstraction-reach', 1000.0, '1209.8-1459.4', [
   r'\bthings?\b', r'\bsomething\b', r'\banything\b', r'\bnothing\b',
   r'\beverything\b', r'\b(?:kind|sort) of\b']),
 ('B2', 'precision-claim', 300.0, '377.1-728.0', [
   r'\bprecis\w+\b', r'\bexact\w*\b', r'\bhonest\w*\b', r'\bcareful\w*\b',
   r'\bclear\w*\b', r'\baccura\w+\b', r'\btru(?:e|th)\b']),
 ('B3', 'totalizer', 110.0, '140.3-269.6', [
   r'\bthe whole of\b', r'\ball of it\b', r'\bthe only\b', r'\bentirely\b',
   r'\bcompletely\b', r'\bthe rest of\b']),
 ('B4', 'simile-frame', 250.0, '310.4-536.5', [
   r'\bthe way\b', r'\blike (?:a|an|the)\b', r'\bas (?:if|though)\b', r'\ba kind of\b']),
 ('B5', 'negation-scaffold', 1000.0, '1162.0-1887.3', [r"\b(?:not|n't)\b"]),
]

# structural checks that are not regex-countable
def structural(chapters):
    out = {}
    firsts, lasts, all_lens, para_pairs = [], [], [], []
    for name, body in chapters:
        ss = sentences(body)
        if not ss: continue
        firsts.append((name, ss[0])); lasts.append((name, ss[-1]))
        for p in paragraphs(body):
            L = [len(words(s)) for s in sentences(p)]
            all_lens += L
            for i in range(len(L)-1): para_pairs.append((L[i], L[i+1]))
    if not all_lens: return out
    srt = sorted(all_lens)
    q = lambda p: srt[min(int(len(srt)*p), len(srt)-1)]
    out['sentence_mean']   = round(statistics.mean(all_lens), 1)
    out['sentence_median'] = q(.50)
    out['sentence_p90']    = q(.90)
    out['pct_le5']         = round(100*sum(1 for x in all_lens if x <= 5)/len(all_lens), 1)
    out['pct_ge30']        = round(100*sum(1 for x in all_lens if x >= 30)/len(all_lens), 1)
    # CADENCE ARCHITECTURE: within-paragraph lag-1 autocorrelation.
    # All four books measure |r| < 0.08 — indistinguishable from shuffling the
    # sentence lengths inside each paragraph. Prose with deliberate cadence does not.
    if para_pairs:
        m = statistics.mean(all_lens); v = statistics.pvariance(all_lens) or 1
        out['cadence_lag1_r'] = round(
            sum((a-m)*(b-m) for a, b in para_pairs)/len(para_pairs)/v, 3)
        lo = [p for p in para_pairs if p[0] >= 25]
        out['P_short_after_long'] = round(100*sum(1 for p in lo if p[1] <= 8)/len(lo), 1) if lo else 0
    # CHAPTER OPEN/CLOSE MONOTONY
    n = len(lasts) or 1
    out['pct_closes_with_and_chain'] = round(
        100*sum(1 for _, s in lasts if len(re.findall(r',\s*and\b', s)) >= 2)/n, 1)
    out['pct_closes_on_negation'] = round(
        100*sum(1 for _, s in lasts if re.search(r"\b(?:not|n't|no|never|nothing|no one|nobody|neither)\b", s, re.I))/n, 1)
    out['pct_opens_on_dialogue'] = round(
        100*sum(1 for _, s in firsts if s.lstrip().startswith(('"', '“')))/n, 1)
    out['pct_opens_state_of_affairs'] = round(
        100*sum(1 for _, s in firsts if re.match(r'^[^.]{0,60}\b(?:was|were|had|is|are|has)\b', s))/n, 1)
    out['pct_paragraphs_1_sentence'] = None
    out['exclamation_marks'] = sum(body.count('!') for _, body in chapters)
    out['question_marks'] = sum(body.count('?') for _, body in chapters)
    return out

# Structural budgets: [lo, hi] or ('max', x) / ('min', x). Four-book actuals in comment.
STRUCT_RULES = {
 # the four books: 0.039 / -0.031 / -0.055 / 0.040. Anything in that band means the
 # sentence order carries no information — a cadence, not a defect you can see.
 'cadence_lag1_r':            ('outside', -0.08, 0.08, 'four books all |r|<0.08 = no cadence architecture'),
 'sentence_median':           ('range', 12, 20,  'four books all landed 10-11'),
 'pct_le5':                   ('max', 20.0,      'four books 23.5-26.4%'),
 'pct_closes_with_and_chain': ('max', 15.0,      'four books 5.6-47.1%'),
 'pct_closes_on_negation':    ('max', 30.0,      'four books 19.4-58.8%'),
 'pct_opens_on_dialogue':     ('min', 10.0,      'four books 0.0% — 138/138 chapters'),
 'pct_opens_state_of_affairs':('max', 35.0,      'four books 41.2-58.8%'),
}

def count_L03(chapters):
    FIN = re.compile(r'\b(?:is|are|was|were|be|been|am|has|have|had|do|does|did|will|would|can|could|should|must|said|says|went|came|stood|sat|looked|knew|felt|took|put|made)\b', re.I)
    SAID = re.compile(r'\b(?:said|says|asked|answered|replied|told)\b[^.!?]*[.!?]"?$')
    n = 0
    for _, body in chapters:
        ss = sentences(body)
        for i in range(len(ss)-1):
            if SAID.search(ss[i]):
                nx = ss[i+1].strip()
                if len(words(nx)) <= 6 and not FIN.search(nx) and not nx.startswith(('"', '“')):
                    n += 1
    return n

def count_L06(chapters):
    NEG = re.compile(r"\b(?:was|were|is|are|had|did|do|does|would|could)\s*n[o']?t\b|\bnot\b")
    COR = re.compile(r'^(?:It|That|This|He|She|They|There|What)\s+(?:was|is|were|are)\b')
    n = 0
    for _, body in chapters:
        ss = sentences(body)
        for i in range(len(ss)-1):
            if NEG.search(ss[i]) and len(words(ss[i])) <= 25 and COR.match(ss[i+1]):
                n += 1
    return n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('target')
    ap.add_argument('--baseline', action='store_true', help='report rates, do not judge')
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()

    chapters = load(a.target)
    if not chapters:
        print(f'no chapters found in {a.target}', file=sys.stderr); return 2
    text = ' '.join(b for _, b in chapters)
    nw = len(words(text)) or 1
    per10k = lambda c: 10000.0 * c / nw

    rows, violations = [], []
    for lid, label, pat, verdict, budget, measured in LEDGER:
        c = (count_L03(chapters) if lid == 'L03'
             else count_L06(chapters) if lid == 'L06'
             else len(re.findall(pat, text)))
        r = round(per10k(c), 2)
        over = (budget is not None and not a.baseline and r > budget)
        if over: violations.append((lid, label, r, budget))
        rows.append({'id': lid, 'label': label, 'verdict': verdict, 'count': c,
                     'per_10k': r, 'budget': budget, 'four_book_range': measured,
                     'over': over})

    basket_rows = []
    for bid, name, budget, measured, pats in BASKETS:
        c = sum(len(re.findall(p, text, re.I)) for p in pats)
        rate = round(100000.0 * c / nw, 1)
        over = (not a.baseline and rate > budget)
        if over: violations.append((bid, 'BASKET ' + name, rate, budget))
        basket_rows.append({'id': bid, 'name': name, 'per_100k': rate,
                            'budget': budget, 'four_book_range': measured, 'over': over})

    st = structural(chapters)
    st_bad = []
    # Chapter-open/close shape is only meaningful over a run of chapters; on a single
    # chapter 1/1 reads as 100%. A memoryless subagent checking one chapter gets the
    # per-10k budgets and the cadence test, not the corpus-shape rules.
    CORPUS_ONLY = {'pct_closes_with_and_chain', 'pct_closes_on_negation',
                   'pct_opens_on_dialogue', 'pct_opens_state_of_affairs'}
    if not a.baseline:
        for k, rule in STRUCT_RULES.items():
            if k in CORPUS_ONLY and len(chapters) < 5: continue
            v = st.get(k)
            if v is None: continue
            kind = rule[0]
            if kind == 'range' and not (rule[1] <= v <= rule[2]):
                st_bad.append((k, v, f'want {rule[1]}-{rule[2]}', rule[3]))
            elif kind == 'max' and v > rule[1]:
                st_bad.append((k, v, f'want <= {rule[1]}', rule[2]))
            elif kind == 'min' and v < rule[1]:
                st_bad.append((k, v, f'want >= {rule[1]}', rule[2]))
            elif kind == 'outside' and rule[1] <= v <= rule[2]:
                st_bad.append((k, v, f'want outside {rule[1]}..{rule[2]}', rule[3]))

    if a.json:
        print(json.dumps({'target': a.target, 'words': nw, 'probes': rows, 'baskets': basket_rows,
                          'structure': st, 'violations': len(violations)+len(st_bad)}, indent=2))
    else:
        print(f'{a.target}  —  {len(chapters)} chapter(s), {nw:,} words\n')
        print(f'{"id":5}{"construction":58}{"n":>6}{"/10k":>8}{"budget":>8}{"4-book":>14}  ')
        for r in rows:
            flag = ' !! OVER' if r['over'] else ('  BAN-CLEAR' if r['verdict'] == 'BAN' and r['count'] == 0 else '')
            b = '-' if r['budget'] is None else f"{r['budget']:.1f}"
            print(f"{r['id']:5}{r['label'][:56]:58}{r['count']:>6}{r['per_10k']:>8}{b:>8}{" "+r["four_book_range"]:>16}{flag}")
        print(f'\nBASKETS (per 100k words) — budget the FAMILY, not the member')
        for r in basket_rows:
            print(f"{r['id']:5}{r['name'][:56]:58}{'':>6}{r['per_100k']:>8}{r['budget']:>8}"
                  f"{' '+r['four_book_range']:>16}{' !! OVER' if r['over'] else ''}")
        print('\nSTRUCTURE')
        for k, v in st.items():
            if v is None: continue
            print(f'  {k:32} {v}')
        if a.baseline:
            print('\n(baseline mode — no verdicts)')
        else:
            print()
            for lid, label, r, b in violations:
                print(f'  OVER BUDGET  {lid} {label}: {r}/10k > {b}/10k')
            for k, v, want, why in st_bad:
                print(f'  STRUCTURE    {k} = {v} ({want}) — {why}')
            total = len(violations) + len(st_bad)
            print(f'\n{total} violation(s).' if total else '\nclean.')
    return 1 if (not a.baseline and (violations or st_bad)) else 0

if __name__ == '__main__':
    sys.exit(main())
