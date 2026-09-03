import pathlib, sys, tempfile, tomllib, unittest
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

    def test_hugo_config_mounts_desks_layouts_and_archetypes(self):
        """Mounts, never [[module.imports]]: an import sends Hugo to themes/desk/hugo and the
        build dies before a page renders."""
        with tempfile.TemporaryDirectory() as d:
            root = new_world.scaffold(pathlib.Path(d) / 'w', 'T')
            cfg = tomllib.loads((root / 'hugo.toml').read_text(encoding='utf-8'))
            self.assertNotIn('imports', cfg.get('module', {}))
            pairs = [(m['source'], m['target']) for m in cfg['module']['mounts']]
            self.assertEqual(pairs, [('layouts', 'layouts'),
                                     ('desk/hugo/layouts', 'layouts'),
                                     ('archetypes', 'archetypes'),
                                     ('desk/hugo/archetypes', 'archetypes')])

    def test_desks_mount_sources_exist_in_desk(self):
        """The mounted paths are desk's own; a typo in either is a silently empty site."""
        desk = pathlib.Path(__file__).resolve().parents[2]
        with tempfile.TemporaryDirectory() as d:
            root = new_world.scaffold(pathlib.Path(d) / 'w', 'T')
            cfg = tomllib.loads((root / 'hugo.toml').read_text(encoding='utf-8'))
            for m in cfg['module']['mounts']:
                if m['source'].startswith('desk/'):
                    rel = m['source'][len('desk/'):]
                    self.assertTrue((desk / rel).is_dir(), f"{m['source']} is not in desk")

    def test_the_world_own_layouts_are_mounted_ahead_of_desks(self):
        """First mount wins, so a world overrides a canon layout the usual Hugo way."""
        with tempfile.TemporaryDirectory() as d:
            root = new_world.scaffold(pathlib.Path(d) / 'w', 'T')
            cfg = tomllib.loads((root / 'hugo.toml').read_text(encoding='utf-8'))
            sources = [m['source'] for m in cfg['module']['mounts'] if m['target'] == 'layouts']
            self.assertLess(sources.index('layouts'), sources.index('desk/hugo/layouts'))

    def test_refuses_to_overwrite_an_existing_manifest(self):
        with tempfile.TemporaryDirectory() as d:
            root = new_world.scaffold(pathlib.Path(d) / 'w', 'T')
            with self.assertRaises(new_world.NewWorldError):
                new_world.scaffold(root, 'T')

    def test_title_with_quotes_and_backslash_round_trips(self):
        with tempfile.TemporaryDirectory() as d:
            title = 'The "Great" War \\ Backslash'
            root = new_world.scaffold(pathlib.Path(d) / 'w', title)
            w = world.load(root)
            self.assertEqual(w.title, title)

    def test_hugo_config_parses_with_special_characters_in_title(self):
        with tempfile.TemporaryDirectory() as d:
            title = 'The "Great" War \\ Backslash'
            root = new_world.scaffold(pathlib.Path(d) / 'w', title)
            hugo_content = (root / 'hugo.toml').read_bytes()
            parsed = tomllib.loads(hugo_content.decode('utf-8'))
            self.assertEqual(parsed['title'], title)


if __name__ == '__main__':
    unittest.main()
