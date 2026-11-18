#!/usr/bin/env python3
"""Crawl every page under https://developers.google.com/search/docs and /crawling/docs
(where Google moved the crawler and robots.txt pages) and save it as Markdown.

How it works
  * Starts at both docs roots and follows every link that stays under them
    (the left-hand navigation on each page lists the whole doc tree).
  * Content comes from Google's own Markdown export (<page-url>.md.txt). If that
    is missing for a page, the article HTML is converted to plain text instead.
  * Output:  <out>/pages/<same path as the URL>.md   one file per page, with
             a small front-matter block (title, url, source format);
             /crawling/docs pages go under <out>/pages/crawling-docs/
             <out>/index.json                         manifest of every page
  * Safe to re-run: pages already saved are skipped (use --force to refetch).

Usage
  python crawl_search_docs.py                  # crawl into ./google-search-docs
  python crawl_search_docs.py --out docs --delay 1.0
  python crawl_search_docs.py --force          # refetch everything

Requires: requests, beautifulsoup4
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup

HOST = "developers.google.com"
ROOT = f"https://{HOST}/search/docs"
# URL path prefix -> subfolder of pages/ that its pages are saved in
SCOPES = {"/search/docs": "", "/crawling/docs": "crawling-docs"}
SEEDS = [ROOT]  # /crawling/docs has no landing page; its pages are reached by links
USER_AGENT = "search-docs-crawler/1.0 (personal offline documentation copy)"


def scope_of(path: str) -> str | None:
    for prefix in SCOPES:
        if path == prefix or path.startswith(prefix + "/"):
            return prefix
    return None


def normalize(href: str, base: str) -> str | None:
    """Absolute, canonical URL if href is a page inside one of SCOPES, else None."""
    parts = urlsplit(urljoin(base, href))
    if parts.scheme not in ("http", "https") or parts.netloc != HOST:
        return None
    path = parts.path.rstrip("/")
    if scope_of(path) is None:
        return None
    if re.search(r"\.(png|jpe?g|gif|svg|webp|pdf|zip|txt|xml|json|mp4)$", path, re.I):
        return None
    return f"https://{HOST}{path}"  # query (?hl=..) and #fragment dropped


class Fetcher:
    def __init__(self, delay: float, retries: int = 5):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self.delay = delay
        self.retries = retries
        self._last = 0.0

    def get(self, url: str) -> requests.Response | None:
        """GET with polite delay and backoff. Returns None on 404 or repeated failure."""
        for attempt in range(self.retries):
            wait = self.delay - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            try:
                resp = self.session.get(url, timeout=30)
                self._last = time.monotonic()
            except requests.RequestException as exc:
                self._last = time.monotonic()
                err = type(exc).__name__
            else:
                if resp.status_code == 200:
                    return resp
                if resp.status_code in (404, 410):
                    return None
                err = f"HTTP {resp.status_code}"
            backoff = min(60, 3 * 2**attempt)
            print(f"    {err} on {url} - retry in {backoff}s", file=sys.stderr)
            time.sleep(backoff)
        return None


def html_to_text(soup: BeautifulSoup) -> str:
    """Fallback when the Markdown export is unavailable."""
    body = soup.select_one("div.devsite-article-body") or soup.find("article") or soup.body
    if body is None:
        return ""
    for tag in body.select("script, style, devsite-feedback, devsite-toc"):
        tag.decompose()
    text = body.get_text("\n")
    return re.sub(r"\n\s*\n\s*\n+", "\n\n", text).strip()


def page_title(soup: BeautifulSoup, markdown: str | None, url: str) -> str:
    if markdown:
        m = re.search(r"^#\s+(.+)$", markdown, re.M)
        if m:
            return m.group(1).split(" | ")[0].strip()
    if soup.title and soup.title.string:
        return soup.title.string.split(" | ")[0].strip()
    return url.rsplit("/", 1)[-1]


def out_path(pages_dir: Path, url: str) -> Path:
    path = urlsplit(url).path
    prefix = scope_of(path)
    rel = path.removeprefix(prefix).strip("/")
    return pages_dir / SCOPES[prefix] / f"{rel or 'index'}.md"


def crawl(out: Path, delay: float, force: bool, limit: int | None) -> int:
    pages_dir = out / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    index_file = out / "index.json"
    index: dict[str, dict] = {}
    if index_file.exists() and not force:
        index = {p["url"]: p for p in json.loads(index_file.read_text("utf-8"))["pages"]}

    fetcher = Fetcher(delay)
    queue, seen = deque(SEEDS), set(SEEDS)
    failed: list[str] = []
    done = 0

    def save_index() -> None:
        pages = sorted(index.values(), key=lambda p: p["url"])
        index_file.write_text(
            json.dumps({"roots": SEEDS, "count": len(pages), "failed": failed, "pages": pages},
                       indent=2, ensure_ascii=False), "utf-8")

    while queue and (limit is None or done < limit):
        url = queue.popleft()
        entry = index.get(url)
        cached = entry is not None and (out / entry["file"]).exists()

        if cached:
            links = entry["links"]
            status = "cached"
        else:
            html = fetcher.get(url)
            if html is None:
                print(f"[fail] {url}")
                failed.append(url)
                continue
            final = normalize(html.url, url)
            if final is None:  # redirected out of scope
                print(f"[skip] {url} -> {html.url}")
                continue
            if final != url and (final in index or final in seen):
                continue  # old URL redirecting to a page that is saved or queued
            seen.add(final)
            soup = BeautifulSoup(html.text, "html.parser")
            links = sorted({n for a in soup.find_all("a", href=True)
                            if (n := normalize(a["href"], final))})

            md = fetcher.get(final + ".md.txt")
            markdown = md.text.strip() if md is not None and "markdown" in md.headers.get(
                "content-type", "") else None
            content = markdown or html_to_text(soup)
            if not content:
                print(f"[fail] {url} (no content)")
                failed.append(url)
                continue
            source = "markdown" if markdown else "html-text"
            title = page_title(soup, markdown, final)

            path = out_path(pages_dir, final)
            path.parent.mkdir(parents=True, exist_ok=True)
            front = f"---\ntitle: {json.dumps(title, ensure_ascii=False)}\nurl: {final}\nsource: {source}\n---\n\n"
            path.write_text(front + content + "\n", "utf-8")
            index[final] = {"url": final, "title": title, "source": source,
                            "file": path.relative_to(out).as_posix(),
                            "chars": len(content), "links": links}
            status = source

        done += 1
        new = [l for l in links if l not in seen]
        seen.update(new)
        queue.extend(new)
        print(f"[{done:>4}] {status:<9} queue={len(queue):<4} {url}")
        if done % 20 == 0:
            save_index()

    save_index()
    print(f"\nDone: {len(index)} pages in {out}  ({len(failed)} failed)")
    for f in failed:
        print(f"  failed: {f}")
    return 1 if failed else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=Path("google-search-docs"), help="output folder")
    ap.add_argument("--delay", type=float, default=0.5, help="seconds between requests")
    ap.add_argument("--force", action="store_true", help="refetch pages already saved")
    ap.add_argument("--limit", type=int, help="stop after N pages (for testing)")
    args = ap.parse_args()
    return crawl(args.out, args.delay, args.force, args.limit)


if __name__ == "__main__":
    sys.exit(main())
