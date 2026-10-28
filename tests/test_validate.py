"""Disposable-copy mutation tests; do not touch the live checkout."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package_validator', ROOT / 'scripts/validate.py')
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


class PackageValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in validator.distributable_files(ROOT):
            source = ROOT / relative
            if source.is_file():
                destination = self.root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, destination)
        self.entry = self.root / validator.SKILL_PATH / 'SKILL.md'

    def codes(self):
        return {d.code for d in validator.validate_package(self.root)}

    def test_clean_copy(self):
        self.assertEqual(validator.validate_package(self.root), [])

    def test_bom(self):
        self.entry.write_bytes(b'\xef\xbb\xbf' + self.entry.read_bytes())
        self.assertIn('bom', self.codes())

    def test_manifest_mismatch(self):
        p = self.root / '.codex-plugin/plugin.json'
        data = json.loads(p.read_text(encoding='utf-8'))
        data['version'] = '9.0.0'
        p.write_text(json.dumps(data), encoding='utf-8')
        self.assertIn('version-mismatch', self.codes())

    def test_broken_link(self):
        p = self.root / 'README.md'
        p.write_text(p.read_text(encoding='utf-8') + '\n[missing](docs/missing.md)\n', encoding='utf-8')
        self.assertIn('link', self.codes())

    def test_personal_path_in_executable(self):
        p = self.root / 'scripts/validate.py'
        bad_path = 'C:' + '/' + 'Users' + '/' + 'private-user/project'
        p.write_text(p.read_text(encoding='utf-8') + '\n# ' + bad_path, encoding='utf-8')
        self.assertIn('personal-path', self.codes())

    def test_malformed_metadata(self):
        for metadata in ('---\nname: wrong\n---\n',
                         '---\nname: ultimate-frontend-designer\nmetadata: [bad]\n---\n',
                         '---\nname: "unterminated\n---\n'):
            with self.subTest(metadata=metadata):
                self.entry.write_text(metadata, encoding='utf-8')
                self.assertIn('frontmatter', self.codes())

    def test_invalid_version(self):
        original = self.entry.read_text(encoding='utf-8')
        fields, error = validator.parse_frontmatter(original)
        self.assertIsNone(error)
        version = fields['version']
        self.entry.write_text(original.replace('"' + version + '"', '"0' + version + '"', 1), encoding='utf-8')
        self.assertIn('version', self.codes())

    def test_invalid_string_scalars_and_cli(self):
        original = self.entry.read_text(encoding='utf-8')
        invalid = ('"bad" trailing"', 'abc: def', 'true', 'false', 'null',
                   '42', '2026-10-14', '"bad\\q"', "'bad' trailing'",
                   '[bad]', 'abc # comment')
        for scalar in invalid:
            with self.subTest(scalar=scalar):
                lines = original.splitlines()
                lines[2] = 'description: ' + scalar
                self.entry.write_text('\n'.join(lines), encoding='utf-8')
                diagnostics = validator.validate_package(self.root)
                self.assertIn('frontmatter', {d.code for d in diagnostics})
                self.assertNotIn(scalar, repr(diagnostics))
                result = subprocess.run(
                    [sys.executable, '-X', 'utf8', 'scripts/validate.py'],
                    cwd=self.root, capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('[frontmatter]', result.stdout)
                self.assertNotIn('Traceback', result.stdout + result.stderr)
                self.assertNotIn(scalar, result.stdout + result.stderr)

    def test_supported_string_scalars(self):
        for scalar, expected in [('plain description', 'plain description'),
                                 ('"true"', 'true'),
                                 ('"quote: \\"ok\\""', 'quote: "ok"'),
                                 ("'it''s valid'", "it's valid"),
                                 ('"\\u4e2d\\ntext"', '中\ntext')]:
            with self.subTest(scalar=scalar):
                fields, error = validator.parse_frontmatter(
                    '---\nname: ultimate-frontend-designer\ndescription: '
                    + scalar + '\nmetadata:\n  version: "4.3.0"\n---\n')
                self.assertIsNone(error)
                self.assertEqual(fields['description'], expected)

    def test_malformed_manifests(self):
        for data in ('{', '[]', 'null'):
            with self.subTest(data=data):
                (self.root / 'plugin.json').write_text(data, encoding='utf-8')
                self.assertIn('manifest', self.codes())

    def test_credential_assignments_are_redacted(self):
        secret = 'synthetic-test-value'
        for filename, prefix in [('scripts/validate.py', 'API_' + 'KEY = '),
                                 ('plugin.json', '"OPENAI_API_' + 'KEY": '),
                                 ('skills/ultimate-frontend-designer/agents/openai.yaml', 'password: ')]:
            with self.subTest(filename=filename):
                p = self.root / filename
                original = p.read_text(encoding='utf-8')
                p.write_text(original + '\n' + prefix + '"' + secret + '"', encoding='utf-8')
                diagnostics = validator.validate_package(self.root)
                self.assertIn('credential', {d.code for d in diagnostics})
                self.assertNotIn(secret, repr(diagnostics))
                p.write_text(original, encoding='utf-8')

    def test_extra_reference(self):
        (self.root / validator.SKILL_PATH / 'references/extra.md').write_text('extra', encoding='utf-8')
        self.assertIn('references', self.codes())

    def test_private_oil_pro_module_is_rejected(self):
        private = self.root / validator.SKILL_PATH / 'extensions/oil-pro/PROVENANCE.md'
        private.parent.mkdir(parents=True)
        private.write_text('private module marker', encoding='utf-8')
        self.assertIn('private-module', self.codes())

    def test_unquoted_credential_assignment(self):
        p = self.root / 'skills/ultimate-frontend-designer/agents/openai.yaml'
        secret = 'synthetic-unquoted-value'
        p.write_text(p.read_text(encoding='utf-8') + '\nAPI_' + 'KEY=' + secret, encoding='utf-8')
        diagnostics = validator.validate_package(self.root)
        self.assertIn('credential', {d.code for d in diagnostics})
        self.assertNotIn(secret, repr(diagnostics))

    def test_duplicate_metadata(self):
        self.entry.write_text(self.entry.read_text(encoding='utf-8').replace(
            'metadata:', 'metadata:\nmetadata:'), encoding='utf-8')
        self.assertIn('frontmatter', self.codes())

    def test_invalid_utf8(self):
        self.entry.write_bytes(b'\xff')
        self.assertIn('encoding', self.codes())

    def test_work_is_excluded(self):
        p = self.root / 'scripts/work/private.md'
        p.parent.mkdir()
        p.write_text('C:' + '/Users/' + 'private', encoding='utf-8')
        self.assertEqual(self.codes(), set())

    def test_optimized_cli_failure_without_traceback(self):
        self.entry.write_bytes(b'\xef\xbb\xbf' + self.entry.read_bytes())
        result = subprocess.run([sys.executable, '-O', '-X', 'utf8', 'scripts/validate.py'],
                                cwd=self.root, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('[bom]', result.stdout)
        self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
