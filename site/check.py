#!/usr/bin/env python3
"""Build the site and verify every internal link resolves. This is the gate.

Hugo does not validate internal links: it renders a link to /method/does-not-exist
without complaint, so a renamed page 404s in production and nothing says so. Every
mature site in this family carries a check of its own for that reason.

Two lessons are already paid for elsewhere and are honoured here:

  * `hugo --minify` strips quotes from attributes, so an extractor matching only
    href="..." reports a clean site while checking nothing. Unquoted values are
    matched too;
  * a checker that finds zero references is broken, not passing. Finding none is a
    failure.

Usage:  python3 site/check.py            generate, build, check
        python3 site/check.py --no-build check the existing public/ tree
"""

import os
import re
import subprocess
import sys
from urllib.parse import unquote, urlparse

SITE = os.path.dirname(os.path.abspath(__file__))
PUBLIC = os.path.join(SITE, "public")

# Quoted or unquoted, since --minify drops the quotes.
REF = re.compile(
    r"""(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+))""",
    re.IGNORECASE,
)
MINIMUM_REFERENCES = 50


def build():
    subprocess.run([sys.executable, os.path.join(SITE, "generate.py")], check=True)
    subprocess.run(["hugo", "-s", SITE, "--gc", "--minify"], check=True)


def target_path(url):
    """Where a site-internal URL must land inside public/, or None if not ours."""
    parsed = urlparse(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None  # external, protocol-relative, or a bare anchor
    path = unquote(parsed.path)
    if not path.startswith("/"):
        return None  # relative links are not produced by this site; ignore rather than guess
    candidate = os.path.join(PUBLIC, path.lstrip("/"))
    return os.path.join(candidate, "index.html") if path.endswith("/") else candidate


def main():
    if "--no-build" not in sys.argv:
        build()

    if not os.path.isdir(PUBLIC):
        sys.exit("check: public/ does not exist — build first")

    seen = 0
    broken = {}
    for dirpath, _, filenames in os.walk(PUBLIC):
        for name in filenames:
            if not name.endswith(".html"):
                continue
            page = os.path.join(dirpath, name)
            with open(page, encoding="utf-8", errors="replace") as handle:
                html = handle.read()
            for match in REF.finditer(html):
                url = match.group(1) or match.group(2) or match.group(3) or ""
                target = target_path(url)
                if target is None:
                    continue
                seen += 1
                if not os.path.exists(target):
                    where = os.path.relpath(page, PUBLIC)
                    broken.setdefault(url, set()).add(where)

    if seen < MINIMUM_REFERENCES:
        sys.exit(
            "check: found only %d internal references — the extractor is broken, "
            "not the site" % seen
        )

    if broken:
        print("check: %d broken internal link(s) in %d reference(s)" % (len(broken), seen))
        for url in sorted(broken):
            pages = ", ".join(sorted(broken[url])[:3])
            print("  %s   <- %s" % (url, pages))
        sys.exit(1)

    print("check: %d internal references, all resolve" % seen)


if __name__ == "__main__":
    main()
