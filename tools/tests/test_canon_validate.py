import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon, world

CHARACTER = '+++\ncanon_kind = "character"\nid = "{id}"\nname = "{name}"\n+++\n\nProse.\n'


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
            p.write_text('---\ncanon_kind: character\n---\n\nProse.\n', encoding='utf-8')
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
            errs = errors_for(d, {'c/a.md': '+++\ncanon_kind = "character"\nid = "a"\n+++\n\nP.\n'})
            self.assertTrue(any('name' in e for e in errs), errs)

    def test_unknown_kind_fails(self):
        with tempfile.TemporaryDirectory() as d:
            errs = errors_for(d, {'c/a.md': '+++\ncanon_kind = "sandwich"\nid = "a"\nname = "A"\n+++\n\nP.\n'})
            self.assertTrue(any('sandwich' in e for e in errs), errs)

    def test_duplicate_ids_fail(self):
        with tempfile.TemporaryDirectory() as d:
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='dup', name='A'),
                                  'c/b.md': CHARACTER.format(id='dup', name='B')})
            self.assertTrue(any('dup' in e for e in errs), errs)

    def test_dangling_cross_reference_fails(self):
        with tempfile.TemporaryDirectory() as d:
            page = ('+++\ncanon_kind = "character"\nid = "a"\nname = "A"\n'
                    'factions = ["ghosts"]\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': page})
            self.assertTrue(any('ghosts' in e for e in errs), errs)

    def test_relationship_needs_exactly_two_members(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\ncanon_kind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a"]\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'), 'c/r.md': rel})
            self.assertTrue(any('two' in e for e in errs), errs)

    def test_relationship_between_must_resolve_to_characters(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\ncanon_kind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "ghost"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "ghost"\n\n'
                   '[[direction]]\nfrom = "ghost"\nto = "a"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'), 'c/r.md': rel})
            self.assertTrue(any('ghost' in e for e in errs), errs)

    def test_relationship_must_declare_both_directions(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\ncanon_kind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "b"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "b"\nnever_says = "his name"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                                  'c/b.md': CHARACTER.format(id='b', name='B'),
                                  'c/r.md': rel})
            self.assertTrue(any('direction' in e for e in errs), errs)

    def test_a_complete_relationship_validates(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\ncanon_kind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "b"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "b"\nnever_says = "his first name"\n\n'
                   '[[direction]]\nfrom = "b"\nto = "a"\nregister = "over-explains"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                                  'c/b.md': CHARACTER.format(id='b', name='B'),
                                  'c/r.md': rel})
            self.assertEqual(errs, [])

    def test_an_empty_ref_is_an_unfilled_slot_not_a_dangling_reference(self):
        """desk's own archetypes ship `origin = ""` and `factions = []`."""
        with tempfile.TemporaryDirectory() as d:
            page = ('+++\ncanon_kind = "artifact"\nid = "a"\nname = "A"\n'
                    'origin = ""\nheld_by = ""\n+++\n\nP.\n')
            self.assertEqual(errors_for(d, {'c/a.md': page}), [])

    def test_an_empty_ref_list_is_an_unfilled_slot(self):
        with tempfile.TemporaryDirectory() as d:
            page = ('+++\ncanon_kind = "character"\nid = "a"\nname = "A"\n'
                    'factions = []\n+++\n\nP.\n')
            self.assertEqual(errors_for(d, {'c/a.md': page}), [])

    def test_every_desk_archetype_passes_desks_own_validator(self):
        """A page made from an archetype is the first page a world writes."""
        archetypes = pathlib.Path(__file__).resolve().parents[2] / 'hugo' / 'archetypes'
        pages = {}
        for src in sorted(archetypes.glob('*.md')):
            pages[f'c/{src.stem}.md'] = src.read_text(encoding='utf-8').replace(
                '{{ .Name }}', src.stem)
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(errors_for(d, pages), [])

    def test_a_ref_field_holding_a_table_is_reported_not_raised(self):
        """A gate must not crash on the material it gates (was: unhashable type: 'dict')."""
        with tempfile.TemporaryDirectory() as d:
            page = ('+++\ncanon_kind = "character"\nid = "a"\nname = "A"\n\n'
                    '[factions]\nprimary = "ghosts"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': page})
            self.assertTrue(any('factions' in e and 'a.md' in e for e in errs), errs)

    def test_a_ref_list_holding_a_table_is_reported_not_raised(self):
        with tempfile.TemporaryDirectory() as d:
            page = ('+++\ncanon_kind = "character"\nid = "a"\nname = "A"\n'
                    'factions = [{ primary = "ghosts" }]\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': page})
            self.assertTrue(any('factions' in e for e in errs), errs)

    def test_a_relationship_with_the_wrong_shapes_is_reported_not_raised(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\ncanon_kind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = [{ a = 1 }, { b = 2 }]\n+++\n\nP.\n')
            errs = errors_for(d, {'c/r.md': rel})
            self.assertTrue(any('between' in e for e in errs), errs)

    def test_a_relationship_direction_that_is_not_a_table_is_reported(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\ncanon_kind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "b"]\ndirection = "both ways"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                                  'c/b.md': CHARACTER.format(id='b', name='B'),
                                  'c/r.md': rel})
            self.assertTrue(any('direction' in e for e in errs), errs)

    def test_underscore_prefixed_file_with_no_front_matter_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            w = make_world(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                               'c/_index.md': 'This is section metadata, no front matter.\n'})
            # Should not raise and should not produce errors
            pages = canon.load_pages(w)
            errs = canon.validate(pages, canon.load_schema(w))
            self.assertEqual(len(pages), 1)  # Only a.md, not _index.md
            self.assertEqual(errs, [])

    def test_underscore_prefixed_file_with_invalid_front_matter_is_skipped(self):
        with tempfile.TemporaryDirectory() as d:
            w = make_world(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                               'c/_index.md': '+++\ntitle = "Section"\n+++\n\nSection prose.\n'})
            # Should not raise even though _index.md has invalid front matter
            pages = canon.load_pages(w)
            errs = canon.validate(pages, canon.load_schema(w))
            self.assertEqual(len(pages), 1)  # Only a.md, not _index.md
            self.assertEqual(errs, [])


if __name__ == '__main__':
    unittest.main()
