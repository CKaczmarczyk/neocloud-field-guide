#!/usr/bin/env python3
"""Build the static Neocloud Field Guide site from src/compute-yard.html and the export/ folder.
Usage: python3 build_site.py  -> writes ./site (index.html, data.json, vercel.json, _blob/*.pdf)
"""
import json, os, glob, shutil, datetime, sys
root = os.path.dirname(os.path.abspath(__file__))
site = os.path.join(root, 'site')
shutil.rmtree(site, ignore_errors=True)
os.makedirs(os.path.join(site, '_blob'))
data = {"__snapshot": datetime.date.today().isoformat()}
for col in ['briefings', 'companies', 'reports', 'metrics', 'themes', 'scenarios']:
    d = {}
    for f in glob.glob(os.path.join(root, 'export', col, '*.json')):
        with open(f) as fh:
            d[os.path.basename(f)[:-5]] = json.load(fh)
    data[col] = d
with open(os.path.join(site, 'data.json'), 'w') as fh:
    json.dump(data, fh)
html = open(os.path.join(root, 'src', 'compute-yard.html')).read()
skel = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n<meta name="robots" content="noindex">\n')
open(os.path.join(site, 'index.html'), 'w').write(skel + html.replace('</style>', '</style>\n</head>\n<body>', 1) + '\n</body>\n</html>\n')
for f in glob.glob(os.path.join(root, 'export', 'assets', '*.pdf')):
    shutil.copy(f, os.path.join(site, '_blob'))
json.dump({"rewrites": [{"source": "/_blob/:id", "destination": "/_blob/:id.pdf"}],
           "headers": [{"source": "/data.json", "headers": [{"key": "Cache-Control", "value": "no-cache"}]}]},
          open(os.path.join(site, 'vercel.json'), 'w'))
print('built', sorted(os.listdir(site)), 'data.json', os.path.getsize(os.path.join(site, 'data.json')), 'bytes')
