# 维护和检查 / Maintenance and checks

README.md 和 README.en.md 是可直接编辑的源文件，不是自动生成的产物。普通文字、标题、截图、示例和链接均可自行调整；脚本不会重写它们。

Both READMEs are editable source files, not generated output. Change the text, headings, screenshots, examples, and links directly. The scripts do not rewrite them.

## 修改后检查 / Check after editing

在仓库根目录运行 / Run at the repository root:

```sh
python -m unittest discover -s tests -v
python tools/check_package.py
```

`check_package.py` 检查技能名称、元数据、插件清单和相对文件链接，不限制 README 的具体措辞或章节顺序。修改说明文字后无须修改测试。

The package check validates skill identity, metadata, manifests, and relative file links. It does not enforce README wording or section order; prose edits do not require test changes.

## 新阅读库 / New reading archive

以下脚本为可选工具。把示例路径替换为自己的路径；已有 Reading 目录时会停止，避免覆盖资料。

These helpers are optional. Replace the example path with your own. Initialization stops if Reading already exists.

```sh
python skills/scientific-research-reading-workflow-skills/scripts/init_archive.py --vault "/path/to/your/vault" --dry-run
python skills/scientific-research-reading-workflow-skills/scripts/init_archive.py --vault "/path/to/your/vault"
python skills/scientific-research-reading-workflow-skills/scripts/audit_archive.py --vault "/path/to/your/vault"
```

审计只读：退出码 0 是结构检查通过，1 是结构错误，2 是哈希差异待检查。人工修改也可能造成差异，不要因此恢复旧内容。

The audit is read-only: exit code 0 means structure checks passed, 1 means structural errors, and 2 means hash differences need review. A difference can be a human edit; do not restore old content just to make it disappear.

## 重新打包 / Rebuild the ZIP

```sh
python tools/package_release.py --output "../scientific-research-reading-workflow-skills-v0.2.0.zip"
```

打包工具会先检查包结构，只收录公开文件清单中的文件；如果增加了新文档，请更新 `tools/package_release.py` 的清单。目标 ZIP 已存在时会停止。不会覆盖 README，也不会包含真实 Reading/、Memory/ 或 Python 缓存。

The packager checks the package first and includes only its explicit public file list. Add new documents to that list in `tools/package_release.py`. It stops if the target ZIP exists. It does not overwrite either README or include real Reading/, Memory/, or Python caches.
