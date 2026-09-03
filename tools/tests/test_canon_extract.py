import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon, world

PAGE = ('+++\nkind = "character"\nid = "a"\nname = "Ashgrove"\n'
        'pronouns = "they/them"\noccupation = "surveyor"\n'
        'factions = ["ghosts"]\n+++\n\nProse.\n')


def load(d, pages):
    (pathlib.Path(d) / 'world.toml').write_text('title = "T"\n', encoding='utf-8')
    for name, text in pages.items():
        p = pathlib.Path(d) / 'content/canon' / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
    return canon.load_pages(world.load(d))


class TestExtract(unittest.TestCase):
    def test_scalar_fields_become_facts_keyed_by_page_id(self):
        with tempfile.TemporaryDirectory() as d:
            facts = canon.facts(load(d, {'a.md': PAGE}))
            pairs = {(f['entity'], f['attribute'], f['value']) for f in facts}
            self.assertIn(('a', 'pronouns', 'they/them'), pairs)
            self.assertIn(('a', 'occupation', 'surveyor'), pairs)

    def test_structure_and_collections_are_not_facts(self):
        with tempfile.TemporaryDirectory() as d:
            attrs = {f['attribute'] for f in canon.facts(load(d, {'a.md': PAGE}))}
            self.assertNotIn('kind', attrs)
            self.assertNotIn('id', attrs)
            self.assertNotIn('name', attrs)
            self.assertNotIn('factions', attrs)

    def test_facts_carry_the_keys_continuity_expects(self):
        with tempfile.TemporaryDirectory() as d:
            for f in canon.facts(load(d, {'a.md': PAGE})):
                self.assertEqual(set(f), {'entity', 'attribute', 'value', 'unit', 'chapter'})

    def test_names_come_from_character_pages_only(self):
        with tempfile.TemporaryDirectory() as d:
            place = '+++\nkind = "place"\nid = "p"\nname = "Ashfall"\n+++\n\nP.\n'
            names = canon.names(load(d, {'a.md': PAGE, 'p.md': place}))
            self.assertEqual(names, {'Ashgrove': ['a']})

    def test_toml_dates_are_converted_to_iso_strings_and_json_serializable(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            event = ('+++\nkind = "event"\nid = "e"\nname = "Founding"\nwhen = 1889-07-14\n'
                     '+++\n\nText.\n')
            facts = canon.facts(load(d, {'e.md': event}))
            # Find the 'when' fact
            when_fact = next((f for f in facts if f['attribute'] == 'when'), None)
            self.assertIsNotNone(when_fact)
            self.assertEqual(when_fact['value'], '1889-07-14')
            # Verify the entire facts list is JSON serializable
            json_str = json.dumps(facts)
            self.assertIsInstance(json_str, str)

    def test_numeric_types_survive_as_numbers(self):
        with tempfile.TemporaryDirectory() as d:
            char = ('+++\nkind = "character"\nid = "c"\nname = "Test"\n'
                    'count = 42\nratio = 3.14\nactive = true\n+++\n\nText.\n')
            facts = canon.facts(load(d, {'c.md': char}))
            facts_by_attr = {f['attribute']: f for f in facts}
            self.assertIn('count', facts_by_attr)
            self.assertEqual(facts_by_attr['count']['value'], 42)
            self.assertIsInstance(facts_by_attr['count']['value'], int)
            self.assertIn('ratio', facts_by_attr)
            self.assertEqual(facts_by_attr['ratio']['value'], 3.14)
            self.assertIsInstance(facts_by_attr['ratio']['value'], float)
            self.assertIn('active', facts_by_attr)
            self.assertEqual(facts_by_attr['active']['value'], True)
            self.assertIsInstance(facts_by_attr['active']['value'], bool)

    def test_inline_tables_are_excluded_like_lists(self):
        with tempfile.TemporaryDirectory() as d:
            char = ('+++\nkind = "character"\nid = "c"\nname = "Test"\n'
                    'config = { key = "value" }\n+++\n\nText.\n')
            facts = canon.facts(load(d, {'c.md': char}))
            attrs = {f['attribute'] for f in facts}
            self.assertNotIn('config', attrs)


if __name__ == '__main__':
    unittest.main()
