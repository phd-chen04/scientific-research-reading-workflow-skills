"""Create a new Reading directory explicitly selected by the user. Standard library only."""
import argparse
import json
from pathlib import Path


def initialize(vault, dry_run=False):
    root = Path(vault).expanduser().resolve()
    reading = root / 'Reading'
    if reading.exists() or reading.is_symlink():
        raise FileExistsError('Reading already exists; keep its configuration and state.')
    config = json.loads((Path(__file__).resolve().parents[1] / 'assets/workflow.example.json').read_text(encoding='utf-8'))
    config['vault_root'] = root.as_posix()
    state = {'schema_version': 1, 'source_status': {}, 'processed_sources': {}, 'pending': [], 'output_sha256': {}}
    files = {
        'workflow.json': json.dumps(config, ensure_ascii=False, indent=2) + '\n',
        '_state/processed.json': json.dumps(state, ensure_ascii=False, indent=2) + '\n',
        'INDEX.md': '# 阅读档案\n\n尚未导入来源。先配置 workflow.json，再使用“更新我的阅读笔记”。\n'
    }
    if not dry_run:
        root.mkdir(parents=True, exist_ok=True)
        reading.mkdir()  # Refuses a concurrent initialization rather than overwriting it.
        for name in ('papers', 'collections', 'topics', 'sources', 'discussions', 'presentations', 'updates', '_state', '_backups'):
            (reading / name).mkdir()
        for name, content in files.items():
            with (reading / name).open('x', encoding='utf-8', newline='\n') as stream:
                stream.write(content)
    return {'status': 'DRY_RUN' if dry_run else 'CREATED', 'vault': str(root), 'files': list(files), 'sources_read': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', required=True)
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps(initialize(args.vault, args.dry_run), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as exc:
        parser.exit(1, f'Initialization stopped: {exc}\nExisting files are not overwritten; review any partial new directory before retrying.\n')
