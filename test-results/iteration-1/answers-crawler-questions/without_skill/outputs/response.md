# Googlebot verification, Google-Extended and GoogleOther

**Short answers**

- **Real vs fake Googlebot:** the user agent is trivially spoofed, so check the IP. Use a reverse DNS lookup followed by a forward lookup, or match the IP against Google's published IP range files.
- **Blocking Google-Extended:** it will not remove you from Google Search or hurt rankings. Google says so explicitly. It also will not keep your content out of AI Overviews or AI Mode, which may be what your boss actually expects.
- **GoogleOther:** it is a legitimate Google crawler and nothing to worry about. Blocking it is optional and does not affect Search.

I checked the details below against Google's live documentation today (13 Nov 2026).

## 1. Checking which "Googlebot" requests are really Google

### Option A: DNS check (good for spot-checking a few IPs)

1. Run a reverse DNS lookup on the IP from your logs.
2. Check that the hostname ends in `googlebot.com`, `google.com` or `googleusercontent.com`.
3. Run a forward DNS lookup on that hostname.
4. Check that it returns the same IP you started with.

Step 4 matters because anyone can set a reverse DNS record on their own IP to say `googlebot.com`. Only Google can make the forward lookup point back.

```
$ host 66.249.66.1
1.66.249.66.in-addr.arpa domain name pointer crawl-66-249-66-1.googlebot.com.

$ host crawl-66-249-66-1.googlebot.com
crawl-66-249-66-1.googlebot.com has address 66.249.66.1
```

On Windows, use `nslookup 66.249.66.1` and then `nslookup crawl-66-249-66-1.googlebot.com`.

The hostname pattern Google documents for each crawler type:

| Type | Reverse DNS pattern |
|---|---|
| Common crawlers (Googlebot, GoogleOther) | `crawl-*.googlebot.com` or `geo-crawl-*.geo.googlebot.com` |
| Special-case crawlers (e.g. AdsBot) | `rate-limited-proxy-*.google.com` |
| User-triggered fetchers | `*.gae.googleusercontent.com` or `google-proxy-*.google.com` |

A request with a Googlebot user agent should resolve to `googlebot.com`. Be careful with `googleusercontent.com`: from my own knowledge (not on Google's page), hostnames ending in `bc.googleusercontent.com` are Google Cloud customer VMs that anyone can rent. Treat those as not Googlebot.

### Option B: IP range match (better for bulk log analysis or firewall rules)

Google publishes its crawler IP ranges as JSON files in CIDR format:

- Common crawlers, including Googlebot: https://developers.google.com/static/crawling/ipranges/common-crawlers.json
- Special-case crawlers: https://developers.google.com/static/crawling/ipranges/special-crawlers.json
- User-triggered fetchers: https://developers.google.com/static/crawling/ipranges/user-triggered-fetchers.json
- User-triggered fetchers (Google): https://developers.google.com/static/crawling/ipranges/user-triggered-fetchers-google.json

Any request claiming to be Googlebot from an IP outside `common-crawlers.json` is an impersonator. The lists change, so re-fetch them on a schedule (daily is reasonable) rather than hardcoding them.

These files moved to `developers.google.com/static/crawling/ipranges/` from their older `/search/apis/ipranges/` location. If you have scripts using the old paths, update them.

### What to do with the fakes

You can safely block or rate-limit anything that fails verification; it has no effect on Google. Many CDNs and WAFs (Cloudflare, Akamai, Fastly and others) have a built-in "verified bots" feature that does this check for you.

One caution: do not block based on an IP "looking sketchy". Real Googlebot crawls mostly from US IPs, but not only, and from several ranges. Verify first, then block.

## 2. Will blocking Google-Extended hurt rankings or remove you from search?

No. Google's crawler documentation states:

> "Google-Extended does not impact a site's inclusion in Google Search nor is it used as a ranking signal in Google Search."

What your boss should know before deciding:

- **What it controls.** Google-Extended governs whether content Google crawls may be used to train future Gemini models, and for grounding in the Gemini apps and Vertex AI.
- **It is not a crawler.** It is only a robots.txt token and has no user agent string of its own. You will never see it in your logs and cannot block it at the firewall or WAF. The only way to use it is robots.txt.
- **It does not opt you out of AI Overviews or AI Mode.** Those are Search features fed by normal Googlebot crawling. Google's AI features page says the controls for them are the ordinary Search ones: `nosnippet`, `data-nosnippet`, `max-snippet` or `noindex`. Those do reduce how you appear in normal search results, so that is a real trade-off.
- **It only applies to Google.** Other AI companies have their own crawlers (for example GPTBot, ClaudeBot, CCBot) that need their own rules.

To block it, add this to `robots.txt`:

```
User-agent: Google-Extended
Disallow: /
```

Make sure it is a separate group and that your existing `User-agent: Googlebot` or `User-agent: *` rules are left unchanged. Accidentally disallowing Googlebot is what would hurt search.

## 3. Is GoogleOther something to worry about?

No. It is a genuine Google crawler, described by Google as a generic crawler that various product teams may use to fetch publicly accessible content, for example one-off crawls for internal research and development. There are also `GoogleOther-Image` and `GoogleOther-Video` variants.

- **It is separate from Search.** Google says robots.txt rules addressed to GoogleOther "don't affect any specific product", so blocking it will not change your indexing or rankings.
- **It respects robots.txt.** If it uses more server resources than you like, you can disallow it:

  ```
  User-agent: GoogleOther
  Disallow: /
  ```

- **It can be spoofed too.** Verify it the same way as Googlebot. It uses the same `googlebot.com` hostnames and the `common-crawlers.json` ranges.

Google does not say exactly which teams use GoogleOther or for what. If your boss's aim is to minimise all non-Search use of your content by Google, disallowing both Google-Extended and GoogleOther is the cautious choice and costs you nothing in Search.

## Sources to forward

All are official Google documentation:

1. **Verify requests from Google crawlers and fetchers** (DNS method, hostname patterns, IP range files): https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests
2. **List of Google's common crawlers** (Google-Extended and GoogleOther definitions, including the "does not impact … Google Search" statement): https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers
3. **AI features and your website** (how AI Overviews and AI Mode are controlled, and where Google-Extended fits): https://developers.google.com/search/docs/appearance/ai-features
4. **Overview of Google crawlers and fetchers** (the full crawler list and categories): https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers
5. **How Google interprets robots.txt** (rule syntax and user-agent group matching): https://developers.google.com/search/docs/crawling-indexing/robots/robots_txt

I opened sources 1 to 3 today and took the quotes from them. Sources 4 and 5 are from memory and I did not re-open them, so click through before forwarding in case the URLs have moved.
