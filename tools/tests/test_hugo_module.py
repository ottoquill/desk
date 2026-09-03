import pathlib, sys, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon

HUGO = pathlib.Path(__file__).resolve().parents[2] / 'hugo'


class TestHugoModule(unittest.TestCase):
    def test_every_base_kind_has_an_archetype(self):
        kinds = set(canon.load_schema()['kinds'])
        found = {p.stem for p in (HUGO / 'archetypes').glob('*.md')}
        self.assertEqual(kinds, found)

    def test_each_archetype_declares_its_required_fields(self):
        schema = canon.load_schema()
        common = schema['common']['required']
        for path in sorted((HUGO / 'archetypes').glob('*.md')):
            meta, _ = canon.parse_page(path)
            required = common + schema['kinds'][path.stem].get('required', [])
            for field in required:
                self.assertIn(field, meta, f"{path.name} missing {field}")

    def test_each_archetype_declares_its_own_kind(self):
        for path in sorted((HUGO / 'archetypes').glob('*.md')):
            meta, _ = canon.parse_page(path)
            self.assertEqual(meta['kind'], path.stem)

    def test_module_declares_itself(self):
        self.assertTrue((HUGO / 'go.mod').is_file())
        self.assertTrue((HUGO / 'config.toml').is_file())

    def test_layouts_and_shortcodes_exist(self):
        for rel in ('layouts/canon/single.html', 'layouts/canon/list.html',
                    'layouts/shortcodes/canonref.html', 'layouts/shortcodes/facts.html',
                    'layouts/partials/facts.html'):
            self.assertTrue((HUGO / rel).is_file(), rel)


if __name__ == '__main__':
    unittest.main()
