import pathlib, sys, tempfile, unittest, warnings
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import continuity


class TestContinuityWorld(unittest.TestCase):
    def test_scan_fact_list_finds_a_key_with_two_values(self):
        facts = [{'entity': 'a', 'attribute': 'rank', 'value': 'captain', 'unit': '', 'chapter': 'x'},
                 {'entity': 'a', 'attribute': 'rank', 'value': 'ensign', 'unit': '', 'chapter': 'y'}]
        self.assertEqual(len(continuity.scan_fact_list(facts)), 1)

    def test_scan_fact_list_passes_a_consistent_store(self):
        facts = [{'entity': 'a', 'attribute': 'rank', 'value': 'captain', 'unit': '', 'chapter': 'x'},
                 {'entity': 'a', 'attribute': 'rank', 'value': 'captain', 'unit': '', 'chapter': 'y'}]
        self.assertEqual(continuity.scan_fact_list(facts), [])

    def test_plus_delimited_front_matter_is_stripped(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'ch01.md'
            p.write_text('+++\npov = "a"\n+++\n\nThe body.\n', encoding='utf-8')
            (name, text), = continuity.load(d)
            self.assertNotIn('pov', text)
            self.assertIn('The body.', text)

    def test_dash_delimited_front_matter_still_stripped(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'ch01.md'
            p.write_text('---\npov: a\n---\n\nThe body.\n', encoding='utf-8')
            (name, text), = continuity.load(d)
            self.assertNotIn('pov', text)
            self.assertIn('The body.', text)

    def test_load_does_not_leak_open_file_handles(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'ch01.md'
            p.write_text('---\npov: a\n---\n\nThe body.\n', encoding='utf-8')
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                continuity.load(d)
            self.assertFalse(any(issubclass(w.category, ResourceWarning) for w in caught))


if __name__ == '__main__':
    unittest.main()
