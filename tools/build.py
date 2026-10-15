from pathlib import Path
from html import escape as e
from urllib.parse import urlsplit
import ipaddress, json, math, os, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT
D = json.loads((ROOT / 'content/site.json').read_text())
TR = D['translations_tr']

def release_base_url(value):
 """Accept a public HTTPS origin only; leave local previews unindexed."""
 if not value.strip():
  return None
 value = value.strip()
 try:
  parts = urlsplit(value)
  host = (parts.hostname or '').lower()
  port = parts.port
 except ValueError:
  raise SystemExit('SITE_BASE_URL must be the real public HTTPS site origin.')
 labels = host.split('.')
 reserved = {'localhost', 'local', 'internal', 'invalid', 'test', 'example'}
 placeholders = {'example', 'placeholder', 'your-site', 'your-app', 'your-domain', 'yourdomain'}
 valid_host = (
  len(labels) >= 2 and len(host) <= 253
  and all(re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label) for label in labels)
  and labels[-1] not in reserved
  and not any(label in placeholders for label in labels)
  and host not in {'example.com', 'example.net', 'example.org'}
  and not host.endswith(('.example.com', '.example.net', '.example.org'))
 )
 try:
  ipaddress.ip_address(host)
  valid_host = False
 except ValueError:
  pass
 if (parts.scheme != 'https' or not valid_host or parts.netloc.lower() != host
     or any(char.isspace() for char in value) or parts.username or parts.password
     or port is not None or parts.path not in ('', '/') or parts.query or parts.fragment):
  raise SystemExit('SITE_BASE_URL must be the real public HTTPS site origin, without a path, port, credentials, query or fragment; local and placeholder hosts are not allowed.')
 return 'https://' + host

SITE_BASE_URL = release_base_url(os.environ.get('SITE_BASE_URL', ''))

def page_url(lang='en', article_id=None):
 path = ('tr/' if lang == 'tr' else '') + (f'journal/{article_id}/' if article_id else '')
 return f'{SITE_BASE_URL}/{path}'

def publication_head(lang, article_id=None):
 if not SITE_BASE_URL:
  return '<meta name="robots" content="noindex, nofollow">'
 alternates = ''.join(f'<link rel="alternate" hreflang="{language}" href="{e(page_url(language, article_id))}">' for language in ['en', 'tr'])
 return (f'<meta name="robots" content="index, follow"><link rel="canonical" href="{e(page_url(lang, article_id))}">'
         + alternates + f'<link rel="alternate" hreflang="x-default" href="{e(page_url("en", article_id))}">'
         + f'<meta property="og:url" content="{e(page_url(lang, article_id))}"><meta property="og:image" content="{e(SITE_BASE_URL)}/assets/portrait.jpg">')

def build_discovery_files():
 if not SITE_BASE_URL:
  # Avoid retaining a previous release URL when regenerating a draft.
  for filename in ['robots.txt', 'sitemap.xml']:
   (OUT / filename).unlink(missing_ok=True)
  return
 urls = ''.join(f'<url><loc>{e(page_url(lang, article_id))}</loc></url>'
                for lang in ['en', 'tr'] for article_id in [None] + [note['id'] for note in D['journal']])
 (OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + '</urlset>\n')
 (OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE_BASE_URL}/sitemap.xml\n')

UI = {
'en': {
 'role':'Mechatronics engineering student', 'work':'Projects', 'journal':'Journal', 'about':'About', 'contact':'Contact', 'cv':'My CV',
 'intro':'An engineer’s curiosity. A maker’s mindset.', 'hero':'Between ideas<br>and <em>the real world.</em>',
 'intro_text':'I’m Mehmet Akif Çakır. I explore robotics, embedded systems and software — one thoughtful experiment at a time.',
 'explore':'Explore my projects', 'read':'Read the journal', 'portrait_caption':'Mehmet Akif Çakır', 'portrait_sub':'Mechatronics · code · curiosity',
 'location':'Based in Izmir, Türkiye', 'scroll':'A little further down', 'focus':'Robotics / Embedded systems / Software',
 'work_kicker':'01 / Selected projects', 'work_title':'Ideas with<br><em>something behind them.</em>',
 'work_intro':'Small, open-source explorations. The code, the current stage, and the questions still worth asking.',
 'code':'View code', 'project_note':'Project note', 'in_scope':'What exists today', 'next':'Read the story',
 'journal_kicker':'02 / The notebook', 'journal_title':'Thinking out loud.<br><em>Writing it down.</em>',
 'journal_intro':'Notes on building, testing and understanding systems. Each story starts with a real project.',
 'search':'Search the notebook', 'search_placeholder':'Search titles, topics or ideas…', 'all':'All notes', 'results':'notes',
 'no_results':'No matching notes. Try another word or topic.', 'clear':'Clear search',
 'about_kicker':'03 / A little about me', 'about_title':'A curious mind.<br><em>A hands-on approach.</em>',
 'education':'Education', 'university':'Manisa Celal Bayar University', 'degree':'Mechatronics Engineering · Student',
 'toolbox':'Working with', 'interests':'Exploring', 'cv_title':'The short version.', 'cv_text':'My education, selected projects and technical interests, in one place.',
 'view_cv':'View CV', 'download_cv':'Download PDF', 'contact_kicker':'04 / Let’s connect', 'contact_title':'Good conversations<br>start with <em>a hello.</em>',
 'contact_intro':'An idea, a question, or a project to talk about? Find me where it feels natural.', 'email':'Email',
 'footer_note':'Built with curiosity. Made to keep evolving.', 'top':'Back to top', 'pause':'Pause effects', 'resume':'Resume effects',
 'reduced':'Reduced motion', 'skip':'Skip to content', 'menu':'Menu', 'close':'Close', 'home':'Home',
 'back':'Back to the notebook', 'sources':'Explore the source', 'source_note':'A technical note based on the project’s public repository. Current implementation and future work are kept distinct.',
 'author_role':'Mechatronics engineering student', 'related':'Continue reading', 'source_repository':'Source repository',
 'read_time':'min read', 'view_project':'Explore the project', 'cv_alt':'Download Mehmet Akif Çakır’s CV as a PDF',
 'feed_title':'ma_cakr — engineering notes', 'academic':'Research profile', 'aria_main':'Main navigation',
 'search_label':'Filter notes by topic', 'note_label':'PROJECT NOTE', 'search_count':'results', 'brand':'ma_cakr, home',
 },
'tr': {
 'role':'Mekatronik mühendisliği öğrencisi', 'work':'Projeler', 'journal':'Günlük', 'about':'Hakkımda', 'contact':'İletişim', 'cv':'Özgeçmişim',
 'intro':'Mühendislik merakı. Üretme tutkusu.', 'hero':'Fikirlerden<br><em>gerçek dünyaya.</em>',
 'intro_text':'Ben Mehmet Akif Çakır. Robotik, gömülü sistemler ve yazılımı, her seferinde yeni bir deneyle keşfediyorum.',
 'explore':'Projelerimi keşfet', 'read':'Günlüğü oku', 'portrait_caption':'Mehmet Akif Çakır', 'portrait_sub':'Mekatronik · kod · merak',
 'location':'İzmir, Türkiye', 'scroll':'Biraz daha aşağıda', 'focus':'Robotik / Gömülü sistemler / Yazılım',
 'work_kicker':'01 / Seçilmiş projeler', 'work_title':'Bir fikrin<br><em>çalışan hâli.</em>',
 'work_intro':'Küçük, açık kaynaklı keşifler. Kodları, bugün geldikleri nokta ve cevap aramaya değer yeni sorular.',
 'code':'Kodu incele', 'project_note':'Proje notu', 'in_scope':'Bugün neler var?', 'next':'Hikâyesini oku',
 'journal_kicker':'02 / Mühendislik defteri', 'journal_title':'Biraz düşünce.<br><em>Biraz mühendislik.</em>',
 'journal_intro':'Sistemleri kurmak, sınamak ve anlamak üzerine notlar. Her yazının başlangıcında gerçek bir proje var.',
 'search':'Günlükte ara', 'search_placeholder':'Başlık, konu veya fikir ara…', 'all':'Tüm yazılar', 'results':'yazı',
 'no_results':'Eşleşen yazı bulunamadı. Başka bir kelime veya konu dene.', 'clear':'Aramayı temizle',
 'about_kicker':'03 / Biraz da benden', 'about_title':'Merakla başlar.<br><em>Üreterek öğrenirim.</em>',
 'education':'Eğitim', 'university':'Manisa Celal Bayar Üniversitesi', 'degree':'Mekatronik Mühendisliği · Öğrenci',
 'toolbox':'Kullandığım araçlar', 'interests':'Keşfettiklerim', 'cv_title':'Kısaca ben.', 'cv_text':'Eğitimim, seçilmiş projelerim ve teknik ilgi alanlarım tek bir yerde.',
 'view_cv':'CV’yi görüntüle', 'download_cv':'PDF indir', 'contact_kicker':'04 / Bir merhaba', 'contact_title':'İyi bir sohbet,<br><em>bir merhabayla başlar.</em>',
 'contact_intro':'Bir fikrin, sorun veya konuşmak istediğin bir proje mi var? Sana en uygun yerden ulaşabilirsin.', 'email':'E-posta',
 'footer_note':'Merakla üretildi. Gelişmeye devam edecek.', 'top':'Başa dön', 'pause':'Efektleri durdur', 'resume':'Efektleri başlat',
 'reduced':'Azaltılmış hareket', 'skip':'İçeriğe geç', 'menu':'Menü', 'close':'Kapat', 'home':'Ana sayfa',
 'back':'Günlüğe dön', 'sources':'Kaynakları incele', 'source_note':'Projenin herkese açık deposuna dayanan teknik bir not. Mevcut uygulama ve gelecek fikirleri ayrı ele alınır.',
 'author_role':'Mekatronik mühendisliği öğrencisi', 'related':'Okumaya devam et', 'source_repository':'Proje deposu',
 'read_time':'dk okuma', 'view_project':'Projeyi keşfet', 'cv_alt':'Mehmet Akif Çakır’ın özgeçmişini PDF olarak indir',
 'feed_title':'ma_cakr — mühendislik notları', 'academic':'Araştırmacı profili', 'aria_main':'Ana menü',
 'search_label':'Yazıları konuya göre filtrele', 'note_label':'PROJE NOTU', 'search_count':'sonuç', 'brand':'ma_cakr, ana sayfa',
 }
}

ICON_PATHS = {
 'arrow':'<path d="M5 19 19 5M5 5h14v14"/>',
 'down':'<path d="M12 3v17m-6-6 6 6 6-6"/>',
 'download':'<path d="M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5"/>',
 'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
 'email':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
 'instagram':'<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
 'linkedin':'<path d="M5 9v11M5 4v.1M10 20V9h5v2c3-4 6-2 6 2v7M15 11v9"/>',
 'github':'<path d="M9 20c-5 1-5-2-7-2m14 4v-4c0-1-.3-2-1-2 4-.5 6-2 6-6 0-1-.4-3-1-3 0-1 0-3-.5-4-2 0-4 2-4 2-2-.5-5-.5-7 0 0 0-2-2-4-2-.5 1-.5 3 0 4-1 1-1 2-1 3 0 4 2 5.5 6 6-.6.5-1 1-1 2v4"/>',
 'location':'<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.2"/>',
 'pause':'<path d="M9 5v14M15 5v14"/>',
 'sun':'<circle cx="12" cy="12" r="4"/><path d="M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1 1m12 12 1 1M5 19l1-1M18 6l1-1"/>',
 'link':'<path d="m10 14 4-4m-5-2 2-2a5 5 0 0 1 7 7l-2 2m-7-2-2 2a5 5 0 0 1-7-7l2-2"/>',
}
def icon(name, cls=''):
 return f'<svg class="icon {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON_PATHS[name]}</svg>'

def mark():
 return '<svg class="brand-mark" viewBox="0 0 48 48" fill="none" aria-hidden="true"><path d="M6 37V11l18 18 18-18v26" stroke="currentColor" stroke-width="3.2" stroke-linejoin="miter"/><path class="mark-accent" d="m14 38 10-25 10 25M18 29h12" stroke="currentColor" stroke-width="2.4"/><path d="M5 44h38" stroke="currentColor" stroke-width="1" opacity=".35"/></svg>'

def logo(label, href):
 return f'<a class="brand" href="{href}" aria-label="{label}">{mark()}<span>ma_cakr<span class="brand-dot">.</span></span></a>'

def artwork(project, variant='card'):
 # Native vector illustrations describe the project theme, rather than pretending to be screenshots.
 if project=='recovertick':
  paths=''.join(f'<path d="M{x} {y}h{w}"/>' for x,y,w in [(68,95,70),(68,114,102),(68,133,53),(231,178,82),(231,197,101),(231,216,62)])
  body=f'<g stroke="#77899d" fill="none"><rect x="42" y="67" width="157" height="96" rx="8"/><rect x="208" y="150" width="158" height="96" rx="8"/>{paths}<path d="M199 114h42q16 0 16 16v20M208 197h-48q-16 0-16-16v-18" stroke-dasharray="4 5"/><circle cx="257" cy="130" r="5" fill="#b66b47" stroke="#b66b47"/><circle cx="144" cy="179" r="5" fill="#b66b47" stroke="#b66b47"/></g><text x="59" y="52" class="art-label">STATE → DECISION → REPLAY</text><text x="337" y="280" class="art-small">01</text>'
 elif project=='openrobotkit':
  body='<g fill="none" stroke="#78869b"><circle cx="206" cy="151" r="84" stroke-dasharray="2 8"/><circle cx="206" cy="151" r="57"/><circle cx="206" cy="151" r="34"/><path d="M206 46v27m0 156v27M101 151h27m156 0h27M151 96l20 20m70 70 20 20M151 206l20-20m70-70 20-20"/><path d="M206 151 245 98" stroke="#b66b47" stroke-width="3"/><circle cx="206" cy="151" r="9" fill="#152a44"/></g><text x="35" y="42" class="art-label">A SMALL INTERFACE FOR MOTION</text><text x="337" y="280" class="art-small">02</text>'
 else:
  body='<g stroke="#8692a0" fill="none"><path d="M48 231h310M48 61v170"/><path d="M48 156h310M48 95h310" stroke-dasharray="2 6" opacity=".5"/><path d="m55 204 35-20 30 8 30-46 30 12 28-31 30 16 36-46 31 9 39-41" stroke="#b66b47" stroke-width="2"/><path d="m55 216 35-12 30 3 30-19 30 9 28-18 30 8 36-21 31 9 39-14" stroke="#152a44" stroke-width="2"/><circle cx="274" cy="97" r="5" fill="#b66b47" stroke="none"/></g><text x="48" y="42" class="art-label">ONE ACCOUNT. EXPLICIT LIMITS.</text><text x="337" y="280" class="art-small">03</text>'
 return f'<svg class="project-art {variant}" viewBox="0 0 410 300" fill="none" aria-hidden="true"><defs><pattern id="grid-{project}-{variant}" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0v20" stroke="#152a44" stroke-width=".4" opacity=".12"/></pattern></defs><rect x="0" y="0" width="410" height="300" fill="url(#grid-{project}-{variant})"/>{body}</svg>'

def minutes(note):
 return max(1, math.ceil(len(' '.join(note['paragraphs']).split()) / 200))

def build(lang='en', article_id=None):
 u=UI[lang]
 bio=D['bio'] if lang=='en' else TR['bio']
 projects=D['projects'] if lang=='en' else [{**p,**next(t for t in TR['projects'] if t['id']==p['id'])} for p in D['projects']]
 notes=D['journal'] if lang=='en' else [{**n,**next(t for t in TR['journal'] if t['id']==n['id'])} for n in D['journal']]
 langpath='' if lang=='en' else 'tr/'
 current=Path(f'{langpath}journal/{article_id}/index.html') if article_id else Path(f'{langpath}index.html')
 depth=len(current.parent.parts)
 rel='../'*depth
 home=rel+langpath
 counterpart=('tr/' if lang=='en' else '')+(f'journal/{article_id}/' if article_id else '')
 noteurl=lambda n: rel+langpath+'journal/'+n['id']+'/'
 a=lambda p: rel+'assets/'+p
 title=(next(n['title'] for n in notes if n['id']==article_id)+' — ma_cakr') if article_id else 'ma_cakr — Mehmet Akif Çakır'
 desc=next(n['subtitle'] for n in notes if n['id']==article_id) if article_id else bio['short']
 nav=''.join(f'<a href="{home}#{key}">{u[key]}</a>' for key in ['work','journal','about','contact'])
 social=''.join(f'<a class="social-icon magnetic" href="{c["url"]}" {"" if c["type"]=="email" else chr(32)+"target=\"_blank\" rel=\"noopener noreferrer\""} aria-label="{c["label"]}">{icon(c["type"])}</a>' for c in D['contacts'] if c['type'] in ['linkedin','instagram','github','email'] and c.get('recommended'))
 cvfile=f'mehmet-akif-cakir-cv-{lang}.pdf'
 header=f'''<header class="site-header wrap">{logo(u['brand'], home+'#top')}<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="navigation"><span>{u['menu']}</span><span class="menu-lines" aria-hidden="true"></span></button><nav id="navigation" aria-label="{u['aria_main']}">{nav}</nav><div class="header-right"><a class="language-switch" href="{rel+counterpart}" lang="{'tr' if lang=='en' else 'en'}" hreflang="{'tr' if lang=='en' else 'en'}" aria-label="{'Türkçeye geç' if lang=='en' else 'Switch to English'}"><span class="{'current' if lang=='en' else ''}">EN</span><span class="lang-divider">/</span><span class="{'current' if lang=='tr' else ''}">TR</span></a><a class="header-cv animated-link" href="{home}#cv">{u['cv']}{icon('arrow')}</a></div></header>'''
 footer=f'''<footer class="site-footer wrap"><div class="footer-top">{logo(u['brand'],home+'#top')}<p>{u['footer_note']}</p><a class="to-top animated-link" href="{home}#top">{u['top']}{icon('down')}</a></div><div class="footer-bottom"><span>© 2026 Mehmet Akif Çakır</span><span>İzmir, Türkiye</span><a href="{rel+counterpart}">{'Türkçe sürüm' if lang=='en' else 'English version'}</a></div></footer>'''
 motion=f'<button class="motion-toggle" type="button" aria-pressed="false" data-pause="{u["pause"]}" data-resume="{u["resume"]}" data-reduced="{u["reduced"]}">{icon("pause")}<span>{u["pause"]}</span></button>'

 if not article_id:
  cards=''
  for i,p in enumerate(projects):
   n=next(n for n in notes if n['project']==p['id'])
   cards+=f'''<article class="project-card reveal"><a class="project-image" href="{noteurl(n)}" aria-label="{e(p['title'])} — {u['project_note']}">{artwork(p['id'])}<span class="image-arrow">{icon('arrow')}</span><span class="project-number">0{i+1} /</span></a><div class="project-meta"><span>{e(p['category'])}</span><span class="stage">{e(p['stage'])}</span></div><h3><a href="{noteurl(n)}">{e(p['title'])}</a></h3><p>{e(p['description'])}</p><div class="tech-tags">{''.join('<span>'+e(t)+'</span>' for t in p['technology'][:3])}</div><div class="project-links"><a class="animated-link" href="{noteurl(n)}">{u['next']}{icon('arrow')}</a><a class="code-link" href="{p['repository']}" target="_blank" rel="noopener noreferrer">{icon('github')}{u['code']}</a></div></article>'''
  categories=list(dict.fromkeys(n['category'] for n in notes))
  filters=f'<button class="topic-filter is-active" type="button" data-topic="all" aria-pressed="true">{u["all"]}</button>'+''.join(f'<button class="topic-filter" type="button" data-topic="{e(c)}" aria-pressed="false">{e(c)}</button>' for c in categories)
  note_cards=''
  for i,n in enumerate(notes):
   searchable=' '.join([n['title'],n['subtitle'],n['category'],' '.join(n['paragraphs'])])
   note_cards+=f'''<article class="note-card reveal" data-topic="{e(n['category'])}" data-search="{e(searchable)}"><a class="note-main" href="{noteurl(n)}"><span class="note-number">0{i+1}</span><div class="note-copy"><div class="note-meta"><span>{e(n['category'])}</span><span>·</span><span>{minutes(n)} {u['read_time']}</span></div><h3>{e(n['title'])}</h3><p>{e(n['subtitle'])}</p></div><span class="note-arrow">{icon('arrow')}</span></a></article>'''
  contacts=''
  for c in D['contacts']:
   if not c.get('recommended'):continue
   label=u['email'] if c['type']=='email' else c['label']
   contacts+=f'<a class="contact-link magnetic" href="{c["url"]}" {"" if c["type"]=="email" else "target=\"_blank\" rel=\"noopener noreferrer\""}><span class="contact-icon">{icon(c["type"])}</span><span><span class="contact-label">{label}</span><span class="contact-handle">{e(c["handle"])}</span></span>{icon("arrow","contact-arrow")}</a>'
  content=f'''
  <section class="hero wrap" aria-labelledby="hero-title"><div class="hero-copy"><div class="eyebrow"><span class="status-dot"></span>{u['role']}</div><h1 id="hero-title">{u['hero']}</h1><p class="hero-intro">{u['intro_text']}</p><div class="hero-actions"><a class="button button-primary magnetic" href="#work">{u['explore']}{icon('arrow')}</a><a class="button-text animated-link" href="#journal">{u['read']}{icon('arrow')}</a></div><div class="hero-socials">{social}<span class="social-line"></span><span class="hero-location">{u['location']}</span></div></div><figure class="portrait-frame"><div class="portrait-decor decor-one" aria-hidden="true"></div><div class="portrait-decor decor-two" aria-hidden="true"></div><div class="portrait-image"><img src="{a('portrait.jpg')}" width="460" height="460" alt="Mehmet Akif Çakır" fetchpriority="high"><span class="portrait-index" aria-hidden="true">M / A / Ç</span></div><figcaption><span>{u['portrait_caption']}<small>{u['portrait_sub']}</small></span><span class="portrait-cross" aria-hidden="true">+</span></figcaption><span class="portrait-side" aria-hidden="true">A WORK IN CONTINUOUS PROGRESS</span></figure><div class="hero-foot"><a href="#work">{icon('down')}{u['scroll']}</a><span>{u['focus']}</span></div></section>
  <section class="projects wrap section" id="work" aria-labelledby="work-title"><div class="section-heading reveal"><div><p class="eyebrow">{u['work_kicker']}</p><h2 id="work-title">{u['work_title']}</h2></div><p class="section-intro">{u['work_intro']}</p></div><div class="projects-grid">{cards}</div></section>
  <section class="journal-section" id="journal" aria-labelledby="journal-title"><div class="wrap section"><div class="section-heading reveal"><div><p class="eyebrow">{u['journal_kicker']}</p><h2 id="journal-title">{u['journal_title']}</h2></div><p class="section-intro">{u['journal_intro']}</p></div><div class="journal-tools"><label class="search-field" for="note-search">{icon('search')}<span class="sr-only">{u['search']}</span><input type="search" id="note-search" placeholder="{u['search_placeholder']}" autocomplete="off"><button class="clear-search" type="button" aria-label="{u['clear']}" hidden>×</button></label><span class="result-count" aria-live="polite" aria-atomic="true" data-unit="{u['results']}">3 {u['results']}</span></div><div class="topic-filters" role="group" aria-label="{u['search_label']}">{filters}</div><div class="notes-list">{note_cards}</div><p class="no-results" hidden>{u['no_results']}</p></div></section>
  <section class="about-section wrap section" id="about" aria-labelledby="about-title"><div class="about-portrait reveal"><div class="about-monogram" aria-hidden="true">{mark()}</div><p class="eyebrow">{u['location']}</p><h3>Mehmet Akif<br>Çakır<span>.</span></h3><p class="about-role">{u['role']}</p><a class="animated-link" href="https://orcid.org/0009-0008-9355-7559" target="_blank" rel="noopener noreferrer">{u['academic']}{icon('arrow')}</a></div><div class="about-copy"><p class="eyebrow reveal">{u['about_kicker']}</p><h2 id="about-title" class="reveal">{u['about_title']}</h2><p class="bio-text reveal">{e(bio['long'])}</p><div class="about-details reveal"><div><h3>{u['education']}</h3><p>{u['university']}<br><span>{u['degree']}</span></p></div><div><h3>{u['toolbox']}</h3><p>Python · Rust · C++<br><span>Git · Arduino · ESP32</span></p></div></div></div></section>
  <section class="cv-section wrap" id="cv"><div class="cv-strip reveal"><div class="cv-symbol" aria-hidden="true">{icon('download')}</div><div><h2>{u['cv_title']}</h2><p>{u['cv_text']}</p></div><div class="cv-actions"><a class="animated-link" href="{a(cvfile)}" target="_blank" rel="noopener">{u['view_cv']}{icon('arrow')}</a><a class="button button-outline magnetic" href="{a(cvfile)}" download="{cvfile}">{u['download_cv']}{icon('download')}</a></div></div></section>
  <section class="contact-section" id="contact" aria-labelledby="contact-title"><div class="wrap section"><p class="eyebrow reveal">{u['contact_kicker']}</p><div class="contact-heading reveal"><h2 id="contact-title">{u['contact_title']}</h2><p>{u['contact_intro']}</p></div><div class="contact-grid">{contacts}</div></div></section>
  '''
 else:
  n=next(n for n in notes if n['id']==article_id)
  p=next(p for p in projects if p['id']==n['project'])
  related=''.join(f'<a class="related-link" href="{noteurl(other)}"><span>{e(other["category"])}</span><h3>{e(other["title"])}</h3>{icon("arrow")}</a>' for other in notes if other['id']!=article_id)
  paragraphs=''.join('<p>'+e(par)+'</p>' for par in n['paragraphs'])
  sources=''.join(f'<li><a class="animated-link" href="{source["url"]}" target="_blank" rel="noopener noreferrer">{e(source["label"])}{icon("arrow")}</a></li>' for source in n['sources'])
  content=f'''<article class="article-page wrap"><a class="article-back animated-link" href="{home}#journal">{icon('arrow')}{u['back']}</a><header class="article-header"><p class="eyebrow">{u['note_label']} <span>/</span> {e(n['category'])}</p><h1>{e(n['title'])}</h1><p class="article-subtitle">{e(n['subtitle'])}</p><div class="article-byline"><img src="{a('portrait.jpg')}" alt="" width="42" height="42"><span>Mehmet Akif Çakır<small>{u['author_role']}</small></span><span class="article-time">{minutes(n)} {u['read_time']}</span></div></header><div class="article-layout"><aside class="article-sidebar"><span class="eyebrow">{u['source_repository']}</span><a class="animated-link" href="{p['repository']}" target="_blank" rel="noopener noreferrer">{e(p['title'])}{icon('arrow')}</a><span class="article-stage">{e(p['stage'])}</span></aside><div class="article-body"><figure class="article-illustration">{artwork(p['id'],'article')}</figure><div class="article-paragraphs">{paragraphs}</div><div class="article-source-note">{u['source_note']}</div><section class="article-sources"><h2>{u['sources']}</h2><ul>{sources}</ul></section></div></div><section class="related-notes"><p class="eyebrow">{u['related']}</p><div>{related}</div></section></article>'''
 metadata=json.dumps({'@context':'https://schema.org','@type':'Person','name':'Mehmet Akif Çakır','alternateName':'ma_cakr','jobTitle':u['role'],'image':D['github']['avatarUrl'],'sameAs':[c['url'] for c in D['contacts'] if c['type'] in ['github','linkedin','instagram']]},ensure_ascii=False)
 html=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f5f1e9">{publication_head(lang, article_id)}<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="{'article' if article_id else 'website'}"><meta property="og:locale" content="{'tr_TR' if lang=='tr' else 'en_US'}"><link rel="icon" href="{a('brand-mark.svg')}" type="image/svg+xml"><link rel="stylesheet" href="{rel}styles.css"><script src="{rel}app.js" defer></script><script type="application/ld+json">{metadata}</script></head><body id="top" data-lang="{lang}"><a class="skip-link" href="#main">{u['skip']}</a><canvas id="ambient-trail" aria-hidden="true"></canvas>{header}<main id="main">{content}</main>{footer}{motion}</body></html>'''
 path=OUT/current
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(html)

for lang in ['en','tr']:
 build(lang)
 for note in D['journal']:build(lang,note['id'])
build_discovery_files()

mark_svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#f5f1e9"/><g fill="none" stroke-linecap="square"><path d="M10 47V13l22 22 22-22v34" stroke="#152a44" stroke-width="4"/><path d="m19 48 13-32 13 32M24 37h16" stroke="#ad5c3a" stroke-width="3"/></g></svg>'
(OUT/'assets/brand-mark.svg').write_text(mark_svg)
(OUT/'favicon.svg').write_text(mark_svg)
(OUT/'assets/ma-cakr-logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 78"><rect width="330" height="78" fill="#f5f1e9"/><g transform="translate(10 7)" fill="none"><path d="M10 47V13l22 22 22-22v34" stroke="#152a44" stroke-width="4"/><path d="m19 48 13-32 13 32M24 37h16" stroke="#ad5c3a" stroke-width="3"/></g><text x="90" y="50" fill="#152a44" font-family="Arial,sans-serif" font-size="39" font-weight="600" letter-spacing="-2">ma_cakr<tspan fill="#ad5c3a">.</tspan></text></svg>')
print('Generated 2 homepages, 6 articles, and SVG brand assets.')
