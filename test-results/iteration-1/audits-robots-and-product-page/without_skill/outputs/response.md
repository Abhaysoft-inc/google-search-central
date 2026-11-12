# SEO audit: robots.txt and /checkout/thank-you

Neither of your two goals works as the files stand. The checkout pages are not reliably kept out of Google, and the kettle cannot get star ratings from this page.

I checked the two files by reading them only; nothing was run through Google's Rich Results Test or Search Console.

## Broken: fix before launch

### 1. The robots.txt block stops Google from seeing your `noindex`
`Disallow: /checkout/` stops Google from fetching the thank-you page, so it never reads the `<meta name="robots" content="noindex">` in it. A blocked URL can still be indexed as a bare URL if anything links to it.

**Fix:** use one mechanism, not both. To keep checkout out of Google, remove `Disallow: /checkout/` and serve `noindex` on every checkout page, as the meta tag or an `X-Robots-Tag: noindex` header.

### 2. The star-rating markup is on the wrong page
The `Product` markup sits on a page that is blocked and noindexed, so Google will never show a rich result from it. Even if the page were indexable, structured data must describe the main content of its page, and a "you might also like" link on an order confirmation does not qualify.

**Fix:** remove the JSON-LD from the thank-you page and put it on `https://www.brightkettle.example/products/kettle-pro`. That page must be indexable and must show the rating to shoppers.

### 3. The rating markup is invalid as written
`aggregateRating` has only `ratingValue`. Google also requires `ratingCount` or `reviewCount`, so the markup is not eligible for stars wherever it lives.

**Fix:** add the real count. The rating and count must come from genuine customer reviews visible on the product page.

### 4. `Noindex: /old-catalogue/` does nothing
Google has not supported `noindex` lines in robots.txt since 2019. The line is ignored, so `/old-catalogue/` is fully crawlable and indexable.

**Fix:** if you want those pages out of Google, add `noindex` to the pages themselves, or redirect them (301) or retire them (404/410). Do not also add a `Disallow` for them, for the reason in item 1.

### 5. `Googlebot-Image` is blocked from the whole site
`User-agent: Googlebot-Image` / `Disallow: /` removes every image on the site from Google Images. It also stops Google using your product photos as thumbnails in product results.

**Fix:** delete that group, unless blocking images was a deliberate decision. For a shop it rarely is.

### 6. The sitemap line is invalid
`Sitemap: /sitemap.xml` is a relative path. Google requires a full URL and ignores this line.

**Fix:** `Sitemap: https://www.brightkettle.example/sitemap.xml` (I assumed that is where the sitemap lives).

### 7. The canonical contradicts the `noindex`
The thank-you page says "don't index me" and also "my canonical is the homepage". These are conflicting signals, and the page is not a duplicate of the homepage.

**Fix:** remove the canonical tag from the thank-you page.

## Nice-to-have

- **`Crawl-delay: 10`:** Google ignores it, so it is harmless there. Other crawlers such as Bing honour it, and 10 seconds is slow for a shop, so I would remove it.
- **Fuller product markup:** on the product page, add `offers` (price, currency, availability), `brand`, `sku` and `description`. Stars need only the valid rating, but price and availability can then show too.
- **Absolute image URL:** in the JSON-LD, use `https://www.brightkettle.example/img/kettle-pro.jpg` rather than `/img/kettle-pro.jpg`.
- **`/cart/`:** it has the same block-versus-noindex issue as checkout. I left it blocked because you only asked about checkout; treat it the same way if you want it guaranteed out of the index.
- **Viewport tag:** the thank-you page has none. That is a mobile usability point for customers, not an SEO one, since the page is noindexed.

Even with everything fixed, Google does not guarantee stars will show. Run the product page through the Rich Results Test after the change.

## Corrected files

The robots.txt drops the checkout block, so only deploy it together with `noindex` on all checkout pages, not just this one.

The JSON-LD snippet has `REPLACE_...` placeholders for review count, price, currency, SKU and description. Fill them with real values before it goes live.

Files are in the outputs folder:
- robots.txt
- thank-you.html
- product-page-jsonld-snippet.html
