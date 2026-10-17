# macakr.me navy redesign

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
