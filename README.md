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

This is a completed local preview and source proposal; no Azure app or domain registration is included yet. The HTML intentionally retains `noindex, nofollow` while the owner reviews the revised design. Remove that metadata from `tools/build.py` and regenerate when preparing the public release. Configure canonical/social-preview URLs after the real deployment URL is known.

The prior `www.macakr.com` CNAME is not carried into this source because the owner confirmed no domain was registered. Do not re-add it until domain control is verified.

## Azure setup

Activate Azure for Students with the owner's Microsoft account and student verification, then create **Static Web Apps / Free**. Connect this repository and the intended publication branch. The checked-in pages can deploy without a framework build: app location `/`, output location empty, and `skip_app_build: true`. Let Azure create the matching deployment workflow and repository secret for that app. Never commit a deployment token.

Azure for Students offers $100 usable within 12 months, without a credit card. Static Web Apps Free is an always-free plan subject to its limits; these are separate benefits. Student eligibility and offer redemption must be confirmed in the owner's account.

For a custom domain, the Student Developer Pack currently lists first-year offers through Name.com, Namecheap (.me) and .TECH. Availability, account eligibility and renewal terms are checked at redemption. A `.com` domain is not covered by these listed free offers.

## Assets and sources

The profile photo is from the authenticated GitHub profile. Brand marks and project illustrations are SVGs authored for this site. Google Fonts (DM Sans and Instrument Serif) are optional remote resources with system font fallbacks. The CVs use verified student and project information; no employment, graduation date, language level or award has been invented.

- [GitHub Student Developer Pack](https://education.github.com/pack)
- [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
- [Static Web Apps plans](https://learn.microsoft.com/en-us/azure/static-web-apps/plans)
- [Build configuration](https://learn.microsoft.com/en-us/azure/static-web-apps/build-configuration)
- [Profile content and contacts](https://github.com/mehmetakifcakr/mehmetakifcakr)
