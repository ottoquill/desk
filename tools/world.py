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
