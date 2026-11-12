# Fake Googlebots, Google-Extended and GoogleOther

**Short answers**

1. **Verifying Googlebot:** ignore the user agent, because Google itself warns it can be spoofed. Check the IP instead, either with a reverse-then-forward DNS lookup or by matching it against Google's published IP ranges.
2. **Blocking Google-Extended:** Google states it does not affect your inclusion in Search and is not a ranking signal. It also does not remove your content from AI Overviews or AI Mode, which may not be what your boss expects.
3. **GoogleOther:** it is a real Google crawler, not a threat. Blocking it does not affect any specific Google product, including Search.

Everything below comes from Google's own documentation (as of 13 November 2026), with links you can forward.

## 1. How to check which "Googlebot" requests are really Google

Google's crawler list carries this caution: "The HTTP user agent string can be spoofed." ([List of Google's common crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers))

Google documents two verification methods ([Verify requests from Google crawlers and fetchers](https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests)).

### Method A: DNS lookup (for a handful of IPs)

1. Run a reverse DNS lookup on the IP from your logs.
2. Check that the hostname is under `googlebot.com`, `google.com` or `googleusercontent.com`.
3. Run a forward DNS lookup on that hostname.
4. Check that it returns the same IP you started with.

Step 4 matters because anyone can set a reverse DNS record on their own IP that claims to be `googlebot.com`; only Google can make the forward lookup point back.

Google's own example:

```
host 66.249.66.1
1.66.249.66.in-addr.arpa domain name pointer crawl-66-249-66-1.googlebot.com.

host crawl-66-249-66-1.googlebot.com
crawl-66-249-66-1.googlebot.com has address 66.249.66.1
```

On Windows, `nslookup 66.249.66.1` followed by `nslookup crawl-66-249-66-1.googlebot.com` does the same job (this is my addition; Google's page only shows `host`).

For a request claiming to be Googlebot specifically, the hostname should match `crawl-***-***-***-***.googlebot.com` or `geo-crawl-***-***-***-***.geo.googlebot.com`. The other Google hostnames belong to other kinds of Google traffic:

| Type | Hostname pattern | IP range file |
|---|---|---|
| Common crawlers (Googlebot, GoogleOther and others) | `crawl-***.googlebot.com` or `geo-crawl-***.geo.googlebot.com` | [common-crawlers.json](https://developers.google.com/static/crawling/ipranges/common-crawlers.json) |
| Special-case crawlers (such as AdsBot) | `rate-limited-proxy-***.google.com` | [special-crawlers.json](https://developers.google.com/static/crawling/ipranges/special-crawlers.json) |
| User-triggered fetchers | `***.gae.googleusercontent.com` or `google-proxy-***.google.com` | [user-triggered-fetchers.json](https://developers.google.com/static/crawling/ipranges/user-triggered-fetchers.json), [user-triggered-fetchers-google.json](https://developers.google.com/static/crawling/ipranges/user-triggered-fetchers-google.json), [user-triggered-agents.json](https://developers.google.com/static/crawling/ipranges/user-triggered-agents.json) |

### Method B: match against Google's IP lists (for a whole log file)

Google recommends this for large-scale checks. Download the JSON files in the table above and test each logged IP against the ranges, which are in CIDR format. Most firewalls, WAFs and log tools can do this.

- An IP with a Googlebot user agent that is in `common-crawlers.json` is genuine.
- An IP with a Googlebot user agent that is in none of the lists, and fails the DNS check, is an impostor. You can block it without any effect on Search.

Two practical notes:

- **Do not judge by country.** Google says it crawls mainly from US IP addresses but may crawl from other countries if it detects a site blocking US requests, and your logs will show many different IPs. ([Overview of Google crawlers and fetchers](https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers))
- **Do not hard-code the ranges.** Fetch the JSON files on a schedule so your list stays current (my recommendation, not Google's wording).

## 2. Will blocking Google-Extended hurt rankings or remove you from Search?

**No.** Google's wording: "Google-Extended does not impact a site's inclusion in Google Search nor is it used as a ranking signal in Google Search." ([List of Google's common crawlers: Google-Extended](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended))

Google repeats this on a second page. ([Things to know about Google's web crawling](https://developers.google.com/crawling/docs/about-crawling))

### What blocking it does

Per the same Google-Extended section, the token controls whether content Google crawls from your site may be used for:

- training future generations of the Gemini models that power Gemini Apps and the Vertex AI API for Gemini
- grounding (supplying content from the Search index to the model at prompt time) in Gemini Apps and Grounding with Google Search on Vertex AI

So your boss is broadly right about training, with one side effect: your content also stops being used to ground answers in the Gemini app.

### What blocking it does not do

**It does not take you out of AI Overviews or AI Mode in Google Search.** Google says AI is built into Search, so the control for those features is Googlebot itself, plus the normal preview controls (`nosnippet`, `data-nosnippet`, `max-snippet`, `noindex`). Google-Extended is described as limiting AI training and grounding in "some of Google's other systems". ([AI features and your website](https://developers.google.com/search/docs/appearance/ai-features))

If the goal is "no Google AI use of our content at all", Google-Extended alone will not achieve it. The remaining options restrict how you appear in ordinary Search too, so that is a real trade-off.

### How to do it

Add this to robots.txt:

```
User-agent: Google-Extended
Disallow: /
```

Three things your team should know:

- **You will never see Google-Extended in your logs.** It has no user agent string of its own; crawling is done with existing Google user agents and the token is only a robots.txt control. ([Google-Extended](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers#google-extended))
- **Do not try to block it at the firewall or by user agent.** There is nothing to match, and you risk blocking the real Googlebot, which would hurt Search.
- **Do not put the rule under `User-agent: Googlebot` or `User-agent: *` with `Disallow: /`.** That blocks Search crawling.

Google's docs also note it intends to support a shared AI-training preference signal (`user-agent: __usage_ai-training`) in early 2027. That is a stated intention, so check the live page before relying on it.

## 3. Is GoogleOther something to worry about?

**No.** Google describes GoogleOther as a generic crawler that various product teams may use to fetch publicly accessible content, for example one-off crawls for internal research and development. ([List of Google's common crawlers: GoogleOther](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers))

- **Blocking it has no Search impact.** Google says crawl preferences for `GoogleOther` "don't affect any specific product".
- **It obeys robots.txt.** It is a common crawler, and those always follow robots.txt for automatic crawls.
- **There are two variants**, `GoogleOther-Image` and `GoogleOther-Video`, each with its own token.
- **It can be spoofed too.** Verify it the same way as Googlebot; genuine requests come from the same common-crawler ranges and hostnames.

Google's docs do not say whether GoogleOther's fetches feed AI training. They only give the generic description above, so I would not tell your boss either way.

Blocking it is optional. If you want to save server load:

```
User-agent: GoogleOther
Disallow: /

User-agent: GoogleOther-Image
Disallow: /

User-agent: GoogleOther-Video
Disallow: /
```

## Sources to forward

- [Verify requests from Google crawlers and fetchers](https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests): the DNS method and the IP range files.
- [List of Google's common crawlers](https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers): the spoofing caution, GoogleOther, and the Google-Extended statement on rankings.
- [Things to know about Google's web crawling](https://developers.google.com/crawling/docs/about-crawling): the second statement that Google-Extended does not affect Search inclusion or ranking.
- [AI features and your website](https://developers.google.com/search/docs/appearance/ai-features): why Google-Extended does not control AI Overviews or AI Mode.
- [Overview of Google crawlers and fetchers](https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers): crawler categories and where Google crawls from.
