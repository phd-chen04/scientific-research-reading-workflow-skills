"""Dependency-free checks for this package's deliberately simple skill metadata."""
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/scientific-research-reading-workflow-skills'


def check():
    entry = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    header = re.match(r'^---\n(.*?)\n---\n', entry, re.S)
    assert header, 'Missing skill frontmatter'
    fields = dict(line.split(': ', 1) for line in header[1].splitlines())
    assert set(fields) == {'name', 'description'}
    assert fields['name'] == SKILL.name
    description = json.loads(fields['description'])
    assert isinstance(description, str) and 0 < len(description) <= 1024
    assert '<' not in description and '>' not in description
    assert not re.search(r'^\s*\[TODO:', entry, re.M)
    metadata = (SKILL / 'agents/openai.yaml').read_text(encoding='utf-8').splitlines()
    assert metadata[0] == 'interface:'
    ui = dict((key.strip(), json.loads(value)) for key, value in (line.split(': ', 1) for line in metadata[1:] if line.strip()))
    assert 25 <= len(ui['short_description']) <= 64
    assert '$scientific-research-reading-workflow-skills' in ui['default_prompt']
    portable = json.loads((ROOT / 'plugin.json').read_text(encoding='utf-8'))
    compat = json.loads((ROOT / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
    marketplace = json.loads((ROOT / '.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
    assert portable['name'] == compat['name'] == SKILL.name
    assert portable['version'] == compat['version']
    assert portable['license'] == compat['license'] == 'MIT'
    assert compat['skills'] == './skills/'
    assert marketplace['name'] == 'scientific-reading'
    assert len(marketplace['plugins']) == 1
    plugin = marketplace['plugins'][0]
    assert plugin['name'] == SKILL.name
    assert plugin['source'] == {'source': 'local', 'path': './'}
    assert plugin['policy']['installation'] == 'AVAILABLE'
    assert plugin['policy']['authentication'] == 'ON_INSTALL'
    assert plugin['category']
    assert compat['interface']['displayName'] == ui['display_name']
    links = 0
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in target or target.startswith('#'):
                continue
            assert (path.parent / target.split('#')[0]).is_file(), (path, target)
            links += 1
    config = json.loads((SKILL / 'assets/workflow.example.json').read_text(encoding='utf-8'))
    assert config['vault_root'] is None
    assert not config['ppt_paths']
    assert not config['chatgpt']['selected_conversation_ids']
    assert all(not config[source]['enabled'] for source in ('zotero', 'xiaolvjing', 'chatgpt'))
    print(json.dumps({'status': 'PASS', 'skill': fields['name'], 'local_links': links, 'plugin_manifests': 'consistent', 'private_configuration': False, 'validator': 'Package-specific scalar metadata and manifest check; not the official skill validator.'}, indent=2))


if __name__ == '__main__':
    check()
