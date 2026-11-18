# seo-canon

A Claude Code plugin and agent skill that bundles an offline copy of Google's official Search
documentation (185 pages from
[developers.google.com/search/docs](https://developers.google.com/search/docs)
and [developers.google.com/crawling/docs](https://developers.google.com/crawling/docs))
so Claude and other agents can ground SEO work in what Google actually
publishes instead of in memory.

Docs snapshot: **2026-11-13**.

Browse the bundled pages online: <https://abhaysoft-inc.github.io/seo-canon/>

## What it does

- **Answers with citations** - what Google requires, supports or recommends,
  with a link to the source page for every claim.
- **Audits** - checks a page, robots.txt, sitemap or JSON-LD against the docs
  and separates real violations from recommendations.
- **Generates compliant output** - JSON-LD, robots.txt rules, hreflang, meta
  robots tags and so on, with required vs recommended properties and no
  invented values.

## Install

**Claude Code** (as a plugin, gets updates):

```bash
claude plugin install seo-canon --marketplace Abhaysoft-inc/seo-canon
```

Or inside a session:

```
/plugin install seo-canon --marketplace Abhaysoft-inc/seo-canon
```

To update later: `claude plugin update seo-canon@abhaysoft`.

**Claude desktop / claude.ai**: zip the `skills/seo-canon` folder (or use a
packaged `.skill` file) and upload it under Settings > Capabilities > Skills.

**Other agent harnesses**: point the agent at `skills/seo-canon/`.
`SKILL.md` is the entry point; everything else is plain Markdown plus two
Python scripts.

## Layout

The repository is a Claude Code plugin and its own one-plugin marketplace.

| Path | Contents |
|---|---|
| `.claude-plugin/plugin.json` | Plugin manifest |
| `.claude-plugin/marketplace.json` | Marketplace `abhaysoft`, listing this plugin |
| `skills/seo-canon/SKILL.md` | When to use the skill, topic map, and instructions |
| `skills/seo-canon/references/pages/` | The 185 doc pages as Markdown, mirroring the site's URL structure |
| `skills/seo-canon/references/page-index.md` | Every page grouped by topic |
| `skills/seo-canon/references/index.json` | Crawl manifest (title, URL, links per page) |
| `skills/seo-canon/references/pages.json` | Slim page list used by the website |
| `skills/seo-canon/scripts/docs.py` | Keyword search, page outlines, index rebuild (standard library only) |
| `skills/seo-canon/scripts/crawl_search_docs.py` | The crawler used to fetch the docs |
| `skills/seo-canon/NOTICE.md` | Attribution for Google's documentation |
| `index.html`, `.nojekyll` | The GitHub Pages site that lists and renders every page |
| `evals/` | Three test cases with pass/fail checks (`claude plugin eval` reads them) |
| `test-results/` | Outputs and scores from the first test run |

## Searching the docs

Run from `skills/seo-canon/`:

```bash
python scripts/docs.py search "hreflang x-default"
python scripts/docs.py outline appearance/structured-data/merchant-listing.md
```

## Refreshing the docs

Needs `requests` and `beautifulsoup4`; takes about 10 minutes. Run from
`skills/seo-canon/`:

```bash
python scripts/crawl_search_docs.py --out references --force
python scripts/docs.py index
```

Then update the snapshot date in `SKILL.md`, `NOTICE.md`, `index.html` and
this file, and bump `version` in `.claude-plugin/plugin.json` so installed
copies pick up the change.

## Test results

Three prompts were run once each with and without the skill
(`test-results/iteration-1/`, summary in `benchmark.md`; open
`test-results/results.html` for a side-by-side view). The skill passed 19 of
19 checks against 16 of 19 without it. The sample is small and was graded by
the skill's author, so treat it as a rough signal. The baseline's misses were
missing source links and an outdated account of FAQ rich results; skill runs
used roughly 30-70% more tokens.

## License

The skill's own files (`SKILL.md`, scripts, test cases, this README) are under
the [MIT License](LICENSE). The bundled Google documentation is not; see below.

## Attribution

The documentation under `skills/seo-canon/references/pages/` is by Google and licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); code samples in it
are under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0).
See [NOTICE.md](skills/seo-canon/NOTICE.md). This project is not affiliated with or endorsed by
Google.
