import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon, world

BASE_KINDS = {'character', 'place', 'faction', 'event', 'artifact', 'term', 'relationship'}


def write(root, name, text):
    p = pathlib.Path(root) / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    return p


class TestSchema(unittest.TestCase):
    def test_base_schema_ships_seven_kinds(self):
        s = canon.load_schema()
        self.assertEqual(set(s['kinds']), BASE_KINDS)

    def test_id_and_name_and_kind_are_required_everywhere(self):
        self.assertEqual(set(canon.load_schema()['common']['required']), {'kind', 'id', 'name'})

    def test_relationship_requires_between_and_refs_characters(self):
        rel = canon.load_schema()['kinds']['relationship']
        self.assertIn('between', rel['required'])
        self.assertEqual(rel['refs']['between'], 'character')

    def test_a_world_extends_the_base_rather_than_replacing_it(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml', 'title = "T"\nschema = "canon/extra.toml"\n')
            write(d, 'canon/extra.toml',
                  '[kinds.technology]\nrequired = ["era"]\n\n'
                  '[kinds.character]\noptional = ["rank"]\n')
            s = canon.load_schema(world.load(d))
            self.assertIn('technology', s['kinds'])
            self.assertIn('era', s['kinds']['technology']['required'])
            self.assertTrue(BASE_KINDS.issubset(set(s['kinds'])))
            self.assertIn('rank', s['kinds']['character']['optional'])
            self.assertIn('pronouns', s['kinds']['character']['optional'])

    def test_world_can_add_new_ref_field_to_existing_kind(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml', 'title = "T"\nschema = "canon/extra.toml"\n')
            write(d, 'canon/extra.toml',
                  '[kinds.character]\nrefs = { aliases = "term" }\n')
            s = canon.load_schema(world.load(d))
            self.assertIn('aliases', s['kinds']['character']['refs'])
            self.assertEqual(s['kinds']['character']['refs']['aliases'], 'term')
            self.assertIn('factions', s['kinds']['character']['refs'])

    def test_world_redeclaring_ref_with_different_target_raises_error(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml', 'title = "T"\nschema = "canon/extra.toml"\n')
            write(d, 'canon/extra.toml',
                  '[kinds.relationship]\nrefs = { between = "faction" }\n')
            with self.assertRaises(canon.CanonError) as cm:
                canon.load_schema(world.load(d))
            self.assertIn('between', str(cm.exception))

    def test_world_redeclaring_identical_ref_is_harmless(self):
        with tempfile.TemporaryDirectory() as d:
            write(d, 'world.toml', 'title = "T"\nschema = "canon/extra.toml"\n')
            write(d, 'canon/extra.toml',
                  '[kinds.relationship]\nrefs = { between = "character" }\n')
            s = canon.load_schema(world.load(d))
            self.assertEqual(s['kinds']['relationship']['refs']['between'], 'character')


if __name__ == '__main__':
    unittest.main()
