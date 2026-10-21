#!/usr/bin/env python3
"""Content-bound review records. Integrity checks are not behavioral proof."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile

STATUSES = {'pass', 'fail', 'unknown', 'unavailable', 'not_applicable'}
SCOPES = {
    'component': ['visual', 'interaction', 'responsive', 'keyboard', 'reduced-motion'],
    'renovation': ['visual', 'interaction', 'responsive', 'keyboard', 'reduced-motion', 'preserved-behavior', 'project-checks'],
    'full-site': ['design-gate', 'visual', 'interaction', 'responsive', 'keyboard', 'reduced-motion', 'project-checks', 'asset-provenance'],
    'review': ['visual', 'task-walkthrough', 'responsive'],
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def read(path: Path) -> dict:
    value = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_object)
    if not isinstance(value, dict):
        raise ValueError('Report root must be an object')
    return value


def write(path: Path, value: dict, *, new: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_symlink():
        raise ValueError('Refusing symlink report')
    if new:
        with path.open('x', encoding='utf-8', newline='\n') as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write('\n')
        return
    descriptor, temporary = tempfile.mkstemp(prefix='.review-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write('\n')
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def evidence(root: Path, path: Path) -> dict:
    root = root.resolve()
    candidate = path if path.is_absolute() else root / path
    resolved = candidate.resolve(strict=True)
    if not resolved.is_relative_to(root) or not resolved.is_file():
        raise ValueError('Evidence must be a file inside the report directory')
    current = candidate.absolute()
    while current != root and current != current.parent:
        if current.is_symlink():
            raise ValueError('Symlink evidence is unsupported')
        current = current.parent
    return {'path': resolved.relative_to(root).as_posix(),
            'sha256': hashlib.sha256(resolved.read_bytes()).hexdigest()}


def check_evidence(root: Path, rows: object, location: str) -> list[str]:
    if not isinstance(rows, list) or not rows:
        return [f'{location}: missing evidence']
    errors = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('path'), str):
            errors.append(f'{location}: malformed evidence reference')
            continue
        try:
            if evidence(root, Path(row['path']))['sha256'] != row.get('sha256'):
                errors.append(f'{location}: evidence changed: {row["path"]}')
        except (OSError, ValueError):
            errors.append(f'{location}: missing or out-of-scope evidence')
    return errors


def validate(data: dict, root: Path) -> list[str]:
    errors = []
    scope = data.get('scope')
    if (type(data.get('schemaVersion')) is not int or data['schemaVersion'] != 1
            or not isinstance(scope, str) or scope not in SCOPES):
        return ['Unsupported schemaVersion or scope']
    revision = data.get('revision')
    if not isinstance(revision, str) or not revision.strip():
        errors.append('Report requires a concrete artifact revision identity')
    checks = data.get('checks')
    findings = data.get('findings')
    if not isinstance(checks, list) or not isinstance(findings, list):
        return ['checks and findings must be arrays']
    seen = set()
    for row in checks:
        if not isinstance(row, dict) or not isinstance(row.get('id'), str):
            errors.append('Malformed check')
            continue
        name = row['id']
        if not name or name in seen:
            errors.append('Missing or duplicate check id')
        seen.add(name)
        required = row.get('required')
        if type(required) is not bool:
            errors.append(f'{name}: required must be boolean')
        if name in SCOPES[scope] and required is not True:
            errors.append(f'{name}: core scope check cannot become optional')
        status = row.get('status')
        if not isinstance(status, str) or status not in STATUSES:
            errors.append(f'{name}: invalid status')
            continue
        note = row.get('note')
        if status in {'pass', 'not_applicable'} and (not isinstance(note, str) or not note.strip()):
            errors.append(f'{name}: result needs a scope note')
        if required is True and status not in {'pass', 'not_applicable'}:
            errors.append(f'{name}: required result is {status}')
        if status == 'not_applicable':
            if name in {'visual', 'design-gate'}:
                errors.append(f'{name}: always applicable for this scope')
            if not isinstance(row.get('scope_basis'), str) or not row['scope_basis'].strip():
                errors.append(f'{name}: exclusion requires an explicit scope basis')
        retained = row.get('evidence')
        if status == 'pass' or retained:
            errors.extend(check_evidence(root, retained, name))
        if status == 'pass':
            errors.extend(check_context(row.get('context'), revision, name))
    for missing in sorted(set(SCOPES[scope]) - seen):
        errors.append(f'Missing scope check: {missing}')
    finding_ids = set()
    for row in findings:
        if not isinstance(row, dict):
            errors.append('Malformed finding')
            continue
        name = row.get('id')
        if not isinstance(name, str) or not name or name in finding_ids:
            errors.append('Missing or duplicate finding id')
            continue
        finding_ids.add(name)
        if type(row.get('blocking')) is not bool or row.get('status') not in {'open', 'resolved'}:
            errors.append(f'{name}: invalid finding state')
        if not isinstance(row.get('description'), str) or not row['description'].strip():
            errors.append(f'{name}: missing finding description')
        retained_recheck = row.get('recheck_evidence')
        if retained_recheck:
            errors.extend(check_evidence(root, retained_recheck, name))
        if row.get('blocking') is True:
            if row.get('status') != 'resolved':
                errors.append(f'{name}: unresolved blocking finding')
            else:
                if not isinstance(row.get('repair'), str) or not row['repair'].strip():
                    errors.append(f'{name}: missing repair')
                if not retained_recheck:
                    errors.extend(check_evidence(root, retained_recheck, name))
                errors.extend(check_context(row.get('recheck_context'), revision, name))
    return errors


def check_context(context, revision, name):
    if not isinstance(context, dict):
        return [f'{name}: missing execution context']
    errors = []
    for field in ['target', 'method', 'state', 'expected', 'actual']:
        if not isinstance(context.get(field), str) or not context[field].strip():
            errors.append(f'{name}: context requires {field}')
    if context.get('revision') != revision:
        errors.append(f'{name}: execution context revision differs from report')
    if name in {'visual', 'responsive'}:
        if not isinstance(context.get('viewport'), str) or not context['viewport'].strip():
            errors.append(f'{name}: requires observed viewport')
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    init = commands.add_parser('init')
    init.add_argument('--scope', choices=sorted(SCOPES), required=True)
    init.add_argument('--out', type=Path, required=True)
    init.add_argument('--revision', required=True)
    record = commands.add_parser('record')
    record.add_argument('--report', type=Path, required=True)
    record.add_argument('--check', required=True)
    record.add_argument('--status', choices=sorted(STATUSES), required=True)
    record.add_argument('--evidence', type=Path, nargs='*', default=[])
    record.add_argument('--note', required=True)
    record.add_argument('--scope-basis')
    for field in ['target', 'method', 'state', 'viewport', 'expected', 'actual']:
        record.add_argument('--' + field)
    check = commands.add_parser('check')
    check.add_argument('--report', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'init':
            if not args.revision.strip():
                raise ValueError('Revision identity cannot be empty')
            write(args.out, {'schemaVersion': 1, 'scope': args.scope, 'revision': args.revision,
                  'checks': [{'id': name, 'required': True, 'status': 'unknown',
                              'evidence': [], 'note': ''} for name in SCOPES[args.scope]],
                  'findings': [], 'limitations': ['Records do not independently prove execution.']}, new=True)
            print('Created UNKNOWN checks; no acceptance implied.')
            return 0
        if args.report.is_symlink():
            raise ValueError('Symlink report is unsupported')
        data = read(args.report)
        if args.command == 'record':
            rows = [row for row in data['checks'] if row['id'] == args.check]
            if len(rows) != 1:
                raise ValueError('Check id missing or duplicated')
            if args.status == 'pass' and not args.evidence:
                raise ValueError('PASS requires real evidence files')
            if not args.note.strip():
                raise ValueError('A scope note is required')
            context = {field: getattr(args, field) for field in ['target', 'method', 'state', 'viewport', 'expected', 'actual']}
            context['revision'] = data.get('revision')
            if args.status == 'pass':
                context_errors = check_context(context, data.get('revision'), args.check)
                if context_errors:
                    raise ValueError('; '.join(context_errors))
            if args.status == 'not_applicable' and (args.check in {'visual', 'design-gate'} or not args.scope_basis):
                raise ValueError('Exclusion needs scope basis; visual and design-gate cannot be excluded')
            bound = [evidence(args.report.parent, p) for p in args.evidence]
            rows[0].update(status=args.status, evidence=bound, note=args.note,
                           scope_basis=args.scope_basis, context=context)
            write(args.report, data)
            print('Recorded declared result and evidence hashes; not independent verification.')
            return 0
        errors = validate(data, args.report.parent)
        for error in errors:
            print('FAIL:', error)
        if errors:
            return 1
        excluded = sum(row['status'] == 'not_applicable' for row in data['checks'])
        print(f'VALID: record integrity; {len(data["checks"]) - excluded} declared applicable results, {excluded} exclusions.')
        print('Scope-qualified declarations only. Actual execution and justified exclusions still require human/agent review.')
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
