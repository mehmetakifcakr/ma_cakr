# ma_cakr — portfolio & engineering journal

A bilingual personal site for Mehmet Akif Çakır, a mechatronics engineering student at Manisa Celal Bayar University. The design uses warm paper, navy and copper, a custom geometric brand mark, and the owner's GitHub portrait.

## Site

- English homepage: `index.html`; Turkish homepage: `tr/index.html`.
- Three original project cards and six full article pages, with a matching language switch on each article.
- Journal search, combinable topic filters, computed reading times and a no-results state.
- GitHub, LinkedIn, Instagram and the professional email from the current public profile README.
- View/download links for one-page English and Turkish PDF CVs.
- Pointer trails, responsive icon/button effects, scroll reveals and a persistent session pause control. System reduced-motion settings are respected.
- Static HTML/CSS/JavaScript. No build dependencies, accounts, database or analytics are required.

## Edit the journal

The source is `content/site.json`. It contains English biography, projects and journal entries, and their Turkish counterparts under `translations_tr`. All project claims are grounded in the linked public repository sources. Roadmap features are not presented as completed work.

To add a note, add an entry to `journal` and a translated entry with the same `id` under `translations_tr.journal`. Each note needs an `id`, `title`, `subtitle`, `category`, `project`, `paragraphs` and `sources`. Use an existing project id, or add the corresponding project and translation first. Then regenerate the static pages with:

```sh
python3 tools/build.py
```

Preview the repository with any static HTTP server. Paths work from a custom domain, an Azure app root or a GitHub Pages project subdirectory.

## Publication status

Live site: [ma_cakr](https://gray-pond-0fbfc1c10.3.azurestaticapps.net/), hosted on Azure Static Web Apps **Free**. The connected deployment branch is `codex/ma-cakr-editorial`. A push to that branch regenerates the eight English/Turkish pages and deploys only the public files; editing `content/site.json` is enough to update content through this workflow.

With `SITE_BASE_URL` unset or empty, `python3 tools/build.py` produces a local review draft with `noindex, nofollow` and removes previously generated discovery files. For a release, supply the actual public HTTPS base URL. A safe deployment subdirectory is supported; ports, credentials, query strings, fragments, local addresses and placeholder hosts are rejected before output is written.

The Azure workflow supplies `https://gray-pond-0fbfc1c10.3.azurestaticapps.net` and generates canonical URLs, reciprocal English/Turkish language metadata, social-preview URLs, `robots.txt` and the eight-page `sitemap.xml`. It then packages the public pages, assets and headers into `_site/` and deploys without a framework build. Deployment credentials are stored as a GitHub Actions secret; never put a token in source files.

No custom domain has been registered or connected. The prior `www.macakr.com` CNAME is excluded because domain control has not been established. Register and verify ownership before adding a custom domain.

## Hosting and domain benefits

The app's Free SKU and the Azure subscription's lifecycle are separate: the hosting plan does not keep a disabled or expired subscription active. Review the account's actual credit, spending limit and expiration in Azure before relying on a long-term deployment. No paid upgrade is part of this source.

Azure for Students offers $100 usable within 12 months to eligible students, without a credit card. Actual redemption, resource availability and regional restrictions are determined by the account. The general Azure free-account credit is a different offer.

The Student Developer Pack currently lists first-year domain offers through Name.com, Namecheap (.me) and .TECH. Availability, eligibility and renewal terms must be checked at redemption. A `.com` domain is not included in those listed free offers.

## Assets and sources

The profile photo is from the authenticated GitHub profile. Brand marks and project illustrations are SVGs authored for this site. Google Fonts (DM Sans and Instrument Serif) are optional remote resources with system font fallbacks. The CVs use verified student and project information; no employment, graduation date, language level or award has been invented.

- [GitHub Student Developer Pack](https://education.github.com/pack)
- [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
- [Static Web Apps plans](https://learn.microsoft.com/en-us/azure/static-web-apps/plans)
- [Build configuration](https://learn.microsoft.com/en-us/azure/static-web-apps/build-configuration)
- [Profile content and contacts](https://github.com/mehmetakifcakr/mehmetakifcakr)
