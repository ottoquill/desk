# site — ottoquill.com

The public wiki, built from this repository's own documents. Hugo with the
[hugo-book](https://github.com/alex-shpak/hugo-book) theme, deployed to Cloudflare
Workers static assets — the same stack as the other Hugo sites in `~/git`.

## Commands

```bash
python3 site/check.py          # generate, build, check every internal link — the gate
python3 site/generate.py       # mirror method/ and templates/ into site/content/
hugo -s site server            # local preview at http://localhost:1313
```

`check.py` is the definition of done for a content change. It exits non-zero on a
broken internal link, and it fails rather than passes if it finds fewer than fifty
references, because a link checker that finds nothing is broken rather than satisfied.

## What is generated and what is written

`content/` is **generated and gitignored**. `method/` and `templates/` are the source
of truth and are never edited to suit the renderer: where the corpus writes a
placeholder as `<emotion>`, `generate.py` escapes it, rather than the document
acquiring backticks it did not need on its own terms.

Pages belonging to the website rather than to the method live in `pages/` and are
committed. Today that is the landing page.

| Source | On the site |
|---|---|
| `method/` | `/method/` — the argument, the rules, the pipeline |
| `method/reference/` | `/method/reference/` — the research library |
| `templates/` | `/desk/templates/` |
| `README.md` | `/desk/` |

A link to a repository file that is not published — `tools/idiolect_probe.py`,
`canon/schema.toml` — is rewritten to GitHub rather than dropped, because the method
documents cite the code constantly and an argument stripped of its evidence is a
different argument.

## The image

`assets/brand/otto-quill.jpg` is the site's one image and the only one committed. Hugo
derives the favicon, the apple-touch icon, the two manifest icons and the 1200x630 Open
Graph card from it at build time, so nothing resized is stored and no derivative can
disagree with its source. Replace that file and every icon and card follows on the next
build; remove it and the build fails rather than the site quietly losing its icon.

The reasoning is in the three templates that do the work —
[`layouts/_partials/brand/mark.html`](layouts/_partials/brand/mark.html),
[`html-head-favicon.html`](layouts/_partials/docs/html-head-favicon.html) and
[`inject/head.html`](layouts/_partials/docs/inject/head.html) — including why the square
crop is anchored at the centre rather than smart-cropped, and why the card is composed
rather than cut out of the portrait.

There is no `/favicon.ico`. Every browser here is served a real 32px PNG through
`<link rel="icon">`; the only thing an .ico would add is an answer for a client that
fetches the path blind, and Hugo cannot write one, so adding it would mean committing a
derivative and a script to make it.

## Deployment

Push to the production branch; Cloudflare Workers Builds does the rest. The one-time
setup, the settings, the domain attach and the troubleshooting are in
[DEPLOYMENT.md](DEPLOYMENT.md).
