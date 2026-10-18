from pathlib import Path
from urllib.parse import urlsplit
import ipaddress, json, os, re, shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT
D = json.loads((ROOT / 'content/site.json').read_text())

def release_base_url(value):
 """Accept a public HTTPS base URL with an optional safe deployment path."""
 if not value.strip():
  return None
 value = value.strip()
 try:
  parts = urlsplit(value)
  host = (parts.hostname or '').lower()
  port = parts.port
 except ValueError:
  raise SystemExit('SITE_BASE_URL must be the real public HTTPS site base URL.')
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
 segments = parts.path.removeprefix('/').removesuffix('/').split('/') if parts.path not in ('', '/') else []
 valid_path = all(segment not in {'.', '..'} and re.fullmatch(r'[A-Za-z0-9._~-]+', segment) for segment in segments)
 if (parts.scheme != 'https' or not valid_host or parts.netloc.lower() != host
     or any(char.isspace() for char in value) or parts.username or parts.password
     or port is not None or not valid_path or '?' in value or '#' in value):
  raise SystemExit('SITE_BASE_URL must be the real public HTTPS site base URL, with only safe path segments and no port, credentials, query or fragment; local and placeholder hosts, dot traversal and encoded paths are not allowed.')
 return 'https://' + host + parts.path.rstrip('/')

SITE_BASE_URL = release_base_url(os.environ.get('SITE_BASE_URL', ''))

from site_layout import build_site

build_site(ROOT, SITE_BASE_URL, D)

mark_svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#0b1930"/><path d="M16 40V24a3 3 0 0 1 5-2l11 11 11-11a3 3 0 0 1 5 2v16" fill="none" stroke="#e7effa" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M28 47h9" stroke="#80d9f5" stroke-width="3.6" stroke-linecap="round"/></svg>'
(OUT/'assets/brand-mark.svg').write_text(mark_svg)
(OUT/'favicon.svg').write_text(mark_svg)
(OUT/'assets/ma-cakr-logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 330 78"><g transform="translate(4 7)"><rect width="64" height="64" rx="18" fill="#0b1930"/><path d="M16 40V24a3 3 0 0 1 5-2l11 11 11-11a3 3 0 0 1 5 2v16" fill="none" stroke="#e7effa" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/><path d="M28 47h9" stroke="#80d9f5" stroke-width="3.6" stroke-linecap="round"/></g><text x="86" y="50" fill="#e7effa" font-family="Arial,sans-serif" font-size="39" font-weight="600" letter-spacing="-2">ma<tspan fill="#80d9f5">_</tspan>cakr<tspan fill="#80d9f5">.</tspan></text></svg>')

# Stable localized CV URLs preserve the original PDF assets unchanged.
shutil.copyfile(ROOT/'assets/mehmet-akif-cakir-cv-en.pdf', ROOT/'cv.pdf')
shutil.copyfile(ROOT/'assets/mehmet-akif-cakir-cv-tr.pdf', ROOT/'tr/cv.pdf')
