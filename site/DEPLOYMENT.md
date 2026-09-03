# Deploying ottoquill.com

## Setup: deploy on push

Before any push:

```bash
python3 site/check.py
```

1. Merge the site to `main` and push.
2. Cloudflare dashboard → **Workers & Pages** → **Create** → **Import a repository** →
   `ottoquill/desk`.
3. **Settings → Builds**:

   | Setting | Value |
   |---|---|
   | Root directory | `site` |
   | Production branch | `main` |
   | Build command | *(empty)* |
   | Deploy command | `npx wrangler deploy` |

4. **Settings → Variables**, Production and Preview: `HUGO_VERSION` = `0.159.0`.
5. Deploy. Read the build log.
6. Attach the domain: uncomment `routes` in [`wrangler.jsonc`](wrangler.jsonc) and push,
   or use the project's **Domains & Routes**. Set `baseURL` in [`hugo.toml`](hugo.toml)
   to match.

After this, every push to `main` deploys. Other branches get preview deployments.

## Manual deployment, from any branch

Deploys whatever is checked out, from this machine, without going through GitHub.

```bash
cd site
npm install          # first time only
npm run preview      # gate, build, upload a version — a preview URL, live site untouched
npm run deploy       # gate, build, deploy to production
```

Authentication is wrangler's own: `npx wrangler login` if not already logged in,
`npx wrangler whoami` to check.

Live now at **https://ottoquill.domains-68b.workers.dev** — deployed manually from
`writing-method`.

## Why

**Manual deploys and the gate.** `npm run deploy` runs `check.py` first and stops on a
broken link, so the gate cannot be skipped by deploying by hand. `npm run preview` uses
`wrangler versions upload`, which uploads a version and returns a preview URL without
moving production traffic — that is the one to use for a branch. Production must exist
before a version can be uploaded against it, so the very first deploy of a new Worker
is `npm run deploy`.

**Step 3, root directory `site`.** The Hugo project is not at the repo root. Without
this the build finds no `hugo.toml`.

**Step 3, empty build command.** `wrangler.jsonc` carries its own `build.command`:
submodule update, `python3 generate.py`, `hugo --gc --minify`. Keeping the dashboard
field empty leaves the build defined in one place. A dashboard command is not wrong,
only a second place to look.

**Step 4, pinned Hugo.** The site is built and checked against 0.159.0 locally. Pinning
stops a build-image change from moving it.

**Step 6, domain last.** `routes` is commented out so a push cannot create DNS records
on the live zone by accident. Attach it once a deploy is known good.

`www` is a separate decision. Adding it as a second custom domain serves the same site
at two hostnames instead of redirecting, which splits the site in search results. A
`www` → apex redirect needs a Worker in front with `"run_worker_first": true`;
`peatyscot/peatyscot` is the model.

**The check.** `check.py` generates, builds, and verifies every internal link. Hugo does
not validate internal links, so a renamed page 404s in production while the build stays
green. It exits non-zero on a broken link, and fails rather than passes if it finds
fewer than fifty references — a link checker that finds nothing is broken, not
satisfied. It writes only the gitignored `site/public/` and deploys nothing.

## Unverified: python3 in the build image

`build.command` calls `python3 generate.py`. Whether Python 3 exists in Cloudflare's
Workers Builds image could not be tested from a developer machine. The first build is
the test.

If the log says `python3: command not found`: port `generate.py` to node — it is one
stdlib file, and its JavaScript original is `ottoquill/talosapien/site/generate.mjs` —
or install Python in `build.command`. Do not commit `site/content/` to work around it;
it is generated from `method/`, and a committed copy is a second source of truth that
will drift.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `python3: command not found` | see above |
| `assets.directory … does not exist` | root directory is not `site`, or `build.command` produced no `public/` |
| `npx hugo` / `could not determine executable to run` | `wrangler.jsonc` missing on the built branch; wrangler then guesses wrong. Hugo is a binary, not an npm package |
| empty `site/themes/hugo-book` | submodule not fetched; check the build log's access to `github.com` |
| pages render `was/felt` with nothing after it | pseudo-tag escaping in `generate.py` has regressed; `tools/tests/test_site_generate.py` covers it |
| old content after a push | check the **Builds** tab; the Cloudflare GitHub app may need re-authorising |
