"""Offline deterministic package checks; Python 3.10+, stdlib only."""
from __future__ import annotations

import codecs
from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote, urlsplit

NAME = 'ultimate-frontend-designer'
SKILL_PATH = Path('skills') / NAME
REFERENCES = {'design-foundation.md', 'pages-and-assets.md',
              'motion-and-video.md', 'prompts-and-state.md'}
MANIFESTS = ('plugin.json', '.codex-plugin/plugin.json')
# Explicit additions are included even before the parent stages them.
DECLARED = ('docs/design-skill-sources.md', 'tests/test_validate.py')
REQUIRED = ('README.md', 'README.zh-CN.md', 'CHANGELOG.md',
            'docs/chatgpt-project.md', 'examples/prompts.md', 'scripts/validate.py',
            'assets/ultimate-designer-logo.svg',
            str(SKILL_PATH / 'agents/openai.yaml'), *MANIFESTS, *DECLARED)
TEXT_SUFFIXES = {'.md', '.py', '.yaml', '.yml', '.json', '.svg', '.txt',
                 '.toml', '.ini', '.cfg', '.js', '.ts', '.sh', '.ps1'}
EXCLUDED = {'.git', 'work', '__pycache__', '.pytest_cache', '.mypy_cache',
            'node_modules', 'dist', '.cache'}
SEMVER = re.compile(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)'
                    r'(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)'
                    r'(?:\.(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?'
                    r'(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?')
PERSONAL_PATH = re.compile(r'[A-Za-z]:[\\/]Users[\\/]', re.IGNORECASE)
CREDENTIAL = re.compile(
    r'''(?im)(?:["']?(?:[A-Za-z_][\w]*[._:-])?'''
    r'''(?:api[_-]?key|access[_-]?token|secret[_-]?key|password|client[_-]?secret)'''
    r'''["']?\s*[:=]\s*)(["'])([^\r\n"']+)\1''')
UNQUOTED_CREDENTIAL = re.compile(
    r'(?im)^\s*(?:\$env:)?(?:[A-Za-z_][\w]*[_-])?'
    r'(?:api[_-]?key|access[_-]?token|secret[_-]?key|password|client[_-]?secret)'
    r'\s*[:=]\s*([A-Za-z0-9][A-Za-z0-9_./+-]{7,})\s*(?:#.*)?$')
SAFE_VALUES = {'pending', 'null', 'none', 'redacted', 'example', 'placeholder',
               'your_api_key', 'your-api-key'}


@dataclass(frozen=True)
class Diagnostic:
    path: str
    code: str
    message: str


def distributable_files(root: Path) -> list[Path]:
    """Use this checkout's index or bounded dirs in unpacked package copies."""
    names: set[str] = {Path(n).as_posix() for n in REQUIRED}
    names.add((SKILL_PATH / 'SKILL.md').as_posix())
    names.update((SKILL_PATH / 'references' / n).as_posix() for n in REFERENCES)
    if (root / '.git').exists():
        result = subprocess.run(['git', 'ls-files', '-z'], cwd=root,
                                capture_output=True, check=False)
        if result.returncode:
            raise ValueError('Cannot enumerate tracked text')
        names.update(result.stdout.decode('utf-8').split('\0'))
    else:
        for directory in ('skills', 'scripts', 'tests', 'docs', 'examples',
                          'assets', '.codex-plugin'):
            names.update(p.relative_to(root).as_posix()
                         for p in (root / directory).rglob('*') if p.is_file())
    return [Path(n) for n in sorted(names) if n and not Path(n).is_absolute()
            and '..' not in Path(n).parts
            and not any(part in EXCLUDED for part in Path(n).parts)
            and Path(n).suffix.lower() in TEXT_SUFFIXES]


def parse_string_scalar(value: str) -> str | None:
    """Single-line subset: JSON double quotes, YAML doubled single quotes,
    or conservative plain strings. Comments and implicit YAML types are rejected.
    Return no source text in diagnostics.
    """
    if value.startswith('"'):
        try:
            decoded = json.loads(value)
        except (ValueError, TypeError):
            return None
        return decoded if isinstance(decoded, str) else None
    if value.startswith("'"):
        if not re.fullmatch(r"'(?:[^']|'')*'", value):
            return None
        return value[1:-1].replace("''", "'")
    if (not value or value != value.strip()
            or value[0] in '-?:,[]{}#&*!|>\'"%@`'
            or re.search(r':(?:\s|$)|\s#|[\[\]{}]', value)):
        return None
    # Reject YAML 1.1/1.2 implicit booleans, nulls, numbers and timestamps.
    if (value.lower() in {'true', 'false', 'yes', 'no', 'on', 'off', 'null', '~'}
            or re.match(r'^[+-]?(?:\d|\.\d|\.inf\b|\.nan\b)', value, re.I)):
        return None
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    """Validate this package's bounded scalar YAML subset, not arbitrary YAML."""
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        return {}, 'Missing opening frontmatter delimiter'
    try:
        end = lines.index('---', 1)
    except ValueError:
        return {}, 'Missing closing frontmatter delimiter'
    fields: dict[str, str] = {}
    in_metadata = False
    seen_metadata = False
    for line in lines[1:end]:
        if not line.strip():
            continue
        if line == 'metadata:':
            if seen_metadata:
                return {}, 'Duplicate metadata mapping'
            in_metadata = seen_metadata = True
            continue
        match = re.fullmatch(r'(  )?([a-z][a-z-]*):\s+(.+)', line)
        if not match:
            return {}, 'Unsupported or malformed frontmatter field'
        indent, key, value = match.groups()
        if indent:
            if not in_metadata or key != 'version':
                return {}, 'Unsupported metadata field or indentation'
        else:
            in_metadata = False
            if key not in {'name', 'description'}:
                return {}, 'Unsupported top-level frontmatter field'
        if key in fields:
            return {}, 'Duplicate frontmatter field'
        value = parse_string_scalar(value)
        if value is None:
            return {}, 'Malformed or non-string frontmatter scalar'
        if not value or len(value) > (1024 if key == 'description' else 128):
            return {}, 'Empty or oversized frontmatter value'
        if value.startswith(('[', '{', '&', '*', '!', '|', '>')):
            return {}, 'Frontmatter requires scalar values'
        fields[key] = value
    if set(fields) != {'name', 'description', 'version'}:
        return {}, 'Required name, description or metadata.version missing'
    return fields, None


def local_markdown_targets(text: str) -> list[str]:
    text = re.sub(r'(?ms)^\s*(`{3,}|~{3,})[^\n]*\n.*?^\s*\1\s*$', '', text)
    text = re.sub(r'`[^`\n]*`', '', text)
    targets = re.findall(r'!?\[[^\]\n]*\]\(\s*(<[^>]+>|[^\s)]+)', text)
    targets += re.findall(r'(?m)^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)', text)
    targets += re.findall(r'<(?:img|a)\b[^>]*(?:src|href)=["\']([^"\']+)', text)
    return [target.strip('<>') for target in targets]


def validate_package(root: Path) -> list[Diagnostic]:
    root = root.resolve()
    diagnostics: list[Diagnostic] = []

    def add(path: Path | str, code: str, message: str) -> None:
        diagnostics.append(Diagnostic(str(path).replace('\\', '/'), code, message))

    try:
        files = distributable_files(root)
    except (OSError, ValueError, UnicodeError):
        add('.', 'inventory', 'Cannot enumerate tracked distributable text')
        return diagnostics
    contents: dict[str, str] = {}
    for relative in files:
        p = root / relative
        if not p.is_file():
            add(relative, 'missing', 'Required or tracked file missing')
            continue
        if p.is_symlink() or not p.resolve().is_relative_to(root):
            add(relative, 'boundary', 'Distributable file leaves package boundary')
            continue
        try:
            raw = p.read_bytes()
            if relative == SKILL_PATH / 'SKILL.md' and raw.startswith(codecs.BOM_UTF8):
                add(relative, 'bom', 'Entrypoint must not contain UTF-8 BOM')
            text = raw.decode('utf-8')
        except (OSError, UnicodeError):
            add(relative, 'encoding', 'File unreadable or not strict UTF-8')
            continue
        contents[relative.as_posix()] = text
        if PERSONAL_PATH.search(text):
            add(relative, 'personal-path', 'Personal Windows path in distributable text')
        for match in CREDENTIAL.finditer(text):
            value = match.group(2)
            if value.lower() not in SAFE_VALUES and not value.startswith(('$', '<')):
                add(relative, 'credential', 'Literal credential assignment; value withheld')
                break
        else:
            if any(m.group(1).lower() not in SAFE_VALUES
                   for m in UNQUOTED_CREDENTIAL.finditer(text)):
                add(relative, 'credential', 'Literal credential assignment; value withheld')
        if relative.suffix.lower() == '.md':
            for target in local_markdown_targets(text):
                try:
                    parsed = urlsplit(target)
                    if parsed.scheme or parsed.netloc or target.startswith('#'):
                        continue
                    link = unquote(parsed.path)
                    if not link:
                        continue
                    destination = (p.parent / link).resolve()
                    if not destination.is_relative_to(root) or not destination.exists():
                        add(relative, 'link', 'Local target missing or outside package')
                except (ValueError, OSError):
                    add(relative, 'link', 'Malformed local Markdown target')

    entry = (SKILL_PATH / 'SKILL.md').as_posix()
    fields, error = parse_frontmatter(contents.get(entry, ''))
    if error:
        add(entry, 'frontmatter', error)
    else:
        if fields['name'] != NAME:
            add(entry, 'name', 'Entrypoint name differs from package identity')
        if not SEMVER.fullmatch(fields['version']):
            add(entry, 'version', 'Entrypoint version is not semantic versioning')
    for name in MANIFESTS:
        try:
            manifest = json.loads(contents.get(name, ''))
            if not isinstance(manifest, dict):
                raise ValueError('Not an object')
        except (ValueError, TypeError):
            add(name, 'manifest', 'Malformed JSON manifest or non-object root')
            continue
        if manifest.get('name') != NAME:
            add(name, 'name', 'Manifest name differs from package identity')
        version = manifest.get('version')
        if not isinstance(version, str) or not SEMVER.fullmatch(version):
            add(name, 'version', 'Manifest version is not semantic versioning')
        elif fields and version != fields['version']:
            add(name, 'version-mismatch', 'Manifest and entrypoint versions differ')
    refs = root / SKILL_PATH / 'references'
    try:
        actual = {p.name for p in refs.iterdir()} if refs.is_dir() else set()
    except OSError:
        actual = set()
    if actual != REFERENCES or any(not (refs / n).is_file() for n in REFERENCES):
        add(SKILL_PATH / 'references', 'references', 'Expected exactly four named chapters')
    return sorted(diagnostics, key=lambda d: (d.path, d.code, d.message))


def main() -> int:
    diagnostics = validate_package(Path(__file__).resolve().parents[1])
    for d in diagnostics:
        print(f'FAIL [{d.code}] {d.path}: {d.message}')
    if diagnostics:
        return 1
    print('PASS: metadata, four references, manifests, links and text hygiene')
    print('Scope: static package integrity only; no generation, runtime, installation or publication test.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
