# ma_cakr — engineering portfolio & workspace

A bilingual personal site for Mehmet Akif Çakır, a mechatronics engineering student at Manisa Celal Bayar University. The current redesign uses a charcoal workspace, lime accents, a persistent sidebar and six visual overview cards. It retains the owner's real portrait, university logo, public contacts, CVs and original engineering articles. This is the original framework-free Azure site in the `ma_cakr` repository.

## Current preview

Run `SITE_BASE_URL=https://macakr.me python3 tools/build.py`, then serve this directory with `python3 -m http.server 8766 --bind 127.0.0.1`. Open [Turkish](http://127.0.0.1:8766/tr/) or [English](http://127.0.0.1:8766/).

The reviewed source stays on `codex/macakr-navy-redesign`. The owner authorized production publication on 18 October 2026; Azure deploys from `codex/ma-cakr-editorial`.

## Site

- English homepage: `index.html`; Turkish homepage: `tr/index.html`.
- Six overview cards and dedicated `/projects/`, `/lab/`, `/mobility/`, `/cv/`, `/uses/`, `/blog/` and `/contact/` pages, with matching `/tr/` routes.
- Nine project entries: the eight supplied projects plus the original AI Trader Paper. Search, category filters, reset, empty states and expandable details distinguish current implementations and planned work.
- Six preserved article URLs with their original paragraph content, computed reading times, source links and copyable setup commands on the RecoverTick article.
- Persistent light/dark theme and a searchable command palette (`Cmd+K` or `Ctrl+K`) for pages, projects, PDFs, language and actions.
- Lab tabs, a draggable illustrative mechanism with angle/reset/autorotation controls, and a schematic travel map with accessible destination selection. Japan remains marked as planned.
- Education, experience, skills and a printable CV page, with the original localized PDF downloads. `/cv.pdf` and `/tr/cv.pdf` are byte-identical aliases of those original assets.
- GitHub, LinkedIn, Instagram and the professional email from the current public profile README.
- Both owner-supplied public email addresses, clipboard controls and a validated form that prepares an email in the visitor's mail app. It does not claim to send or store a message.
- An actual İstanbul clock, keyboard navigation, reduced-motion support, offscreen/hidden animation pausing and core content/navigation that also work without JavaScript.
- Static HTML/CSS/JavaScript. No build dependencies, accounts, database or analytics are required.

No actual STL/GLB/Sketchfab URL, CT dataset, fabrication photos or generated videos were supplied. Lab media therefore uses explicitly labeled vector schematics and honest pending-media notices. Materials, slicer parameters and project results are not invented. Existing CV PDFs remain unchanged and are identified as the earlier published files; the online CV contains the newly supplied information.

## Source layout

```text
content/site.json          # preserved projects, contacts and original journal
content/portfolio.json     # supplied portfolio, all subpage copy and EN/TR data
content/interface.json     # navigation and homepage EN/TR copy
tools/build.py             # URL validation and public build entry point
tools/site_layout.py       # shared shell, home and article rendering
tools/portfolio_pages.py   # seven localized page renderers and vector artwork
portfolio.css              # responsive dark/light design and print styles
portfolio.js               # local, dependency-free interactions
assets/                    # preserved portrait, official logo, PDFs and brand assets
```

## Edit the journal

The original journal source remains `content/site.json`, with Turkish counterparts under `translations_tr`. New owner-provided portfolio content is in `content/portfolio.json`; homepage and shared navigation copy are in `content/interface.json`. Keep both languages together when editing. The new renderer uses the original journal source directly, so articles retain their URLs and text. Roadmap features are not presented as completed work.

To add a note, add an entry to `journal` and a translated entry with the same `id` under `translations_tr.journal`. Each note needs an `id`, `title`, `subtitle`, `category`, `project`, `paragraphs` and `sources`. Use an existing project id, or add the corresponding project and translation first. Then regenerate the static pages with:

```sh
python3 tools/build.py
```

Preview the repository with any static HTTP server. Paths work from a custom domain, an Azure app root or a GitHub Pages project subdirectory.

## Publication status

Existing live site: [macakr.me](https://macakr.me/), hosted on the original Azure Static Web App, `ma-cakr`. Its Azure hostname is `gray-pond-0fbfc1c10.3.azurestaticapps.net`. The connected production branch is `codex/ma-cakr-editorial`, not `main`. A push to that branch regenerates the 22 English/Turkish pages and deploys only the public files.

The workspace redesign was prepared and reviewed on `codex/macakr-navy-redesign`. The owner authorized publishing it to `macakr.me` on 18 October 2026. The production release uses `codex/ma-cakr-editorial` and the existing Azure app and domain; no hosting migration, DNS, credentials, billing or resource changes are part of this release.

With `SITE_BASE_URL` unset or empty, `python3 tools/build.py` produces a local review draft with `noindex, nofollow` and removes previously generated discovery files. For a release, supply the actual public HTTPS base URL. A safe deployment subdirectory is supported; ports, credentials, query strings, fragments, local addresses and placeholder hosts are rejected before output is written.

The Azure workflow's public URL is `https://macakr.me`, generating canonical URLs, reciprocal English/Turkish language metadata, social-preview URLs, `robots.txt` and the 22-page `sitemap.xml` for the owned domain. Existing triggers, deployment paths and the Azure app stay unchanged. The packaging step now includes the new page directories and `portfolio.css`/`portfolio.js`, and deploys without a framework build. Deployment credentials remain in the existing GitHub Actions secret; never put a token in source files.

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
