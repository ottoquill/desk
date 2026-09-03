import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon, world

CHARACTER = '+++\nkind = "character"\nid = "{id}"\nname = "{name}"\n+++\n\nProse.\n'


def make_world(d, pages):
    (pathlib.Path(d) / 'world.toml').write_text('title = "T"\n', encoding='utf-8')
    for name, text in pages.items():
        p = pathlib.Path(d) / 'content/canon' / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
    return world.load(d)


def errors_for(d, pages):
    w = make_world(d, pages)
    return canon.validate(canon.load_pages(w), canon.load_schema(w))


class TestValidate(unittest.TestCase):
    def test_a_valid_page_produces_no_errors(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A')}), [])

    def test_front_matter_must_be_toml_delimited_by_plus_signs(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'p.md'
            p.write_text('---\nkind: character\n---\n\nProse.\n', encoding='utf-8')
            with self.assertRaises(canon.CanonError):
                canon.parse_page(p)

    def test_body_survives_parsing(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'p.md'
            p.write_text(CHARACTER.format(id='a', name='A'), encoding='utf-8')
            meta, body = canon.parse_page(p)
            self.assertEqual(meta['id'], 'a')
            self.assertIn('Prose.', body)

    def test_missing_required_field_fails(self):
        with tempfile.TemporaryDirectory() as d:
            errs = errors_for(d, {'c/a.md': '+++\nkind = "character"\nid = "a"\n+++\n\nP.\n'})
            self.assertTrue(any('name' in e for e in errs), errs)

    def test_unknown_kind_fails(self):
        with tempfile.TemporaryDirectory() as d:
            errs = errors_for(d, {'c/a.md': '+++\nkind = "sandwich"\nid = "a"\nname = "A"\n+++\n\nP.\n'})
            self.assertTrue(any('sandwich' in e for e in errs), errs)

    def test_duplicate_ids_fail(self):
        with tempfile.TemporaryDirectory() as d:
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='dup', name='A'),
                                  'c/b.md': CHARACTER.format(id='dup', name='B')})
            self.assertTrue(any('dup' in e for e in errs), errs)

    def test_dangling_cross_reference_fails(self):
        with tempfile.TemporaryDirectory() as d:
            page = ('+++\nkind = "character"\nid = "a"\nname = "A"\n'
                    'factions = ["ghosts"]\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': page})
            self.assertTrue(any('ghosts' in e for e in errs), errs)

    def test_relationship_needs_exactly_two_members(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\nkind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a"]\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'), 'c/r.md': rel})
            self.assertTrue(any('two' in e for e in errs), errs)

    def test_relationship_between_must_resolve_to_characters(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\nkind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "ghost"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "ghost"\n\n'
                   '[[direction]]\nfrom = "ghost"\nto = "a"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'), 'c/r.md': rel})
            self.assertTrue(any('ghost' in e for e in errs), errs)

    def test_relationship_must_declare_both_directions(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\nkind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "b"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "b"\nnever_says = "his name"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                                  'c/b.md': CHARACTER.format(id='b', name='B'),
                                  'c/r.md': rel})
            self.assertTrue(any('direction' in e for e in errs), errs)

    def test_a_complete_relationship_validates(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\nkind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "b"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "b"\nnever_says = "his first name"\n\n'
                   '[[direction]]\nfrom = "b"\nto = "a"\nregister = "over-explains"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                                  'c/b.md': CHARACTER.format(id='b', name='B'),
                                  'c/r.md': rel})
            self.assertEqual(errs, [])


if __name__ == '__main__':
    unittest.main()
