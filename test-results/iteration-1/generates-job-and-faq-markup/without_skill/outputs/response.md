The job markup below is ready to paste, but the FAQ markup will not get you the expandable FAQ results. Google restricted FAQ rich results in August 2023 to well-known government and health sites, so a careers page is not eligible. I've included the FAQ JSON-LD anyway since it is valid and harmless, but it is optional.

I wrote both blocks from memory of Google's documentation and have not run them through a validator, so check them in the Rich Results Test before shipping.

## 1. JobPosting (this is the one that matters)

Paste into the `<head>` or `<body>` of the individual job page, not a listings page.

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org/",
  "@type": "JobPosting",
  "title": "Senior Data Engineer",
  "description": "<p>Design and run our batch and streaming data pipelines on GCP. You will own data quality for the analytics platform and mentor two junior engineers.</p><p>5+ years of data engineering experience required.</p>",
  "datePosted": "2026-11-10",
  "validThrough": "2026-12-15T23:59:59-08:00",
  "employmentType": "FULL_TIME",
  "hiringOrganization": {
    "@type": "Organization",
    "name": "Northwind Analytics",
    "sameAs": "https://www.northwind-analytics.example"
  },
  "jobLocationType": "TELECOMMUTE",
  "applicantLocationRequirements": {
    "@type": "Country",
    "name": "Canada"
  },
  "experienceRequirements": {
    "@type": "OccupationalExperienceRequirements",
    "monthsOfExperience": 60
  }
}
</script>
```

Things to check or fill in:

- **Closing time:** I set `validThrough` to 11:59 pm Pacific on 2026-12-15, so the job stays open through the end of that day everywhere in Canada. Change the time or offset if your deadline is different.
- **Remote setup:** `jobLocationType: TELECOMMUTE` plus `applicantLocationRequirements` of Canada is how Google expects a "100% remote, must live in Canada" job to be marked up. I left out `jobLocation` on purpose, because there is no physical work location.
- **Description:** it must match the text visible on the page. If the page has a longer description, put the full version here (HTML tags such as `<p>`, `<ul>`, `<li>` are fine).
- **Salary:** I did not add `baseSalary` because you didn't give one. Google recommends it if you publish a range on the page.
- **Logo:** add `"logo": "https://…"` inside `hiringOrganization` if you want your logo shown; I didn't invent a URL.
- **Job ID:** if you have an internal requisition number, add an `identifier` property.
- **After it closes:** on 2026-12-15, remove the markup, or return a 404/410 for the page. Leaving expired postings marked up can lead to a manual action.

## 2. FAQPage (optional, will not produce rich results)

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

If you do use it, the questions and answers must appear on the page with the same wording as in the markup. Google may have changed FAQ eligibility again since I last saw the documentation, so check the current FAQPage page in Google Search Central if the rich result matters to you.
