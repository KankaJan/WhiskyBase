# WhiskyBase site

Static-site frontend for the WhiskyBase Scotch whisky reference.
Consumes the YAML data layer at `/data/` and renders pages per
the design document at `/docs/build-pipeline-plan.md`.

## Stack

- **Astro 5** — static-site generator
- **TypeScript** — type-checked frontmatter
- **yaml** (`yaml` npm package) — YAML parsing
- **marked** — markdown rendering for prose fields and reference
  pages, with a custom link renderer for entity-pattern href
  rewriting
- **Pagefind** — static-site search; runs after `astro build` and
  emits `/pagefind/` into the output directory
- **MapLibre GL** (loaded from CDN at runtime) — distillery map

## Status

All 8 items of the `/docs/build-pipeline-plan.md` §Implementation
sequencing list have landed (last updated 2026-05-18).

Render-complete:
- Home page with sortable populated-entities table
- Distillery / production-line / bottling / bottler / cask /
  supplier index + detail pages
- Concept overview + per-kind sub-indexes + concept detail pages
  with per-kind block dispatch (methodology, educational,
  equipment, practice, glossary)
- `/search/` full-text search (Pagefind)
- `/map/` map with distillery pins (MapLibre GL + Carto Positron)
- `/explore/` cross-cutting queries: by-region, by-ownership,
  by-peating, by-presentation, by-cask-category
- `/reference/` design and policy docs ported from `/docs/`:
  about, source-policy, voice-register, bibliography,
  schema-design-notes, contributing

## Local development

Requires Node.js ≥ 18.17.0.

```sh
cd site
npm install
npm run dev              # http://localhost:4321
npm run build            # static output to /site/dist/ + /site/dist/pagefind/
npm run build:astro-only # skip Pagefind for fast iteration
npm run preview          # serve the built output
npm run check            # TypeScript + Astro type check
```

The build script chains `astro build` and a post-build helper
(`scripts/postbuild.mjs`) that resolves the output directory
(default `./dist`, overridable via `ASTRO_OUT_DIR`) and runs
`npx pagefind --site <outDir>`.

## Markdown helper

`src/lib/markdown.ts` exports `renderMarkdown()` / `renderInline()`
with two custom rewrites:

- Entity-pattern hrefs (`concept/<kind>/<slug>`,
  `distillery/<slug>`, `production_line/<slug>`,
  `bottling/<slug>`, `bottler/<slug>`, `cask/<slug>`,
  `supplier/<slug>`) get rewritten to absolute site URLs.
- Inline `[N]` citations get rewritten to anchored superscript
  footnotes pointing at the page's sources block. The valid
  source-ID set is passed in so literal `[42]` outside citation
  context passes through unchanged.

## Reference pages

`src/lib/references.ts` registers the design/policy docs that get
exposed at `/reference/<slug>/`. Each entry names a source
markdown file under `/docs/`; the leading h1 is stripped at
render time so the page can supply its own header.

## Directory layout

```
site/
├── package.json
├── astro.config.mjs
├── tsconfig.json
├── README.md
├── scripts/
│   └── postbuild.mjs               # runs Pagefind after astro build
└── src/
    ├── lib/
    │   ├── data.ts                 # YAML loaders, typed
    │   ├── markdown.ts             # marked helper, link/citation rewriting
    │   └── references.ts           # /reference/ registry
    ├── layouts/
    │   └── BaseLayout.astro        # header + footer shell; pagefind hooks
    ├── components/                 # shared entity components + per-kind concept blocks
    └── pages/
        ├── index.astro             # /
        ├── search.astro            # /search/ (PagefindUI)
        ├── map.astro               # /map/ (MapLibre)
        ├── distilleries/           # detail + index
        ├── production-lines/       # detail + index
        ├── bottlings/              # detail + index
        ├── bottlers/               # detail + index
        ├── casks/                  # detail + index
        ├── suppliers/              # detail + index
        ├── concept/                # overview + per-kind sub-indexes + detail
        ├── explore/                # cross-cutting query pages
        └── reference/              # policy/design docs ported from /docs/
```

## Cross-platform build notes

- `vite.cacheDir` is pinned to `/tmp/whiskybase-vite-cache` so a
  Linux build doesn't trip over Windows-created cache files (the
  cross-OS unlink-permission case that bit the early iterations).
- The output directory can be overridden via `ASTRO_OUT_DIR`; the
  Pagefind post-build step honours the same variable. Default is
  `./dist`.

## Licensing

- Site source code (everything under `/site/`): **MIT**
- Data and reference documents under `/data/` and `/docs/`:
  **CC-BY-SA 4.0** (per project root README)

The build output bundles data into the rendered pages; the
footer carries both licence notices with links.
