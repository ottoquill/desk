import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import world


def write(root, name, text):
    p = pathlib.Path(root) / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    return p


class TestWorld(unittest.TestCase):
    def test_minimal_manifest_gets_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml', 'title = "Test World"\n')
            w = world.load(d)
            self.assertEqual(w.title, 'Test World')
            self.assertEqual(w.desk, pathlib.Path(d) / 'desk')
            self.assertEqual(w.canon, pathlib.Path(d) / 'content/canon')
            self.assertIsNone(w.schema)
            self.assertEqual(w.products, [])

    def test_explicit_paths_override_defaults(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml',
                  'title = "T"\ncanon = "lore"\ndesk = "vendor/desk"\nschema = "canon/extra.toml"\n')
            w = world.load(d)
            self.assertEqual(w.canon, pathlib.Path(d) / 'lore')
            self.assertEqual(w.desk, pathlib.Path(d) / 'vendor/desk')
            self.assertEqual(w.schema, pathlib.Path(d) / 'canon/extra.toml')

    def test_product_lookup_resolves_paths(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml',
                  'title = "T"\n\n[[products]]\nid = "one"\nkind = "book"\npath = "books/one"\n')
            p = world.load(d).product('one')
            self.assertEqual(p.kind, 'book')
            self.assertEqual(p.manuscript, pathlib.Path(d) / 'books/one/manuscript')
            self.assertEqual(p.editorial, pathlib.Path(d) / 'books/one/editorial')

    def test_unknown_product_names_the_available_ids(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml',
                  'title = "T"\n\n[[products]]\nid = "one"\nkind = "book"\npath = "books/one"\n')
            with self.assertRaises(world.WorldError) as cm:
                world.load(d).product('two')
            self.assertIn('one', str(cm.exception))

    def test_malformed_manifest_names_the_file(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml', 'title = "unterminated\n')
            with self.assertRaises(world.WorldError) as cm:
                world.load(d)
            self.assertIn('world.toml', str(cm.exception))

    def test_missing_manifest_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(world.WorldError):
                world.load(d)

    def test_product_missing_a_key_is_an_error(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml', 'title = "T"\n\n[[products]]\nid = "one"\nkind = "book"\n')
            with self.assertRaises(world.WorldError) as cm:
                world.load(d)
            self.assertIn('path', str(cm.exception))


if __name__ == '__main__':
    unittest.main()
