# google-search-central

An agent skill that bundles an offline copy of Google's official Search
documentation (185 pages from
[developers.google.com/search/docs](https://developers.google.com/search/docs)
and [developers.google.com/crawling/docs](https://developers.google.com/crawling/docs))
so Claude and other agents can ground SEO work in what Google actually
publishes instead of in memory.

Docs snapshot: **2026-11-13**.

## What it does

- **Answers with citations** - what Google requires, supports or recommends,
  with a link to the source page for every claim.
- **Audits** - checks a page, robots.txt, sitemap or JSON-LD against the docs
  and separates real violations from recommendations.
- **Generates compliant output** - JSON-LD, robots.txt rules, hreflang, meta
  robots tags and so on, with required vs recommended properties and no
  invented values.

## Install

The repository root is the skill folder.

**Claude Code** (all projects):

```bash
git clone https://github.com/Abhaysoft-inc/google-search-central ~/.claude/skills/google-search-central
```

For a single project, clone into `.claude/skills/google-search-central` inside
that project instead.

**Claude desktop / claude.ai**: zip the folder (or use a packaged `.skill`
file) and upload it under Settings > Capabilities > Skills.

**Other agent harnesses**: point the agent at this folder. `SKILL.md` is the
entry point; everything else is plain Markdown plus two Python scripts.

## Layout

| Path | Contents |
|---|---|
| `SKILL.md` | When to use the skill, topic map, and instructions |
| `references/pages/` | The 185 doc pages as Markdown, mirroring the site's URL structure |
| `references/page-index.md` | Every page grouped by topic |
| `references/index.json` | Crawl manifest (title, URL, links per page) |
| `scripts/docs.py` | Keyword search, page outlines, index rebuild (standard library only) |
| `scripts/crawl_search_docs.py` | The crawler used to fetch the docs |
| `evals/` | Three test cases with pass/fail checks |
| `test-results/` | Outputs and scores from the first test run |

## Searching the docs

```bash
python scripts/docs.py search "hreflang x-default"
python scripts/docs.py outline appearance/structured-data/merchant-listing.md
```

## Refreshing the docs

Needs `requests` and `beautifulsoup4`; takes about 10 minutes.

```bash
python scripts/crawl_search_docs.py --out references --force
python scripts/docs.py index
```

Then update the snapshot date in `SKILL.md`, `NOTICE.md` and this file.

## Test results

Three prompts were run once each with and without the skill
(`test-results/iteration-1/`, summary in `benchmark.md`; open
`test-results/results.html` for a side-by-side view). The skill passed 19 of
19 checks against 16 of 19 without it. The sample is small and was graded by
the skill's author, so treat it as a rough signal. The baseline's misses were
missing source links and an outdated account of FAQ rich results; skill runs
used roughly 30-70% more tokens.

## Attribution

The documentation under `references/pages/` is by Google and licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); code samples in it
are under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
See [NOTICE.md](NOTICE.md). This project is not affiliated with or endorsed by
Google.
