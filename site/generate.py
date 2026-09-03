#!/usr/bin/env python3
"""Generate the Hugo content tree for ottoquill.com out of desk's own documents.

The documents under method/ and templates/ are the source of truth and are never
modified here. This mirrors them into site/content/ (gitignored) and, for each page:

  1. lifts the first `# H1` into a frontmatter `title`, which hugo-book uses for the
     sidebar, the menu and <title>. The H1 stays in the body, because the theme
     renders no title of its own and removing it would leave the page headless;
  2. derives `weight` from a leading `NN-` in the filename, so 00 … 07 keep the order
     the argument was written in rather than sorting alphabetically by title;
  3. renames each directory's README.md to _index.md, making it that section's
     landing page;
  4. rewrites every relative link. A link to another published page becomes its site
     URL; a link to a repo file that is not published — tools/*.py, canon/schema.toml —
     becomes a link into GitHub, because the method documents cite the code constantly
     and dropping those links would strip the argument of its evidence.

Stdlib only, per the repo's convention that a subagent with no environment can run
the tooling.
"""

import os
import posixpath
import re
import shutil
import sys

SITE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(SITE)
OUT = os.path.join(SITE, "content")
PAGES = os.path.join(SITE, "pages")

BLOB = "https://github.com/ottoquill/desk/blob/main/"

# (source, destination under content/). A source directory is mirrored whole; a
# source file lands at exactly the destination named.
SOURCES = [
    ("method", "method"),
    ("templates", "desk/templates"),
    ("README.md", "desk/_index.md"),
]

LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(\s+\"[^\"]*\")?\)")

# The corpus writes placeholders as <product>, <emotion>, <beat-id>. Outside a code
# span a renderer reads those as HTML: goldmark drops them silently, so the rule
# "'[pronoun] was/felt <emotion>' outside quoted monologue" would publish as "'[pronoun]
# was/felt ' outside quoted monologue" — a corrupted rule that still reads as prose.
# Escaping them here keeps the documents themselves untouched, which is the point of
# generating rather than editing. <sub> is real formatting and carries the attribution
# on 440 research entries, so it is kept.
KEEP_HTML = {"sub", "/sub"}
PSEUDO_TAG = re.compile(r"<(/?[a-z][a-z0-9 _-]*)>", re.IGNORECASE)
FENCE = re.compile(r"^\s*```", re.MULTILINE)
CODE_SPAN = re.compile(r"`[^`]*`")


def escape_pseudo_tags(text):
    """Escape angle-bracket placeholders, leaving code and real formatting alone."""

    def in_prose(chunk):
        def one(match):
            if match.group(1).lower() in KEEP_HTML:
                return match.group(0)
            return "&lt;%s&gt;" % match.group(1)

        # Protect inline code spans, which may themselves span a line break.
        parts, last = [], 0
        for span in CODE_SPAN.finditer(chunk):
            parts.append(PSEUDO_TAG.sub(one, chunk[last:span.start()]))
            parts.append(span.group(0))
            last = span.end()
        parts.append(PSEUDO_TAG.sub(one, chunk[last:]))
        return "".join(parts)

    # Odd-indexed segments are inside fenced blocks and are left verbatim.
    segments = FENCE.split(text)
    return "".join(seg if i % 2 else in_prose(seg) for i, seg in enumerate(segments))
H1 = re.compile(r"^# (.+?)\s*$", re.MULTILINE)
NUMBERED = re.compile(r"^(\d+)-")


def dest_for(src_rel, dest_root):
    """Map a source path relative to its source root onto a content/ path."""
    base = posixpath.basename(src_rel)
    if base == "README.md":
        parent = posixpath.dirname(src_rel)
        return posixpath.join(dest_root, parent, "_index.md") if parent else posixpath.join(dest_root, "_index.md")
    return posixpath.join(dest_root, src_rel)


def url_for(dest_rel):
    """The site URL a content/ path will be served at."""
    if dest_rel.endswith("/_index.md"):
        return "/" + dest_rel[: -len("/_index.md")].lower() + "/"
    if dest_rel == "_index.md":
        return "/"
    return "/" + dest_rel[: -len(".md")].lower() + "/"


def collect():
    """Every (repo-relative source, content-relative destination) pair to publish."""
    pairs = []
    for source, dest_root in SOURCES:
        abs_source = os.path.join(REPO, source)
        if os.path.isfile(abs_source):
            pairs.append((source, dest_root))
            continue
        for dirpath, dirnames, filenames in os.walk(abs_source):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "_")))
            for name in sorted(filenames):
                if not name.endswith(".md") or name == "CLAUDE.md":
                    continue
                abs_file = os.path.join(dirpath, name)
                within = os.path.relpath(abs_file, abs_source).replace(os.sep, "/")
                pairs.append((posixpath.join(source, within), dest_for(within, dest_root)))
    return pairs


def build_url_map(pairs):
    """Repo-relative path -> site URL, for files and for the directories they head."""
    urls = {}

    # Directories first, so a file's own mapping wins over its parent's if they collide.
    # A source directory is a section on the site whether or not it carries a README:
    # ensure_sections() gives the ones that don't an index page, and a link to
    # templates/ must reach /desk/templates/ rather than falling through to GitHub.
    for source, dest_root in SOURCES:
        abs_source = os.path.join(REPO, source)
        if not os.path.isdir(abs_source):
            continue
        for dirpath, dirnames, _ in os.walk(abs_source):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith((".", "_")))
            within = os.path.relpath(dirpath, abs_source).replace(os.sep, "/")
            src_dir = source if within == "." else posixpath.join(source, within)
            dest_dir = dest_root if within == "." else posixpath.join(dest_root, within)
            url = "/" + dest_dir.lower() + "/"
            urls[src_dir] = url
            urls[src_dir + "/"] = url

    for src_rel, dest_rel in pairs:
        url = url_for(dest_rel)
        urls[src_rel] = url
        if posixpath.basename(src_rel) == "README.md":
            parent = posixpath.dirname(src_rel)
            urls[parent] = url
            urls[parent + "/"] = url
    return urls


def rewrite_links(body, src_dir, urls, warnings):
    def replace(match):
        bang, text, target, title = match.group(1), match.group(2), match.group(3), match.group(4) or ""
        if re.match(r"^([a-z][a-z0-9+.-]*:|/|#)", target, re.IGNORECASE):
            return match.group(0)  # external, already absolute, or a bare anchor
        path_part, _, anchor = target.partition("#")
        anchor = "#" + anchor if anchor else ""
        if not path_part:
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(src_dir, path_part))
        if resolved.startswith(".."):
            warnings.append(f"link escapes the repository: {target}")
            return text
        if resolved in urls:
            return f"{bang}[{text}]({urls[resolved]}{anchor}{title})"
        if path_part.endswith("/") and resolved + "/" in urls:
            return f"{bang}[{text}]({urls[resolved + '/']}{anchor}{title})"
        if os.path.exists(os.path.join(REPO, resolved)):
            suffix = "/" if os.path.isdir(os.path.join(REPO, resolved)) else ""
            return f"{bang}[{text}]({BLOB}{resolved}{suffix}{anchor}{title})"
        warnings.append(f"link resolves to nothing: {target} (from {src_dir or '.'})")
        return text

    return LINK.sub(replace, body)


def frontmatter(title, weight):
    lines = ["---", "title: %s" % _yaml_scalar(title)]
    if weight is not None:
        lines.append("weight: %d" % weight)
    lines += ["---", ""]
    return "\n".join(lines)


def _yaml_scalar(text):
    return '"%s"' % text.replace("\\", "\\\\").replace('"', '\\"')


def humanize(slug):
    return NUMBERED.sub("", slug).replace("-", " ").replace("_", " ").title()


def ensure_sections(root):
    """Hugo does not promote a bare directory to a section; every one needs an index."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(dirnames)
        if dirpath == root or "_index.md" in filenames:
            continue
        name = os.path.basename(dirpath)
        with open(os.path.join(dirpath, "_index.md"), "w", encoding="utf-8") as handle:
            handle.write(frontmatter(humanize(name), None))


def main():
    pairs = collect()
    urls = build_url_map(pairs)
    warnings = []

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    for src_rel, dest_rel in pairs:
        with open(os.path.join(REPO, src_rel), encoding="utf-8") as handle:
            raw = handle.read()
        match = H1.search(raw)
        title = re.sub(r"[*`_]", "", match.group(1)).strip() if match else humanize(
            posixpath.basename(src_rel)[: -len(".md")]
        )
        number = NUMBERED.match(posixpath.basename(src_rel))
        weight = int(number.group(1)) if number else None
        body = escape_pseudo_tags(rewrite_links(raw, posixpath.dirname(src_rel), urls, warnings))

        dest = os.path.join(OUT, dest_rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as handle:
            handle.write(frontmatter(title, weight) + body)

    # Hand-written pages that are the site's own, not desk's: the landing page and
    # anything else that belongs to the website rather than to the method.
    if os.path.isdir(PAGES):
        for dirpath, _, filenames in os.walk(PAGES):
            for name in sorted(filenames):
                if not name.endswith(".md"):
                    continue
                within = os.path.relpath(os.path.join(dirpath, name), PAGES)
                dest = os.path.join(OUT, within)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(os.path.join(dirpath, name), dest)

    ensure_sections(OUT)

    for warning in dict.fromkeys(warnings):
        print("warning: %s" % warning, file=sys.stderr)
    print("generated %d pages -> site/content/" % len(pairs))


if __name__ == "__main__":
    main()
