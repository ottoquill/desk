import pathlib, sys, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import prose_audit

TEMPLATE = pathlib.Path(__file__).resolve().parents[2] / 'templates' / 'voice-profile.toml'


class TestProfile(unittest.TestCase):
    def test_template_loads(self):
        self.assertTrue(TEMPLATE.is_file(), f"missing {TEMPLATE}")
        prose_audit.load_profile(TEMPLATE)

    def test_cadence_targets_survive_as_two_element_ranges(self):
        cadence = prose_audit.load_profile(TEMPLATE)['cadence']
        self.assertEqual(cadence['sentence_mean'], [14.0, 19.0])
        self.assertEqual(cadence['sentence_median'], [9, 14])

    def test_budgets_are_numbers_not_strings(self):
        budgets = prose_audit.load_profile(TEMPLATE)['budgets']
        self.assertEqual(budgets['simile-frame:the-way-you'], 8.0)
        self.assertEqual(budgets['epiphany:it-was-then'], 0.0)
        for name, value in budgets.items():
            self.assertIsInstance(value, (int, float), name)

    def test_comment_keys_are_gone(self):
        text = TEMPLATE.read_text(encoding='utf-8')
        self.assertNotIn('_comment', text)
        self.assertIn('#', text)

    def test_chapter_words_and_declared_refrains_present(self):
        p = prose_audit.load_profile(TEMPLATE)
        self.assertEqual(p['chapter_words'], [2400, 3600])
        self.assertEqual(p['declared_refrains'], [])


if __name__ == '__main__':
    unittest.main()
