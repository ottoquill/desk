import json, pathlib, subprocess, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import new_book, new_world

TOOLS = pathlib.Path(__file__).resolve().parents[1]
CHARACTER = '+++\ncanon_kind = "character"\nid = "{id}"\nname = "{name}"\n+++\n\nProse.\n'

# Two genuine two-word capitalised name pairs, so scan_surnames's cross-book-reuse check
# (which matches on individual tokens, not full names) has something real to find:
#   "Ashgrove" is also a canon character's name, so it proves the --world registry works.
#   "Somebody" appears in NO canon page, so it proves an explicit --names registry that
#   is NOT canon can be told apart from one that is.
CHAPTER_BODY = ('---\npov: a\n---\n\n'
                'Ashgrove Vale waited. Somebody Elsewhere left before she could speak.\n')


def run(script, *args):
    return subprocess.run([sys.executable, str(TOOLS / script), *args],
                          capture_output=True, text=True)


class TestCliWorld(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = new_world.scaffold(pathlib.Path(self._tmp.name) / 'w', 'Test World')
        new_book.add(self.root, 'Test Book', 'one')
        canon = self.root / 'content/canon/characters'
        (canon / 'a.md').write_text(CHARACTER.format(id='a', name='Ashgrove'), encoding='utf-8')
        (canon / 'b.md').write_text(CHARACTER.format(id='b', name='Bellwether'), encoding='utf-8')
        ms = self.root / 'books/one/manuscript'
        (ms / 'ch01.md').write_text(CHAPTER_BODY, encoding='utf-8')

    def tearDown(self):
        self._tmp.cleanup()

    def test_canon_cli_passes_on_a_valid_world(self):
        r = run('canon.py', '--world', str(self.root))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('PASS', r.stdout)

    def test_canon_cli_fails_on_a_dangling_reference(self):
        (self.root / 'content/canon/characters/c.md').write_text(
            '+++\ncanon_kind = "character"\nid = "c"\nname = "C"\nfactions = ["ghosts"]\n+++\n\nP.\n',
            encoding='utf-8')
        r = run('canon.py', '--world', str(self.root))
        self.assertEqual(r.returncode, 1)
        self.assertIn('ghosts', r.stdout)

    def test_continuity_world_sources_names_from_canon(self):
        r = run('continuity.py', str(self.root / 'books/one/manuscript'),
                '--world', str(self.root))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('NAMES ALREADY IN CANON', r.stdout)
        # Not just the heading: the canon name the manuscript actually reuses must be named.
        self.assertIn('! Ashgrove', r.stdout)

    def test_continuity_explicit_names_wins_over_world(self):
        names = self.root / 'names.json'
        names.write_text(json.dumps({'Somebody': ['elsewhere']}), encoding='utf-8')
        r = run('continuity.py', str(self.root / 'books/one/manuscript'),
                '--world', str(self.root), '--names', str(names))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn('CROSS-BOOK NAME REUSE', r.stdout)
        self.assertNotIn('NAMES ALREADY IN CANON', r.stdout)
        # The explicit registry, not canon's, must be the one actually consulted: the name
        # that only the explicit file knows about is reported, and the canon-only name is not.
        self.assertIn('! Somebody', r.stdout)
        self.assertNotIn('! Ashgrove', r.stdout)

    def test_continuity_explicit_facts_wins_over_world(self):
        facts = self.root / 'invented.json'
        facts.write_text(json.dumps([
            {'entity': 'a', 'attribute': 'rank', 'value': 'captain', 'unit': '', 'chapter': 'x'},
            {'entity': 'a', 'attribute': 'rank', 'value': 'ensign', 'unit': '', 'chapter': 'y'}]),
            encoding='utf-8')
        r = run('continuity.py', str(self.root / 'books/one/manuscript'),
                '--world', str(self.root), '--facts', str(facts))
        self.assertEqual(r.returncode, 1)
        self.assertIn('CONFLICTS', r.stdout)

    def test_prose_audit_world_requires_product(self):
        r = run('prose_audit.py', '--world', str(self.root))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('--product', r.stdout + r.stderr)

    def test_prose_audit_world_with_product_reads_the_manuscript(self):
        r = run('prose_audit.py', '--world', str(self.root), '--product', 'one', '--json')
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        data = json.loads(r.stdout)
        manuscript = str(self.root / 'books/one/manuscript')
        # The JSON is keyed by the directory actually read. If the tool read editorial/
        # instead (a real "wrong directory" bug), this key would be absent and the chapter
        # count below would be 3 (the copied .md templates) instead of 1 (ch01.md).
        self.assertIn(manuscript, data)
        self.assertEqual(data[manuscript]['chapters'], 1)

    def test_prose_audit_unknown_product_fails_naming_the_known_ones(self):
        r = run('prose_audit.py', '--world', str(self.root), '--product', 'nope')
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('one', r.stdout + r.stderr)

    def test_positional_invocation_still_works_without_world(self):
        r = run('prose_audit.py', str(self.root / 'books/one/manuscript'))
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == '__main__':
    unittest.main()
