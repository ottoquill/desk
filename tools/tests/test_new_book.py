import pathlib, sys, tempfile, tomllib, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import new_book, new_world, world


class TestNewBook(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = new_world.scaffold(pathlib.Path(self._tmp.name) / 'w', 'T')

    def tearDown(self):
        self._tmp.cleanup()

    def test_product_is_declared_and_loads(self):
        new_book.add(self.root, 'Book One', 'book-one')
        p = world.load(self.root).product('book-one')
        self.assertEqual(p.kind, 'book')
        self.assertTrue(p.manuscript.is_dir())

    def test_templates_are_copied_into_editorial(self):
        new_book.add(self.root, 'Book One', 'book-one')
        e = world.load(self.root).product('book-one').editorial
        for name in ('voice-profile.toml', 'style-sheet.md', 'promise-ledger.md',
                     'critic-briefs.md'):
            self.assertTrue((e / name).is_file(), name)

    def test_manifest_comments_survive_the_append(self):
        before = (self.root / 'world.toml').read_text(encoding='utf-8')
        new_book.add(self.root, 'Book One', 'book-one')
        after = (self.root / 'world.toml').read_text(encoding='utf-8')
        self.assertTrue(after.startswith(before))
        self.assertIn('# The whole interface', after)

    def test_two_products_both_load(self):
        new_book.add(self.root, 'One', 'one')
        new_book.add(self.root, 'Two', 'two')
        w = world.load(self.root)
        self.assertEqual({p.id for p in w.products}, {'one', 'two'})

    def test_duplicate_slug_is_refused(self):
        new_book.add(self.root, 'One', 'one')
        with self.assertRaises(new_book.NewBookError):
            new_book.add(self.root, 'One Again', 'one')

    def test_voice_profile_book_field_is_set_to_title(self):
        new_book.add(self.root, 'Book One', 'book-one')
        profile_path = world.load(self.root).product('book-one').editorial / 'voice-profile.toml'
        data = tomllib.loads(profile_path.read_text(encoding='utf-8'))
        self.assertEqual(data['book'], 'Book One')

    def test_title_and_slug_with_quotes_and_backslash_round_trip(self):
        title = 'The "Great" Book \\ Backslash'
        slug = 'book-"weird"-\\slug'
        new_book.add(self.root, title, slug)
        w = world.load(self.root)
        p = w.product(slug)
        self.assertEqual(p.id, slug)
        profile_path = p.editorial / 'voice-profile.toml'
        data = tomllib.loads(profile_path.read_text(encoding='utf-8'))
        self.assertEqual(data['book'], title)


if __name__ == '__main__':
    unittest.main()
