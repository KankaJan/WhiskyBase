// =============================================================================
// Repository-root resolution for build-time data access.
// =============================================================================
// The data layer (/data/) and policy docs (/docs/) live in the repo
// root, outside /site/. Resolution must NOT derive from
// import.meta.url: the bundler relocates compiled chunks (Astro 6
// places prerender chunks at site/.astro/.prerender/chunks/, four
// levels below the root; Astro 5 happened to place them three), so
// source-relative ../../.. paths break across bundler layouts.
//
// The working directory is the stable anchor instead — Astro always
// runs from /site (npm scripts locally, working-directory: site in
// CI) — and the root is identified by its marker directories.
// =============================================================================

import { existsSync } from 'node:fs';
import { dirname, join } from 'node:path';

function findRepoRoot(): string {
  let dir = process.cwd();
  for (;;) {
    if (existsSync(join(dir, 'data')) && existsSync(join(dir, 'docs'))) {
      return dir;
    }
    const parent = dirname(dir);
    if (parent === dir) {
      throw new Error(
        `Repository root (directory containing /data and /docs) not found ` +
          `walking up from ${process.cwd()}`,
      );
    }
    dir = parent;
  }
}

export const REPO_ROOT = findRepoRoot();
