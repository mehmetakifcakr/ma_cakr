# ma_cakr — portfolio & engineering journal

A bilingual personal site for Mehmet Akif Çakır, a mechatronics engineering student at Manisa Celal Bayar University. The redesign uses deep navy, cool blue and cyan, a soft `ma_cakr` monogram, the owner's existing portrait and the official university logo. This is the original Azure site's source, not the separate Next.js draft in the parent directory.

## Site

- English homepage: `index.html`; Turkish homepage: `tr/index.html`.
- Three original project cards and six full article pages, with a matching language switch on each article.
- Journal search, combinable topic filters, computed reading times and a no-results state.
- GitHub, LinkedIn, Instagram and the professional email from the current public profile README.
- View/download links for one-page English and Turkish PDF CVs.
- A pointer-responsive ambient network, card illumination, restrained magnetic controls, scroll progress, section navigation and an actual İstanbul clock. Motion preferences persist and respect the system's reduced-motion setting; constrained devices use lighter effects.
- Static HTML/CSS/JavaScript. No build dependencies, accounts, database or analytics are required.

## Edit the journal

The source is `content/site.json`. It contains English biography, projects and journal entries, and their Turkish counterparts under `translations_tr`. All project claims are grounded in the linked public repository sources. Roadmap features are not presented as completed work.

To add a note, add an entry to `journal` and a translated entry with the same `id` under `translations_tr.journal`. Each note needs an `id`, `title`, `subtitle`, `category`, `project`, `paragraphs` and `sources`. Use an existing project id, or add the corresponding project and translation first. Then regenerate the static pages with:

```sh
python3 tools/build.py
```

Preview the repository with any static HTTP server. Paths work from a custom domain, an Azure app root or a GitHub Pages project subdirectory.

## Publication status

Existing live site: [macakr.me](https://macakr.me/), hosted on the original Azure Static Web App, `ma-cakr`. Its Azure hostname is `gray-pond-0fbfc1c10.3.azurestaticapps.net`. The connected production branch is `codex/ma-cakr-editorial`, not `main`. A push to that branch regenerates the eight English/Turkish pages and deploys only the public files.

The navy redesign is prepared separately on `codex/macakr-navy-redesign`. It has not been pushed or deployed. Review its local preview before approving a production update. Keep the existing Azure app and domain; no hosting migration, DNS, credentials, billing or resource changes are part of this redesign.

With `SITE_BASE_URL` unset or empty, `python3 tools/build.py` produces a local review draft with `noindex, nofollow` and removes previously generated discovery files. For a release, supply the actual public HTTPS base URL. A safe deployment subdirectory is supported; ports, credentials, query strings, fragments, local addresses and placeholder hosts are rejected before output is written.

The Azure workflow's public URL is corrected to `https://macakr.me`, generating canonical URLs, reciprocal English/Turkish language metadata, social-preview URLs, `robots.txt` and the eight-page `sitemap.xml` for the owned domain. Existing triggers, deployment paths and the Azure app stay unchanged. It packages the public pages, assets and headers into `_site/` and deploys without a framework build. Deployment credentials remain in the existing GitHub Actions secret; never put a token in source files.

On 18 October 2026, a read-only request to `https://macakr.me/` returned exactly the original checkout's 32,819-byte HTML. The domain connection is already working. The prior `www.macakr.com` address remains excluded.

## Hosting and domain benefits

The app's Free SKU and the Azure subscription's lifecycle are separate: the hosting plan does not keep a disabled or expired subscription active. Review the account's actual credit, spending limit and expiration in Azure before relying on a long-term deployment. No paid upgrade is part of this source.

Azure for Students offers $100 usable within 12 months to eligible students, without a credit card. Actual redemption, resource availability and regional restrictions are determined by the account. The general Azure free-account credit is a different offer.

The Student Developer Pack currently lists first-year domain offers through Name.com, Namecheap (.me) and .TECH. Availability, eligibility and renewal terms must be checked at redemption. A `.com` domain is not included in those listed free offers.

## Assets and sources

The profile photo and CV PDFs are preserved from the original site. Brand marks, the share image and project illustrations are authored SVG assets. The interface uses system sans and monospace fonts without a remote font request. The CVs use the existing verified student and project information; no employment, graduation date, language level or award has been added.

The university logo is the unmodified official PNG from the [MCBÜ press materials](https://basin.mcbu.edu.tr/hakkimizda/basin-materyalleri.70201.tr.html), displayed with its original colors and proportions on a light inset. University branding is used to identify education, not to imply an endorsement.

- [GitHub Student Developer Pack](https://education.github.com/pack)
- [Azure for Students](https://azure.microsoft.com/en-us/free/students/)
- [Static Web Apps plans](https://learn.microsoft.com/en-us/azure/static-web-apps/plans)
- [Build configuration](https://learn.microsoft.com/en-us/azure/static-web-apps/build-configuration)
- [Profile content and contacts](https://github.com/mehmetakifcakr/mehmetakifcakr)
