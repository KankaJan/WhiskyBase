// =============================================================================
// Markdown helper with entity-link rewriting and inline-citation
// resolution.
// =============================================================================
// Per docs/build-pipeline-plan.md §Markdown-link rewriting:
//
//   [text](concept/<kind>/<slug>)  -> [text](/concept/<kind>/<slug>/)
//   [text](distillery/<slug>)      -> [text](/distilleries/<slug>/)
//   [text](production_line/<slug>) -> [text](/production-lines/<slug>/)
//   [text](bottling/<slug>)        -> [text](/bottlings/<slug>/)
//   [text](bottler/<slug>)         -> [text](/bottlers/<slug>/)
//   [text](cask/<slug>)            -> [text](/casks/<slug>/)
//   [text](supplier/<slug>)        -> [text](/suppliers/<slug>/)
//
// Plus inline [N] citation patterns are rewritten to anchored
// superscript footnotes targeting #source-N anchors on the page.
// The caller passes the page's declared source-id set so the
// rewriter only converts patterns that actually resolve.
// =============================================================================

import { marked, type Tokens } from 'marked';

// External URLs and anchors pass through unchanged. Anything that
// matches one of these patterns gets rewritten to an absolute site
// URL.
const ENTITY_PATTERNS: Array<[RegExp, string]> = [
  [/^concept\/([a-z]+)\/([a-z0-9][a-z0-9-]*)$/, '/concept/$1/$2/'],
  [/^distillery\/([a-z0-9][a-z0-9-]*)$/, '/distilleries/$1/'],
  [/^production_line\/([a-z0-9][a-z0-9-]*)$/, '/production-lines/$1/'],
  [/^bottling\/([a-z0-9][a-z0-9-]*)$/, '/bottlings/$1/'],
  [/^bottler\/([a-z0-9][a-z0-9-]*)$/, '/bottlers/$1/'],
  [/^cask\/([a-z0-9][a-z0-9-]*)$/, '/casks/$1/'],
  [/^supplier\/([a-z0-9][a-z0-9-]*)$/, '/suppliers/$1/'],
];

/**
 * Rewrite an entity-pattern href to its absolute site URL. Returns
 * the href unchanged if no pattern matches (external URLs, anchor
 * hashes, mailto links, etc., all pass through).
 */
export function rewriteEntityHref(href: string): string {
  for (const [pattern, replacement] of ENTITY_PATTERNS) {
    if (pattern.test(href)) {
      return href.replace(pattern, replacement);
    }
  }
  return href;
}

// Configure marked once at module load with the custom link
// renderer. The renderer is otherwise default — paragraphs,
// emphasis, lists, headings all render with marked's defaults.
marked.use({
  gfm: true,
  breaks: false,
  renderer: {
    link({ href, title, tokens }: Tokens.Link) {
      const target = rewriteEntityHref(href);
      const titleAttr = title ? ` title="${escapeAttr(title)}"` : '';
      const text = this.parser.parseInline(tokens);
      return `<a href="${escapeAttr(target)}"${titleAttr}>${text}</a>`;
    },
  },
});

function escapeAttr(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/"/g, '&quot;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

/**
 * Rewrite inline [N] citation patterns to anchored superscript
 * footnotes. The valid set of source IDs must be passed in so the
 * rewriter doesn't accidentally convert literal text that happens
 * to look like [1] but isn't an actual citation.
 *
 * Skips bracket pairs inside fenced code blocks and inside link
 * brackets ([text](url)) by doing the rewriting AFTER markdown ->
 * HTML conversion, on the resulting HTML.
 */
export function rewriteInlineCitations(
  html: string,
  validIds: ReadonlySet<number>,
): string {
  // Match [N] patterns outside of HTML tags. Use a simple approach:
  // split on tags so we only process text content.
  return html.replace(
    /(<[^>]+>)|(\[(\d+)\])/g,
    (_match, tag: string | undefined, citation: string | undefined, idStr: string | undefined) => {
      if (tag) return tag;
      if (citation && idStr) {
        const id = parseInt(idStr, 10);
        if (validIds.has(id)) {
          return `<sup class="citation"><a href="#source-${id}" aria-label="Source ${id}">[${id}]</a></sup>`;
        }
      }
      return citation ?? '';
    },
  );
}

/**
 * Render a markdown string to HTML with entity-link rewriting
 * (via the configured marked instance) and inline [N] citation
 * resolution. Pass the page's declared source IDs to enable
 * citation rewriting.
 */
export function renderMarkdown(
  md: string | null | undefined,
  validSourceIds?: ReadonlySet<number>,
): string {
  if (!md) return '';
  const html = marked.parse(md, { async: false }) as string;
  if (!validSourceIds || validSourceIds.size === 0) return html;
  return rewriteInlineCitations(html, validSourceIds);
}

/**
 * Render a plain-text prose field (e.g., a description that may
 * contain inline citations but no markdown structure) as an
 * inline HTML string. Used for description fields that should
 * render with citation links but without paragraph wrapping.
 */
export function renderInline(
  text: string | null | undefined,
  validSourceIds?: ReadonlySet<number>,
): string {
  if (!text) return '';
  // Use marked's inline parser to handle any markdown links / emphasis,
  // then rewrite inline citations.
  const html = marked.parseInline(text, { async: false }) as string;
  if (!validSourceIds || validSourceIds.size === 0) return html;
  return rewriteInlineCitations(html, validSourceIds);
}

/**
 * Collect declared source IDs from an entity's `sources` array
 * for use with the citation-rewriting functions.
 */
export function collectSourceIds(
  sources: Array<{ id?: number }> | undefined,
): Set<number> {
  const out = new Set<number>();
  if (!sources) return out;
  for (const s of sources) {
    if (typeof s.id === 'number') out.add(s.id);
  }
  return out;
}
