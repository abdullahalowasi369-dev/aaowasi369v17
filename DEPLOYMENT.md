# Deployment — v17

The deployed site is static HTML/CSS/browser JavaScript. Node.js is used only for repository validation and the copy-based build step; there is no Node server runtime in production.

## Pre-deploy

```bash
npm run check
npm run build
npm run postbuild
```

Deploy the generated `out/` directory.

## Cloudflare Pages

Recommended repository settings:

- Framework preset: **None**
- Build command: `npm run build`
- Build output directory: `out`
- Node version: **22** (the repository includes `.nvmrc` and `.node-version`)

No Pages Function or Worker is required for the portfolio itself. The live risk pulse fetches public CISA data directly from the visitor’s browser; failure is non-blocking and degrades to an explicit unavailable state.

## Vercel

The included `vercel.json` declares:

- `framework: null`
- `buildCommand: "npm run build"`
- `outputDirectory: "out"`

If an existing Vercel project has dashboard-level Build & Development overrides, align them with the repository values above.

## Static-host fallback

Any host that can publish a directory of static files can serve `out/`. The client runtime does not depend on Vercel APIs, Cloudflare APIs, Node built-ins, React, Next.js, or a bundler.

## Live public-risk data

The browser attempts:

1. CISA’s official `cisagov/kev-data` GitHub mirror.
2. CISA’s canonical KEV JSON feed.

The official mirror is maintained for programmatic use and CISA states that it is synchronized with the canonical catalog within minutes. No deployment secret or API key is required. A fetch failure does not block navigation or the rest of the portfolio.

## Canonical URL

The canonical tag, Open Graph URL, `robots.txt`, and `sitemap.xml` currently use:

`https://aaowasi369v10.pages.dev/`

If the production hostname changes, update `index.html`, `robots.txt`, and `sitemap.xml` together before building.
