# WhiskyBase site

Static-site frontend for the WhiskyBase Scotch whisky reference.
Consumes the YAML data layer at `/data/` and renders pages per
the design document at `/docs/build-pipeline-plan.md`.

## Stack

- **Astro 5** — static-site generator
- **TypeScript** — type-checked frontmatter
- **yaml** (`yaml` npm package) — YAML parsing
- Pagefind (search) and MapLibre GL (map) deferred to later
  iterations

## Status

**First-iteration scaffolding, 2026-05-17.**

Render-complete:
- Home page
- Distilleries index
- Distillery detail page (all 9 populated distilleries render)

Deferred to subsequent iterations:
- Production lines / bottlings / bottlers / casks / suppliers /
  concepts (entity-type pages)
- Cross-cutting `/explore/` query pages
- Reference pages (about, bibliography, etc.)
- Search (Pagefind)
- Map (MapLibre)
- Markdown-link rewriting plugin

See `/docs/build-pipeline-plan.md` for the full implementation
sequencing.

## Local development

Requires Node.js ≥ 18.17.0.

```sh
cd site
npm install
npm run dev          # http://localhost:4321
npm run build        # static output to /site/dist/
npm run preview      # serve the built output
npm run check        # TypeScript + Astro type check
```

## Directory layout

```
site/
├── package.json
├── astro.config.mjs
├── tsconfig.json
├── README.md
└── src/
    ├── lib/
    │   └── data.ts                  # YAML loaders, typed
    ├── layouts/
    │   └── BaseLayout.astro         # header + footer shell
    ├── components/
    │   ├── EntityHeader.astro
    │   ├── EquipmentSpec.astro
    │   ├── Footer.astro
    │   ├── LocationBlock.astro
    │   ├── OwnershipHistory.astro
    │   ├── ProductionLinesList.astro
    │   └── SourcesBlock.astro
    └── pages/
        ├── index.astro               # /
        └── distilleries/
            ├── index.astro           # /distilleries/
            └── [slug].astro          # /distilleries/<slug>/
```

## Licensing

- Site source code (everything under `/site/`): **MIT**
- Data and reference documents under `/data/` and `/docs/`:
  **CC-BY-SA 4.0** (per project root README)

The build output bundles data into the rendered pages; the
footer carries both licence notices with links.
