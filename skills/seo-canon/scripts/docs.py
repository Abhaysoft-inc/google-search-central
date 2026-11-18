#!/usr/bin/env python3
"""Find things in the bundled Google Search Central docs. Standard library only.

  python scripts/docs.py search "hreflang x-default"      ranked pages + matching lines
  python scripts/docs.py search "noindex" -n 3 -l 8        top 3 pages, 8 lines each
  python scripts/docs.py outline appearance/structured-data/merchant-listing.md
                                                           headings with line numbers
  python scripts/docs.py index                             rebuild references/page-index.md
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
import sys
from pathlib import Path

REFS = Path(__file__).resolve().parent.parent / "references"
PAGES = REFS / "pages"

SECTIONS = [  # (path prefix, "Short name: description") - first match wins; order = display order
    ("fundamentals", "Fundamentals: SEO basics, how Search works, AI and helpful-content guidance"),
    ("essentials", "Search Essentials: technical requirements and spam policies"),
    ("crawling-docs/robots-txt", "robots.txt: syntax, rules and examples"),
    ("crawling-indexing/robots/", "robots.txt: syntax, rules and examples"),
    ("crawling-docs/crawlers-fetchers", "Google crawlers: user agents, verification, crawl rate"),
    ("crawling-docs", "Crawling: crawl budget, faceted navigation, HTTP status and network errors"),
    ("crawling-indexing/sitemaps", "Sitemaps: XML, image, video and news sitemaps"),
    ("crawling-indexing/javascript", "JavaScript SEO: rendering, lazy loading, dynamic rendering"),
    ("crawling-indexing/amp", "AMP: enhance, validate and remove AMP pages"),
    ("crawling-indexing", "Indexing: canonicals, redirects, noindex, meta tags, site moves, URLs, mobile"),
    ("appearance/structured-data", "Structured data: rich results, one page per feature"),
    ("appearance", "Search appearance: titles, snippets, images, video, Discover, ranking systems"),
    ("specialty/ecommerce", "Ecommerce: product data, URL structure, pagination"),
    ("specialty/international", "International: multilingual sites and hreflang"),
    ("specialty", "Explicit content: SafeSearch guidelines and troubleshooting"),
    ("monitor-debug/security", "Security: malware and social engineering"),
    ("monitor-debug", "Monitoring: Search Console, traffic drops, search operators"),
    ("", "Overview: top-level landing pages"),
]


def read_page(path: Path) -> tuple[dict, list[str]]:
    """Return (front matter, all lines). Line numbers stay those of the file on disk."""
    lines = path.read_text("utf-8").splitlines()
    meta: dict[str, str] = {}
    if lines and lines[0] == "---":
        for line in lines[1:]:
            if line == "---":
                break
            key, _, value = line.partition(":")
            meta[key.strip()] = html.unescape(value.strip().strip('"').replace('\\"', '"'))
    return meta, lines


def all_pages() -> list[Path]:
    return sorted(PAGES.rglob("*.md"))


def rel(path: Path) -> str:
    return path.relative_to(PAGES).as_posix()


def cmd_search(args: argparse.Namespace) -> int:
    terms = [t.lower() for t in re.findall(r"[\w@:.\-]+", args.query)]
    if not terms:
        print("empty query", file=sys.stderr)
        return 2
    pages = [(path, *read_page(path)) for path in all_pages()]
    # Rare words say more about a page than common ones ("faq" vs "data").
    weight_of = {}
    for t in terms:
        df = sum(1 for _, _, lines in pages if any(t in line.lower() for line in lines))
        weight_of[t] = math.log((len(pages) + 1) / (df + 1)) + 0.2
    total = sum(weight_of.values())
    results = []
    for path, meta, lines in pages:
        title = meta.get("title", "").lower()
        name = rel(path).lower()
        score, hits, found = 0.0, [], set()
        for no, line in enumerate(lines, 1):
            low = line.lower()
            matched = [t for t in terms if t in low]
            if not matched:
                continue
            found.update(matched)
            line_score = sum(weight_of[t] for t in matched) * (4 if line.startswith("#") else 1)
            score += line_score
            hits.append((line_score, no, line.strip()))
        for t in terms:
            if t in title or t in name:
                score += 25 * weight_of[t]
                found.add(t)
        if not found:
            continue
        # strongly prefer pages covering every (important) term
        score *= (sum(weight_of[t] for t in found) / total) ** 2
        results.append((score, path, meta, hits))
    results.sort(key=lambda r: -r[0])
    if not results:
        print("No matches. Try fewer or different words, or read references/page-index.md.")
        return 1
    for score, path, meta, hits in results[: args.pages]:
        print(f"\n## references/pages/{rel(path)}")
        print(f"   {meta.get('title', '')}  <{meta.get('url', '')}>")
        best = sorted(sorted(hits, key=lambda h: -h[0])[: args.lines], key=lambda h: h[1])
        for _, no, text in best:
            print(f"   {no:>5}: {text[:200]}")
    rest = len(results) - args.pages
    if rest > 0:
        print(f"\n({rest} more pages matched; raise -n to see them)")
    return 0


def cmd_outline(args: argparse.Namespace) -> int:
    path = PAGES / args.page.removeprefix("references/pages/")
    if not path.exists():
        print(f"not found: {path}", file=sys.stderr)
        return 2
    meta, lines = read_page(path)
    print(f"{meta.get('title', '')}  <{meta.get('url', '')}>  ({len(lines)} lines)")
    fenced = False
    for no, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced and re.match(r"#{1,4} ", line):
            print(f"{no:>5}: {line}")
    return 0


def cmd_index(_: argparse.Namespace) -> int:
    groups: dict[str, list[str]] = {}
    for path in all_pages():
        meta, lines = read_page(path)
        r = rel(path)
        heading = next(h for prefix, h in SECTIONS if r.startswith(prefix))
        groups.setdefault(heading, []).append(
            f"- `{r}` - {meta.get('title', r)} ({len(lines)} lines)")
    out = ["# Page index", "",
           "Every bundled page, grouped by topic. Paths are relative to `references/pages/`.",
           "Generated by `python scripts/docs.py index`; do not edit by hand.", ""]
    for heading in dict.fromkeys(h for _, h in SECTIONS):
        if heading in groups:
            out += [f"## {heading}", "", *groups[heading], ""]
    (REFS / "page-index.md").write_text("\n".join(out), "utf-8")
    # Slim list for the GitHub Pages browser (index.html at the repo root).
    listing = []
    for path in all_pages():
        meta, lines = read_page(path)
        r = rel(path)
        listing.append({"file": r, "title": meta.get("title", r), "url": meta.get("url", ""),
                        "section": next(h for prefix, h in SECTIONS if r.startswith(prefix))})
    order = list(dict.fromkeys(h for _, h in SECTIONS))
    listing.sort(key=lambda p: (order.index(p["section"]), p["file"]))
    (REFS / "pages.json").write_text(json.dumps(listing, ensure_ascii=False, indent=0), "utf-8")
    print(f"wrote {REFS / 'page-index.md'} ({sum(map(len, groups.values()))} pages)")
    return 0


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="keyword search across all pages")
    s.add_argument("query")
    s.add_argument("-n", "--pages", type=int, default=6, help="pages to show (default 6)")
    s.add_argument("-l", "--lines", type=int, default=5, help="matching lines per page (default 5)")
    s.set_defaults(func=cmd_search)
    o = sub.add_parser("outline", help="headings of one page, with line numbers")
    o.add_argument("page", help="path relative to references/pages/")
    o.set_defaults(func=cmd_outline)
    i = sub.add_parser("index", help="rebuild references/page-index.md")
    i.set_defaults(func=cmd_index)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
