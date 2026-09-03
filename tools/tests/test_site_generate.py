import importlib.util, pathlib, sys, unittest

SITE = pathlib.Path(__file__).resolve().parents[2] / 'site'
spec = importlib.util.spec_from_file_location('site_generate', SITE / 'generate.py')
generate = importlib.util.module_from_spec(spec)
sys.modules['site_generate'] = generate
spec.loader.exec_module(generate)


class TestPseudoTags(unittest.TestCase):
    """The corpus writes placeholders as <emotion>. A renderer reads those as HTML and
    drops them, publishing a rule with a hole in it that still scans as prose."""

    def test_placeholder_in_prose_is_escaped(self):
        out = generate.escape_pseudo_tags("[name] was/felt <emotion>' outside monologue")
        self.assertIn('&lt;emotion&gt;', out)

    def test_attribution_markup_is_kept(self):
        out = generate.escape_pseudo_tags('practice · <sub>Gardner, The Art of Fiction</sub>')
        self.assertIn('<sub>', out)
        self.assertIn('</sub>', out)

    def test_code_span_is_left_alone(self):
        out = generate.escape_pseudo_tags('run `prose_audit.py --product <product>` first')
        self.assertIn('`prose_audit.py --product <product>`', out)

    def test_code_span_across_a_line_break_is_left_alone(self):
        out = generate.escape_pseudo_tags('a line of the form `symptom @ ch<N>:\n<line>` and more')
        self.assertNotIn('&lt;line&gt;', out)

    def test_fenced_block_is_left_alone(self):
        out = generate.escape_pseudo_tags('text\n\n```bash\nnew_book.py <world> --slug <slug>\n```\n')
        self.assertIn('new_book.py <world> --slug <slug>', out)


class TestLinkRewriting(unittest.TestCase):
    def setUp(self):
        self.urls = {'method/02-the-rules.md': '/method/02-the-rules/',
                     'method': '/method/', 'method/': '/method/'}

    def rewrite(self, body, src_dir='method'):
        self.warnings = []
        return generate.rewrite_links(body, src_dir, self.urls, self.warnings)

    def test_published_page_becomes_a_site_url(self):
        self.assertEqual(self.rewrite('see [the rules](02-the-rules.md)'),
                         'see [the rules](/method/02-the-rules/)')

    def test_anchor_is_preserved(self):
        self.assertEqual(self.rewrite('[R12](02-the-rules.md#r12)'),
                         '[R12](/method/02-the-rules/#r12)')

    def test_unpublished_repo_file_becomes_a_github_link(self):
        out = self.rewrite('the gate is [idiolect_probe.py](../tools/idiolect_probe.py)')
        self.assertIn('https://github.com/ottoquill/desk/blob/main/tools/idiolect_probe.py', out)

    def test_external_link_is_untouched(self):
        body = '[Hugo](https://gohugo.io/docs/)'
        self.assertEqual(self.rewrite(body), body)

    def test_dead_link_keeps_the_text_and_warns(self):
        out = self.rewrite('[gone](99-not-a-file.md)')
        self.assertEqual(out, 'gone')
        self.assertTrue(self.warnings)


class TestUrlMapping(unittest.TestCase):
    def test_readme_heads_its_section(self):
        self.assertEqual(generate.url_for('method/_index.md'), '/method/')

    def test_page_url_matches_its_path(self):
        self.assertEqual(generate.url_for('method/reference/00-summary.md'),
                         '/method/reference/00-summary/')

    def test_a_directory_source_is_reachable_without_a_readme(self):
        """templates/ has no README; a link to it must still reach the site rather
        than falling through to GitHub."""
        urls = generate.build_url_map(generate.collect())
        self.assertEqual(urls.get('templates'), '/desk/templates/')


if __name__ == '__main__':
    unittest.main()
