# macakr.me navy redesign

## Current revision — portfolio workspace, 18 October 2026

The owner supplied an expanded bilingual portfolio brief. The current preview replaces the earlier navy layout with a charcoal/lime workspace, sidebar, interactive mechanism schematic and six overview cards, while retaining this original static Azure repository and redesign branch.

- Added seven pages in each language: projects, lab, mobility, CV, uses, blog and contact. Together with both homepages and the six original articles, there are 22 HTML pages.
- Preserved `content/site.json`, all original article paragraph text and routes, the real portrait, official university logo, public contacts and the original CV PDFs. Added byte-identical `/cv.pdf` and `/tr/cv.pdf` aliases and retained the original home section anchors.
- New owner-provided content lives in `content/portfolio.json`; navigation and homepage translations live in `content/interface.json`. Python modules generate all public pages without external dependencies.
- Added persistent light/dark theme, keyboard command palette, project/blog search and filters, project details, lab tabs, a draggable/keyboard-controlled illustrative mechanism, travel destination selection, print styling, email copying, code copying and a mail-client contact form.
- Actual 3D models, fabrication photos, slicer settings and videos were not supplied. Schematics are labeled as illustrative, missing media is disclosed, Japan is planned, and no project metrics or completed leadership roles were invented. The CV download remains the earlier published PDF; the online CV carries the newly supplied details.
- Deployment packaging includes the new pages and assets. Production triggers, host, domain and credentials are unchanged. The owner explicitly authorized publishing this reviewed version to `macakr.me` on 18 October 2026. Release target: `codex/ma-cakr-editorial`; the GitHub Actions Azure workflow records deployment status.
- Current QA: 22 routes and 926 internal file/anchor links pass static validation; all original article paragraphs are preserved. All 22 routes at five widths pass browser overflow checks; no script errors or failed local requests were found. All 16 main routes pass automated WCAG A/AA scans in both themes; eight additional open-palette/mobile-menu scans also report no violations. This does not replace manual accessibility review.
- EN/TR browser interaction checks cover command search/keyboard/focus return, theme persistence, normalized filters/reset/empty states, tabs, model controls, destination selection, form validation, clipboard/code controls and Istanbul time. Initial and dynamic reduced-motion handling passes repeated tests in Chromium and installed Chrome. CV printing uses dark text on white, including the email address. Core content and navigation remain usable with JavaScript disabled.
- Chromium and installed Chrome checks passed; mobile WebKit smoke checks passed. Firefox could not launch its local browser profile in this environment, so no new Firefox pass is claimed for this revision. Screenshots and the QA report are in `/Users/mehmetakifcakir/.codex/visualizations/2026/10/18/01a14e9d-b409-71c1-9726-258a182a636f/` (`portfolio-desktop.png`, `portfolio-mobile.png`, `portfolio-full.png`, `portfolio-qa.json` and subpage screenshots).
- Public deployment packaging was reproduced locally: all 22 HTML pages, assets and both byte-identical CV aliases are included; content source files, Python tools and repository metadata are excluded. No Lighthouse or deployed-performance score is claimed.

Preview: [Turkish](http://127.0.0.1:8766/tr/) · [English](http://127.0.0.1:8766/). See README for source layout and commands.

The remaining sections record the previous navy iteration, before this expanded portfolio request and its subsequent launch authorization.

## Source and boundaries

This is an isolated worktree of `mehmetakifcakr/ma_cakr`, the verified original Azure site. Branch: `codex/macakr-navy-redesign`, based on `c7532c2`. The original source was recovered from the two **GitHub Student hosting seç ve siteyi** chats. The original `index.html` exactly matched the live `https://macakr.me/` HTML before editing.

Production is `codex/ma-cakr-editorial`, not `main`. Do not push to production or change DNS, Azure resources, secrets or billing. No framework migration is needed.

## Design

Deep navy, cool blue and cyan, soft `ma_cakr` identity, real existing portrait, official university logo, interactive ambient network, gentle pointer/card effects, accessible controls, reduced motion and lightweight behavior. Preserve both languages, all eight existing pages, public contacts and existing CV PDFs.

## Implementation complete for review

- Recover and verify original source: complete.
- Isolated worktree: complete.
- Updated page composition, soft SVG logo/favicon, preserved portrait, social preview image and canonical domain: complete and visually checked.
- Official MCBÜ logo downloaded without recoloring from `https://basin.mcbu.edu.tr/db_images/cbu_tanitim/logomuz/cbu_dik.png`; source page: `https://basin.mcbu.edu.tr/hakkimizda/basin-materyalleri.70201.tr.html`.
- CSS and interaction redesign: complete across both homepages and all six existing article pages.
- Local checks: Python page generation, JavaScript syntax, clean diff formatting, all internal files/anchors, and preserved content JSON passed.
- Browser checks: English/Turkish layouts at 360, 390, 768, 1280 and 1920 px passed without horizontal overflow. Search (including Turkish character normalization), topic filters, empty-state/reset, mobile menu, Escape focus return, motion persistence and dynamic reduced-motion passed.
- Automated WCAG A/AA scans: no violations on either homepage after revealing all sections. This does not replace manual accessibility review.
- Chromium, Firefox and mobile WebKit smoke checks passed. All six article routes, original text and canonical URLs passed. Core content also remains visible with JavaScript disabled.
- Interaction checks additionally confirmed real Istanbul time, bounded canvas rendering, visibility pause/resume (simulated visibility event), Save-Data default and explicit override, pointer effects, progress and scroll navigation.
- Screenshots and detailed QA JSON are in `/Users/mehmetakifcakir/.codex/visualizations/2026/10/17/01a14ba6-1c6e-7d00-add6-bf9fc1fe47c0/` (`macakr-desktop.png`, `macakr-full.png`, `macakr-mobile.png`, `macakr-qa.json`).
- No Lighthouse or deployed-performance score is claimed. No GitHub push, deployment, DNS/resource/account/billing change was made. The work is ready for visual review and a separate launch instruction.

## Preview and generation

Generate with `SITE_BASE_URL=https://macakr.me python3 tools/build.py`. Serve with `python3 -m http.server 8766 --bind 127.0.0.1` from this worktree. The deployment workflow's only intended change is its canonical `SITE_BASE_URL` value; existing build paths, host, credentials and branch triggers remain as before.
