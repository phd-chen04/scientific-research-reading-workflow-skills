"""Read-only audit of the documented archive format; not a synchronizer or fact check."""
import argparse
import hashlib
import json
import re
from pathlib import Path, PureWindowsPath


def identity_fields(text):
    match = re.match(r'\A\ufeff?---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
    if not match:
        raise ValueError('Missing frontmatter')
    result = {}
    for line in match[1].splitlines():
        item = re.match(r'^(paper_id|zotero_key|zotero_library):[ \t]*(.*)$', line)
        if not item:
            continue
        key, raw = item.groups()
        if key in result:
            raise ValueError('Repeated identity field: ' + key)
        if raw in ('null', '~', ''):
            value = None
        elif raw.startswith('"'):
            value = json.loads(raw)
        elif raw[0] in "'|>!&*[{" or ' #' in raw:
            raise ValueError('Use a single-line JSON-quoted identity value: ' + key)
        else:
            value = raw.strip()
        if value is not None and not isinstance(value, str):
            raise ValueError('Identity must be a string or null')
        result[key] = value
    return result


def link_text(text):
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
        if marker:
            current = marker[1]
            if fence is None:
                fence = current
            elif current[0] == fence[0] and len(current) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return re.sub(r'(`+).*?\1', '', '\n'.join(lines))


def inside(path, root):
    try:
        path.resolve().relative_to(root)
        return True
    except ValueError:
        return False


def local_path(root, value, boundary=None):
    if not isinstance(value, str) or Path(value).is_absolute() or PureWindowsPath(value).drive:
        return None
    path = root / value.replace('\\', '/')
    return path if inside(path, boundary or root) else None


def audit(vault):
    root = Path(vault).expanduser().resolve()
    reading = root / 'Reading'
    errors, differences, identities = [], [], {}
    paper_count = links = 0
    if not reading.is_dir() or not inside(reading, root) or reading.is_symlink():
        return {'status': 'FAIL', 'errors': [{'type': 'missing_or_unsafe_reading_directory'}], 'hash_differences': [], 'paper_count': 0}
    for path in reading.rglob('*.md'):
        if '_backups' in path.relative_to(reading).parts:
            continue
        if path.is_symlink() or any(p.is_symlink() for p in path.parents if p.is_relative_to(root)) or not inside(path, root):
            errors.append({'type': 'symlink_skipped', 'path': str(path)})
            continue
        try:
            text = path.read_text(encoding='utf-8-sig')
        except (OSError, UnicodeError) as exc:
            errors.append({'type': 'unreadable_markdown', 'path': str(path), 'message': str(exc)})
            continue
        if path.is_relative_to(reading / 'papers'):
            paper_count += 1
            try:
                fields = identity_fields(text)
                library, key = fields.get('zotero_library'), fields.get('zotero_key')
                if bool(library) != bool(key):
                    raise ValueError('Both Zotero library and parent key are required together')
                identity = ('zotero', library, key) if library and key else ('native', fields.get('paper_id'))
                if not identity[-1]:
                    raise ValueError('Missing paper identity')
                if identity in identities:
                    errors.append({'type': 'duplicate_identity', 'paths': [identities[identity], str(path)]})
                else:
                    identities[identity] = str(path)
            except (ValueError, TypeError) as exc:
                errors.append({'type': 'invalid_identity', 'path': str(path), 'message': str(exc)})
        for raw in re.findall(r'\[\[([^\]\n]+)\]\]', link_text(text)):
            target = raw.split('|', 1)[0].split('#', 1)[0]
            if not target:
                continue
            links += 1
            candidates = []
            for base in (root, path.parent):
                for suffix in ('', '.md'):
                    item = local_path(base, target + suffix, root)
                    if item is not None and inside(item, root):
                        candidates.append(item)
            if not any(p.is_file() for p in candidates):
                errors.append({'type': 'unresolved_wikilink', 'path': str(path), 'target': target})
    state = {}
    try:
        state_path = reading / '_state/processed.json'
        if not inside(state_path, root):
            raise ValueError('State resolves outside vault')
        state = json.loads(state_path.read_text(encoding='utf-8-sig'))
        if not isinstance(state, dict) or not isinstance(state.get('output_sha256', {}), dict) or not isinstance(state.get('pending', []), list):
            raise ValueError('State must contain an object of hashes and a pending list')
        for relative, expected in state.get('output_sha256', {}).items():
            path = local_path(root, relative)
            if path is None or not isinstance(expected, str) or not re.fullmatch(r'[a-fA-F0-9]{64}', expected):
                errors.append({'type': 'invalid_hash_entry', 'path': relative})
            elif not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected.lower():
                differences.append(relative)
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        errors.append({'type': 'unreadable_state', 'message': str(exc)})
        state = {}
    return {'status': 'FAIL' if errors else 'REVIEW_HASH_DIFFERENCES' if differences else 'PASS',
            'paper_count': paper_count, 'unique_identities': len(identities), 'wiki_targets_checked': links,
            'errors': errors, 'hash_differences': differences, 'pending_count': len(state.get('pending', [])),
            'scope': 'Structure only. No content verification, no synchronization, no automatic repair.'}


def exit_code(result):
    return {'PASS': 0, 'FAIL': 1, 'REVIEW_HASH_DIFFERENCES': 2}[result['status']]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vault', required=True)
    args = parser.parse_args()
    result = audit(args.vault)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code(result))
