// =============================================================================
// Reference pages — design and policy documents ported into routed
// /reference/<slug>/ pages.
// =============================================================================
// Source docs live in the repo at /docs/ (outside /site/). They're
// read at build time and rendered with the existing marked helper.
// The leading h1 in each source file is stripped so the page can
// provide its own header.
// =============================================================================

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { REPO_ROOT } from './repo-root';

export interface ReferenceEntry {
  /** URL slug under /reference/. */
  slug: string;
  /** Display title for the page header. */
  title: string;
  /** One-line description used in the index and home table. */
  description: string;
  /** Path to the source markdown file relative to repo root. */
  source: string;
  /** Category grouping for the index. */
  category: 'policy' | 'design' | 'about';
}

export const REFERENCES: ReferenceEntry[] = [
  {
    slug: 'about',
    title: 'About WhiskyBase',
    description:
      'What this project is, what it is not, scope and licensing.',
    source: 'docs/about.md',
    category: 'about',
  },
  {
    slug: 'source-policy',
    title: 'Source-conflict policy',
    description:
      'How sources are selected, how conflicts are resolved, and the source-type vocabulary.',
    source: 'docs/source-conflict-policy.md',
    category: 'policy',
  },
  {
    slug: 'voice-register',
    title: 'Voice register',
    description:
      'Writing-discipline rules for production-data prose and educational content.',
    source: 'docs/voice-register.md',
    category: 'policy',
  },
  {
    slug: 'bibliography',
    title: 'Bibliography',
    description:
      'Curated catalogue of in-depth, peer-reviewed, and institutional reference works.',
    source: 'docs/bibliography.md',
    category: 'policy',
  },
  {
    slug: 'schema-design-notes',
    title: 'Schema design notes',
    description:
      'Rationale behind the structured-data schemas — what was promoted, what was rejected, and why.',
    source: 'docs/schema-design-notes.md',
    category: 'design',
  },
  {
    slug: 'contributing',
    title: 'Contributing',
    description: 'How to add or correct entries.',
    source: 'docs/contributing.md',
    category: 'about',
  },
];

/**
 * Strip a leading h1 line ("# Title") from a markdown document, so
 * the rendered reference page can supply its own header.
 */
function stripLeadingH1(md: string): string {
  return md.replace(/^#\s+[^\n]*\n+/, '');
}

/** Read the markdown body for a single reference entry. */
export function loadReferenceBody(entry: ReferenceEntry): string {
  const path = join(REPO_ROOT, entry.source);
  if (!existsSync(path)) {
    throw new Error(
      `Reference source not found: ${entry.source} (resolved to ${path})`,
    );
  }
  const raw = readFileSync(path, 'utf8');
  return stripLeadingH1(raw);
}

/** Get a single entry by slug, or null if absent. */
export function getReference(slug: string): ReferenceEntry | null {
  return REFERENCES.find((r) => r.slug === slug) ?? null;
}
