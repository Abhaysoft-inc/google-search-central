# SEO audit: robots.txt and /checkout/thank-you

Checked against Google's Search Central documentation (snapshot dated 2026-11-13). I only had the two files, so I could not check the live response headers, the rendered page, the sitemap, or `/products/kettle-pro`.

## Verdict

Neither goal works as the files stand.

- **Keeping checkout out of Google:** not reliable. robots.txt blocks Google from crawling `/checkout/`, so Google never sees the page's `noindex`, and the URL can still be indexed.
- **Star ratings for the kettle:** will not show. The markup is on a page you are hiding from Google, the rating is not visible on the page, and a required property is missing. The markup belongs on the kettle's own product page.

Corrected files are in the same outputs folder as this response:

- `robots.txt`
- `thank-you.html`
- `kettle-pro-product-jsonld.html` (markup for the product page, with placeholders for the real rating data)

## Broken (fix before launch)

### 1. `Disallow: /checkout/` cancels the page's `noindex`

- **Where:** robots.txt line 3 (`Disallow: /checkout/`) together with thank-you.html line 6 (`<meta name="robots" content="noindex">`).
- **What Google says:** for `noindex` to work, the page must not be blocked by robots.txt. If it is, the crawler never sees the rule and the page "can still appear in search results" ([Block Search indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing)). Google also warns against using robots.txt to hide pages from results, because a disallowed URL can still be indexed if it is linked from elsewhere ([Introduction to robots.txt](https://developers.google.com/search/docs/crawling-indexing/robots/intro)).
- **Fix:** remove `Disallow: /checkout/` and keep `noindex` on every checkout URL. An `X-Robots-Tag: noindex` response header on the whole `/checkout/` path does the same job without relying on each template.
- **Same trap for `/cart/`:** it is also only disallowed. If you want cart URLs guaranteed out of results too, treat them the same way. I left `Disallow: /cart/` in place because you only asked about checkout.

### 2. Star ratings cannot show from the thank-you page

There are four separate blockers in the `Product` JSON-LD (thank-you.html lines 8-19):

| Problem | What Google says |
|---|---|
| The page is `noindex` and blocked in robots.txt. | Don't block structured data pages with robots.txt, `noindex` or other access controls ([General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)). A page that is not in the index has no search result to carry stars. |
| `aggregateRating` has no `ratingCount` or `reviewCount`. | At least one of the two is required ([Review snippet](https://developers.google.com/search/docs/appearance/structured-data/review-snippet)). |
| The 4.9 rating appears nowhere in the visible page. | With `AggregateRating`, users must be able to see that rating on the page, and you must not mark up content that is not visible ([Review snippet](https://developers.google.com/search/docs/appearance/structured-data/review-snippet), [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)). |
| The page is an order confirmation, not a page about the kettle. | Product rich results only support pages that focus on a single product, and markup must not be unrelated to the focus of the page ([Product snippet](https://developers.google.com/search/docs/appearance/structured-data/product-snippet), [General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)). |

The review snippet guidelines carry a manual-action warning for violations, so the markup is worth removing from this page, not just leaving in place.

**Fix:**

1. Delete the JSON-LD from the thank-you page (done in the corrected file).
2. Put `Product` markup on `https://www.brightkettle.example/products/kettle-pro`, using `kettle-pro-product-jsonld.html` as the starting point.
3. Fill in the real average rating and the real number of ratings, and show both on that product page. I left placeholders because I don't know the true count and could not confirm where 4.9 comes from.
4. The ratings must be collected on your own site. Google says not to aggregate ratings from other websites.
5. Make sure the product page is crawlable and indexable, then test it with the Rich Results Test.

Google does not guarantee rich results even for valid markup, so this makes the page eligible, not certain.

### 3. `Googlebot-Image` is blocked from the whole site

- **Where:** robots.txt lines 7-8 (`User-agent: Googlebot-Image` / `Disallow: /`).
- **What Google says:** this rule blocks all your images from Google, and it affects Google Images, Discover and every Search feature that shows images, logos and favicons ([Useful robots.txt rules](https://developers.google.com/crawling/docs/robots-txt/useful-robots-txt-rules), [Google's common crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers)). Image URLs in structured data must be crawlable and indexable ([General structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)).
- **Fix:** I removed the group in the corrected file, on the assumption that a shop wants its product photos in Google. If the block is deliberate, put it back, but expect no product images in search results.

### 4. The `Sitemap:` line is not a valid URL

- **Where:** robots.txt line 10 (`Sitemap: /sitemap.xml`).
- **What Google says:** the value must be a fully qualified URL including protocol and host ([How Google interprets the robots.txt specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)).
- **Fix:** `Sitemap: https://www.brightkettle.example/sitemap.xml`. I assumed the sitemap lives on the `www` host; adjust if not.

### 5. `Noindex: /old-catalogue/` does nothing

- **Where:** robots.txt line 5.
- **What Google says:** a `noindex` rule in robots.txt is not supported ([Block Search indexing with noindex](https://developers.google.com/search/docs/crawling-indexing/block-indexing)). Google ignores the line, so `/old-catalogue/` is currently crawlable and indexable.
- **Fix:** I removed the line. If those pages should leave Google, add a `noindex` meta tag or `X-Robots-Tag` header to them and leave them crawlable. If they have been replaced, a 301 redirect to the new pages is the usual choice (general practice; it depends on what the old catalogue is).

## Nice-to-have

- **Canonical pointing at the homepage** (thank-you.html line 7). Google documents `rel="canonical"` as a way to consolidate duplicate or very similar pages, and the thank-you page is not a duplicate of the homepage ([How to specify a canonical URL](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)). Combining it with `noindex` also sends mixed signals; that point is general SEO practice, not something the docs state. I removed the tag, since `noindex` alone does the job.
- **`Crawl-delay: 10`** (robots.txt line 2). Google does not support this field and ignores it ([How Google interprets the robots.txt specification](https://developers.google.com/crawling/docs/robots-txt/robots-txt-spec)). It is harmless. I kept it in case you set it for other search engines; delete it if it was meant for Google.
- **Relative image URL in the markup** (`"image": "/img/kettle-pro.jpg"`). Google's examples all use absolute URLs. I did not find a rule in the docs that forbids relative ones, so treat this as best practice. The new product-page snippet uses the absolute URL.

## Fine

- The `noindex` meta tag itself is correctly written and is the right tool for this page.
- `User-agent` and `Disallow` syntax is valid, and the groups are structured correctly.
- `Product` has the required `name`, and `aggregateRating` satisfies the "one of `review`, `aggregateRating` or `offers`" requirement, so the markup's shape is right once it moves to the product page and gains a count.
- The link to `/products/kettle-pro` is a normal crawlable `<a href>`, and the image has descriptive alt text.

## After you deploy

- Confirm in Search Console's URL Inspection tool that a checkout URL is crawlable and reports `noindex`.
- If any checkout URLs are already indexed, they drop out only after Google recrawls them and sees the `noindex`.
- Run the product page through the Rich Results Test once the real rating data is in.
