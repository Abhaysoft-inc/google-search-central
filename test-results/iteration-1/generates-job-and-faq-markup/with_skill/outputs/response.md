The job markup is below and ready to paste, but the FAQ half won't get you what you're after: Google no longer documents an FAQ rich result, so FAQ schema will not produce the expandable questions in search results.

## 1. JobPosting JSON-LD

Paste this into the HTML of the single job page (not a listings page):

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "JobPosting",
  "title": "Senior Data Engineer",
  "description": "<p>Design and run our batch and streaming data pipelines on GCP. You will own data quality for the analytics platform and mentor two junior engineers.</p><p>5+ years of data engineering experience required.</p><p>This is a full-time, 100% remote position. Applicants must live in Canada.</p>",
  "datePosted": "2026-11-10",
  "validThrough": "2026-12-15T23:59",
  "employmentType": "FULL_TIME",
  "jobLocationType": "TELECOMMUTE",
  "applicantLocationRequirements": {
    "@type": "Country",
    "name": "Canada"
  },
  "hiringOrganization": {
    "@type": "Organization",
    "name": "Northwind Analytics",
    "sameAs": "https://www.northwind-analytics.example"
  },
  "experienceRequirements": {
    "@type": "OccupationalExperienceRequirements",
    "monthsOfExperience": 60
  }
}
</script>
```

Things to check before you publish:

- **Remote wording in the description.** I added the last paragraph ("100% remote… must live in Canada") from the facts you gave me. Google requires the job description itself to clearly state that the job is 100% remote and where applicants may be located, and the markup has to match what is visible on the page. Add that sentence to the on-page description too, or reword both to match.
- **Closing time.** I set `validThrough` to the end of 15 December with no time zone. If applications close at a specific time, change it and add your UTC offset, e.g. `2026-12-15T23:59:00-05:00`.
- **Thin description.** Google does not allow incomplete job descriptions and expects responsibilities, qualifications, skills, hours and education/experience requirements. If the page has more detail than the three sentences you sent, put the full text in `description`.
- **A way to apply.** The page must let people apply, and must be viewable without a login.
- **When the job closes or is filled.** Remove the page or the markup, or leave `validThrough` in the past. Expired jobs left live can lead to a manual action.

What is and isn't in the markup:

| Property | Status | Note |
|---|---|---|
| `title`, `description`, `datePosted`, `hiringOrganization` | Required | Included. |
| `jobLocation` | Required, except for remote jobs | Left out: not needed when `applicantLocationRequirements` is present and there is no office to report to. |
| `jobLocationType`, `applicantLocationRequirements` | Required for 100% remote jobs | Included (`TELECOMMUTE`, Canada). |
| `validThrough` | Required when the posting has an expiry date | Included. |
| `employmentType` | Recommended | Included. |
| `experienceRequirements` | Recommended (beta) | Included as 60 months; Google says it may have no visible effect yet. |
| `baseSalary`, `identifier`, `directApply`, `hiringOrganization.logo` | Recommended | Left out because you didn't give me values. Add them if you have a salary shown on the page, a job/requisition ID, a one-step application on your own site, or a logo URL. |

Source: [Job posting (JobPosting) structured data](https://developers.google.com/search/docs/appearance/structured-data/job-posting).

## 2. FAQ schema: not supported for rich results

- **No FAQ feature.** FAQ is absent from Google's [list of supported structured data](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) (checked against a copy of the docs dated 2026-11-13), and there is no FAQ documentation page any more.
- **`QAPage` is not a substitute.** Google's [Q&A docs](https://developers.google.com/search/docs/appearance/structured-data/qapage) say not to use it for FAQ pages written by the site itself or for pages with multiple questions.

My recommendation is to keep the three questions as visible content on the page and skip the FAQ markup. They still help candidates, and the "fully remote, anywhere in Canada" answer backs up the remote claim in the job markup.

If you want the markup anyway, this is valid schema.org and harmless alongside the JobPosting, but it will not produce a rich result in Google:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Is this role fully remote?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Yes, anywhere in Canada."
      }
    },
    {
      "@type": "Question",
      "name": "Do you sponsor visas?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Not for this role."
      }
    },
    {
      "@type": "Question",
      "name": "What is the interview process?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A recruiter call, a take-home exercise, and a panel interview."
      }
    }
  ]
}
</script>
```

## 3. Validate and get it crawled

1. Run the page through the [Rich Results Test](https://search.google.com/test/rich-results); it should detect one valid Job posting item. I have not run this markup through the test myself.
2. After deploying, check the page with URL Inspection in Search Console.
3. For job URLs Google recommends notifying it through the Indexing API rather than relying on the sitemap alone, both when the job goes live and when it closes.

Google does not guarantee that valid markup will be shown in the job experience ([general structured data guidelines](https://developers.google.com/search/docs/appearance/structured-data/sd-policies)).
