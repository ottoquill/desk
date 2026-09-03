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
