#!/usr/bin/env node
// Post-build: run Pagefind against whichever directory Astro wrote
// HTML into. Astro's outDir is controlled by ASTRO_OUT_DIR (set in
// astro.config.mjs); we mirror that here so the same script works on
// Windows-native (./dist) and sandbox (/tmp/whiskybase-dist) runs.
import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const siteRoot = path.resolve(__dirname, '..');
const outDir = process.env.ASTRO_OUT_DIR
  ? path.resolve(process.env.ASTRO_OUT_DIR)
  : path.resolve(siteRoot, 'dist');

if (!existsSync(outDir)) {
  console.error(`postbuild: outDir not found: ${outDir}`);
  process.exit(1);
}

console.log(`postbuild: indexing ${outDir} with Pagefind`);

const result = spawnSync('npx', ['pagefind', '--site', outDir], {
  stdio: 'inherit',
  shell: process.platform === 'win32',
});

if (result.status !== 0) {
  console.error('postbuild: pagefind exited non-zero');
  process.exit(result.status ?? 1);
}
