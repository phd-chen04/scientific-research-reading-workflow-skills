"""Build a public ZIP from an explicit file list. Never rewrite the README files."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
from check_package import check

ROOT = Path(__file__).resolve().parents[1]
SLUG = 'scientific-research-reading-workflow-skills'
SKILL = 'skills/' + SLUG
PUBLIC_FILES = [
    '.gitattributes', '.gitignore', 'LICENSE', 'README.md', 'README.en.md', 'plugin.json',
    '.codex-plugin/plugin.json', '.agents/plugins/marketplace.json',
    'docs/INSTALL.md', 'docs/MAINTAINING.md', 'docs/PUBLISHING.md', 'docs/VALIDATION.md',
    SKILL + '/SKILL.md', SKILL + '/agents/openai.yaml', SKILL + '/assets/workflow.example.json',
    SKILL + '/references/schema.md', SKILL + '/references/xiaolvjing-web.md',
    SKILL + '/scripts/audit_archive.py', SKILL + '/scripts/init_archive.py',
    'tests/test_archive.py', 'tools/check_package.py', 'tools/package_release.py',
]


def package(output):
    output = Path(output).expanduser().resolve()
    checksum = output.with_suffix(output.suffix + '.sha256')
    if output.exists() or checksum.exists():
        raise FileExistsError('Release or checksum already exists; choose a new output name.')
    check()
    for relative in PUBLIC_FILES:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink() or not path.resolve().is_relative_to(ROOT):
            raise ValueError('Missing or unsafe public file: ' + relative)
    with zipfile.ZipFile(output, 'x', zipfile.ZIP_DEFLATED) as archive:
        for relative in PUBLIC_FILES:
            archive.write(ROOT / relative, SLUG + '/' + relative)
    with zipfile.ZipFile(output) as archive:
        if archive.testzip() is not None:
            raise ValueError('ZIP integrity check failed')
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    with checksum.open('x', encoding='utf-8') as stream:
        stream.write(digest + '  ' + output.name + '\n')
    return {'status': 'PASS', 'archive': str(output), 'files': len(PUBLIC_FILES), 'bytes': output.stat().st_size, 'sha256': digest}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(package(args.output), ensure_ascii=False, indent=2))
    except (OSError, ValueError, AssertionError) as exc:
        parser.exit(1, str(exc) + '\n')
