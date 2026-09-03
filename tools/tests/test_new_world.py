import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon, new_world, world


class TestNewWorld(unittest.TestCase):
    def test_scaffold_round_trips_through_world_load(self):
        with tempfile.TemporaryDirectory() as d:
            root = new_world.scaffold(pathlib.Path(d) / 'w', 'A Test World')
            w = world.load(root)
            self.assertEqual(w.title, 'A Test World')
            self.assertEqual(w.products, [])
            self.assertTrue(w.canon.is_dir())

    def test_scaffolded_canon_validates_as_empty(self):
        with tempfile.TemporaryDirectory() as d:
            w = world.load(new_world.scaffold(pathlib.Path(d) / 'w', 'T'))
            self.assertEqual(canon.validate(canon.load_pages(w), canon.load_schema(w)), [])

    def test_hugo_config_mounts_the_desk_module(self):
        with tempfile.TemporaryDirectory() as d:
            root = new_world.scaffold(pathlib.Path(d) / 'w', 'T')
            self.assertIn('desk/hugo', (root / 'hugo.toml').read_text(encoding='utf-8'))

    def test_refuses_to_overwrite_an_existing_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root = new_world.scaffold(pathlib.Path(d) / 'w', 'T')
            with self.assertRaises(SystemExit):
                new_world.scaffold(root, 'T')


if __name__ == '__main__':
    unittest.main()
