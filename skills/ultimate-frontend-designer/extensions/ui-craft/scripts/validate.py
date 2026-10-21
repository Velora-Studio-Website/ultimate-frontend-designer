#!/usr/bin/env python3
"""Offline module integrity; does not establish visual quality or Pro parity."""
from __future__ import annotations
import argparse
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

REQUIRED = ['GUIDE.md', 'PROVENANCE.md', 'vendor/oil-ui/LICENSE',
            'references/direction-polish.md', 'references/interaction-states.md',
            'references/workspaces-renovation.md', 'references/review-protocol.md',
            'references/component-patterns.md', 'references/tooling.md',
            'scripts/review.py', 'assets/component-lab.html',
            'assets/component-lab.css', 'assets/component-lab.js', 'source-manifest.json']


class Lab(HTMLParser):
    def __init__(self):
        super().__init__()
        self.patterns = []
        self.resources = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'data-pattern' in values:
            self.patterns.append(values['data-pattern'])
        if tag in {'script', 'link', 'img'}:
            ref = values.get('src') or values.get('href')
            if ref:
                self.resources.append(ref)


def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors = [f'Missing {name}' for name in REQUIRED if not (root / name).is_file()]
    if errors:
        return errors
    for path in root.rglob('*'):
        if path.is_symlink():
            errors.append(f'Unsupported symlink: {path.relative_to(root)}')
    for path in [root / 'GUIDE.md', *sorted((root / 'references').glob('*.md'))]:
        text = path.read_text(encoding='utf-8')
        text = re.sub(r'(?ms)^```.*?^```\s*$', '', text)
        for ref in re.findall(r'\[[^\]\n]*\]\(([^\s)]+)', text):
            parsed = urlsplit(ref)
            if parsed.scheme or ref.startswith('#'):
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                errors.append(f'Broken/outside link in {path.relative_to(root)}: {ref}')
    lab = Lab()
    lab.feed((root / 'assets/component-lab.html').read_text(encoding='utf-8'))
    if len(lab.patterns) != 19 or len(set(lab.patterns)) != 19 or not all(lab.patterns):
        errors.append('Lab must contain 19 distinct data-pattern containers')
    for ref in lab.resources:
        if urlsplit(ref).scheme or ref.startswith('//'):
            errors.append('Lab must not load remote resources')
        elif not (root / 'assets' / ref).is_file():
            errors.append(f'Missing lab resource: {ref}')
    manifest = json.loads((root / 'source-manifest.json').read_text(encoding='utf-8'))
    rows = manifest.get('files', {})
    actual = {p.relative_to(root).as_posix() for p in (root / 'vendor').rglob('*') if p.is_file()}
    if set(rows) != actual:
        errors.append('Vendored source inventory differs from provenance manifest')
    for name, digest in rows.items():
        p = (root / name).resolve()
        if not p.is_relative_to(root / 'vendor') or not p.is_file():
            errors.append('Invalid vendored source path')
        elif hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            errors.append(f'Vendored source changed: {name}')
    if list((root / 'vendor').rglob('SKILL.md')):
        errors.append('Vendored discovery entrypoint is forbidden; use supporting methods only')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, nargs='?', default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors = validate(args.root)
    except (OSError, ValueError, TypeError, AttributeError) as error:
        print(f'FAIL: unreadable or malformed package: {error}')
        return 1
    for error in errors:
        print('FAIL:', error)
    if errors:
        return 1
    print('PASS: module files, links, 19 pattern inventory, offline assets and source hashes.')
    print('Scope: static integrity only; browser use and design outcomes require actual execution.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
