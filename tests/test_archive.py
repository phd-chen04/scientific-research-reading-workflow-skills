"""All fixtures are synthetic; no account, browser, or live vault access."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/scientific-research-reading-workflow-skills/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


initializer = load('init_archive')
checker = load('audit_archive')


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'research-notes'

    def start(self):
        initializer.initialize(self.root)
        return self.root / 'Reading'

    def paper(self, name='one', native=False):
        path = self.root / 'Reading/papers' / (name + '.md')
        fields = 'paper_id: "xiaolvjing:document:synthetic-id"\nzotero_key: null' if native else 'zotero_library: "synthetic-library"\nzotero_key: "EXAMPLE1"'
        path.write_text('---\n' + fields + '\n---\n# Synthetic fixture\n', encoding='utf-8')
        return path

    def state(self, value):
        (self.root / 'Reading/_state/processed.json').write_text(json.dumps(value), encoding='utf-8')

    def test_dry_run_leaves_no_files(self):
        self.assertEqual(initializer.initialize(self.root, True)['status'], 'DRY_RUN')
        self.assertFalse(self.root.exists())

    def test_initialization_and_refusal_to_overwrite(self):
        reading = self.start()
        marker = reading / 'INDEX.md'
        marker.write_text('User content', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            initializer.initialize(self.root)
        self.assertEqual(marker.read_text(), 'User content')
        self.assertEqual(checker.audit(self.root)['status'], 'PASS')

    def test_distinct_identity_routes(self):
        self.start()
        self.paper()
        self.paper('two', native=True)
        self.assertEqual(checker.audit(self.root)['unique_identities'], 2)
        self.assertEqual(checker.audit(self.root)['status'], 'PASS')

    def test_duplicate_and_missing_identity(self):
        reading = self.start()
        self.paper()
        self.paper('duplicate')
        (reading / 'papers/missing.md').write_text('# No identity', encoding='utf-8')
        kinds = {e['type'] for e in checker.audit(self.root)['errors']}
        self.assertTrue({'duplicate_identity', 'invalid_identity'} <= kinds)

    def test_hash_change_is_review_only_and_read_only(self):
        self.start()
        paper = self.paper()
        self.state({'output_sha256': {'Reading/papers/one.md': hashlib.sha256(paper.read_bytes()).hexdigest()}})
        paper.write_text(paper.read_text() + 'Human judgment', encoding='utf-8')
        before = {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = checker.audit(self.root)
        self.assertEqual(result['status'], 'REVIEW_HASH_DIFFERENCES')
        self.assertEqual(checker.exit_code(result), 2)
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})

    def test_real_links_checked_but_code_examples_ignored(self):
        reading = self.start()
        self.paper()
        (reading / 'INDEX.md').write_text('[[Reading/papers/one#Section|Alias]]\n```md\n[[fake-code]]\n```\n`[[inline]]`\n<!-- [[comment]] -->', encoding='utf-8')
        self.assertEqual(checker.audit(self.root)['wiki_targets_checked'], 1)
        self.assertEqual(checker.audit(self.root)['status'], 'PASS')
        (reading / 'INDEX.md').write_text('[[Reading/missing]]', encoding='utf-8')
        self.assertEqual(checker.audit(self.root)['status'], 'FAIL')

    def test_external_hash_path_is_rejected(self):
        self.start()
        self.state({'output_sha256': {'../private.txt': '0' * 64}})
        self.assertEqual(checker.audit(self.root)['errors'][0]['type'], 'invalid_hash_entry')

    def test_relative_sibling_link_within_vault(self):
        reading = self.start()
        paper = self.paper()
        paper.write_text(paper.read_text() + '[[../INDEX]]', encoding='utf-8')
        self.assertEqual(checker.audit(self.root)['status'], 'PASS')

    def test_bad_state_and_partial_identity_fail(self):
        reading = self.start()
        (reading / '_state/processed.json').write_text('broken', encoding='utf-8')
        (reading / 'papers/partial.md').write_text('---\nzotero_key: "EXAMPLE1"\n---\n', encoding='utf-8')
        kinds = {e['type'] for e in checker.audit(self.root)['errors']}
        self.assertTrue({'unreadable_state', 'invalid_identity'} <= kinds)

    def test_missing_root_fails(self):
        self.assertEqual(checker.audit(self.root)['status'], 'FAIL')


if __name__ == '__main__':
    unittest.main()
