#!/usr/bin/env python3
"""
gen_tokens — turn a brand.json (see references/brand-json.md) into real token files:
  tokens.css   :root { --color-<role> … } + a Tailwind v4 @theme mirror
  tokens.json  { color, font, text, radius, spacing }

Keeps the book, the companion skill, and the product in sync — regenerate whenever
brand.json changes. Stdlib only.

Usage:
  gen_tokens.py brand.json --out-dir .          # writes tokens.css + tokens.json
  gen_tokens.py brand.json --print              # print CSS to stdout
"""
import json, sys, os, argparse

# semantic role -> our conventional CSS variable name
ROLE_VAR = {
    'background': 'paper', 'surface': 'mist', 'border': 'line', 'neutral': 'slate',
    'muted': 'graphite', 'foreground': 'ink', 'accent': 'accent',
    'accent-secondary': 'accent-2',
}


def build(brand):
    colors = brand.get('colors', [])
    cvars = []          # (varname, hex)
    cjson = {}
    for c in colors:
        role = c.get('role', '')
        name = ROLE_VAR.get(role, role or c.get('name', 'x').lower().replace(' ', '-'))
        cvars.append((f'color-{name}', c['hex']))
        cjson[name] = c['hex']
        if c.get('accentText'):
            cvars.append(('color-accent-text', c['accentText']))
            cjson['accent-text'] = c['accentText']

    ty = brand.get('typography', {})
    fam = {'sans': ty.get('body', {}).get('family') or ty.get('display', {}).get('family'),
           'mono': ty.get('mono', {}).get('family')}
    scale = ty.get('scale', {})
    lay = brand.get('layout', {})
    radius = lay.get('radius', {})
    spacing = lay.get('spacingBase')

    lines = [':root{']
    if fam['sans']:
        fb = ', '.join(ty.get('body', ty.get('display', {})).get('fallbacks', []))
        lines.append(f'  --font-sans: "{fam["sans"]}"{", " + fb if fb else ""};')
    if fam['mono']:
        fb = ', '.join(ty.get('mono', {}).get('fallbacks', []))
        lines.append(f'  --font-mono: "{fam["mono"]}"{", " + fb if fb else ""};')
    for v, hexv in cvars:
        lines.append(f'  --{v}: {hexv};')
    for k, v in scale.items():
        lines.append(f'  --text-{k}: {v}px;')
    for k, v in radius.items():
        lines.append(f'  --radius-{k}: {v};')
    if spacing:
        lines.append(f'  --space-base: {spacing};')
    lines.append('}')

    # Tailwind v4 @theme mirror
    theme = ['@theme{']
    if fam['sans']:
        theme.append(f'  --font-sans: "{fam["sans"]}";')
    if fam['mono']:
        theme.append(f'  --font-mono: "{fam["mono"]}";')
    for v, hexv in cvars:
        theme.append(f'  --{v}: {hexv};')
    theme.append('}')

    css = '\n'.join(lines) + '\n\n' + '\n'.join(theme) + '\n'
    tokens = {'color': cjson, 'font': {k: v for k, v in fam.items() if v},
              'text': {k: f'{v}px' for k, v in scale.items()},
              'radius': radius, 'spacing': {'base': spacing} if spacing else {}}
    return css, tokens


def main():
    ap = argparse.ArgumentParser(prog='gen_tokens')
    ap.add_argument('brand_json')
    ap.add_argument('--out-dir', default=None)
    ap.add_argument('--print', dest='to_stdout', action='store_true')
    a = ap.parse_args()
    brand = json.load(open(a.brand_json))
    css, tokens = build(brand)
    if a.to_stdout or not a.out_dir:
        print(css)
        return
    os.makedirs(a.out_dir, exist_ok=True)
    open(os.path.join(a.out_dir, 'tokens.css'), 'w').write(css)
    open(os.path.join(a.out_dir, 'tokens.json'), 'w').write(json.dumps(tokens, indent=2) + '\n')
    print(f'wrote tokens.css + tokens.json to {a.out_dir} '
          f'({len(tokens["color"])} colours, fonts {list(tokens["font"].values())})')


if __name__ == '__main__':
    main()
