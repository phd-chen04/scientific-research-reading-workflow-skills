# 发布此技能包

建议仓库名：`scientific-research-reading-workflow-skills`。

建议描述：`A Codex skill for incremental literature notes across Zotero, Xiaolvjing, ChatGPT, presentations, and Obsidian.`

## 发布内容

仓库根目录应直接包含 README.md、README.en.md、LICENSE、plugin.json、.codex-plugin/、.agents/、skills/、tests/ 和 tools/。两个点开头的目录也是插件安装所需文件。只上传这个独立目录；上层工作区可能保存真实阅读来源和私人配置，不能一起上传。

本包采用 MIT，默认版权署名是项目贡献者。若希望显示个人或组织署名，可在发布前修改 LICENSE 的版权行。

## 使用 Git

把发布包解压到一个独立目录，再在该目录运行以下命令。先在自己的 GitHub 账户创建空仓库；下面 `YOUR_ACCOUNT` 是需要替换的占位符。

```sh
git init -b main
git add README.md README.en.md LICENSE plugin.json .codex-plugin .agents .gitignore .gitattributes skills tests tools docs
git diff --cached --stat
git diff --cached
git commit -m "Add literature reading workflow skill"
git remote add origin https://github.com/YOUR_ACCOUNT/scientific-research-reading-workflow-skills.git
git push -u origin main
```

如果该目录已经是 Git 仓库，应先检查现有状态和远程地址，不重复初始化或覆盖已有 remote。

## 发布前核对

```sh
python -m unittest discover -s tests -v
python tools/check_package.py
```

测试使用虚构临时文件，不连接个人账户。包检查覆盖自身简单元数据和文档链接；不是官方 skill 校验器，也不替代真实来源接入验证。

上传后，读者可以通过仓库添加插件来源：

```sh
codex plugin marketplace add YOUR_ACCOUNT/scientific-research-reading-workflow-skills
codex plugin add scientific-research-reading-workflow-skills@scientific-reading
```

`YOUR_ACCOUNT` 需换成你的真实 GitHub 用户名。这里没有预填尚不存在的仓库链接；GitHub 分发与官方插件目录上架是两回事。

真实笔记、聊天导出、浏览器认证信息、PPT、PDF、私人本地配置和状态文件均不属于公开包。`.gitignore` 只是减少误提交，提交前仍应看具体 diff。
