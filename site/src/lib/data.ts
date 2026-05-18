// =============================================================================
// WhiskyBase data loader
// =============================================================================
// Build-time helpers to load YAML entries from /data/ into TypeScript
// objects. Runs in Astro's Node frontmatter context (page generation).
//
// Type definitions are minimal pass-throughs: the YAML loader returns
// the parsed structure verbatim, and per-entity-type interfaces
// capture the shape the rendering components rely on. The interfaces
// are NOT a substitute for the JSON Schema validation that runs via
// scripts/check_references.py — they only describe what the rendering
// code reads.
// =============================================================================

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse as parseYaml } from 'yaml';

// Resolve /data/ relative to this file at build time.
const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, '..', '..', '..', 'data');

// ----- Source citations (shared across all entity types) -----

export interface Source {
  id: number;
  type: string;
  url?: string | null;
  citation?: string | null;
  accessed?: string | null;
  notes?: string | null;
  methodology?: unknown;
}

// ----- Distillery -----

export interface DistilleryOwnershipPeriod {
  owner: string;
  from?: number | null;
  to?: number | null;
  notes?: string | null;
}

export interface DistilleryStill {
  count?: number | null;
  capacity_litres?: number | null;
  charge_litres?: number | null;
  shape?: string | null;
  height_m?: number | null;
  heating?: string | null;
  lyne_arm_angle?: string | null;
  condenser?: string | null;
}

export interface DistilleryWarehouse {
  id?: string;
  type?: string | null;
  location?: string | null;
  climate_notes?: string | null;
}

export interface Distillery {
  id: string;
  name: string;
  also_known_as?: string[];
  website?: string | null;
  country: string;
  region?: string | null;
  sub_region?: string | null;
  locality?: string | null;
  coordinates?: { lat?: number | null; lon?: number | null };
  status: string;
  founded?: number | null;
  first_spirit?: string | number | null;
  mothballed_periods?: Array<{
    from?: number | null;
    to?: number | null;
    note?: string | null;
    notes?: string | null;
  }>;
  ownership?: {
    current?: string | null;
    parent?: string | null;
    history?: DistilleryOwnershipPeriod[];
  };
  water_source?: string | null;
  mash_tun?: {
    type?: string | null;
    material?: string | null;
    capacity_kg?: number | null;
  };
  washbacks?: {
    count?: number | null;
    material?: string | null;
    capacity_litres?: number | null;
    notes?: string | null;
  };
  stills?: {
    wash_still?: DistilleryStill;
    spirit_still?: DistilleryStill;
    intermediate_still?: DistilleryStill;
  };
  warehouses?: DistilleryWarehouse[];
  annual_capacity_lpa?: number | null;
  production_lines?: string[];
  also_used_by_blenders?: string[];
  distinctive_features?: string[];
  description?: string | null;
  sources?: Source[];
  schema_version: number | string;
  confidence: 'high' | 'medium' | 'low' | 'stub';
  last_reviewed?: string | null;
}

// ----- Loaders -----

function loadYamlFile<T>(path: string): T | null {
  if (!existsSync(path)) return null;
  const text = readFileSync(path, 'utf-8');
  const parsed = parseYaml(text);
  if (parsed === null || typeof parsed !== 'object') return null;
  return parsed as T;
}

function listYamlFiles(dir: string): string[] {
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => f.endsWith('.yml') && !f.startsWith('.'))
    .sort();
}

export function loadDistilleries(): Distillery[] {
  const dir = join(DATA_DIR, 'distilleries');
  return listYamlFiles(dir)
    .map((f) => loadYamlFile<Distillery>(join(dir, f)))
    .filter((d): d is Distillery => d !== null)
    .sort((a, b) => a.name.localeCompare(b.name));
}

export function loadDistillery(slug: string): Distillery | null {
  const path = join(DATA_DIR, 'distilleries', `${slug}.yml`);
  return loadYamlFile<Distillery>(path);
}

// ----- Production lines (minimal, for distillery's referenced lines) -----

export interface ProductionLine {
  id: string;
  name: string;
  distillery: string;
  status?: string;
  description?: string | null;
}

export function loadProductionLine(slug: string): ProductionLine | null {
  const path = join(DATA_DIR, 'production_lines', `${slug}.yml`);
  return loadYamlFile<ProductionLine>(path);
}

// ----- Concepts (for distinctive_features cross-references) -----

export interface Concept {
  id: string;
  title: string;
  kind: 'methodology' | 'educational' | 'equipment' | 'practice' | 'glossary';
  summary?: string | null;
}

export function loadConcept(kind: string, slug: string): Concept | null {
  const path = join(DATA_DIR, 'concepts', kind, `${slug}.yml`);
  return loadYamlFile<Concept>(path);
}

/**
 * Resolve a "<kind>/<slug>" concept reference (the form used in
 * distinctive_features and related_concepts fields).
 */
export function loadConceptByRef(ref: string): Concept | null {
  const [kind, slug] = ref.split('/', 2);
  if (!kind || !slug) return null;
  return loadConcept(kind, slug);
}

// ----- Counts (for front-page summary) -----

export interface EntityCount {
  topic: string;
  description: string;
  href: string;
  count: number;
}

function countYamlInDir(relPath: string): number {
  const dir = join(DATA_DIR, relPath);
  if (!existsSync(dir)) return 0;
  // Count files whose YAML parses to a non-empty dict — matches the
  // resolver's behaviour, which skips empty placeholder files
  // (e.g., superseded-stub files overwritten with empty YAML).
  let count = 0;
  for (const f of readdirSync(dir)) {
    if (!f.endsWith('.yml') || f.startsWith('.')) continue;
    const parsed = loadYamlFile<Record<string, unknown>>(join(dir, f));
    if (parsed !== null && typeof parsed === 'object') count++;
  }
  return count;
}

function countYamlRecursive(relPath: string): number {
  const dir = join(DATA_DIR, relPath);
  if (!existsSync(dir)) return 0;
  let total = 0;
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      total += countYamlRecursive(join(relPath, entry.name));
    } else if (entry.name.endsWith('.yml') && !entry.name.startsWith('.')) {
      const parsed = loadYamlFile<Record<string, unknown>>(join(dir, entry.name));
      if (parsed !== null && typeof parsed === 'object') total += 1;
    }
  }
  return total;
}

export function getEntityCounts(): EntityCount[] {
  return [
    {
      topic: 'Distilleries',
      description: 'Physical production sites — location, equipment, ownership, history.',
      href: '/distilleries/',
      count: countYamlInDir('distilleries'),
    },
    {
      topic: 'Production lines',
      description: 'Recipes / specs run at a distillery. One distillery may run several.',
      href: '/production-lines/',
      count: countYamlInDir('production_lines'),
    },
    {
      topic: 'Bottlings',
      description: 'Specific commercial releases with their per-release specifications.',
      href: '/bottlings/',
      count: countYamlInDir('bottlings'),
    },
    {
      topic: 'Bottlers',
      description: 'Commercial bottling entities — independent bottlers and distillery operations.',
      href: '/bottlers/',
      count: countYamlInDir('bottlers'),
    },
    {
      topic: 'Casks',
      description: 'Reusable cask-type references cited from bottlings and production lines.',
      href: '/casks/',
      count: countYamlInDir('casks'),
    },
    {
      topic: 'Suppliers',
      description: 'Upstream commercial parties: maltsters, cooperage sources, yeast houses.',
      href: '/suppliers/',
      count: countYamlInDir('suppliers'),
    },
    {
      topic: 'Concepts',
      description: 'Reference pages: methodology, educational, equipment, practice, glossary.',
      href: '/concept/',
      count: countYamlRecursive('concepts'),
    },
  ];
}

// ----- Extended Concept type with all per-kind blocks -----

export interface ConceptMethodologyBlock {
  measures?: string[];
  method?: string;
  compounds?: string;
  used_by?: string[];
  adopted?: string | number | null;
  limitations?: string | null;
}

export interface ConceptEducationalBlock {
  prerequisites?: string[];
  covers?: string[];
}

export interface ConceptEquipmentBlock {
  category?: string;
  used_at_distilleries?: string[];
  distinguishing_features?: string | null;
  alternatives?: string[];
}

export interface ConceptPracticeBlock {
  adopted_by?: string[];
  consequences?: string | null;
  contrast_with?: string[];
}

export interface ConceptGlossaryBlock {
  aliases?: string[];
  part_of_speech?: 'noun' | 'verb' | 'adjective' | 'phrase' | null;
  see_also?: string[];
}

export interface ConceptFull extends Concept {
  body?: string | null;
  related_concepts?: string[];
  methodology?: ConceptMethodologyBlock | null;
  educational?: ConceptEducationalBlock | null;
  equipment?: ConceptEquipmentBlock | null;
  practice?: ConceptPracticeBlock | null;
  glossary?: ConceptGlossaryBlock | null;
  sources?: Source[];
  schema_version?: number | string;
  confidence?: 'high' | 'medium' | 'low' | 'stub';
  last_reviewed?: string | null;
}

const CONCEPT_KINDS = [
  'methodology',
  'educational',
  'equipment',
  'practice',
  'glossary',
] as const;

export type ConceptKind = (typeof CONCEPT_KINDS)[number];

/**
 * Load all concept entries across all kinds. Returns a flat list
 * with each entry's kind attached (so callers can filter or group).
 */
export function loadConcepts(): ConceptFull[] {
  const out: ConceptFull[] = [];
  for (const kind of CONCEPT_KINDS) {
    out.push(...loadConceptsByKind(kind));
  }
  return out;
}

/**
 * Load all concept entries of a single kind, sorted by id.
 */
export function loadConceptsByKind(kind: ConceptKind): ConceptFull[] {
  const dir = join(DATA_DIR, 'concepts', kind);
  return listYamlFiles(dir)
    .map((f) => loadYamlFile<ConceptFull>(join(dir, f)))
    .filter((c): c is ConceptFull => c !== null)
    .map((c) => ({ ...c, kind }))
    .sort((a, b) => a.id.localeCompare(b.id));
}

/**
 * Load a specific concept entry by kind + slug. Falls back to
 * scanning all kinds if the kind is unknown (defensive).
 */
export function loadConceptFull(kind: string, slug: string): ConceptFull | null {
  const path = join(DATA_DIR, 'concepts', kind, `${slug}.yml`);
  const c = loadYamlFile<ConceptFull>(path);
  if (c === null) return null;
  return { ...c, kind: kind as ConceptKind };
}
