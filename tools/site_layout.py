"""Dependency-free portfolio shell, homepage and preserved engineering articles."""
from html import escape as e
from pathlib import Path
import json
import math
from portfolio_pages import PORTFOLIO, render_page, get_projects, get_personal, project_art

ROOT = Path(__file__).resolve().parents[1]
UI = json.loads((ROOT / 'content/interface.json').read_text())
PAGES = ['home', 'projects', 'lab', 'mobility', 'cv', 'uses', 'blog', 'contact']
PATHS = {
 'home':'<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
 'projects':'<rect x="3" y="6" width="18" height="15" rx="2"/><path d="M8 6V3h8v3M3 12h18m-11 0v3h4v-3"/>',
 'lab':'<path d="M9 3h6m-5 0v7L4 20q-.5 1 1 1h14q1.5 0 1-1l-6-10V3M7 15h10"/><circle cx="11" cy="18" r=".6"/>',
 'mobility':'<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 7h14M5 17h14"/>',
 'cv':'<path d="M14 2H5v20h14V7l-5-5Zm0 0v6h5M8 12h8m-8 4h6"/>',
 'uses':'<path d="m14 5 5-2 2 2-2 5-3 1L7 20a2 2 0 0 1-3-3l9-9 1-3Z"/><path d="m4 4 4 4M3 3l3 1-2 2-1-3Z"/>',
 'blog':'<path d="M12 5C9 2 5 3 2 4v16c3-1 7-2 10 1 3-3 7-2 10-1V4c-3-1-7-2-10 1Zm0 0v16"/>',
 'contact':'<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 7 9 6 9-6"/>',
 'email':'<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m3 7 9 6 9-6"/>',
 'github':'<path d="M9 21v-4c-4 .8-4-2-6-2m13 6v-4c0-1-.3-2-1-2 4-.5 6-2 6-6 0-1-.4-2-1-3 0-1 0-2-.5-3-2 0-4 2-4 2-2-.5-5-.5-7 0 0 0-2-2-4-2-.5 1-.5 2 0 3-1 1-1 2-1 3 0 4 2 5.5 6 6-.6.5-1 1-1 2"/>',
 'linkedin':'<path d="M5 9v11M5 4v.1M10 20V9h5v2c3-4 6-2 6 2v7M15 11v9"/>',
 'instagram':'<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
 'arrow':'<path d="M5 12h14m-6-6 6 6-6 6"/>',
 'external':'<path d="M7 17 17 7M7 7h10v10"/>',
 'download':'<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
 'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
 'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1 1m12 12 1 1M5 19l1-1M18 6l1-1"/>',
 'moon':'<path d="M21 13a9 9 0 0 1-10-10A9 9 0 1 0 21 13Z"/>',
 'menu':'<path d="M4 6h16M4 12h16M4 18h16"/>',
 'close':'<path d="m6 6 12 12M6 18 18 6"/>',
 'code':'<path d="m8 6-6 6 6 6m8-12 6 6-6 6m-3-15-2 18"/>',
 'chip':'<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4m6-4v4M9 18v4m6-4v4M2 9h4m-4 6h4m12-6h4m-4 6h4"/><rect x="9" y="9" width="6" height="6" rx="1"/>',
 'cube':'<path d="m12 2 10 5v10l-10 5-10-5V7l10-5Zm0 10v10M2 7l10 5 10-5M7 4.5l10 5"/>',
 'location':'<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.2"/>',
 'sparkles':'<path d="m12 3 2.8 6.2L21 12l-6.2 2.8L12 21l-2.8-6.2L3 12l6.2-2.8L12 3Zm7-2v4m-2-2h4"/>',
 'copy':'<rect x="8" y="8" width="13" height="13" rx="2"/><path d="M16 8V3H3v13h5"/>',
 'reset':'<path d="M3 10a9 9 0 1 1 1 7M3 3v7h7"/>',
 'play':'<path d="m8 4 12 8-12 8V4Z"/>',
 'print':'<path d="M7 8V2h10v6M7 17H3V8h18v9h-4M7 14h10v8H7v-8Z"/>',
 'check':'<path d="m5 12 4 4L19 6"/>',
 'rss':'<path d="M4 4a16 16 0 0 1 16 16M4 11a9 9 0 0 1 9 9"/><circle cx="5" cy="19" r="1"/>',
 'globe':'<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18"/>',
}

def icon(name, cls=''):
 return f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.55" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{PATHS.get(name, PATHS["arrow"])}</svg>'

def robot_svg(suffix='hero'):
 return f'''<svg class="robot-scene" viewBox="0 0 420 350" fill="none" aria-hidden="true">
 <defs><linearGradient id="steel-{suffix}" x1="140" y1="85" x2="220" y2="230" gradientUnits="userSpaceOnUse"><stop stop-color="#7c8588"/><stop offset=".4" stop-color="#3b4448"/><stop offset="1" stop-color="#20282c"/></linearGradient><linearGradient id="lime-{suffix}" x1="120" y1="100" x2="200" y2="190" gradientUnits="userSpaceOnUse"><stop stop-color="#d4ff9b"/><stop offset="1" stop-color="#7ab53f"/></linearGradient><radialGradient id="floor-{suffix}"><stop stop-color="#b9f568" stop-opacity=".13"/><stop offset="1" stop-color="#b9f568" stop-opacity="0"/></radialGradient></defs>
 <ellipse cx="214" cy="272" rx="178" ry="69" fill="url(#floor-{suffix})"/>
 <g stroke="#536452" stroke-opacity=".35" stroke-width=".7"><path d="m21 249 181-92 192 96M21 272l181-92 192 96M43 293l181-92 171 85M74 310l171-88 139 70M38 239l183 94M71 222l183 95M105 205l183 94M138 188l183 94M171 172l183 94"/><ellipse cx="213" cy="262" rx="151" ry="68" stroke-dasharray="3 7"/></g>
 <g class="robot-body"><path d="m117 260 80-40 96 44-80 42-96-46Z" fill="#20282a" stroke="#5b6567"/><path d="m117 260 96 46v13l-96-46v-13Z" fill="#151b1f" stroke="#455055"/><path d="m213 306 80-42v13l-80 42v-13Z" fill="#101719" stroke="#455055"/><path d="m138 263 60-29 72 32-58 29-74-32Z" fill="#353e40" stroke="#5f6d64"/><path d="m181 291 28 13" stroke="#b9f568" stroke-width="3"/>
 <ellipse cx="199" cy="246" rx="38" ry="21" fill="#121a1b" stroke="#617066"/><path d="M163 235v12c0 26 73 26 73 0v-12" fill="#303c39" stroke="#667a59"/><ellipse cx="199" cy="235" rx="36" ry="20" fill="url(#lime-{suffix})" stroke="#deffac"/><ellipse cx="199" cy="235" rx="23" ry="12" fill="#405733" stroke="#88af63"/>
 <path d="m177 225-9-37 12-8 31 15 9 37c-3 14-31 13-43-7Z" fill="url(#steel-{suffix})" stroke="#7c8784"/><path d="m172 193-47-59 23-17 51 64-27 12Z" fill="url(#steel-{suffix})" stroke="#85948d"/><path d="m136 133 38 49 9-5-38-49" fill="url(#lime-{suffix})"/>
 <ellipse cx="180" cy="190" rx="23" ry="24" transform="rotate(-25 180 190)" fill="#35422f" stroke="#a4cf77"/><ellipse cx="179" cy="187" rx="16" ry="17" transform="rotate(-25 179 187)" fill="url(#lime-{suffix})"/><ellipse cx="179" cy="187" rx="6" ry="7" fill="#334b25" stroke="#d6ffa8"/>
 <path d="m130 130 70-57 18 14-70 59-18-16Z" fill="url(#steel-{suffix})" stroke="#819184"/><path d="m142 124 60-45 6 4-59 48-7-7Z" fill="#b9f568"/><ellipse cx="135" cy="132" rx="21" ry="20" transform="rotate(-25 135 132)" fill="#657f45" stroke="#c6f59b"/><ellipse cx="133" cy="129" rx="14" ry="14" fill="url(#lime-{suffix})"/><ellipse cx="133" cy="129" rx="5" ry="5" fill="#344b28"/>
 <path d="m200 74 22-3 27 20-11 19-26-18-12-18Z" fill="url(#steel-{suffix})" stroke="#819184"/><path d="m219 77 11 7-6 13-12-8 7-12Z" fill="#b9f568"/><path d="m244 92 18-6 17 14-5 13-13-10-12 4m-11 2 12 15 19 8 8-8-14-6-11-15" fill="#2a3438" stroke="#a1afaa" stroke-width="2"/>
 <path d="M190 228c-40-45-29-63-61-88-14-16 5-29 22-43l40-32" stroke="#0e171a" stroke-width="4"/><path d="M190 228c-40-45-29-63-61-88-14-16 5-29 22-43l40-32" stroke="#8d9b8d" stroke-width="1"/>
 <g fill="#a7b29e"><circle cx="142" cy="261" r="2"/><circle cx="211" cy="292" r="2"/><circle cx="269" cy="264" r="2"/></g></g>
 <g stroke="#b9f568" stroke-opacity=".6" stroke-width=".8"><path d="M272 100h45v-24h35M150 188H76v23H45M239 250h88v-24h24"/><circle cx="271" cy="100" r="3" fill="#b9f568"/><circle cx="150" cy="188" r="3" fill="#b9f568"/><circle cx="239" cy="250" r="3" fill="#b9f568"/></g>
 <g class="scene-label" fill="#9da99c" font-family="monospace" font-size="8" letter-spacing="1"><text x="316" y="66">ACTUATION</text><text x="35" y="226">CONTROL</text><text x="323" y="218">FABRICATION</text><text x="47" y="60">X  0.284</text><text x="47" y="73">Y  0.176</text><text x="47" y="86">Z  0.392</text></g></svg>'''

def mini_map():
 return '''<svg class="mini-world" viewBox="0 0 340 145" fill="none" aria-hidden="true"><g stroke="currentColor" stroke-width=".7" opacity=".32"><path d="m5 36 24-18 30 3 9 13 26 2 9 17-15 12-18-5-10 22-15-4-5-24-22-4-13-14ZM72 86l22-13 20 13 2 24-21 33-12-18-11-39ZM138 34l13-18 19 8 13-10 46 3 13 11 42 2 25 17-9 25-26-3-18 18-24-11-17 12-16-20-21-2-12-21-23 9-13-20ZM146 59l24-6 23 23-5 27-18 22-14-21-10-45ZM278 111l27-7 26 17-9 17-30-4-14-23Z"/><path d="M0 45h340M0 85h340M85 0v145M170 0v145M255 0v145" stroke-dasharray="2 5"/></g><path d="M147 42Q160 12 172 39T284 49" stroke="#b9f568" stroke-dasharray="4 4" stroke-width="1.3"/><circle cx="147" cy="42" r="4" fill="#b9f568"/><circle cx="172" cy="39" r="4" fill="#b9f568"/><circle cx="284" cy="49" r="4" fill="#0f1512" stroke="#b9f568"/><g fill="currentColor" font-size="9" font-family="monospace"><text x="127" y="64">ES</text><text x="176" y="31">RO</text><text x="291" y="52">JP ‘27</text></g></svg>'''

def home_content(lang, base, rel, data):
 u=UI[lang]; personal=get_personal(lang); projects=get_projects(lang)
 cv=f'{rel}assets/mehmet-akif-cakir-cv-{lang}.pdf'
 source_cards=''
 for p in projects[:2]:
  source_cards+=f'<a class="repo-row" href="{e(p["github"])}" target="_blank" rel="noopener noreferrer"><span class="repo-icon">{icon("code")}</span><span><strong>{e(p["title"])}</strong><small>{e(p["stage"])}</small></span>{icon("external")}</a>'
 notes=data['journal'] if lang=='en' else [{**n,**next(t for t in data['translations_tr']['journal'] if t['id']==n['id'])} for n in data['journal']]
 note_cards=''.join(f'<a class="home-note panel" href="{base}journal/{n["id"]}/"><span class="note-top"><span class="mono">0{i+1} / {e(n["category"])}</span>{icon("external")}</span><h3>{e(n["title"])}</h3><p>{e(n["subtitle"])}</p><span class="note-reading">{max(1,math.ceil(len(" ".join(n["paragraphs"]).split())/200))} {u["read_time"]}</span></a>' for i,n in enumerate(notes))
 return f'''
 <section class="hero" aria-labelledby="hero-title"><div class="hero-copy"><p class="hero-status"><span class="status-dot"></span>{u['status']}</p><p class="eyebrow hero-eyebrow">{u['edition']}</p><h1 id="hero-title">Mehmet Akif<br>Çakır<span class="accent">.</span></h1><p class="hero-tagline">{u['tagline']}</p><p class="hero-intro">{u['intro']}</p><div class="hero-actions"><a class="btn btn-primary" href="{base}projects/">{u['projects_cta']}{icon('arrow')}</a><a class="btn btn-outline" id="cv" href="{cv}" download>{icon('download')}{u['cv_cta']}</a></div><div class="hero-location">{icon('location')}{u['location']}<span class="hero-divider">/</span><a href="{personal['github']}" target="_blank" rel="noopener noreferrer">{icon('github')} GitHub {icon('external')}</a></div></div>
 <div class="hero-visual panel" data-model-viewer><div class="visual-top"><span><span class="small-cross">+</span> {u['diagram']}</span><span class="visual-live"><i></i> {u['live']}</span></div><div class="model-perspective"><div data-model-rotate>{robot_svg()}</div></div><div class="visual-bottom"><div><strong>{u['diagram_title']}</strong><small>{u['diagram_note']}</small></div><button class="icon-button" type="button" data-model-reset aria-label="{u['reset']}">{icon('reset')}</button></div><div class="visual-corner" aria-hidden="true">XYZ / 01</div></div></section>
 <section class="overview-section" id="work" aria-labelledby="overview-title"><div class="section-heading"><div><p class="eyebrow">{u['bento_kicker']}</p><h2 id="overview-title">{u['bento_title']}</h2></div><a class="text-link" href="{base}projects/">{u['all_projects']}{icon('arrow')}</a></div>
 <div class="bento-grid"><article class="bento-card bento-code panel"><div class="card-top"><span class="eyebrow">{u['open_label']}</span><span class="card-icon">{icon('code')}</span></div><h3>{u['small_code']}<br><span class="accent">{u['real_possibilities']}</span></h3><div class="repo-list">{source_cards}</div><div class="card-foot"><span class="tags"><span>Rust</span><span>Python</span><span>{u['open_source']}</span></span><a href="{base}projects/" aria-label="{u['all_projects']}" class="icon-link">{icon('external')}</a></div></article>
 <article class="bento-card bento-robot panel"><div class="card-top"><span class="eyebrow">{u['robot_label']}</span><span class="card-icon">{icon('chip')}</span></div><div class="board-art" aria-hidden="true"><div class="board-traces"></div><div class="board-chip"><span>STM32</span><small>ARM® CORTEX®</small></div><i class="board-led"></i><span class="board-label">NUCLEO / PROTOTYPE</span></div><h3>{u['robot_title']}</h3><p>{u['robot_desc']}</p><div class="card-foot"><span class="tags"><span>STM32</span><span>C/C++</span><span>Arduino</span></span><a class="icon-link" href="{base}projects/?category=robotics" aria-label="{u['robot_title']}">{icon('external')}</a></div></article>
 <article class="bento-card bento-model panel"><div class="card-top"><span class="eyebrow">{u['model_label']}</span><span class="card-icon">{icon('cube')}</span></div><div class="model-mini">{robot_svg('mini')}</div><h3>{u['model_title']}</h3><p>{u['model_desc']}</p><div class="card-foot"><span class="tags"><span>CAD</span><span>3D printing</span></span><a class="icon-link" href="{base}lab/" aria-label="{u['model_action']}">{icon('external')}</a></div></article>
 <article class="bento-card bento-map panel"><div class="card-top"><span class="eyebrow">{u['map_label']}</span><span class="card-icon">{icon('globe')}</span></div>{mini_map()}<h3>{u['map_title']}</h3><p>{u['map_desc']}</p><div class="card-foot"><span class="mini-flags"><span>ES</span><span>RO</span><span class="planned">JP 2027</span></span><a class="icon-link" href="{base}mobility/" aria-label="{u['map_title']}">{icon('external')}</a></div></article>
 <article class="bento-card bento-ai panel"><div class="card-top"><span class="eyebrow">{u['ai_label']}</span><span class="card-icon">{icon('sparkles')}</span></div><div class="waveform" aria-hidden="true">{''.join(f'<i style="--bar:{h}px;--delay:{i*-.08}s"></i>' for i,h in enumerate([10,18,30,19,45,60,38,76,54,93,69,41,80,100,73,54,91,66,42,70,36,52,28,44,20,31,15]))}</div><h3>{u['ai_title']}</h3><p>{u['ai_desc']}</p><div class="card-foot"><span class="tags"><span>Veo</span><span>n8n</span><span>Higgsfield</span></span><a class="icon-link" href="{base}lab/?tab=ai" aria-label="{u['ai_title']}">{icon('external')}</a></div></article>
 <article class="bento-card bento-role panel"><div class="card-top"><span class="eyebrow">{u['role_label']}</span><span class="card-icon">{icon('blog')}</span></div><div class="university-mark"><span class="university-image"><img src="{rel}assets/mcbu-official.png" width="50" height="62" alt="Manisa Celal Bayar Üniversitesi" loading="lazy"></span><span>MCBÜ <span class="accent">×</span> PAGİT<small>{u['now']} / 2026</small></span></div><h3>{u['role_title']}</h3><p>{u['role_desc']}</p><div class="card-foot"><span class="muted mono">{u['availability']}</span><a class="icon-link" href="{base}cv/" aria-label="{u['more_about']}">{icon('external')}</a></div></article></div></section>
 <section class="home-notebook" id="journal" aria-labelledby="notebook-title"><div class="section-heading"><div><p class="eyebrow">{u['note_kicker']}</p><h2 id="notebook-title">{u['note_title']}</h2></div><a class="text-link" href="{base}blog/">{u['all_notes']}{icon('arrow')}</a></div><div class="home-notes-grid">{note_cards}</div></section>
 <section class="home-about panel" id="about"><img src="{rel}assets/portrait.jpg" alt="Mehmet Akif Çakır" width="86" height="86" loading="lazy"><div><p class="eyebrow">{u['profile']}</p><p>{u['profile_desc']}</p></div><a class="text-link" href="{base}cv/">{u['more_about']}{icon('arrow')}</a></section>
 <section class="contact-banner" id="contact"><div><span class="eyebrow">{u['connect_label']}</span><h2>{u['contact_title']}</h2><p>{u['contact_desc']}</p></div><a class="btn btn-primary" href="{base}contact/">{u['contact_cta']}{icon('external')}</a></section>'''

def article_content(lang, article_id, base, rel, data):
 u=UI[lang]; notes=data['journal'] if lang=='en' else [{**n,**next(t for t in data['translations_tr']['journal'] if t['id']==n['id'])} for n in data['journal']]
 n=next(n for n in notes if n['id']==article_id)
 p=next(p for p in get_projects(lang) if p['id']==n['project'])
 paras=''.join(f'<p>{e(text)}</p>' for text in n['paragraphs'])
 if n['project']=='recovertick':
  paras+=f'<section class="article-code"><div><span>{u["code_sample"]}</span><button type="button" data-copy-code="#source-command">{icon("copy")}{u["copy_code"]}</button></div><pre><code id="source-command">git clone https://github.com/mehmetakifcakr/recovertick.git\ncd recovertick\ncargo test</code></pre></section>'
 sources=''.join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener noreferrer">{e(s["label"])}{icon("external")}</a></li>' for s in n['sources'])
 related=''.join(f'<a class="panel related-card" href="{base}journal/{other["id"]}/"><span class="eyebrow">{e(other["category"])}</span><h3>{e(other["title"])}</h3>{icon("arrow")}</a>' for other in notes if other['id']!=article_id)
 return f'''<article class="engineering-article"><a class="text-link article-back" href="{base}blog/">{icon('arrow')}{u['article_back']}</a><header class="article-heading"><span class="eyebrow">{e(n['category'])}</span><h1>{e(n['title'])}</h1><p>{e(n['subtitle'])}</p><div class="article-byline"><img src="{rel}assets/portrait.jpg" alt="" width="38" height="38"><span>Mehmet Akif Çakır</span><span class="muted">/</span><span>{max(1,math.ceil(len(' '.join(n['paragraphs']).split())/200))} {u['read_time']}</span></div></header><div class="article-figure panel">{project_art(p['id'])}</div><div class="article-prose">{paras}<aside class="article-source-note">{u['article_note']}</aside><h2>{u['article_sources']}</h2><ul class="article-sources">{sources}</ul></div><section class="article-related"><h2>{u['article_related']}</h2><div>{related}</div></section></article>'''

def build_site(root, site_base_url, data):
 urls=[]
 for lang in ['en','tr']:
  for page,article_id in [(p,None) for p in PAGES]+[('article',n['id']) for n in data['journal']]:
   u=UI[lang]; prefix='tr/' if lang=='tr' else ''
   path=prefix+(f'journal/{article_id}/' if article_id else f'{page}/' if page!='home' else '')
   current=Path(path+'index.html'); rel='../'*len(current.parent.parts); base=rel+prefix
   alternate=('tr/' if lang=='en' else '')+(f'journal/{article_id}/' if article_id else f'{page}/' if page!='home' else '')
   other_lang='tr' if lang=='en' else 'en'
   current_nav='blog' if article_id else page
   title=(next(n['title'] for n in (data['journal'] if lang=='en' else data['translations_tr']['journal']) if n['id']==article_id) if article_id else u['nav'][page])+' — Mehmet Akif Çakır'
   desc=get_personal(lang)['bio']
   nav=''.join(f'<a class="nav-link {"active" if p==current_nav else ""}" href="{base}{"" if p=="home" else p+"/"}" {"aria-current=\"page\"" if p==current_nav else ""}>{icon(p)}<span>{u["nav"][p]}</span>{"<span class=nav-dot></span>" if p==current_nav else ""}{"<span class=nav-tag>3D / AI</span>" if p=="lab" else ""}</a>' for p in PAGES)
   socials=''.join(f'<a href="{e(c["url"])}" target="_blank" rel="noopener noreferrer">{icon(c["type"])}<span>{e(c["label"])}</span>{icon("external")}</a>' for c in data['contacts'] if c['type'] in ['github','linkedin','instagram'])
   sidebar=f'''<aside class="sidebar"><a class="brand" href="{base}" aria-label="ma_cakr — {u['home']}"><span class="brand-symbol">m<span>_</span></span><span>ma_cakr<span class="accent">.</span></span></a><div class="sidebar-profile"><img src="{rel}assets/portrait.jpg" alt="Mehmet Akif Çakır" width="42" height="42"><div><strong>Mehmet Akif Çakır</strong><span>{u['creative_tech']}</span></div></div><p class="nav-label">{u['workspace']}</p><nav id="site-navigation" aria-label="{u['explore']}">{nav}</nav><div class="sidebar-elsewhere"><p class="nav-label">{u['elsewhere']}</p>{socials}</div><div class="sidebar-bottom"><p><span class="status-dot"></span>{u['availability']}</p><span class="sidebar-domain">macakr.me <span>© 2026</span></span></div></aside>'''
   context={'rel':rel,'base':base,'icon':icon}
   content=article_content(lang,article_id,base,rel,data) if article_id else home_content(lang,base,rel,data) if page=='home' else render_page(page,lang,context)
   palette_items=''.join(f'<a href="{base}{"" if p=="home" else p+"/"}" data-command-item data-search="{e(u["nav"][p])} {p}">{icon(p)}<span>{u["nav"][p]}</span><span class="command-arrow">↵</span></a>' for p in PAGES)
   palette_items+=''.join(f'<a href="{base}projects/#{p["id"]}" data-command-item data-search="{e(p["title"]+" "+" ".join(p["tech"]))}">{icon("projects")}<span>{e(p["title"])}</span><small>{u["nav"]["projects"]}</small></a>' for p in get_projects(lang))
   palette_items+=f'<a href="{rel}assets/mehmet-akif-cakir-cv-{lang}.pdf" download data-command-item data-search="cv pdf download indir özgeçmiş resume">{icon("download")}<span>{u["cv_cta"]}</span></a><button type="button" data-command-item data-theme-toggle data-search="theme tema dark light koyu açık">{icon("sun")}<span>{u["theme"]}</span></button><button type="button" data-command-item data-copy="mehmetakifcakir525@gmail.com" data-search="email e-posta copy kopyala">{icon("copy")}<span>{u["copy_email"]}</span></button><a href="{rel+alternate}" data-command-item data-search="language dil english türkçe tr en">{icon("globe")}<span>{"Türkçeye geç" if lang=="en" else "Switch to English"}</span></a>'
   palette=f'''<dialog class="command-palette" id="command-palette" aria-labelledby="command-title"><h2 id="command-title" class="sr-only">{u['palette_title']}</h2><div class="command-search">{icon('search')}<label class="sr-only" for="command-input">{u['palette_title']}</label><input id="command-input" data-command-search placeholder="{u['palette_placeholder']}" autocomplete="off"><button type="button" data-command-close aria-label="{u['close']}"><kbd>esc</kbd></button></div><div class="command-list" data-command-list>{palette_items}</div><p class="command-empty muted" data-command-empty hidden>{u['palette_empty']}</p><div class="command-footer"><span><kbd>↑</kbd> <kbd>↓</kbd> {u['palette_hint']}</span><span><kbd>↵</kbd> {u['palette_enter']}</span><span><kbd>esc</kbd> {u['palette_esc']}</span></div></dialog>'''
   head='<meta name="robots" content="noindex, nofollow">'
   if site_base_url:
    canonical=f'{site_base_url}/{path}'; other=f'{site_base_url}/{alternate}'
    head=f'<meta name="robots" content="index, follow"><link rel="canonical" href="{e(canonical)}"><link rel="alternate" hreflang="{lang}" href="{e(canonical)}"><link rel="alternate" hreflang="{other_lang}" href="{e(other)}"><link rel="alternate" hreflang="x-default" href="{e(canonical if lang=="en" else other)}"><meta property="og:url" content="{e(canonical)}"><meta property="og:image" content="{e(site_base_url)}/assets/social-card.png">'
    urls.append(canonical)
   metadata=json.dumps({'@context':'https://schema.org','@type':'Person','name':'Mehmet Akif Çakır','alternateName':'ma_cakr','jobTitle':u['role'],'sameAs':[c['url'] for c in data['contacts'] if c['type'] in ['github','linkedin','instagram']]},ensure_ascii=False).replace('<','\\u003c')
   initial_theme="try{document.documentElement.dataset.theme=localStorage.getItem('macakr-theme')==='light'?'light':'dark'}catch(e){}"
   html=f'''<!doctype html><html lang="{lang}" data-theme="dark"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#0b0e11">{head}<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="{'article' if article_id else 'website'}"><link rel="icon" href="{rel}assets/brand-mark.svg" type="image/svg+xml"><script>{initial_theme}</script><link rel="stylesheet" href="{rel}portfolio.css"><script src="{rel}portfolio.js" defer></script><script type="application/ld+json">{metadata}</script></head><body id="top" data-lang="{lang}" data-page="{page}"><a class="skip-link" href="#main">{u['skip']}</a><button type="button" class="menu-backdrop" data-menu-backdrop hidden aria-label="{u['close']}"></button>{sidebar}<div class="site-body"><header class="topbar"><div class="topbar-left"><button class="icon-button menu-toggle" type="button" data-menu-toggle aria-expanded="false" aria-controls="site-navigation" aria-label="{u['menu']}">{icon('menu')}</button><div class="breadcrumb"><span>{u['breadcrumb']}</span><span class="crumb-slash">/</span><strong>{u['nav'][current_nav]}</strong></div></div><div class="topbar-actions"><button class="search-trigger" type="button" data-command-open aria-label="{u['keyboard']}">{icon('search')}<span>{u['search']}</span><kbd>⌘ K</kbd></button><div class="language-switch"><a href="{rel+path if lang=='en' else rel+alternate}" class="{'current' if lang=='en' else ''}" lang="en" hreflang="en" {'aria-current="page"' if lang=='en' else ''}>EN</a><a href="{rel+path if lang=='tr' else rel+alternate}" class="{'current' if lang=='tr' else ''}" lang="tr" hreflang="tr" {'aria-current="page"' if lang=='tr' else ''}>TR</a></div><button class="icon-button theme-toggle" type="button" data-theme-toggle aria-label="{u['theme']}">{icon('sun')}</button></div></header><main id="main" class="main-content" tabindex="-1">{content}</main><footer class="site-footer"><span>© 2026 Mehmet Akif Çakır<span class="footer-divider">/</span>{u['made']}</span><div><span class="clock-dot"></span><span data-clock>UTC+03:00</span><span class="muted">{u['local_time']}</span><a href="https://github.com/mehmetakifcakr/ma_cakr" target="_blank" rel="noopener noreferrer" aria-label="{u['footer_source']}">{icon('github')}</a></div></footer></div>{palette}<div class="toast" data-toast role="status" aria-live="polite"></div></body></html>'''
   target=root/current; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(html)
 if site_base_url:
  (root/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{e(url)}</loc></url>' for url in urls)+'</urlset>\n')
  (root/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {site_base_url}/sitemap.xml\n')
 else:
  for name in ['sitemap.xml','robots.txt']: (root/name).unlink(missing_ok=True)
 print(f'Generated {len(PAGES)*2} portfolio pages and {len(data["journal"])*2} preserved articles.')
