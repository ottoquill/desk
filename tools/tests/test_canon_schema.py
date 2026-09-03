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


if __name__ == '__main__':
    unittest.main()
