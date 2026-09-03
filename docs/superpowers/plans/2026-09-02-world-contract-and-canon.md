# World Contract and Canon Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `desk/` world-independent infrastructure that a world repo consumes as a submodule, with canon as a validated substrate of Markdown pages.

**Architecture:** A world declares itself in `world.toml`. `tools/world.py` is the only thing that reads it, and every other tool reaches a world through it. Canon is Markdown with `+++` TOML front matter; `tools/canon.py` validates pages against a schema desk ships and emits the fact store and name registry that `continuity.py` consumes. Nothing in desk names a world.

**Tech Stack:** Python 3.11+ (stdlib only — `tomllib`, `unittest`, `pathlib`, `re`, `json`). Hugo for the wiki module (no build step in this repo).

**Spec:** [docs/superpowers/specs/2026-09-02-world-contract-design.md](../specs/2026-09-02-world-contract-design.md)

## Global Constraints

- **`tools/` is stdlib-only.** No third-party imports, ever. A subagent with no environment must be able to run the gate.
- **Python 3.11+** is the floor, for `tomllib`.
- **Config is human-owned and machine-read (TOML). State is machine-owned and machine-read (JSON).**
- **No tool rewrites a config file.** `new_book.py` may only *append* a `[[products]]` table at end of file.
- **Nothing in desk names a world**, a book, or any world's noun. Fixtures in `tools/tests/` are the sole exception, and they use obviously synthetic names.
- **Markdown wraps at 100 columns.**
- **Prose added to the repo must pass `python3 tools/idiolect_probe.py <file>` (exit 0) before commit**, per `CLAUDE.md`.
- **Tests run with `python3 -m unittest discover -s tools/tests -t .`** from the repo root.
- **Commit messages carry the reasoning and the numbers in full paragraphs**, ending with `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.

---

## File Structure

| Path | Responsibility |
|---|---|
| `tools/world.py` | Load `world.toml`, apply defaults, resolve paths. The only reader of the manifest. |
| `tools/canon.py` | Parse canon pages, load and merge schema, validate, extract facts and names. |
| `canon/schema.toml` | The seven base kinds and their fields. |
| `tools/new_world.py` | Scaffold a world. |
| `tools/new_book.py` | Add a book product to an existing world. |
| `hugo/` | Hugo module: archetypes, layouts, shortcodes, config fragment. |
| `templates/voice-profile.toml` | Replaces `voice-profile.json`. |
| `method/00-starting-a-world.md` | The entry point. |
| `tools/tests/` | stdlib `unittest` suite. |

Modified: `tools/continuity.py` (`--world`, `+++` front matter, fact-list refactor), `tools/prose_audit.py` (`--world`, TOML profile, `+++` front matter), `tools/idiolect_probe.py` (`+++` front matter), `CLAUDE.md`, `method/*.md`, `templates/*.md`. Deleted: `names.json`, `templates/voice-profile.json`.

---

### Task 1: `tools/world.py` — the manifest loader

**Files:**
- Create: `tools/world.py`
- Create: `tools/tests/__init__.py` (empty)
- Test: `tools/tests/test_world.py`

**Interfaces:**
- Consumes: nothing.
- Produces: `world.load(path) -> World`; `World.root`, `.title`, `.desk`, `.canon`, `.schema` (all `pathlib.Path`, `.schema` may be `None`), `.products` (list of `Product`), `.product(id) -> Product`; `Product.id`, `.kind` (str), `.path`, `.manuscript`, `.editorial` (`pathlib.Path`); `world.WorldError`.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/__init__.py` as an empty file, then `tools/tests/test_world.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'world'`

- [ ] **Step 3: Write the implementation**

Create `tools/world.py`:

```python
#!/usr/bin/env python3
"""
world.py — load a world manifest and resolve its paths.

desk knows product kinds; a world names instances. This module is the whole of what desk learns
about a world: where canon lives, which products exist, and what kind each one is. Nothing else in
desk reads world.toml.

    from world import load
    w = load('/path/to/world')            # a directory, or the world.toml itself
    w.canon                                # Path to the canon pages
    w.product('book-1').manuscript         # Path

Stdlib only. Requires Python 3.11+ for tomllib.
"""
import pathlib
import tomllib

MANIFEST = 'world.toml'
DEFAULT_DESK = 'desk'
DEFAULT_CANON = 'content/canon'


class WorldError(Exception):
    """A manifest is missing, malformed, or does not declare what was asked for."""


class Product:
    def __init__(self, world, data):
        for key in ('id', 'kind', 'path'):
            if key not in data:
                raise WorldError(f"{world.manifest}: a [[products]] entry is missing {key!r}")
        self.id = data['id']
        self.kind = data['kind']
        self.path = world.root / data['path']
        self.manuscript = self.path / 'manuscript'
        self.editorial = self.path / 'editorial'

    def __repr__(self):
        return f"Product(id={self.id!r}, kind={self.kind!r})"


class World:
    def __init__(self, manifest, data):
        self.manifest = pathlib.Path(manifest)
        self.root = self.manifest.parent
        self.title = data.get('title', '')
        self.desk = self.root / data.get('desk', DEFAULT_DESK)
        self.canon = self.root / data.get('canon', DEFAULT_CANON)
        schema = data.get('schema')
        self.schema = self.root / schema if schema else None
        self.products = [Product(self, p) for p in data.get('products', [])]

    def product(self, pid):
        for p in self.products:
            if p.id == pid:
                return p
        have = ', '.join(p.id for p in self.products) or 'none declared'
        raise WorldError(f"no product {pid!r} in {self.manifest} (declared: {have})")

    def __repr__(self):
        return f"World(title={self.title!r}, products={len(self.products)})"


def load(path):
    """Load the manifest at `path`, which may be a world root or the world.toml itself."""
    p = pathlib.Path(path)
    if p.is_dir():
        p = p / MANIFEST
    if not p.is_file():
        raise WorldError(f"no world manifest at {p}")
    try:
        data = tomllib.loads(p.read_text(encoding='utf-8'))
    except tomllib.TOMLDecodeError as e:
        raise WorldError(f"{p}: {e}") from None
    return World(p, data)
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 7 tests, OK

- [ ] **Step 5: Commit**

```bash
git add tools/world.py tools/tests/__init__.py tools/tests/test_world.py
git commit -m "$(cat <<'EOF'
Add world.py: the one place desk reads a world manifest

desk knows product kinds and a world names instances, so the manifest is the
entire interface between them. Every other tool reaches a world through this
module rather than assuming a layout, which is what removes the path coupling
to <book>/manuscript that ran through thirteen files.

Defaults cover the conventional layout, so a world declares its products and
little else. Products are declared rather than discovered: letting desk guess
what counts as a product would put a world's shape back inside desk.

Seven tests, the repo's first.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: `canon/schema.toml` and schema loading

**Files:**
- Create: `canon/schema.toml`
- Create: `tools/canon.py` (schema loading only; page handling arrives in Task 3)
- Test: `tools/tests/test_canon_schema.py`

**Interfaces:**
- Consumes: `world.load`, `World.schema` from Task 1.
- Produces: `canon.load_schema(world=None) -> dict` with keys `common` (`{'required': [...]}`) and `kinds` (`{name: {'required': [...], 'optional': [...], 'refs': {field: kind}}}`); `canon.CanonError`.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_canon_schema.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'canon'`

- [ ] **Step 3: Write the schema and the loader**

Create `canon/schema.toml`:

```toml
# The base canon kinds. desk ships the kinds; a world names the instances.
#
# A world EXTENDS this through the `schema` key in its world.toml. Extension adds kinds and adds
# fields to existing kinds; it never removes either, because a world that could delete a base field
# would put desk's guarantees at the mercy of each world.
#
#   required  fields that must be present, beyond [common]
#   optional  fields the validator recognises and leaves alone
#   refs      field -> the kind its value(s) must resolve to, by id

[common]
required = ["kind", "id", "name"]

[kinds.character]
required = []
optional = ["pronouns", "occupation", "factions", "first_seen"]
refs     = { factions = "faction" }

[kinds.place]
required = []
optional = ["region", "factions"]
refs     = { factions = "faction" }

[kinds.faction]
required = []
optional = ["seat", "founded"]
refs     = { seat = "place" }

[kinds.event]
required = ["when"]
optional = ["where", "participants"]
refs     = { where = "place", participants = "character" }

[kinds.artifact]
required = []
optional = ["origin", "held_by"]
refs     = { origin = "place", held_by = "character" }

[kinds.term]
required = []
optional = ["aliases"]
refs     = {}

# An edge, not a node. Card's network (Characters & Viewpoint, 1988, ch1): the self is "a kind of
# network, many threads connecting us to many different people", and "we are different people in
# different relationships." Both directions live in this one page so the halves cannot drift.
[kinds.relationship]
required = ["between"]
optional = []
refs     = { between = "character" }
```

Create `tools/canon.py`:

```python
#!/usr/bin/env python3
"""
canon.py — validate a world's canon and extract what the other instruments need.

Canon is Markdown in Hugo's native shape: TOML front matter carrying the checkable facts, prose in
the body carrying the lore. One artifact, three consumers — Hugo renders it, this script checks it,
and continuity.py reads the front matter as a typed fact store.

    python3 tools/canon.py --world PATH [--json]

Stdlib only. Requires Python 3.11+ for tomllib.
"""
import pathlib
import tomllib

SCHEMA = pathlib.Path(__file__).resolve().parent.parent / 'canon' / 'schema.toml'


class CanonError(Exception):
    """Canon could not be read: a missing schema, unparseable front matter, bad TOML."""


def _read_toml(path):
    try:
        return tomllib.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    except FileNotFoundError:
        raise CanonError(f"no such file: {path}") from None
    except tomllib.TOMLDecodeError as e:
        raise CanonError(f"{path}: {e}") from None


def load_schema(world=None):
    """The base schema, extended (never replaced) by the world's own if it declares one."""
    schema = _read_toml(SCHEMA)
    schema.setdefault('common', {}).setdefault('required', [])
    schema.setdefault('kinds', {})
    if world is None or not world.schema:
        return schema
    for kind, spec in _read_toml(world.schema).get('kinds', {}).items():
        base = schema['kinds'].setdefault(kind, {'required': [], 'optional': [], 'refs': {}})
        for key, value in spec.items():
            if isinstance(value, list):
                base[key] = sorted(set(base.get(key, [])) | set(value))
            elif isinstance(value, dict):
                base.setdefault(key, {}).update(value)
            else:
                base[key] = value
    return schema
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 11 tests total, OK

- [ ] **Step 5: Commit**

```bash
git add canon/schema.toml tools/canon.py tools/tests/test_canon_schema.py
git commit -m "$(cat <<'EOF'
Ship the base canon schema: seven kinds, extensible by a world

desk ships what a character, place, faction, event, artifact, term and
relationship require; a world supplies the instances. A world extends the base
through the schema key in world.toml and can never remove from it, because a
world able to delete a base field would put desk's guarantees at the mercy of
each world — which is this repo's coupling problem aimed the other way.

relationship is the odd one and the reason the set is seven rather than six. It
is an edge among nodes, and it carries Card's rationale in a comment: the self
is a network of threads to different people, and we are different people in
different relationships.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Canon page parsing and validation

**Files:**
- Modify: `tools/canon.py` (append parsing, loading, validation, and a CLI)
- Test: `tools/tests/test_canon_validate.py`

**Interfaces:**
- Consumes: `canon.load_schema`, `canon.CanonError`, `world.load`.
- Produces: `canon.parse_page(path) -> (meta: dict, body: str)`; `canon.load_pages(world) -> list[(pathlib.Path, dict, str)]`; `canon.validate(pages, schema) -> list[str]` (empty list means valid).

**Note on the spec's example.** The spec illustrates per-direction fields as `[sable_to_toro]`, deriving a table name from two ids. That breaks on any id containing a hyphen, which `sable-toro` itself does. This task uses `[[direction]]` tables carrying explicit `from` and `to` keys instead. Same content, same "both halves in one file" guarantee, no name mangling. Flag this deviation when reporting the task complete.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_canon_validate.py`:

```python
import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon, world

CHARACTER = '+++\nkind = "character"\nid = "{id}"\nname = "{name}"\n+++\n\nProse.\n'


def make_world(d, pages):
    (pathlib.Path(d) / 'world.toml').write_text('title = "T"\n', encoding='utf-8')
    for name, text in pages.items():
        p = pathlib.Path(d) / 'content/canon' / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
    return world.load(d)


def errors_for(d, pages):
    w = make_world(d, pages)
    return canon.validate(canon.load_pages(w), canon.load_schema(w))


class TestValidate(unittest.TestCase):
    def test_a_valid_page_produces_no_errors(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A')}), [])

    def test_front_matter_must_be_toml_delimited_by_plus_signs(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'p.md'
            p.write_text('---\nkind: character\n---\n\nProse.\n', encoding='utf-8')
            with self.assertRaises(canon.CanonError):
                canon.parse_page(p)

    def test_body_survives_parsing(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'p.md'
            p.write_text(CHARACTER.format(id='a', name='A'), encoding='utf-8')
            meta, body = canon.parse_page(p)
            self.assertEqual(meta['id'], 'a')
            self.assertIn('Prose.', body)

    def test_missing_required_field_fails(self):
        with tempfile.TemporaryDirectory() as d:
            errs = errors_for(d, {'c/a.md': '+++\nkind = "character"\nid = "a"\n+++\n\nP.\n'})
            self.assertTrue(any('name' in e for e in errs), errs)

    def test_unknown_kind_fails(self):
        with tempfile.TemporaryDirectory() as d:
            errs = errors_for(d, {'c/a.md': '+++\nkind = "sandwich"\nid = "a"\nname = "A"\n+++\n\nP.\n'})
            self.assertTrue(any('sandwich' in e for e in errs), errs)

    def test_duplicate_ids_fail(self):
        with tempfile.TemporaryDirectory() as d:
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='dup', name='A'),
                                  'c/b.md': CHARACTER.format(id='dup', name='B')})
            self.assertTrue(any('dup' in e for e in errs), errs)

    def test_dangling_cross_reference_fails(self):
        with tempfile.TemporaryDirectory() as d:
            page = ('+++\nkind = "character"\nid = "a"\nname = "A"\n'
                    'factions = ["ghosts"]\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': page})
            self.assertTrue(any('ghosts' in e for e in errs), errs)

    def test_relationship_needs_exactly_two_members(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\nkind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a"]\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'), 'c/r.md': rel})
            self.assertTrue(any('two' in e for e in errs), errs)

    def test_relationship_between_must_resolve_to_characters(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\nkind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "ghost"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "ghost"\n\n'
                   '[[direction]]\nfrom = "ghost"\nto = "a"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'), 'c/r.md': rel})
            self.assertTrue(any('ghost' in e for e in errs), errs)

    def test_relationship_must_declare_both_directions(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\nkind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "b"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "b"\nnever_says = "his name"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                                  'c/b.md': CHARACTER.format(id='b', name='B'),
                                  'c/r.md': rel})
            self.assertTrue(any('direction' in e for e in errs), errs)

    def test_a_complete_relationship_validates(self):
        with tempfile.TemporaryDirectory() as d:
            rel = ('+++\nkind = "relationship"\nid = "r"\nname = "R"\n'
                   'between = ["a", "b"]\n\n'
                   '[[direction]]\nfrom = "a"\nto = "b"\nnever_says = "his first name"\n\n'
                   '[[direction]]\nfrom = "b"\nto = "a"\nregister = "over-explains"\n+++\n\nP.\n')
            errs = errors_for(d, {'c/a.md': CHARACTER.format(id='a', name='A'),
                                  'c/b.md': CHARACTER.format(id='b', name='B'),
                                  'c/r.md': rel})
            self.assertEqual(errs, [])


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `AttributeError: module 'canon' has no attribute 'parse_page'`

- [ ] **Step 3: Append parsing, validation and a CLI to `tools/canon.py`**

Add `import argparse`, `import re`, `import sys` to the imports, then append:

```python
FRONTMATTER = re.compile(r'\A\+\+\+[ \t]*\n(.*?)\n\+\+\+[ \t]*\n?', re.S)

# Fields that are structure rather than facts about the entity.
NOT_A_FACT = {'kind', 'id', 'name', 'direction'}


def parse_page(path):
    """A canon page: TOML front matter delimited `+++`, prose in the body."""
    raw = pathlib.Path(path).read_text(encoding='utf-8')
    m = FRONTMATTER.match(raw)
    if not m:
        raise CanonError(f"{path}: no `+++` TOML front matter")
    try:
        meta = tomllib.loads(m.group(1))
    except tomllib.TOMLDecodeError as e:
        raise CanonError(f"{path}: front matter: {e}") from None
    return meta, raw[m.end():]


def load_pages(world):
    """Every canon page under the world's canon directory, sorted by path."""
    if not world.canon.is_dir():
        raise CanonError(f"no canon directory at {world.canon}")
    pages = []
    for p in sorted(world.canon.rglob('*.md')):
        meta, body = parse_page(p)
        pages.append((p, meta, body))
    return pages


def _check_relationship(path, meta, errors):
    between = meta.get('between') or []
    if len(between) != 2:
        errors.append(f"{path}: relationship needs exactly two members in `between`, "
                      f"got {len(between)}")
        return
    want = {(between[0], between[1]), (between[1], between[0])}
    got = {(d.get('from'), d.get('to')) for d in (meta.get('direction') or [])}
    if got != want:
        errors.append(f"{path}: relationship must declare both directions "
                      f"{sorted(want)}; got {sorted(got)}")


def validate(pages, schema):
    """Every problem with this canon, as a list of strings. Empty means valid."""
    errors = []
    common = schema['common']['required']
    kinds = schema['kinds']
    seen = {}
    ids_by_kind = {}
    for path, meta, _ in pages:
        ids_by_kind.setdefault(meta.get('kind'), set()).add(meta.get('id'))

    for path, meta, _ in pages:
        for field in common:
            if field not in meta:
                errors.append(f"{path}: missing required field {field!r}")
        kind = meta.get('kind')
        pid = meta.get('id')
        if pid is not None:
            if pid in seen:
                errors.append(f"{path}: duplicate id {pid!r} (also in {seen[pid]})")
            else:
                seen[pid] = path
        if kind is None:
            continue
        if kind not in kinds:
            errors.append(f"{path}: unknown kind {kind!r}; schema declares "
                          f"{', '.join(sorted(kinds))}")
            continue
        spec = kinds[kind]
        for field in spec.get('required', []):
            if field not in meta:
                errors.append(f"{path}: {kind} missing required field {field!r}")
        for field, target in (spec.get('refs') or {}).items():
            value = meta.get(field)
            if value is None:
                continue
            for v in (value if isinstance(value, list) else [value]):
                if v not in ids_by_kind.get(target, set()):
                    errors.append(f"{path}: {field} -> {v!r} does not resolve to a {target}")
        if kind == 'relationship':
            _check_relationship(path, meta, errors)
    return errors


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--world', required=True, help='world root, or the world.toml itself')
    a = ap.parse_args()

    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import world as world_mod
    try:
        w = world_mod.load(a.world)
        pages = load_pages(w)
        errors = validate(pages, load_schema(w))
    except (CanonError, world_mod.WorldError) as e:
        sys.exit(f"canon: {e}")

    print(f"\n  CANON — {w.canon}  ({len(pages)} pages)")
    for e in errors:
        print(f"    x {e}")
    print(f"\n  {'FAIL' if errors else 'PASS'} — {len(errors)} finding(s)\n")
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 22 tests total, OK

- [ ] **Step 5: Commit**

```bash
git add tools/canon.py tools/tests/test_canon_validate.py
git commit -m "$(cat <<'EOF'
Validate canon pages: schema conformance, unique ids, live references

A canon page is Markdown with `+++` TOML front matter, which is one of Hugo's
native forms and parses from the stdlib with unambiguous types. That last part
matters for a file whose front matter is the typed fact store the continuity
gate reads.

Validation covers what a hand-maintained data file used to promise and never
delivered: required fields per kind, ids unique across the world, and every
cross-reference resolving to a page of the right kind. A relationship gets two
extra checks — exactly two members, and both directions declared — because a
relationship recording only one side is the flat default the kind exists to
prevent.

Deviation from the spec's illustration: per-direction fields use [[direction]]
tables with explicit from/to keys rather than a table name derived from two ids.
Deriving `sable_to_toro` breaks on any id containing a hyphen, and `sable-toro`
contains one.

Eleven tests.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Fact and name extraction from canon

**Files:**
- Modify: `tools/canon.py` (append two functions; wire them into `main`)
- Test: `tools/tests/test_canon_extract.py`

**Interfaces:**
- Consumes: `canon.load_pages`, `canon.validate`.
- Produces: `canon.facts(pages) -> list[dict]` with keys `entity`, `attribute`, `value`, `unit`, `chapter` — the shape `continuity.scan_facts` already keys on; `canon.names(pages) -> dict[str, list[str]]` mapping a character's name to the page ids carrying it.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_canon_extract.py`:

```python
import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import canon, world

PAGE = ('+++\nkind = "character"\nid = "a"\nname = "Ashgrove"\n'
        'pronouns = "they/them"\noccupation = "surveyor"\n'
        'factions = ["ghosts"]\n+++\n\nProse.\n')


def load(d, pages):
    (pathlib.Path(d) / 'world.toml').write_text('title = "T"\n', encoding='utf-8')
    for name, text in pages.items():
        p = pathlib.Path(d) / 'content/canon' / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding='utf-8')
    return canon.load_pages(world.load(d))


class TestExtract(unittest.TestCase):
    def test_scalar_fields_become_facts_keyed_by_page_id(self):
        with tempfile.TemporaryDirectory() as d:
            facts = canon.facts(load(d, {'a.md': PAGE}))
            pairs = {(f['entity'], f['attribute'], f['value']) for f in facts}
            self.assertIn(('a', 'pronouns', 'they/them'), pairs)
            self.assertIn(('a', 'occupation', 'surveyor'), pairs)

    def test_structure_and_collections_are_not_facts(self):
        with tempfile.TemporaryDirectory() as d:
            attrs = {f['attribute'] for f in canon.facts(load(d, {'a.md': PAGE}))}
            self.assertNotIn('kind', attrs)
            self.assertNotIn('id', attrs)
            self.assertNotIn('name', attrs)
            self.assertNotIn('factions', attrs)

    def test_facts_carry_the_keys_continuity_expects(self):
        with tempfile.TemporaryDirectory() as d:
            for f in canon.facts(load(d, {'a.md': PAGE})):
                self.assertEqual(set(f), {'entity', 'attribute', 'value', 'unit', 'chapter'})

    def test_names_come_from_character_pages_only(self):
        with tempfile.TemporaryDirectory() as d:
            place = '+++\nkind = "place"\nid = "p"\nname = "Ashfall"\n+++\n\nP.\n'
            names = canon.names(load(d, {'a.md': PAGE, 'p.md': place}))
            self.assertEqual(names, {'Ashgrove': ['a']})


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `AttributeError: module 'canon' has no attribute 'facts'`

- [ ] **Step 3: Append the extractors to `tools/canon.py`**

Insert before `def main():`:

```python
def facts(pages):
    """Scalar front-matter fields as a typed fact store, in continuity.py's shape.

    Collections are skipped: a list of factions is membership, not a single-valued fact, and
    feeding it to a contradiction check that keys on (entity, attribute) would report every
    multi-valued field as a conflict."""
    out = []
    for path, meta, _ in pages:
        entity = meta.get('id')
        for key, value in meta.items():
            if key in NOT_A_FACT or isinstance(value, (list, dict)):
                continue
            out.append({'entity': entity, 'attribute': key, 'value': value,
                        'unit': '', 'chapter': str(path)})
    return out


def names(pages):
    """Character names, mapped to the page ids that carry them."""
    out = {}
    for _, meta, _ in pages:
        if meta.get('kind') == 'character' and meta.get('name'):
            out.setdefault(meta['name'], []).append(meta.get('id'))
    return out
```

Then, in `main()`, add a summary line before the `FAIL`/`PASS` line:

```python
    print(f"    {len(facts(pages))} facts, {len(names(pages))} character names")
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 26 tests total, OK

- [ ] **Step 5: Commit**

```bash
git add tools/canon.py tools/tests/test_canon_extract.py
git commit -m "$(cat <<'EOF'
Extract facts and names from canon in the shape continuity.py keys on

Canon front matter is already a typed fact store; it only needed reading in the
shape scan_facts keys on — entity, attribute, value, unit, chapter. That removes
the parallel facts.json the earlier design carried, which was a second copy of
canon that somebody had to keep in step.

Collections are deliberately not facts. A list of factions is membership rather
than a single-valued attribute, and handing it to a check that reports any
(entity, attribute) key carrying two values would flag every multi-valued field
in canon as a contradiction.

Character names come out of the same pass, which is what dissolves the separate
used-names registry.

Four tests.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: `continuity.py --world`, and delete `names.json`

**Files:**
- Modify: `tools/continuity.py:36` (front matter), `tools/continuity.py:174-190` (CLI and sourcing), and `scan_facts`
- Delete: `names.json`
- Test: `tools/tests/test_continuity_world.py`

**Interfaces:**
- Consumes: `canon.load_pages`, `canon.facts`, `canon.names`, `world.load`.
- Produces: `continuity.scan_fact_list(facts: list[dict]) -> list[tuple]`; `continuity.scan_facts(path)` kept as a thin wrapper over it.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_continuity_world.py`:

```python
import pathlib, sys, tempfile, unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import continuity


class TestContinuityWorld(unittest.TestCase):
    def test_scan_fact_list_finds_a_key_with_two_values(self):
        facts = [{'entity': 'a', 'attribute': 'rank', 'value': 'captain', 'unit': '', 'chapter': 'x'},
                 {'entity': 'a', 'attribute': 'rank', 'value': 'ensign', 'unit': '', 'chapter': 'y'}]
        self.assertEqual(len(continuity.scan_fact_list(facts)), 1)

    def test_scan_fact_list_passes_a_consistent_store(self):
        facts = [{'entity': 'a', 'attribute': 'rank', 'value': 'captain', 'unit': '', 'chapter': 'x'},
                 {'entity': 'a', 'attribute': 'rank', 'value': 'captain', 'unit': '', 'chapter': 'y'}]
        self.assertEqual(continuity.scan_fact_list(facts), [])

    def test_plus_delimited_front_matter_is_stripped(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'ch01.md'
            p.write_text('+++\npov = "a"\n+++\n\nThe body.\n', encoding='utf-8')
            (name, text), = continuity.load(d)
            self.assertNotIn('pov', text)
            self.assertIn('The body.', text)

    def test_dash_delimited_front_matter_still_stripped(self):
        with tempfile.TemporaryDirectory() as d:
            p = pathlib.Path(d) / 'ch01.md'
            p.write_text('---\npov: a\n---\n\nThe body.\n', encoding='utf-8')
            (name, text), = continuity.load(d)
            self.assertNotIn('pov', text)
            self.assertIn('The body.', text)


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `AttributeError: module 'continuity' has no attribute 'scan_fact_list'`

- [ ] **Step 3: Modify `tools/continuity.py`**

Replace line 36:

```python
FRONTMATTER = re.compile(r'\A(?:---|\+\+\+)\s*\n.*?\n(?:---|\+\+\+)\s*\n', re.S)
```

Replace the body of `scan_facts` with a split:

```python
def scan_fact_list(facts):
    """A typed fact store: any (entity, attribute) with two values is a contradiction."""
    keyed = defaultdict(list)
    for f in facts:
        keyed[(str(f['entity']).strip().lower(), str(f['attribute']).strip().lower())].append(f)
    out = []
    for (e, a), rows in keyed.items():
        vals = {f"{str(r.get('value')).strip().lower()} {str(r.get('unit', '')).strip().lower()}".strip()
                for r in rows}
        if len(vals) > 1:
            out.append((e, a, sorted(vals), [r.get('chapter', '?') for r in rows]))
    return out


def scan_facts(path):
    return scan_fact_list(json.load(open(path)))
```

In `main()`, add the flag after `--names`:

```python
    ap.add_argument('--world', help='world root or world.toml; sources facts and names from canon')
```

and replace the fact/registry sourcing so explicit flags win:

```python
    a = ap.parse_args()

    chapters = load(a.manuscript)
    if not chapters:
        sys.exit(f'no chapters in {a.manuscript}')

    facts, registry, source = None, None, None
    if a.world:
        sys.path.insert(0, str(os.path.dirname(os.path.abspath(__file__))))
        import canon, world as world_mod
        try:
            w = world_mod.load(a.world)
            pages = canon.load_pages(w)
        except (canon.CanonError, world_mod.WorldError) as e:
            sys.exit(f"continuity: {e}")
        facts, registry, source = canon.facts(pages), canon.names(pages), str(w.canon)
    if a.facts:
        facts, source = json.load(open(a.facts)), a.facts
    if a.names:
        registry = json.load(open(a.names))
    fail = 0
```

Then replace the `if a.facts:` report block header so it scans the list rather than a path:

```python
    if facts is not None:
        conflicts = scan_fact_list(facts)
        print(f"\n  FACT STORE  ({'CONFLICTS' if conflicts else 'clean'} — {len(facts)} from {source})")
```

leaving the loop under it unchanged, and the `else:` branch unchanged.

Finally, relabel the reuse report, since with `--world` the registry is this world's canon rather than a previous book:

```python
        label = 'NAMES ALREADY IN CANON' if a.world and not a.names else 'CROSS-BOOK NAME REUSE'
        print(f"\n  {label}  ({len(reused)} matched)")
```

Delete `names.json`:

```bash
git rm names.json
```

- [ ] **Step 4: Run the test and a smoke check**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 30 tests total, OK

Then confirm the pre-existing path still works unchanged, against a real chapter:

```bash
T=$(mktemp -d); printf '%s\n' '---' 'pov: a' '---' '' 'Ash walked. Ash waited.' > "$T/ch01.md"
python3 tools/continuity.py "$T"; echo "exit=$?"; rm -rf "$T"
```

Expected: a scan report ending `PASS — 0 finding(s)` and `exit=0`. Pointing this at a directory
with no `.md` files exits 1 by design, so it must be given one.

- [ ] **Step 5: Commit**

```bash
git add tools/continuity.py tools/tests/test_continuity_world.py
git rm --cached names.json 2>/dev/null; rm -f names.json
git commit -m "$(cat <<'EOF'
continuity.py reads canon; names.json is deleted

--world sources both the fact store and the name registry from canon pages, so
the highest-yield check in the operation stops depending on somebody remembering
to merge a JSON file. Explicit --facts and --names still win when given, since a
per-wave invented.json is a different lifecycle from canon and both need to be
scannable.

names.json goes. It was per-book state living in shared infrastructure, and
every character page carries a name, so the registry was always a second copy of
something canon already knew. The report label changes with it: under --world
the registry is this world's canon rather than a previous book's names, and
calling that "cross-book reuse" would be a lie.

scan_facts splits into scan_fact_list plus a path wrapper, because canon
produces facts in memory and the old signature could only take a filename.

Front matter now strips either delimiter. Chapters keep --- and canon uses +++,
and a world that wants to unify may.

Four tests.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: TOML voice profile and `prose_audit.py --world`

**Files:**
- Create: `templates/voice-profile.toml`
- Delete: `templates/voice-profile.json`
- Modify: `tools/prose_audit.py:20` (front matter), `tools/prose_audit.py:358-367` (CLI and profile loading), `tools/idiolect_probe.py:25` (front matter)
- Test: `tools/tests/test_profile.py`

**Interfaces:**
- Consumes: `world.load`, `World.product`.
- Produces: `prose_audit.load_profile(path) -> dict` — the same nested dict shape the JSON profile produced, with keys `cadence`, `chapter_words`, `budgets`, `declared_refrains`, `narrators`, `screen`, `forbidden_image_bank`.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_profile.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `AttributeError: module 'prose_audit' has no attribute 'load_profile'`

- [ ] **Step 3: Write the TOML profile and the loader**

Create `templates/voice-profile.toml` — every `_comment` array from the JSON becomes a real comment:

```toml
# A voice constitution, specified where voice actually lives: syntax and cadence, not adjectives.
# Prose style sheets say "lucid, precise, unshowy"; four books obeyed that and came out identical.
# This file is the half a style sheet cannot express.
#
# Copy to <product>/editorial/voice-profile.toml, set the targets, then:
#   python3 <desk>/tools/prose_audit.py --world . --product <id>
#
# See method/07-voice-engineering.md for how to choose the numbers, and
# method/06-idiolect-ledger.md for what the inherited bans are and why they accumulate.

book = "TITLE"
inherits_ledger = "method/06-idiolect-ledger.md"
chapter_words = [2400, 3600]

# Phrases the style sheet deliberately repeats; the audit stops calling these refrains. Anything
# NOT listed here that recurs in three or more chapters is self-priming rather than craft. Each
# declared refrain must name its owner and its home chapter in the style sheet.
declared_refrains = []

# DIAGNOSTIC ONLY — never hand these to a drafting agent as a target. Tested: given numeric cadence
# targets, drafts came back rated 3.0/10 for quality and 8.7/10 for mannered, last of six by every
# judge ("you can hear the period key being pressed"). Use them to DETECT drift back to the
# median-11 default, then fix by rewriting the prose brief, never by asking for shorter sentences.
[cadence]
sentence_mean       = [14.0, 19.0]
sentence_median     = [9, 14]
sentence_p90        = [30, 45]
pct_very_short_le5  = [12.0, 26.0]
pct_long_ge40       = [5.0, 14.0]
long_then_short_rate = [20.0, 50.0]
dialogue_pct        = [6.0, 25.0]

# Instances per 10,000 words. Ceilings, not targets. These are the constraints that work: a
# prohibition leaves the solution unspecified so it must be invented, while a target names the
# solution so it can be complied with. Bans name a CONSTRUCTION, never a phrase — Sentience banned
# "I want to be precise about" and got true / clear / modest / careful instead. Run the
# measure-revise loop against these, never against the cadence block above.
[budgets]
"simile-frame:the-way-you"      = 8.0
"hedge:not-quite"               = 2.0
"hedge:want-to-be-X-about"      = 0.3
"hedge:X-is-the-only-Y"         = 0.5
"negate-then-correct"           = 4.0
"hard-cut:not-X-period-Y"       = 9.0
"summarizing-close:whole-of"    = 0.5
"deferred-appositive:which-was" = 6.0
"abstraction-reach:thing"       = 30.0
"abstraction-reach:something"   = 12.0
"abstraction-reach:kind-sort-of" = 8.0
"abstraction-reach:a-shape"     = 0.5
"causal-reflex:because"         = 30.0
"narrator-aside:of-course"      = 2.0
"filter-verbs"                  = 20.0
"emotion-named"                 = 8.0
"adverb:-ly"                    = 70.0
"epiphany:it-was-then"          = 0.0
"fancy-attribution"             = 1.0

# Per-narrator fingerprints, assigned BEFORE drafting and audited after (R15). Parallel drafting
# agents diverge on facts and converge on tics; the ledger defends the facts and this defends the
# voices. Give each narrator a syntactic habit, a metaphor domain it owns exclusively, a
# characteristic evasion, and one figure no other narrator may touch.
[narrators.NARRATOR_A]
syntax          = "long subordinated sentences that qualify themselves; rarely a fragment"
metaphor_domain = "instruments, measurement, calibration"
owns_figures    = ["the specific image only this narrator may use"]
forbidden_figures = ["figures owned by other narrators"]
evasion         = "what this narrator reaches for instead of saying the true thing"
sentence_median = [12, 18]

[narrators.NARRATOR_B]
syntax          = "parataxis; short declaratives joined by 'and'; fragments permitted"
metaphor_domain = "weather, animals, the body"
owns_figures    = []
forbidden_figures = []
evasion         = ""
sentence_median = [7, 11]

# The aridity screen (method/05). abstract_terms are THIS book's idea vocabulary; people are the
# characters whose presence anchors a scene. Both are product-specific — declare them or the
# screen is skipped.
[screen]
abstract_terms = ["consciousness", "identity", "substrate", "theorem", "proof", "experience",
                  "instance", "continuity", "subject", "argument", "structure", "measure"]
people     = ["CHARACTER_A", "CHARACTER_B"]
body_terms = []

# The most productive constraint in testing: forbid a whole metaphorical domain so the book's
# central conceits must be reinvented rather than retrieved. Name the domain this book OWNS and
# the domain it may not enter.
[forbidden_image_bank]
owns      = []
forbidden = []
```

Delete the JSON template:

```bash
git rm templates/voice-profile.json
```

In `tools/prose_audit.py`, replace line 20:

```python
FRONTMATTER = re.compile(r'\A(?:---|\+\+\+)\s*\n.*?\n(?:---|\+\+\+)\s*\n', re.S)
```

Add `import tomllib` to the imports, and add above `def main():`:

```python
def load_profile(path):
    """A voice profile is human-authored config, so it is TOML."""
    with open(path, 'rb') as fh:
        return tomllib.load(fh)
```

In `main()`, replace the `--profile` argument and the profile line:

```python
    ap.add_argument('dirs', nargs='*', help='manuscript director(ies)')
    ap.add_argument('--profile', help='voice profile TOML (budgets, cadence targets, refrains)')
    ap.add_argument('--world', help='world root or world.toml')
    ap.add_argument('--product', help='product id within --world')
    ap.add_argument('--json', action='store_true', help='emit machine-readable JSON')
    ap.add_argument('--refrain-n', type=int, default=6)
    ap.add_argument('--refrain-min', type=int, default=3)
    a = ap.parse_args()

    dirs, profile_path = list(a.dirs), a.profile
    if a.world:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import world as world_mod
        try:
            w = world_mod.load(a.world)
            p = w.product(a.product) if a.product else None
        except world_mod.WorldError as e:
            sys.exit(f"prose_audit: {e}")
        if p is None:
            sys.exit("prose_audit: --world requires --product")
        dirs.append(str(p.manuscript))
        profile_path = profile_path or str(p.editorial / 'voice-profile.toml')
    if not dirs:
        sys.exit("prose_audit: give a manuscript directory, or --world with --product")

    profile = load_profile(profile_path) if profile_path else {}
    declared = tuple(profile.get('declared_refrains', []))
```

and change the loop header from `for d in a.dirs:` to `for d in dirs:`.

In `tools/idiolect_probe.py`, replace line 25 with the same two-delimiter pattern:

```python
FRONTMATTER = re.compile(r'\A(?:---|\+\+\+)\s*\n.*?\n(?:---|\+\+\+)\s*\n', re.S)
```

- [ ] **Step 4: Run the tests and confirm the gate is unchanged**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 35 tests total, OK

Run: `python3 tools/idiolect_probe.py method/ | tail -3`
Expected: unchanged from before this task — `12 violation(s)`, exit 1. The front-matter change is a no-op on documents that have none.

- [ ] **Step 5: Commit**

```bash
git add templates/voice-profile.toml tools/prose_audit.py tools/idiolect_probe.py tools/tests/test_profile.py
git rm --cached templates/voice-profile.json 2>/dev/null; rm -f templates/voice-profile.json
git commit -m "$(cat <<'EOF'
Move the voice profile to TOML, and teach prose_audit.py --world

Config is human-owned and machine-read, so it is TOML. The voice profile is the
file this most improves: nine _comment keys and a 431-character escaped string
become real comments, and tomllib parses it from the stdlib so the rule that
tools/ takes no dependency survives.

Unambiguous types matter more here than readability. The profile's entire
content is numeric ceilings that gate a build, and YAML — the other candidate —
would read NO as false and 1.20 as a float. No book consumes the JSON form, so
removing it breaks no existing consumer.

--world plus --product resolves the manuscript directory and the profile from
the manifest, so no invocation needs to know a layout. An explicit --profile
still wins.

Both prose tools now strip either front-matter delimiter, which is a no-op on
every document in this repo and the thing that lets them read canon pages later.
Verified: idiolect_probe.py on method/ reports the same 12 violations as before.

Five tests.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: `tools/new_world.py`

**Files:**
- Create: `tools/new_world.py`
- Test: `tools/tests/test_new_world.py`

**Interfaces:**
- Consumes: `world.load`, `canon.load_pages`, `canon.load_schema`, `canon.validate`.
- Produces: `new_world.scaffold(path, title) -> pathlib.Path` (the world root); CLI `python3 tools/new_world.py PATH --title T`.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_new_world.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'new_world'`

- [ ] **Step 3: Write the implementation**

Create `tools/new_world.py`:

```python
#!/usr/bin/env python3
"""
new_world.py — scaffold a world that references desk.

Mechanical setup only. It creates the manifest, the canon skeleton and a Hugo config that mounts
desk's module, then prints the commands to run next. It drafts nothing and drives no stage.

    python3 tools/new_world.py PATH --title "Title"

Stdlib only.
"""
import argparse
import pathlib
import sys

MANIFEST = '''# The whole interface between this world and desk.
# Paths below are defaults; declare only what differs. Products are declared, never discovered.

title = "{title}"
desk  = "desk"
canon = "content/canon"

# [[products]]
# id   = "book-one"
# kind = "book"
# path = "books/book-one"
'''

HUGO = '''# Mounts desk's canon module. A world that renders no wiki can delete this file.
baseURL = "/"
title   = "{title}"

[[module.imports]]
path = "desk/hugo"
'''

CANON_DIRS = ('characters', 'places', 'factions', 'events', 'artifacts', 'terms', 'relationships')


def scaffold(path, title):
    root = pathlib.Path(path)
    if (root / 'world.toml').exists():
        sys.exit(f"new_world: {root / 'world.toml'} already exists; refusing to overwrite")
    for sub in CANON_DIRS:
        (root / 'content' / 'canon' / sub).mkdir(parents=True, exist_ok=True)
        (root / 'content' / 'canon' / sub / '.gitkeep').write_text('', encoding='utf-8')
    (root / 'world.toml').write_text(MANIFEST.format(title=title), encoding='utf-8')
    (root / 'hugo.toml').write_text(HUGO.format(title=title), encoding='utf-8')
    return root


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('path', help='directory to create the world in')
    ap.add_argument('--title', required=True)
    a = ap.parse_args()

    root = scaffold(a.path, a.title)
    print(f"""
created {root}/
  world.toml            the manifest desk reads
  hugo.toml             mounts desk/hugo
  content/canon/        canon pages: +++ TOML front matter, prose body

next:
  cd {root}
  git init && git submodule add <desk-remote> desk
  python3 desk/tools/new_book.py . --title "…" --slug book-one
  python3 desk/tools/canon.py --world .

then Stage 1, the spine, which is never delegated. See desk/method/00-starting-a-world.md.
""")


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 39 tests total, OK

- [ ] **Step 5: Commit**

```bash
git add tools/new_world.py tools/tests/test_new_world.py
git commit -m "$(cat <<'EOF'
Scaffold a world: manifest, canon skeleton, Hugo mount

The repo carried 39 rules and 12 pipeline stages and no way to start. This is
half the answer: mechanical setup, and the ordered commands printed rather than
run. It drafts nothing and drives no stage, which is piece 2's job.

The submodule command is printed rather than executed because it needs a remote
this script cannot know, and because a scaffold that silently runs git against a
directory the user just named is the wrong kind of helpful.

Tested by round-trip rather than by shape: the scaffold must load through
world.py and its empty canon must validate, which is a stronger assertion than
checking that files exist.

Four tests.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 8: `tools/new_book.py`

**Files:**
- Create: `tools/new_book.py`
- Test: `tools/tests/test_new_book.py`

**Interfaces:**
- Consumes: `world.load`, `new_world.scaffold` (tests only).
- Produces: `new_book.add(world_path, title, slug) -> pathlib.Path` (the product directory); CLI `python3 tools/new_book.py WORLD --title T --slug S`.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_new_book.py`:

```python
import pathlib, sys, tempfile, unittest
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
        with self.assertRaises(SystemExit):
            new_book.add(self.root, 'One Again', 'one')


if __name__ == '__main__':
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'new_book'`

- [ ] **Step 3: Write the implementation**

Create `tools/new_book.py`:

```python
#!/usr/bin/env python3
"""
new_book.py — add a book product to an existing world.

Copies desk's templates into the product's editorial directory, creates the manuscript directory,
and APPENDS a [[products]] table to world.toml. Appending at end of file is a text operation that
preserves every comment, which is how this respects the rule that no tool rewrites a config file.

    python3 tools/new_book.py WORLD --title "Title" --slug book-one

Stdlib only.
"""
import argparse
import pathlib
import shutil
import sys

TEMPLATES = pathlib.Path(__file__).resolve().parent.parent / 'templates'
COPY = ('voice-profile.toml', 'style-sheet.md', 'promise-ledger.md', 'critic-briefs.md')

STANZA = '''
[[products]]
id   = "{slug}"
kind = "book"
path = "{path}"
'''


def add(world_path, title, slug):
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import world as world_mod

    root = pathlib.Path(world_path)
    manifest = root / 'world.toml'
    if not manifest.is_file():
        sys.exit(f"new_book: no world manifest at {manifest}")
    if any(p.id == slug for p in world_mod.load(root).products):
        sys.exit(f"new_book: {slug!r} is already declared in {manifest}")

    rel = f"books/{slug}"
    product = root / rel
    (product / 'manuscript').mkdir(parents=True, exist_ok=True)
    editorial = product / 'editorial'
    editorial.mkdir(parents=True, exist_ok=True)
    for name in COPY:
        src = TEMPLATES / name
        if not src.is_file():
            sys.exit(f"new_book: missing template {src}")
        shutil.copyfile(src, editorial / name)

    with open(manifest, 'a', encoding='utf-8') as fh:
        fh.write(STANZA.format(slug=slug, path=rel))
    return product


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('world', help='world root, or the world.toml itself')
    ap.add_argument('--title', required=True)
    ap.add_argument('--slug', required=True)
    a = ap.parse_args()

    root = pathlib.Path(a.world)
    if root.name == 'world.toml':
        root = root.parent
    product = add(root, a.title, a.slug)
    print(f"""
created {product}/
  editorial/voice-profile.toml   set the cadence targets and inherit the budgets
  editorial/style-sheet.md       R9a, R10, R11: sentences and prohibitions, never moods
  editorial/promise-ledger.md
  editorial/critic-briefs.md     held fixed across products; editing it makes yields incomparable
  manuscript/

declared in {root / 'world.toml'}

next:
  1. Stage 1, the spine. Never delegated. Gate: back-cover copy and last line exist.
  2. python3 {pathlib.Path(__file__).parent}/canon.py --world {root}
""")


if __name__ == '__main__':
    main()
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 44 tests total, OK

- [ ] **Step 5: Commit**

```bash
git add tools/new_book.py tools/tests/test_new_book.py
git commit -m "$(cat <<'EOF'
Add a book product to a world, by appending to the manifest

Config is human-owned and no tool rewrites it. Round-tripping TOML while
preserving comments needs a third-party library and would break the stdlib-only
rule, so this appends a [[products]] table at end of file instead — a text
operation that cannot disturb a single comment above it. A test asserts the
manifest after the append still starts with exactly the bytes that were there
before.

Templates are copied rather than referenced, because a product's voice profile
diverges from the template the moment it inherits a budget and tightens one.
critic-briefs.md is the exception in spirit: it is copied so it travels, and it
is held fixed across products because an instrument that changes between
measurements measures nothing.

Five tests.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 9: The Hugo module

**Files:**
- Create: `hugo/go.mod`, `hugo/config.toml`
- Create: `hugo/archetypes/{character,place,faction,event,artifact,term,relationship}.md`
- Create: `hugo/layouts/canon/single.html`, `hugo/layouts/canon/list.html`
- Create: `hugo/layouts/shortcodes/{canonref,facts}.html`
- Create: `hugo/layouts/partials/facts.html`
- Test: `tools/tests/test_hugo_module.py`

**Interfaces:**
- Consumes: `canon.parse_page`, `canon.load_schema`.
- Produces: no Python API. The test asserts each archetype's front matter parses as TOML and carries every field its kind requires.

- [ ] **Step 1: Write the failing test**

Create `tools/tests/test_hugo_module.py`:

```python
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
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: FAIL — `FileNotFoundError` or an assertion naming the missing `hugo/archetypes`.

- [ ] **Step 3: Write the module**

`hugo/go.mod`:

```
module github.com/ottoquill/desk/hugo
```

`hugo/config.toml`:

```toml
# Mounted by a world's hugo.toml. Canon pages live under content/canon and render with the canon
# layouts; a world that wants its own look overrides them in the usual Hugo way.

[[module.mounts]]
source = "layouts"
target = "layouts"

[[module.mounts]]
source = "archetypes"
target = "archetypes"
```

`hugo/archetypes/character.md`:

```markdown
+++
kind       = "character"
id         = "{{ .Name }}"
name       = ""
pronouns   = ""
occupation = ""
factions   = []
+++

Prose. What this person is like to be in a room with.
```

`hugo/archetypes/place.md`:

```markdown
+++
kind     = "place"
id       = "{{ .Name }}"
name     = ""
region   = ""
factions = []
+++

Prose.
```

`hugo/archetypes/faction.md`:

```markdown
+++
kind    = "faction"
id      = "{{ .Name }}"
name    = ""
seat    = ""
founded = ""
+++

Prose.
```

`hugo/archetypes/event.md`:

```markdown
+++
kind         = "event"
id           = "{{ .Name }}"
name         = ""
when         = ""
where        = ""
participants = []
+++

Prose.
```

`hugo/archetypes/artifact.md`:

```markdown
+++
kind    = "artifact"
id      = "{{ .Name }}"
name    = ""
origin  = ""
held_by = ""
+++

Prose.
```

`hugo/archetypes/term.md`:

```markdown
+++
kind    = "term"
id      = "{{ .Name }}"
name    = ""
aliases = []
+++

Prose.
```

`hugo/archetypes/relationship.md` — both directions present from the start, since a relationship
recording one side is the flat default the kind exists to prevent:

```markdown
+++
kind    = "relationship"
id      = "{{ .Name }}"
name    = ""
between = ["", ""]

# Behavioural, never adjectival. "Warm but guarded" is the specification four style sheets proved
# inert. What earns a slot: what A never says to B, which register A drops, who may interrupt
# whom, which topic A routes around, whose sentences shorten.
[[direction]]
from          = ""
to            = ""
never_says    = ""
register      = ""
routes_around = []

[[direction]]
from          = ""
to            = ""
never_says    = ""
register      = ""
routes_around = []
+++

Prose. What is between them, and what changed.
```

`hugo/layouts/canon/single.html`:

```html
{{ define "main" }}
<article class="canon canon--{{ .Params.kind }}">
  <h1>{{ .Params.name | default .Title }}</h1>
  <p class="canon__kind">{{ .Params.kind }}</p>
  {{ partial "facts.html" . }}
  <div class="canon__body">{{ .Content }}</div>
</article>
{{ end }}
```

`hugo/layouts/canon/list.html`:

```html
{{ define "main" }}
<h1>{{ .Title }}</h1>
<ul class="canon__index">
  {{ range .Pages.ByTitle }}
  <li><a href="{{ .RelPermalink }}">{{ .Params.name | default .Title }}</a>
      <span class="canon__kind">{{ .Params.kind }}</span></li>
  {{ end }}
</ul>
{{ end }}
```

`hugo/layouts/shortcodes/canonref.html` — a cross-reference by canon id:

```html
{{- $id := .Get 0 -}}
{{- $target := index (where (where site.RegularPages "Section" "canon") "Params.id" $id) 0 -}}
{{- with $target -}}
<a class="canonref" href="{{ .RelPermalink }}">{{ .Params.name | default .Title }}</a>
{{- else -}}
<span class="canonref canonref--dangling" title="no canon page with id {{ $id }}">{{ $id }}</span>
{{- end -}}
```

`hugo/layouts/shortcodes/facts.html` — the front matter as a table:

```html
<table class="facts">
  {{ range $k, $v := .Page.Params }}
    {{ if not (in (slice "kind" "id" "name" "direction" "title" "date" "draft") $k) }}
  <tr><th>{{ $k }}</th><td>{{ delimit ($v | slice | first 1) "" | default $v }}</td></tr>
    {{ end }}
  {{ end }}
</table>
```

Also create `hugo/layouts/partials/facts.html` with the same body as the shortcode, so
`canon/single.html` can call it as a partial.

- [ ] **Step 4: Run the test to verify it passes**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 49 tests total, OK

- [ ] **Step 5: Commit**

```bash
git add hugo tools/tests/test_hugo_module.py
git commit -m "$(cat <<'EOF'
Ship the Hugo module: archetypes, layouts, shortcodes

A Hugo theme is world-independent and reusable — it carries no world's nouns and
every world with a wiki wants the same layouts — so it belongs in desk even
though a world shipping only a game will never mount it. "Optional for a given
world" is a different test from "world-specific", and an earlier draft of the
spec conflated them and ruled Hugo out on the wrong grounds.

The archetypes are the interesting part, because they are checked. Each one must
parse as TOML and carry every field its kind requires, asserted against the same
schema canon.py validates against, so an archetype cannot drift from the schema
without a test failing. The relationship archetype ships both direction tables
already present: a relationship recording one side is exactly the flat default
the kind exists to prevent, and an archetype that made the second one optional
would invite it.

Five tests.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 10: `method/00-starting-a-world.md`

**Files:**
- Create: `method/00-starting-a-world.md`
- Modify: `method/README.md` (add the row to the table of documents)

**Interfaces:**
- Consumes: every CLI built in Tasks 1–9.
- Produces: prose only.

- [ ] **Step 1: Write the document**

Create `method/00-starting-a-world.md`. It must contain, in order: what a world is and what desk is; adding desk as a submodule; `new_world.py`; canon and the page shape; `new_book.py`; then the ordered path from concept to draft naming the gate command at each stage, drawn from `03-the-pipeline.md` Stages 1 through 5. Wrap at 100 columns. Every command must be one that exists after Tasks 1–9 — verify each by running `--help` before writing it down.

Include this table, since it is the part a reader needs most:

```markdown
| Stage | What happens | The gate |
|---|---|---|
| 0 · Inherit | `new_world.py`, then `new_book.py` | the profile inherits every prior ban and tightens one |
| 1 · The spine | premise, argument, ending, refusals. Never delegated | back-cover copy and the last line exist |
| 2 · Canon and outline | canon pages, machine-readable outline | `python3 desk/tools/canon.py --world .` returns zero |
| 4 · Wave drafting | chapters in waves, in the reader's ignorance | `python3 desk/tools/continuity.py <ms> --world .` returns zero |
| 5 · Post-wave audit | after each wave, never at book end | `python3 desk/tools/idiolect_probe.py <ms>` exits zero |
```

- [ ] **Step 2: Verify every command in the document runs**

For each command in the file, run its `--help` and confirm the flags match:

```bash
python3 tools/new_world.py --help && python3 tools/new_book.py --help \
  && python3 tools/canon.py --help && python3 tools/continuity.py --help \
  && python3 tools/prose_audit.py --help && python3 tools/idiolect_probe.py --help
```

Expected: six usage blocks, no traceback, and every flag used in the document present in one of them.

- [ ] **Step 3: Run the gate on the new prose**

Run: `python3 tools/idiolect_probe.py method/00-starting-a-world.md`
Expected: `clean.`, exit 0. If it reports a construction over budget, rewrite the sentence — do not adjust a budget.

- [ ] **Step 4: Add the row to `method/README.md`**

In the table of method documents, add as the first row:

```markdown
| [00 · Starting a World](00-starting-a-world.md) | The entry point. Submodule, manifest, canon, first product, and the ordered path from concept to draft with the gate at each stage. |
```

- [ ] **Step 5: Commit**

```bash
git add method/00-starting-a-world.md method/README.md
git commit -m "$(cat <<'EOF'
Add the entry point the repo never had

Grepping this repo for how to start a book returned three incidental phrases.
Stage 0 said a book begins by pulling from desk and listed what it pulls, and no
procedure anywhere followed it — 39 rules, 12 stages, a 10,000-line research
library, and no first step.

This is the first step, and every command in it was run before it was written
down. The stage table gives each stage its gate as a command rather than as a
description, because a gate stated in prose is the thing R28 exists to catch: a
plan is not a revision, and a stage is not passed until the detector says so.

Clean against the gate.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

### Task 11: Decouple the docs

**Files:**
- Modify: `method/README.md`, `method/03-the-pipeline.md`, `method/05-instruments.md`, `method/06-idiolect-ledger.md`, `templates/style-sheet.md`, `templates/promise-ledger.md`, `templates/critic-briefs.md`, `tools/idiolect_probe.py` (docstring), `tools/prose_audit.py` (docstring), `tools/continuity.py` (docstring), `CLAUDE.md`

**Interfaces:**
- Consumes: nothing.
- Produces: prose only.

- [ ] **Step 1: Find every coupled path**

Run:

```bash
grep -rn "<book>/\|desk/tools/\|desk/method/\|voice-profile\.json" \
  --include='*.md' --include='*.py' --include='*.json' . | grep -v '^./docs/'
```

Expected: a list of every line to change. Record the count before editing.

- [ ] **Step 2: Rewrite each occurrence world-relative**

Apply these substitutions by hand, reading each line in context rather than running a blind
`sed` — several are inside prose sentences that need rewording, not just a path swap:

- `<book>/manuscript` becomes `<product>/manuscript`, and where an invocation is shown, prefer
  `--world . --product <id>`.
- `<book>/editorial/voice-profile.json` becomes `<product>/editorial/voice-profile.toml`.
- `desk/tools/X.py` becomes `<desk>/tools/X.py` in prose, or a bare `tools/X.py` where the command
  is being run from inside this repo.
- `desk/method/NN-*.md` becomes `method/NN-*.md`.
- Any sentence asserting that desk sits alongside a book is rewritten to say a world references
  desk as a submodule.

In `CLAUDE.md`, replace the sentence beginning "It is checked out alongside a book" in the
**What this repository is** section with:

```markdown
A world repo references `desk/` as a git submodule and declares itself in `world.toml`; desk reads
that manifest and learns nothing else about the world. Invocations take `--world` and `--product`
rather than assuming a layout.
```

and add to the **Commands** block:

```bash
# The world contract. Every tool reaches a world through the manifest.
python3 tools/world.py --help          # loader; used by the tools below
python3 tools/canon.py --world <world>
python3 tools/new_world.py <path> --title "…"
python3 tools/new_book.py <world> --title "…" --slug <slug>
```

- [ ] **Step 3: Verify no coupled path survives**

Run:

```bash
grep -rn "<book>/\|voice-profile\.json" --include='*.md' --include='*.py' --include='*.json' . \
  | grep -v '^./docs/'
```

Expected: no output. Design documents under `docs/` keep their historical text and are excluded
deliberately — a spec records what was decided when, and editing it to match later work destroys
that.

- [ ] **Step 4: Run the full suite and the gate**

Run: `python3 -m unittest discover -s tools/tests -t . -v`
Expected: PASS — 49 tests, OK

Run: `python3 tools/idiolect_probe.py CLAUDE.md`
Expected: `clean.`, exit 0

Run: `python3 tools/idiolect_probe.py method/ | tail -2`
Expected: the same violation count as recorded in `method/README.md`'s closing section. If it
changed, the edits altered the prose enough to move a rate — update that section's numbers in the
same commit rather than leaving the recorded figure wrong.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "$(cat <<'EOF'
Decouple the docs from any book's layout

Path coupling to <book>/manuscript and desk/tools ran through thirteen files,
including all four templates, and it encoded an arrangement that is now wrong:
desk is not checked out alongside a book, it is referenced from a world as a
submodule. Invocations take --world and --product and assume nothing.

Design documents under docs/ are deliberately excluded. A spec records what was
decided and when, and editing it to match later work destroys the record.

Full suite green, CLAUDE.md clean against the gate, and method/'s recorded
violation count re-checked rather than assumed.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Verification

After Task 11, the whole thing should stand up end to end. Run this from the repo root:

```bash
set -e
python3 -m unittest discover -s tools/tests -t . -q
T=$(mktemp -d)
python3 tools/new_world.py "$T/w" --title "Smoke World"
python3 tools/new_book.py "$T/w" --title "Smoke Book" --slug smoke
cat > "$T/w/content/canon/characters/a.md" <<'EOF'
+++
kind = "character"
id   = "a"
name = "Aleph"
+++
Prose.
EOF
cat > "$T/w/content/canon/characters/b.md" <<'EOF'
+++
kind = "character"
id   = "b"
name = "Bet"
+++
Prose.
EOF
cat > "$T/w/content/canon/relationships/ab.md" <<'EOF'
+++
kind    = "relationship"
id      = "a-b"
name    = "Aleph and Bet"
between = ["a", "b"]

[[direction]]
from = "a"
to   = "b"
never_says = "her name"

[[direction]]
from = "b"
to   = "a"
register = "over-explains"
+++
Prose.
EOF
python3 tools/canon.py --world "$T/w"
echo "smoke OK"
rm -rf "$T"
```

Expected: the suite passes, the scaffolds run, `canon.py` reports `PASS — 0 finding(s)` and exits 0, and `smoke OK` prints.
