# Deploying ottoquill.com — Cloudflare Workers Builds via the GitHub app

The site deploys on a git push. The flow:

```
git push  →  GitHub  →  Cloudflare GitHub app  →  Workers Builds runs:
                                                     npx wrangler deploy
                                                       └─ build.command:
                                                          git submodule update …
                                                          python3 generate.py
                                                          hugo --gc --minify
                                                       └─ upload site/public
                                                   →  live
```

This is a **Workers** project serving static assets, not a classic Pages project, and
the build runs inside Cloudflare's build environment.

## The build is repo-driven

[`wrangler.jsonc`](wrangler.jsonc) is committed and makes `npx wrangler deploy`
self-contained: `build.command` fetches the theme submodule, generates `content/` from
`method/` and `templates/`, and runs Hugo. No dashboard **Build command** is needed, and
leaving it empty keeps the build defined in one place.

Two failures are already paid for in `ottoquill/tinarex` and are avoided here by
construction. `npx hugo` fails — Hugo is a native binary in the build image, not an npm
package. And `assets.directory … does not exist` means nothing built `public/`, which is
what `build.command` is for.

## One-time setup

**1. Push the branch.** Workers Builds can only see what is on GitHub. The site
currently lives on `writing-method`; merge to `main` first if `main` is to be the
production branch.

**2. Create the Worker.** Cloudflare dashboard → **Workers & Pages** → **Create** →
**Import a repository** → the Cloudflare GitHub app → `ottoquill/desk`.

**3. Settings → Builds:**

| Setting | Value | Notes |
|---|---|---|
| Git repository | `ottoquill/desk` | via the Cloudflare GitHub app |
| **Root directory** | **`site`** | required — the Hugo project is not at the repo root |
| Production branch | `main` | the branch whose builds go live |
| **Build command** | *(leave EMPTY)* | `wrangler.jsonc`'s `build.command` does the build |
| Deploy command | `npx wrangler deploy` | the default — leave as-is |

**4. Settings → Variables**, for Production **and** Preview:

| Variable | Value | Why |
|---|---|---|
| `HUGO_VERSION` | `0.159.0` | matches the version the site is built and checked against locally; pinning stops a build-image change from moving it |

**5. Deploy, and read the log.** The first build is the one that answers the open
question below.

**6. Attach the domain, deliberately.** `routes` is commented out in `wrangler.jsonc`
so that a push cannot create DNS records on the live `ottoquill.com` zone by accident.
When the deploy is known good, either uncomment it and push, or attach the domain in the
dashboard under the project's **Domains & Routes**. Then set `baseURL` in
[`hugo.toml`](hugo.toml) to the live URL if it is not already right.

`www` is a separate decision. Adding it as a second custom domain serves the same site
at two hostnames rather than redirecting one to the other, which splits the site in
search results. A `www` → apex redirect needs a real Worker in front with
`"run_worker_first": true`; `peatyscot/peatyscot` does exactly that and is the model.

## The open question: python3 in the build image

`build.command` calls `python3 generate.py`. Whether Python 3 is present in Cloudflare's
Workers Builds image is **unverified** — it could not be tested from a developer
machine, and the first build is the test.

If the log shows `python3: command not found`, there are two ways out. Port
`generate.py` to node — it is one stdlib file, and the JavaScript it was ported from is
`ottoquill/talosapien/site/generate.mjs`. Or install Python in `build.command` if the
image allows it. Do not work around this by committing `site/content/`: it is generated
from `method/`, and a committed copy is a second source of truth that will drift.

## Before pushing

```bash
python3 site/check.py
```

Generates, builds, and verifies that every internal link resolves. It exits non-zero on
a broken link, and it fails rather than passes if it finds fewer than fifty references,
because a link checker that finds nothing is broken rather than satisfied. Hugo does not
validate internal links on its own — a renamed page 404s silently in production and the
build stays green.

This is the definition of done for a content change. It does not deploy anything; it
only writes the local `site/public/`, which is gitignored.

## Troubleshooting

- **`python3: command not found`** — see the open question above.
- **`assets.directory … does not exist`** — `build.command` did not run or produced no
  `public/`. Confirm `wrangler.jsonc` is committed on the branch being built and that
  **Root directory** is `site`; read the Hugo output in the build log.
- **Theme missing / empty `site/themes/hugo-book`** — the `git submodule update` in
  `build.command` covers this. If it still fails, check the build log's network access
  to `github.com`.
- **Pages render with placeholders missing** (`was/felt ` with nothing after it) — the
  pseudo-tag escaping in `generate.py` has regressed. `tools/tests/test_site_generate.py`
  covers it; run the suite.
- **Old content after a push** — check the project's **Builds** tab; the Cloudflare
  GitHub app may need re-authorising.
