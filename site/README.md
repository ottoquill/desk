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

## Deployment

Cloudflare project settings: **Root directory** `site`, build command left empty
(`wrangler.jsonc` carries its own), and `HUGO_VERSION` set as an environment variable
for Production and Preview.

Two things are unverified until the first deploy:

1. **`python3` in the Workers Builds image.** `build.command` calls it. If the image
   has no Python, the generator wants porting to node — it is a single stdlib file and
   the JavaScript original it was ported from is in `ottoquill/talosapien/site`.
2. **The custom domain.** `routes` is commented out in `wrangler.jsonc` so that a push
   cannot create DNS records on the live zone by accident.
