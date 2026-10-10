# 手动安装 Skill / Manual skill installation

只想加载工作流、暂时不用插件市场时，可单独安装 Skill。插件和 Skill 两种方式选一种即可，避免重复加载同一流程。

You can install the skill on its own if you do not want to use a plugin marketplace. Choose one installation method to avoid loading two copies.

在仓库根目录运行 / Run at the repository root:

```sh
python -c "import os,pathlib,shutil; base=pathlib.Path(os.environ.get('CODEX_HOME') or pathlib.Path.home()/'.codex'); shutil.copytree('skills/scientific-research-reading-workflow-skills',base/'skills'/'scientific-research-reading-workflow-skills')"
```

命令使用 `CODEX_HOME/skills`，未设置时用 `~/.codex/skills`。已有同名目录会停止，不覆盖旧版本。安装后重新加载技能或开启新会话。这个兼容目录在本包的测试环境中可用；若你的客户端采用其他技能目录，请按该客户端的设置安装。

The command uses `CODEX_HOME/skills`, or `~/.codex/skills` when unset. It stops if the destination exists. Reload skills or start a new chat afterward. This compatibility location is available in the tested environment; follow your client's settings if it uses a different skill location.

提示 / Prompt:

```text
使用 $scientific-research-reading-workflow-skills 更新我的阅读笔记。
Use $scientific-research-reading-workflow-skills to update my reading notes.
```

缺少 Python 时，也可以手动把完整技能文件夹复制到相应目录，保留其中的 references、assets、scripts 和 agents 子目录。

Without Python, copy the entire skill folder manually, keeping its references, assets, scripts, and agents directories.
