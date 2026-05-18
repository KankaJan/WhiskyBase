// @ts-check
import { defineConfig } from 'astro/config';

// Astro 5 configuration for the WhiskyBase site.
// Static output (no SSR): every page is generated at build time
// from the YAML data layer at /data/.

export default defineConfig({
  site: undefined,
  output: 'static',
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
  // Build output dir: override via env var for cross-platform sandbox
  // builds where /tmp gives Vite full unlink permissions. Defaults to
  // ./dist when env var unset (Windows / native development).
  outDir: process.env.ASTRO_OUT_DIR ?? './dist',
  markdown: {
    // Astro defaults are appropriate for the project's markdown
    // content (concept body fields, etc.); no remark/rehype
    // plugins added in this scaffolding pass.
  },
  vite: {
    // Redirect Vite's dependency cache out of node_modules so
    // cross-platform installs (npm install on Windows, build
    // on Linux sandbox) don't hit unlink-permission issues on
    // Windows-created files. The cache will rebuild on demand.
    cacheDir: '/tmp/whiskybase-vite-cache',
  },
});
