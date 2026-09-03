#!/usr/bin/env python3
"""
canon.py — validate a world's canon and extract what the other instruments need.

Canon is Markdown in Hugo's native shape: TOML front matter carrying the checkable facts, prose in
the body carrying the lore. One artifact, three consumers — Hugo renders it, this script checks it,
and continuity.py reads the front matter as a typed fact store.

Canon pages are read from the world's canon directory. Files whose names begin with an underscore
are skipped — these are Hugo section metadata (_index.md) and branch-bundle configuration, not canon
pages themselves.

    python3 tools/canon.py --world PATH

Stdlib only. Requires Python 3.11+ for tomllib.
"""
import argparse
import pathlib
import re
import sys
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
            # A world writing `required = "when"` where the base holds a list used to fall through
            # to the scalar branch and REPLACE the list, after which every page reported a missing
            # field named 'w', 'h', 'e', 'n'; `refs = "place"` blew up with AttributeError instead.
            if key in base and not isinstance(value, type(base[key])):
                raise CanonError(
                    f"{kind}.{key}: the base schema holds a {type(base[key]).__name__} here, "
                    f"the world declares a {type(value).__name__} ({value!r})"
                )
            if isinstance(value, list):
                base[key] = sorted(set(base.get(key, [])) | set(value))
            elif isinstance(value, dict):
                # refs merge: add new fields, reject redirects, allow identical redeclarations
                base_dict = base.setdefault(key, {})
                for field, target in value.items():
                    if field in base_dict and base_dict[field] != target:
                        raise CanonError(
                            f"{kind}.{key}.{field}: world tried to change target from "
                            f'"{base_dict[field]}" to "{target}"'
                        )
                    base_dict[field] = target
            else:
                base[key] = value
    return schema


FRONTMATTER = re.compile(r'\A\+\+\+[ \t]*\n(.*?)\n\+\+\+[ \t]*\n?', re.S)

# Fields that are structure rather than facts about the entity.
NOT_A_FACT = {'canon_kind', 'id', 'name', 'direction'}


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
        # Skip underscore-prefixed files — these are Hugo section metadata, not canon pages
        if p.name.startswith('_'):
            continue
        meta, body = parse_page(p)
        pages.append((p, meta, body))
    return pages


# An unfilled slot, not a reference. desk's own archetypes ship `origin = ""` and `factions = []`,
# so without this a page made from desk's archetype fails desk's own validator as a dangling ref.
def _is_empty(value):
    return value is None or value == '' or value == []


def _check_refs(path, field, target, value, ids_by_kind, errors):
    """Every id in a ref field resolves to a page of the target kind.

    A gate must not crash on the material it gates: a field holding a TOML table used to raise
    `TypeError: unhashable type: 'dict'` out of the membership test, killing the whole run on one
    malformed page. Wrong types are reported as findings like any other."""
    if _is_empty(value):
        return
    for v in (value if isinstance(value, list) else [value]):
        if isinstance(v, (dict, list)):
            shape = 'table' if isinstance(v, dict) else 'list'
            errors.append(f"{path}: {field} holds a {shape} where an id was expected; "
                          f"a reference is an id or a list of ids")
        elif _is_empty(v):
            continue
        elif v not in ids_by_kind.get(target, set()):
            errors.append(f"{path}: {field} -> {v!r} does not resolve to a {target}")


def _check_relationship(path, meta, errors):
    between = meta.get('between') or []
    if not isinstance(between, list) or len(between) != 2:
        errors.append(f"{path}: relationship needs exactly two members in `between`, "
                      f"got {between!r}")
        return
    if not all(isinstance(m, str) for m in between):
        errors.append(f"{path}: relationship `between` holds two ids; got {between!r}")
        return
    directions = meta.get('direction') or []
    if not isinstance(directions, list) or not all(isinstance(d, dict) for d in directions):
        errors.append(f"{path}: relationship `direction` is a list of tables; "
                      f"got {directions!r}")
        return
    got = set()
    for d in directions:
        frm, to = d.get('from'), d.get('to')
        if not isinstance(frm, str) or not isinstance(to, str):
            errors.append(f"{path}: relationship `direction` needs a string `from` and `to`; "
                          f"got {frm!r} -> {to!r}")
            return
        got.add((frm, to))
    want = {(between[0], between[1]), (between[1], between[0])}
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
        ids_by_kind.setdefault(meta.get('canon_kind'), set()).add(meta.get('id'))

    for path, meta, _ in pages:
        for field in common:
            if field not in meta:
                errors.append(f"{path}: missing required field {field!r}")
        kind = meta.get('canon_kind')
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
            _check_refs(path, field, target, meta.get(field), ids_by_kind, errors)
        if kind == 'relationship':
            _check_relationship(path, meta, errors)
    return errors


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
            # Convert non-JSON-serializable types. Numbers pass through unchanged because the
            # contradiction check depends on numeric equality (two spellings of the same number
            # must compare equal, and stringifying would break that).
            if isinstance(value, (str, int, float, bool)):
                converted = value
            elif hasattr(value, 'isoformat'):
                converted = value.isoformat()
            else:
                converted = str(value)
            out.append({'entity': entity, 'attribute': key, 'value': converted,
                        'unit': '', 'chapter': str(path)})
    return out


def names(pages):
    """Character names, mapped to the page ids that carry them."""
    out = {}
    for _, meta, _ in pages:
        if meta.get('canon_kind') == 'character' and meta.get('name'):
            out.setdefault(meta['name'], []).append(meta.get('id'))
    return out


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
    print(f"    {len(facts(pages))} facts, {len(names(pages))} character names")
    print(f"\n  {'FAIL' if errors else 'PASS'} — {len(errors)} finding(s)\n")
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
