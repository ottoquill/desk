import os, pathlib, shutil, subprocess, sys, tempfile, tomllib, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon, new_world

DESK = pathlib.Path(__file__).resolve().parents[2]
HUGO = DESK / 'hugo'


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
            self.assertEqual(meta['canon_kind'], path.stem)

    def test_each_archetype_seeds_its_id_from_the_page_name(self):
        """`hugo new` substitutes {{ .Name }}; a literal id makes every page a duplicate."""
        for path in sorted((HUGO / 'archetypes').glob('*.md')):
            meta, _ = canon.parse_page(path)
            self.assertEqual(meta['id'], '{{ .Name }}', path.name)

    def test_nothing_in_the_module_uses_hugo_s_removed_kind_key(self):
        """`kind` in front matter was removed in Hugo v0.144.0 and now fails the build."""
        for path in sorted(HUGO.rglob('*')):
            if not path.is_file() or path.suffix not in ('.md', '.html'):
                continue
            text = path.read_text(encoding='utf-8')
            self.assertNotIn('.Params.kind', text, path)
            for line in text.splitlines():
                self.assertFalse(line.startswith('kind'),
                                 f"{path}: front matter still declares `kind`")

    def test_module_declares_itself(self):
        self.assertTrue((HUGO / 'go.mod').is_file())
        self.assertTrue((HUGO / 'config.toml').is_file())

    def test_module_config_mounts_layouts_and_archetypes_that_exist(self):
        cfg = tomllib.loads((HUGO / 'config.toml').read_text(encoding='utf-8'))
        mounts = cfg['module']['mounts']
        self.assertEqual([(m['source'], m['target']) for m in mounts],
                         [('layouts', 'layouts'), ('archetypes', 'archetypes')])
        for m in mounts:
            self.assertTrue((HUGO / m['source']).is_dir(), f"mount source {m['source']} missing")

    def test_layouts_and_shortcodes_exist(self):
        for rel in ('layouts/_default/baseof.html',
                    'layouts/canon/single.html', 'layouts/canon/list.html',
                    'layouts/shortcodes/canonref.html', 'layouts/shortcodes/facts.html',
                    'layouts/partials/facts.html'):
            self.assertTrue((HUGO / rel).is_file(), rel)

    def test_the_canon_layouts_have_a_base_to_fill(self):
        """`{{ define "main" }}` without a baseof renders a one-byte page."""
        base = (HUGO / 'layouts/_default/baseof.html').read_text(encoding='utf-8')
        self.assertIn('block "main"', base)
        for rel in ('layouts/canon/single.html', 'layouts/canon/list.html'):
            self.assertIn('define "main"', (HUGO / rel).read_text(encoding='utf-8'))

    def test_the_facts_shortcode_delegates_to_the_partial(self):
        """Two copies of the panel drift the first time the skip list changes."""
        shortcode = (HUGO / 'layouts/shortcodes/facts.html').read_text(encoding='utf-8')
        partial = (HUGO / 'layouts/partials/facts.html').read_text(encoding='utf-8')
        self.assertIn('partial "facts.html"', shortcode)
        self.assertNotEqual(shortcode, partial)
        self.assertNotIn('<table', shortcode)

    def test_the_fact_panel_skips_hugo_s_own_front_matter_fields(self):
        """Hugo injects these into .Params whether declared or not; they are not canon."""
        partial = (HUGO / 'layouts/partials/facts.html').read_text(encoding='utf-8')
        for field in ('iscjklanguage', 'draft', 'title', 'date', 'lastmod', 'type', 'weight'):
            self.assertIn(f'"{field}"', partial, f"fact panel would print {field} as a fact")


CHARACTER = '''+++
canon_kind = "character"
id         = "sable"
name       = "Sable Ferrow"
pronouns   = "she/her"
occupation = "salvager"
+++

Sable came up through the yards.
'''


@unittest.skipUnless(shutil.which('hugo'), 'hugo is not installed')
class TestHugoBuild(unittest.TestCase):
    """The only check that the module actually renders. Everything above is shape."""

    def test_a_scaffolded_world_builds_and_renders_its_canon(self):
        with tempfile.TemporaryDirectory() as d:
            root = new_world.scaffold(pathlib.Path(d) / 'w', 'A Test World')
            (root / 'desk').symlink_to(DESK, target_is_directory=True)
            page = root / 'content' / 'canon' / 'characters' / 'sable.md'
            page.write_text(CHARACTER, encoding='utf-8')

            env = dict(os.environ, HUGO_CACHEDIR=str(pathlib.Path(d) / 'cache'))
            r = subprocess.run([shutil.which('hugo')], cwd=root, env=env,
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, f"{r.stdout}\n{r.stderr}")
            self.assertNotIn('ERROR', r.stderr)

            out = root / 'public' / 'canon' / 'characters' / 'sable' / 'index.html'
            self.assertTrue(out.is_file(), 'canon page did not render')
            html = out.read_text(encoding='utf-8')
            self.assertIn('Sable Ferrow', html)
            self.assertIn('salvager', html)
            self.assertIn('</html>', html)          # a baseof filled, not a bare fragment
            self.assertNotIn('iscjklanguage', html)  # Hugo internals kept out of the fact panel
            self.assertGreater(len(html), 200)


if __name__ == '__main__':
    unittest.main()
