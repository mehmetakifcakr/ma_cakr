"""Localized static portfolio pages; the existing journal stays the source of truth."""

from html import escape
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = json.loads((ROOT / 'content/portfolio.json').read_text())
ORIGINAL = json.loads((ROOT / 'content/site.json').read_text())
PAGE_NAMES = {key: value['name'] for key, value in PORTFOLIO['pages'].items()}


def e(value):
    return escape(str(value), quote=True)


def localized(value, lang):
    return value.get(lang, value.get('en', '')) if isinstance(value, dict) else value


def get_personal(lang='en'):
    return {key: localized(value, lang) for key, value in PORTFOLIO['personal'].items()}


def get_projects(lang='en'):
    categories = {c['id']: localized(c['label'], lang) for c in PORTFOLIO['categories']}
    result = []
    for project in PORTFOLIO['projects']:
        item = {key: localized(value, lang) for key, value in project.items()}
        item['category_id'] = project['category']
        item['category'] = categories[project['category']]
        for field in ('github', 'crates', 'article', 'limitation'):
            item.setdefault(field, '')
        if item['article']:
            item['article'] = 'journal/' + item['article'] + '/'
        result.append(item)
    return result


def tags(items):
    return '<div class="tags">' + ''.join(f'<span>{e(item)}</span>' for item in items) + '</div>'


def project_art(project_id, instance=''):
    """Native schematic illustrations, never screenshots or project photographs."""
    key = e(project_id + ('-' + instance if instance else ''))
    line = 'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    if project_id == 'recovertick':
        body = '<rect x="42" y="71" width="126" height="92" rx="12"/><rect x="192" y="112" width="105" height="78" rx="12"/><rect x="322" y="72" width="116" height="92" rx="12"/><path d="M168 117h24m105 34h25V118M67 94h57m-57 21h75m-75 21h42M216 137h58m-58 24h35M346 96h65m-65 22h42m-42 22h61"/><path class="art-accent" d="m176 110 8 7-8 7m137 20 9 7-9 7"/><circle class="art-accent" cx="244" cy="64" r="20"/><path d="M244 51v13l8 7"/>'
    elif project_id == 'openrobotkit':
        body = '<path d="m180 183 60-35 62 35v34l-62 35-60-35z"/><path d="m180 183 60 35 62-35m-62 35v34"/><path d="M240 148v-29l-54-37 20-32 78 47v68"/><circle class="art-accent" cx="241" cy="119" r="18"/><circle cx="198" cy="67" r="15"/><path d="m206 50 48-31 19 12-48 31m29-43 23 20 23-12m-23 12-3 25"/><path d="M128 187c-22-39-12-89 21-116m183 103c12-47-9-92-45-109" stroke-dasharray="5 8"/>'
    elif project_id in ('autonomous-egg-robot', 'tennis-ball-robot'):
        body = '<path d="m129 140 124-50 111 46-129 56zM129 140v49l106 51 129-56v-48M235 192v48"/><path d="m160 130 34-14 31 13-34 14zM273 107l37 15-35 15-37-15z"/><ellipse cx="164" cy="198" rx="23" ry="30"/><ellipse cx="326" cy="191" rx="23" ry="30"/><path d="M160 130V76l-36-26m68 69V67l25-17M127 77l25-11M231 193l47-52 49 18-50 53"/><circle class="art-accent" cx="254" cy="173" r="15"/><circle class="art-accent" cx="297" cy="192" r="13"/><path d="M103 217h-31m305-34h34m-51-108h33" stroke-dasharray="4 7"/>'
    elif project_id == 'traffic-priority-system':
        body = '<path d="M32 183h416M183 28v202m111-202v202" stroke-dasharray="7 9" opacity=".4"/><rect x="88" y="64" width="40" height="103" rx="16"/><circle cx="108" cy="87" r="8"/><circle cx="108" cy="115" r="8"/><circle class="art-accent" cx="108" cy="143" r="8"/><path d="M108 167v60"/><rect x="322" y="75" width="104" height="58" rx="13"/><path d="M347 75V62h29v13m-21 14v27m-13-14h27M322 113h104"/><circle cx="343" cy="136" r="11"/><circle cx="404" cy="136" r="11"/><path class="art-accent" d="M296 90c-17-15-17-27 0-42m-15 53c-29-25-29-51 0-76M151 91c17 15 17 27 0 42"/>'
    elif project_id == 'biomedical-shoulder-3d':
        body = '<path d="M216 45c-31-9-67 3-85 31-20 29-20 60-9 83l35 51 48-21 19-54-12-32 34-32z"/><path d="m143 83 58 20-19 53-25 54m25-54-60 3m90-56-30 53 23 33" opacity=".6"/><ellipse class="art-accent" cx="259" cy="93" rx="35" ry="37"/><path d="M258 126c-9 25-8 48-4 68l9 48h40l-11-54c-7-33-11-48-10-69"/><path d="M222 77c20-19 57-20 75 6m-82 25c22 31 44 49 76 57" stroke-dasharray="5 6"/><path d="M302 61h54m-23 139h47M105 115H64"/>'
    elif project_id == 'biomimetic-robot-arm':
        body = '<path d="m167 206 65-35 87 32-62 39zM167 206v18l90 34 62-36v-19"/><path d="M237 174V130l-47-54 20-19 65 61v69"/><circle class="art-accent" cx="255" cy="132" r="21"/><circle cx="201" cy="68" r="16"/><path d="m203 51 49-25 23 19-54 28m31-47 40-1 20 20m-37 0 20 20 25-8m-25 8 8 21 23-9M206 89l36 58"/><path d="M146 183c-32-46-8-104 14-121m177 114c20-57-2-97-22-113" stroke-dasharray="4 8"/>'
    elif project_id == 'high-altitude-rocket':
        body = '<path d="M239 26c-24 27-31 42-31 68v91h62V94c0-26-9-43-31-68z"/><path d="M208 121h62m-62 48h62m-39-75v75m18-75v75m-41 11-31 42h31m62-42 31 42h-31M224 186l-5 21h40l-6-21"/><circle class="art-accent" cx="239" cy="91" r="15"/><path class="art-accent" d="m226 218 13 27 14-27"/><path d="M169 93h-35m174 30h40m-162 46h-46m157 23h46"/><circle cx="134" cy="93" r="4"/><circle cx="348" cy="123" r="4"/>'
    else:
        body = '<path d="M62 211h357M62 49v162"/><path d="M62 91h357M62 131h357M62 171h357" opacity=".25" stroke-dasharray="4 6"/><path class="art-accent" d="m72 188 34-17 27 8 36-43 36 15 32-31 30 13 32-37 39 5 32-34 34 9"/><path d="m72 201 34-8 27 3 36-19 36 8 32-15 30 6 32-17 39 3 32-16 34 4"/><circle class="art-accent" cx="299" cy="96" r="6"/>'
    return (f'<svg class="project-art" viewBox="0 0 480 280" fill="none" aria-hidden="true">'
            f'<defs><pattern id="p-grid-{key}" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0v24" stroke="currentColor" stroke-width=".5" opacity=".13"/></pattern></defs>'
            f'<rect width="480" height="280" fill="url(#p-grid-{key})"/><g {line}>{body}</g></svg>')


def page_head(page, lang):
    data = PORTFOLIO['pages'][page]
    return (f'<header class="p-page-head"><p class="eyebrow">{e(localized(data["eyebrow"], lang))}</p>'
            f'<h1 class="page-title">{e(localized(data["title"], lang))}</h1>'
            f'<p class="page-intro muted">{e(localized(data["intro"], lang))}</p></header>')


def external_link(url, label, icon):
    return f'<a class="text-link" href="{e(url)}" target="_blank" rel="noopener noreferrer">{e(label)}{icon("arrow")}</a>'


def filter_controls(categories, lang, ui, kind='projects'):
    is_blog = kind == 'blog'
    search_label = ui['search_notes' if is_blog else 'search_projects']
    all_label = ui['all_notes' if is_blog else 'all']
    filter_label = ui['filter_notes' if is_blog else 'filter_projects']
    buttons = f'<button type="button" class="filter-chip is-active" data-filter="all" aria-pressed="true">{e(all_label)}</button>'
    buttons += ''.join(f'<button type="button" class="filter-chip" data-filter="{e(key)}" aria-pressed="false">{e(label)}</button>' for key, label in categories)
    return (f'<div class="filter-toolbar"><div class="filter-chips" role="group" aria-label="{e(filter_label)}">{buttons}</div>'
            f'<div class="filter-search"><label class="sr-only" for="{kind}-search">{e(search_label)}</label>'
            f'<input id="{kind}-search" type="search" data-filter-search placeholder="{e(ui["search_project_placeholder"])}" autocomplete="off"></div>'
            f'<button class="btn btn-small filter-reset" type="button" data-filter-reset>{e(ui["clear_filters"])}</button></div>')


def render_projects(lang, context, ui):
    icon, base = context['icon'], context['base']
    projects = get_projects(lang)
    categories = [(c['id'], localized(c['label'], lang)) for c in PORTFOLIO['categories']]
    cards = []
    for index, project in enumerate(projects, 1):
        links = []
        if project['github']:
            links.append(external_link(project['github'], ui['code'], icon))
        if project['crates']:
            links.append(external_link(project['crates'], ui['package'], icon))
        if project['article']:
            links.append(f'<a class="text-link" href="{e(base + project["article"])}">{e(ui["article"])}{icon("arrow")}</a>')
        limitation = f'<div class="scope-note"><h4>{e(ui["current_scope"])}</h4><p>{e(project["limitation"])}</p></div>' if project['limitation'] else ''
        search = ' '.join([project['title'], project['summary'], project['description'], project['category'], *project['tech']])
        cards.append(f'''<article id="{e(project['id'])}" class="panel portfolio-project project-card" data-filter-item data-category="{e(project['category_id'])}" data-search="{e(search)}">
          <div class="project-visual"><span class="project-sequence">{index:02d}</span>{project_art(project['id'])}<span class="art-caption">{e(ui['illustration'])}</span></div>
          <div class="project-content project-body"><div class="project-meta"><span>{e(project['category'])}</span><span>{e(project['date'])}</span></div>
          <h2>{e(project['title'])}</h2><p>{e(project['summary'])}</p>{tags(project['tech'])}
          <details class="project-details"><summary>{e(ui['details'])}<span aria-hidden="true">+</span></summary><div><p>{e(project['description'])}</p>{limitation}<div class="project-links">{''.join(links)}</div></div></details></div></article>''')
    return (filter_controls(categories, lang, ui) + f'<p class="filter-summary" aria-live="polite"><span data-filter-count>{len(cards)}</span> {e(ui["results"])}</p>'
            + '<div class="project-grid" data-filter-grid>' + ''.join(cards) + '</div>'
            + f'<p class="empty-state panel" data-filter-empty hidden>{e(ui["empty"])}</p>')


def model_viewer(ui):
    return f'''<section class="model-exhibit model-viewer panel" aria-labelledby="model-title" data-model-viewer>
      <div class="model-stage model-viewport" aria-label="{e(ui['model_label'])}">
        <div class="model-rotate" data-model-rotate>{project_art('biomimetic-robot-arm', 'viewer')}</div>
        <span class="model-coordinate coordinate-x" aria-hidden="true">X</span><span class="model-coordinate coordinate-y" aria-hidden="true">Y</span><span class="model-coordinate coordinate-z" aria-hidden="true">Z</span>
        <span class="model-stage-label">{e(ui['illustration'])}</span></div>
      <div class="model-copy"><p class="eyebrow">CAD / 3D</p><h2 id="model-title">{e(ui['model_title'])}</h2><p>{e(ui['model_note'])}</p><p class="small muted">{e(ui['drag'])}</p>
      <div class="model-controls"><label for="model-angle">{e(ui['angle'])}</label><input id="model-angle" data-model-angle type="range" min="0" max="360" value="24" step="1"><div class="button-row"><button class="btn btn-small" data-model-reset type="button">{e(ui['reset'])}</button><button class="btn btn-small" data-model-auto type="button" aria-pressed="false" data-start="{e(ui['auto_rotate'])}" data-stop="{e(ui['stop_rotate'])}">{e(ui['auto_rotate'])}</button></div></div></div></section>'''


def render_lab(lang, context, ui):
    tabs = f'''<div class="lab-tabs" role="tablist" aria-label="{e(ui['lab_tabs'])}"><button class="filter-chip is-active" type="button" role="tab" id="tab-fabrication" aria-controls="panel-fabrication" aria-selected="true" data-tab="fabrication">{e(ui['fabrication'])}</button><button class="filter-chip" type="button" role="tab" id="tab-ai" aria-controls="panel-ai" aria-selected="false" data-tab="ai">{e(ui['ai'])}</button></div>'''
    fabrication = ''
    for item in PORTFOLIO['lab']['fabrication']:
        artwork = project_art('biomedical-shoulder-3d' if item['id'] == 'shoulder' else 'biomimetic-robot-arm')
        fabrication += f'''<article class="panel lab-card"><div class="lab-card-art">{artwork}<span class="art-caption">{e(ui['illustration'])}</span></div><div class="lab-card-copy"><span class="status-label">{e(ui['supply_pending'])}</span><h3>{e(localized(item['title'], lang))}</h3><p>{e(localized(item['description'], lang))}</p>{tags(item['tools'])}<p class="small muted">{e(localized(item['material'], lang))}</p></div></article>'''
    ai = ''
    for index, item in enumerate(PORTFOLIO['lab']['ai'], 1):
        ai += f'''<article class="panel ai-card"><div class="ai-card-visual" aria-hidden="true"><span class="ai-orbit"></span><span class="ai-frame"></span><span class="ai-frame ai-frame-two"></span><span class="ai-visual-index">0{index} / AI</span></div><div class="lab-card-copy"><span class="status-label">{e(ui['supply_pending'])}</span><h3>{e(localized(item['title'], lang))}</h3><p>{e(localized(item['description'], lang))}</p>{tags(item['tools'])}<details class="project-details"><summary>{e(ui['workflow'])}<span aria-hidden="true">+</span></summary><p>{e(localized(item['pipeline'], lang))}</p></details></div></article>'''
    return (tabs + f'<section id="panel-fabrication" class="lab-tab-panel" role="tabpanel" aria-labelledby="tab-fabrication" data-tab-panel="fabrication">'
            + model_viewer(ui) + f'<h2 class="section-title">{e(ui["cad_models"])}</h2><div class="lab-grid">{fabrication}</div></section>'
            + f'<section id="panel-ai" class="lab-tab-panel" role="tabpanel" aria-labelledby="tab-ai" data-tab-panel="ai"><h2 class="section-title">{e(ui["ai_studies"])}</h2><p class="notice panel">{e(ui["ai_note"])}</p><div class="lab-grid">{ai}</div></section>')


def mobility_map(ui, lang):
    names = {place['id']: localized(place['country'], lang) for place in PORTFOLIO['mobility']}
    return f'''<svg class="mobility-map" viewBox="0 0 900 390" role="img" aria-labelledby="route-map-title route-map-desc"><title id="route-map-title">{e(ui['map_label'])}</title><desc id="route-map-desc">{e(ui['mobility_note'])}</desc>
      <defs><pattern id="mobility-grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0v30" fill="none" stroke="currentColor" opacity=".12"/></pattern></defs><rect width="900" height="390" fill="url(#mobility-grid)"/>
      <g class="map-land" fill="currentColor" opacity=".08" stroke="currentColor"><path d="m99 176 24-27 13-33 34-8 18-21 35 7 20 27 38-8 28 24 36-18 29 20 34-9 29 24 38-11 47 18 33-8 47 30-11 19-41-5-24 19-37-8-23 21-45-10-26 19-32-16-28 13-27-15-16 23-33-15-15-39-30-7-16-26-25 12-8 33-32 6-10-29-28-4z"/><path d="m178 222 45-12 31 31 16 50-22 51-26-8-15-49-24-25zM674 197l13 16-8 23-11-11zM694 172l11-10 6 20-12 24-12-7z"/></g>
      <g class="map-route" fill="none" stroke="currentColor" stroke-width="2"><path d="M160 193Q201 91 269 169"/><path class="map-route-planned" d="M269 169Q461 11 696 203" stroke-dasharray="7 8"/></g>
      <g class="map-point" fill="currentColor"><circle cx="160" cy="193" r="6"/><circle cx="269" cy="169" r="6"/><circle cx="696" cy="203" r="6" fill="none" stroke="currentColor" stroke-width="2"/></g>
      <g class="map-place-label" fill="currentColor" font-family="inherit" font-size="15"><text x="112" y="225">{e(names['spain'])}</text><text x="240" y="145">{e(names['romania'])}</text><text x="652" y="235">{e(ui['japan_label'])}</text></g></svg>'''


def render_mobility(lang, context, ui):
    places = PORTFOLIO['mobility']
    controls = ''.join(f'<button class="place-button" type="button" data-place="{p["id"]}" aria-controls="place-{p["id"]}" aria-pressed="false">{e(localized(p["country"], lang))}<span>{e(ui["planned"] if p["status"] == "planned" else ui["completed"])}</span></button>' for p in places)
    cards = ''
    for index, place in enumerate(places, 1):
        status = ui['planned'] if place['status'] == 'planned' else ui['completed']
        cards += f'''<article class="panel place-card {'place-planned' if place['status'] == 'planned' else ''}" id="place-{place['id']}" data-place-card="{place['id']}" tabindex="-1"><div class="place-number" aria-hidden="true">0{index}</div><div class="place-copy"><div class="project-meta"><span class="status-label">{e(status)}</span><span>{e(localized(place['date'], lang))}</span></div><p class="place-country">{e(localized(place['country'], lang))} / {e(localized(place['city'], lang))}</p><h2>{e(localized(place['title'], lang))}</h2><ul>{''.join(f'<li>{e(localized(point, lang))}</li>' for point in place['highlights'])}</ul></div></article>'''
    return f'<section class="panel map-panel">{mobility_map(ui, lang)}<p class="map-caption muted">{e(ui["map_note"])}</p><div class="place-controls" role="group" aria-label="{e(ui["places"])}">{controls}</div></section><h2 class="section-title">{e(ui["route"])}</h2><div class="mobility-timeline">{cards}</div><p class="small muted">{e(ui["mobility_note"])}</p>'


def render_cv(lang, context, ui):
    person = get_personal(lang)
    cv_path = context['rel'] + f'assets/mehmet-akif-cakir-cv-{lang}.pdf'
    education = ''
    for item in PORTFOLIO['education']:
        education += f'<article class="timeline-entry timeline-item"><p class="eyebrow">{e(localized(item["period"], lang))}</p><h3>{e(localized(item["degree"], lang))}</h3><p class="timeline-institution">{e(localized(item["institution"], lang))}</p><p class="small muted">{e(localized(item["faculty"], lang))}</p><p>{e(localized(item["details"], lang))}</p></article>'
    experience = ''
    for item in PORTFOLIO['experiences']:
        experience += f'<article class="timeline-entry timeline-item"><p class="eyebrow">{e(localized(item["period"], lang))}</p><h3>{e(localized(item["role"], lang))}</h3><p class="timeline-institution">{e(localized(item["organization"], lang))}</p><ul>{"".join("<li>" + e(localized(h, lang)) + "</li>" for h in item["highlights"])}</ul></article>'
    skills = ''
    for group in PORTFOLIO['skills']:
        items = group.get('items', [localized(item, lang) for item in group.get('items_localized', [])])
        skills += f'<article class="panel skill-card"><h3>{e(localized(group["category"], lang))}</h3>{tags(items)}</article>'
    return f'''<div class="cv-actions button-row"><a class="btn btn-primary" href="{e(cv_path)}" download>{e(ui['download_cv'])}{context['icon']('download')}</a><button type="button" class="btn" data-print>{e(ui['print'])}</button></div><p class="small muted cv-pdf-note">{e(ui['cv_note'])}</p>
      <section class="panel cv-profile"><p class="eyebrow">{e(ui['profile'])}</p><h2>{e(person['name'])}</h2><p>{e(person['bio'])}</p><div class="cv-contact-line"><a href="mailto:{e(person['emails'][0])}">{e(person['emails'][0])}</a><span>{e(person['university_location'])} · {e(person['hometown_location'])}</span></div></section>
      <div class="cv-columns"><section class="panel cv-section" aria-labelledby="education-title"><h2 id="education-title">{e(ui['education'])}</h2><div class="timeline">{education}</div></section><section class="panel cv-section" aria-labelledby="experience-title"><h2 id="experience-title">{e(ui['experience'])}</h2><div class="timeline">{experience}</div></section></div>
      <section class="skills-section" aria-labelledby="skills-title"><h2 class="section-title" id="skills-title">{e(ui['skills'])}</h2><p class="small muted">{e(ui['skills_note'])}</p><div class="skills-grid">{skills}</div></section>'''


def render_uses(lang, context, ui):
    cards = ''
    symbols = {'computing': '01', 'embedded': '02', 'workshop': '03', 'software': '04'}
    for group in PORTFOLIO['uses']:
        cards += f'<article class="panel uses-card"><span class="uses-index" aria-hidden="true">{symbols[group["id"]]}</span><h2>{e(localized(group["category"], lang))}</h2><p class="muted">{e(localized(group["description"], lang))}</p><ul>{"".join("<li>" + e(localized(item, lang)) + "</li>" for item in group["items"])}</ul></article>'
    return f'<div class="uses-grid">{cards}</div><p class="small muted">{e(ui["uses_note"])}</p>'


def get_notes(lang='en'):
    notes = ORIGINAL['journal']
    if lang == 'tr':
        translated = {note['id']: note for note in ORIGINAL['translations_tr']['journal']}
        notes = [{**note, **translated.get(note['id'], {})} for note in notes]
    return notes


def render_blog(lang, context, ui):
    notes = get_notes(lang)
    category_ids = {category: f'topic-{index}' for index, category in enumerate(dict.fromkeys(note['category'] for note in notes))}
    categories = [(key, category) for category, key in category_ids.items()]
    cards = ''
    for index, note in enumerate(notes, 1):
        minutes = max(1, math.ceil(len(' '.join(note['paragraphs']).split()) / 200))
        search = ' '.join([note['title'], note['subtitle'], note['category'], *note['paragraphs']])
        href = context['base'] + 'journal/' + note['id'] + '/'
        cards += f'''<article class="panel blog-card" data-filter-item data-category="{category_ids[note['category']]}" data-search="{e(search)}"><a class="blog-card-link" href="{e(href)}"><span class="blog-index" aria-hidden="true">0{index}</span><div><div class="project-meta"><span>{e(note['category'])}</span><span>{minutes} {e(ui['readtime'])}</span></div><h2>{e(note['title'])}</h2><p>{e(note['subtitle'])}</p><span class="text-link">{e(ui['read_note'])}{context['icon']('arrow')}</span></div></a></article>'''
    return (filter_controls(categories, lang, ui, 'blog') + f'<p class="filter-summary" aria-live="polite"><span data-filter-count>{len(notes)}</span> {e(ui["results"])}</p>'
            + f'<div class="blog-grid" data-filter-grid>{cards}</div><p class="panel empty-state" data-filter-empty hidden>{e(ui["notes_empty"])}</p><p class="small muted">{e(ui["blog_note"])}</p>')


def render_contact(lang, context, ui):
    person = get_personal(lang)
    addresses = ''
    for address in person['emails']:
        addresses += f'<div class="email-card"><a href="mailto:{e(address)}">{e(address)}</a><button class="copy-button" type="button" data-copy="{e(address)}" data-copied="{e(ui["copied"])}" aria-label="{e(ui["copy_email"])}: {e(address)}">{e(ui["copy_email"])}</button></div>'
    contacts = [contact for contact in ORIGINAL['contacts'] if contact.get('recommended') and contact['type'] != 'email']
    links = ''.join(external_link(contact['url'], contact['label'], context['icon']) for contact in contacts)
    options = ''.join(f'<option value="{e(address)}">{e(address)}</option>' for address in person['emails'])
    return f'''<div class="contact-grid"><div class="contact-details"><section class="panel contact-panel"><h2>{e(ui['email'])}</h2>{addresses}<h3>{e(ui['public_profiles'])}</h3><div class="contact-socials">{links}</div></section><section class="panel location-panel"><h2>{e(ui['locations'])}</h2><dl><div><dt>{e(ui['university'])}</dt><dd>{e(person['university_location'])}</dd></div><div><dt>{e(ui['hometown'])}</dt><dd>{e(person['hometown_location'])}</dd></div></dl></section></div>
      <section class="panel contact-form-panel"><h2>{e(ui['message_title'])}</h2><p id="form-explanation" class="muted">{e(ui['form_note'])}</p><form class="contact-form" data-contact-form aria-describedby="form-explanation" action="mailto:{e(person['emails'][0])}" method="get" enctype="text/plain"><label for="contact-recipient">{e(ui['recipient'])}</label><select id="contact-recipient" name="recipient">{options}</select><label for="contact-email">{e(ui['your_email'])}</label><input id="contact-email" name="email" type="email" autocomplete="email" required><label for="contact-subject">{e(ui['subject'])}</label><input id="contact-subject" name="subject" type="text" maxlength="160" required><label for="contact-message">{e(ui['message'])}</label><textarea id="contact-message" name="message" rows="6" maxlength="8000" required></textarea><button class="btn btn-primary" type="submit">{e(ui['send'])}{context['icon']('arrow')}</button><p class="form-status small" data-contact-status role="status"></p></form><p class="small muted">{e(ui['form_fallback'])}</p></section></div>'''


def render_page(page, lang, context):
    """Return page body. Context: rel asset prefix, base localized home, icon callable."""
    if lang not in ('en', 'tr'):
        raise ValueError('Unsupported portfolio language: ' + lang)
    renderers = {'projects': render_projects, 'lab': render_lab, 'mobility': render_mobility, 'cv': render_cv, 'uses': render_uses, 'blog': render_blog, 'contact': render_contact}
    if page not in renderers:
        raise ValueError('Unknown portfolio page: ' + page)
    ui = {key: localized(value, lang) for key, value in PORTFOLIO['ui'].items()}
    return '<div class="portfolio-page page-' + e(page) + '">' + page_head(page, lang) + renderers[page](lang, context, ui) + '</div>'
