"""Offline package checks; no tools, credentials, network or installation needed."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills' / 'ultimate-frontend-designer'
required = ['design-foundation.md', 'pages-and-assets.md', 'motion-and-video.md', 'prompts-and-state.md']
for name in required:
    assert (SKILL / 'references' / name).is_file(), f'Missing reference: {name}'
assert len(list((SKILL / 'references').glob('*.md'))) == 4, 'Expected four reference chapters'
main = (SKILL / 'SKILL.md').read_text(encoding='utf-8-sig')
assert main.startswith('---\n'), 'Missing YAML frontmatter'
assert 'name: ultimate-frontend-designer' in main
assert 'description:' in main.split('---', 2)[1]
version = re.search(r'version: "([^"]+)"', main).group(1)
for name in ['plugin.json', '.codex-plugin/plugin.json']:
    manifest = json.loads((ROOT / name).read_text(encoding='utf-8-sig'))
    assert manifest['name'] == 'ultimate-frontend-designer'
    assert manifest['version'] == version, f'Version mismatch: {name}'
assert '内容范围与视觉确认' in main
assert '内容完整性检查' in (SKILL / 'references/pages-and-assets.md').read_text(encoding='utf-8-sig')
assert 'minimax_h3' in main
assert 'prebuild_review → implementation → verification → delivery' in main
for path in ROOT.rglob('*.md'):
    if '.git' in path.parts:
        continue
    content = path.read_text(encoding='utf-8-sig')
    assert not re.search(r'[A-Za-z]:[\\/]Users[\\/]', content), f'Personal path in {path}'
    assert 'Local developer' not in content
    for link in re.findall(r'\]\(([^)]+)\)', content):
        if re.match(r'^[a-z]+://', link) or link.startswith('#'):
            continue
        target = link.split('#', 1)[0]
        if target:
            assert (path.parent / target).exists(), f'Broken local link: {path.name}: {link}'
for name in ['README.md', 'README.zh-CN.md', 'docs/chatgpt-project.md', 'examples/prompts.md']:
    assert (ROOT / name).stat().st_size > 300, f'Empty guide: {name}'
print(f'PASS: package v{version}; four references; bilingual guides; manifests; links; no personal paths')
print('Scope: static package validation only; no model, image, video or cross-client runtime test.')
