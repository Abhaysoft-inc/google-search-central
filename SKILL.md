---
name: google-search-central
description: Offline copy of Google's official Search Central documentation (185 pages - SEO fundamentals, Search Essentials and spam policies, crawling and indexing, robots.txt, Googlebot and other Google crawlers, sitemaps, canonicals, redirects, noindex, JavaScript SEO, hreflang, structured data and rich results for every supported type, title links, snippets, images, video, AI features, ranking systems, ecommerce, site moves). Use this skill whenever the user asks what Google says, requires, supports or recommends for Search; whenever you are about to write or review JSON-LD / schema.org markup, robots.txt, meta robots rules, canonical tags, hreflang, sitemaps or redirects; and whenever you audit a page or site for Google SEO compliance - even if the user does not mention Google's docs. Google's requirements change often and remembered details (required properties, supported rich result types, crawler names) are frequently out of date, so check here instead of answering from memory.
---

# Google Search Central docs

This skill bundles a snapshot of Google's own documentation from
`developers.google.com/search/docs` and `developers.google.com/crawling/docs`,
one Markdown file per page, so that answers, audits and generated markup can be
grounded in what Google actually publishes rather than in recollection.

**Snapshot date: 2026-11-13.** See "Freshness" at the end.

## Why look things up instead of answering from memory

SEO is full of advice that used to be true. Google regularly adds and retires
rich result types, changes which structured data properties are required,
renames crawlers and moves pages. What you remember may describe a past version
of the docs, and SEO folklore from blogs is mixed in with it. The bundled pages
are the ground truth for this skill: read the relevant page before you state a
requirement, and let the page win when it disagrees with what you expected.

If the docs do not cover something, say so plainly ("Google's Search docs don't
document this") and keep any general-knowledge answer clearly separate from
what is sourced. A feature that has no page here - for example a structured
data type missing from `appearance/structured-data/search-gallery.md` - is not
something Google currently documents as supported, which is itself a useful
answer for the user.

## Finding the right page

Everything lives in `references/pages/`. Each file starts with front matter
giving the page `title` and its live `url`.

1. Start from the topic map below; it covers most questions.
2. If the map doesn't settle it, search:
   `python scripts/docs.py search "hreflang x-default"` prints the best pages
   with matching line numbers. Rare, specific words work best (`x-default`,
   `soft 404`, `max-image-preview`, `priceValidUntil`).
3. `references/page-index.md` lists all 185 pages by topic with their sizes.
4. Some pages are long (merchant listings is 1,400+ lines). Run
   `python scripts/docs.py outline <page>` to get the headings with line
   numbers, then read only the sections you need.

No Python available? Plain `grep -rn` over `references/pages/` works too.

Read the page itself before relying on it; search output and the topic map tell
you where to look, not what the page says. Two or three pages are usually
enough. Pages cross-link using live URLs: a link to
`https://developers.google.com/search/docs/X` is the local file
`references/pages/X.md`, and `https://developers.google.com/crawling/docs/X` is
`references/pages/crawling-docs/X.md`.

### Topic map

Paths are relative to `references/pages/`.

| Topic | Start here |
|---|---|
| What Google requires at minimum; spam and policy violations | `essentials.md`, `essentials/technical.md`, `essentials/spam-policies.md` |
| SEO basics, how Search works | `fundamentals/seo-starter-guide.md`, `fundamentals/how-search-works.md`, `fundamentals/get-started-developers.md` |
| Content quality, E-E-A-T, AI-generated content | `fundamentals/creating-helpful-content.md`, `fundamentals/using-gen-ai-content.md` |
| AI Overviews / AI Mode and how to appear in them | `appearance/ai-features.md`, `fundamentals/ai-optimization-guide.md` |
| robots.txt syntax, matching rules, examples | `crawling-docs/robots-txt/robots-txt-spec.md`, `crawling-docs/robots-txt/create-robots-txt.md`, `crawling-docs/robots-txt/useful-robots-txt-rules.md`, `crawling-indexing/robots/intro.md` |
| Googlebot and other Google crawlers, user-agent tokens, verifying a request is from Google | `crawling-docs/crawlers-fetchers/` (overview, common, special-case, user-triggered, verify) |
| Crawl budget, crawl rate, faceted navigation | `crawling-docs/crawl-budget.md`, `crawling-docs/crawlers-fetchers/reduce-crawl-rate.md`, `crawling-docs/faceted-navigation.md` |
| HTTP status codes, network/DNS errors, soft 404 | `crawling-docs/troubleshooting/http-status-codes.md`, `crawling-docs/troubleshooting/dns-network-errors.md`, `crawling-indexing/troubleshoot-crawling-errors.md` |
| noindex, robots meta tag, X-Robots-Tag, data-nosnippet | `crawling-indexing/block-indexing.md`, `crawling-indexing/robots-meta-tag.md`, `crawling-indexing/special-tags.md` |
| Removing or hiding content from Google | `crawling-indexing/control-what-you-share.md`, `crawling-indexing/remove-information.md` |
| Canonical URLs and duplicates | `crawling-indexing/canonicalization.md`, `crawling-indexing/consolidate-duplicate-urls.md`, `crawling-indexing/canonicalization-troubleshooting.md` |
| Redirects, site moves, hosting changes, pausing a site | `crawling-indexing/301-redirects.md`, `crawling-indexing/site-move-with-url-changes.md`, `crawling-indexing/site-move-no-url-changes.md`, `crawling-indexing/pause-online-business.md` |
| Sitemaps (XML, index files, image, video, news) | `crawling-indexing/sitemaps/` (start with `build-sitemap.md`) |
| URL structure, links, nofollow/sponsored/ugc | `crawling-indexing/url-structure.md`, `crawling-indexing/links-crawlable.md`, `crawling-indexing/qualify-outbound-links.md` |
| JavaScript sites, rendering, lazy loading | `crawling-indexing/javascript/javascript-seo-basics.md`, `fix-search-javascript.md`, `lazy-loading.md` in the same folder |
| Mobile-first indexing | `crawling-indexing/mobile/mobile-sites-mobile-first-indexing.md` |
| hreflang, multilingual and multi-regional sites | `specialty/international/localized-versions.md`, `specialty/international/managing-multi-regional-sites.md` |
| Structured data: which types Google supports | `appearance/structured-data/search-gallery.md` |
| Structured data: rules that apply to all types | `appearance/structured-data/sd-policies.md`, `appearance/structured-data/intro-structured-data.md` |
| Structured data for one type (Article, Product, Recipe, Event, JobPosting, LocalBusiness, Organization, Breadcrumb, Video, Review ...) | `appearance/structured-data/<type>.md` - see the page index for exact names |
| Products and shops | `appearance/structured-data/product.md` (explains product snippet vs merchant listing), then `product-snippet.md`, `merchant-listing.md`, `product-variants.md`, `return-policy.md`, `shipping-policy.md`; `specialty/ecommerce/` |
| Title links, snippets and meta descriptions, site names, favicons, sitelinks, dates | `appearance/title-link.md`, `appearance/snippet.md`, `appearance/site-names.md`, `appearance/favicon-in-search.md`, `appearance/sitelinks.md`, `appearance/publication-dates.md` |
| Images, video, Discover, Web Stories | `appearance/google-images.md`, `appearance/video.md`, `appearance/google-discover.md` |
| Ranking systems, core and spam updates, page experience, Core Web Vitals | `appearance/ranking-systems-guide.md`, `appearance/core-updates.md`, `appearance/page-experience.md`, `appearance/core-web-vitals.md` |
| Paywalls, interstitials, A/B testing | `appearance/structured-data/paywalled-content.md`, `appearance/flexible-sampling.md`, `appearance/avoid-intrusive-interstitials.md`, `crawling-indexing/website-testing.md` |
| Traffic drops, Search Console, search operators | `monitor-debug/debugging-search-traffic-drops.md`, `monitor-debug/search-console-start.md`, `monitor-debug/search-operators.md` |
| Hacked sites, malware, user-generated spam | `monitor-debug/security/`, `monitor-debug/prevent-abuse.md` |
| Explicit content and SafeSearch | `specialty/explicit/guidelines.md` |

## Three kinds of work

### 1. Answering questions

Lead with the direct answer, then the supporting detail from the docs. Cite
every factual claim about Google's behaviour or requirements with the page
title linked to its live `url` from the front matter, so the user can verify
it and see the current version, e.g.
`([Robots meta tags specifications](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag))`.
Cite local file paths only if the user is working with the files themselves.

Keep Google's own strength of wording. The docs distinguish *required* from
*recommended*, and "Google may" from "Google does"; a recommendation reported
as a rule (or the reverse) misleads the user about what will actually break.
Short quotes are fine where exact wording matters; otherwise paraphrase.

### 2. Auditing a page, file or site

The user gives you something concrete (HTML, a URL you can fetch, a
robots.txt, a sitemap, JSON-LD, a template) and wants to know what is wrong
with it by Google's standards.

1. Work out which doc pages govern what you were given and read them first.
   For structured data that is the type's own page plus `sd-policies.md`.
2. Check the artifact against what those pages say, item by item. Check for
   interactions as well as single rules - a classic one is a page blocked in
   robots.txt that also carries `noindex`, where Google can never see the
   `noindex`.
3. Report findings grouped by severity, most serious first:

   - **Violations** - breaks something the docs state as required or
     prohibited (missing required property, spam policy breach, invalid
     syntax). These can lose a rich result, block indexing, or risk a manual
     action.
   - **Recommendations** - the docs recommend it but don't require it.
   - **Fine** - a brief note of what you checked and found correct, so the
     user knows the scope of the audit.

   For each finding give: what is wrong and where (quote the line or
   property), what the docs say (with link), and the concrete fix.

Only report what you verified against the docs. Label anything that is general
best practice rather than Google guidance as such. If you could not check
something (no access to the live page, rendered HTML, server headers), say so
rather than assuming it's fine.

### 3. Generating compliant output

For JSON-LD, robots.txt, meta tags, hreflang sets, sitemaps, redirect maps and
the like:

1. Read the governing page first. For structured data, find the "Structured
   data type definitions" section; it lists required and recommended
   properties and the expected value formats.
2. Include every required property, and each recommended property the user
   has real data for. Never invent values to fill a property - made-up
   ratings, prices or dates violate the structured data policies in
   `sd-policies.md`, which also require that markup reflects content actually
   visible on the page. Use an obvious placeholder (`"REPLACE_WITH_..."`) and
   list what the user still needs to supply.
3. Prefer JSON-LD for structured data unless the user asks otherwise; it is
   the format Google recommends.
4. After the output, add a short note: which doc page it follows (linked),
   which properties are required vs recommended, anything left as a
   placeholder, and how to validate it (the Rich Results Test for structured
   data; the relevant Search Console report otherwise).
5. If the user asks for something Google's docs don't support (a rich result
   type absent from the search gallery, a robots.txt directive Google
   ignores), tell them before or instead of generating it. Valid schema.org
   markup that Google has no feature for is harmless but won't produce a rich
   result, and the user should know that before investing in it.

## Freshness

The pages are a snapshot taken on 2026-11-13. For anything where being current
matters a lot (a recently announced change, a beta feature, a deprecation),
mention the snapshot date and point to the live URL. If you have web access and
the stakes justify it, fetch the live page: appending `.md.txt` to any docs URL
returns its Markdown.

To refresh the whole copy (takes about 10 minutes, needs `requests` and
`beautifulsoup4`):

```bash
python scripts/crawl_search_docs.py --out references --force
python scripts/docs.py index
```

Then update the snapshot date in this file.

## Not covered

- Search Console help-centre articles (`support.google.com/webmasters`), the
  Search Central blog, and the Search Console / Indexing API references.
- Other search engines. Bing, Yandex and others have their own rules; don't
  present Google's as universal.
- Schema.org itself. These pages document the subset of properties Google
  uses, not the full vocabulary.

## Attribution

Documentation content is by Google, licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); code samples are
under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
See `NOTICE.md`. Pages are unmodified apart from the added front matter.
