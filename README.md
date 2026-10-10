# scientific research reading workflow-skills

**中文** · [English](README.en.md)

读论文的时候，你可能已经习惯了：Zotero 收论文，小绿鲸翻译和记笔记，遇到问题就问 ChatGPT，组会前再挑几篇做 PPT。

麻烦往往出在之后：记得自己读过，却想不起来当时记了什么、问过什么、哪次汇报用过。

这份工作流就是帮你把这些记录放到一起。你继续按原来的习惯读论文，想整理时，在 Codex 里说一句：

> 更新我的阅读笔记。

Codex 会根据能读到的资料，把笔记、讨论和汇报记录整理到你的 Obsidian 文献库里。

## 它能帮你做什么

- **把一篇论文的记录放在一起。** 小绿鲸的笔记、ChatGPT 的相关问答、PPT 的对应页面，都能回到同一份论文笔记里。
- **有笔记就能整理。** 不需要先做 PPT；是否用于汇报会另外标出来。
- **接着上次整理。** 新增了备注，或者改了原来的理解，就更新对应内容，保留你自己写的判断。
- **沿用你熟悉的分类。** 可以按 Zotero 或小绿鲸的原文件夹整理，一篇论文放在多个分类下也不用复制多份正文。
- **尽量不打断你。** 默认优先读取已登录的独立网页，不操作桌面客户端。暂时读不到的内容会列出来，方便下次补上。

适合平时会记阅读笔记、经常做组会汇报，或者想把零散论文记录慢慢整理成自己资料库的人。只想整理手头几篇论文，也可以从小范围开始。

## Codex 插件安装方式

### 从下载的文件夹安装

1. 下载并解压这个仓库。在解压后的**仓库根目录**打开终端。
2. 如果已经安装 Codex CLI，运行下面两条命令：

```sh
codex plugin marketplace add .
codex plugin add scientific-research-reading-workflow-skills@scientific-reading
```

3. 安装完成后，在 Codex 中新建一个会话，再开始使用。

这两条命令分别添加本仓库的插件来源、安装其中的插件。本仓库附带了所需的插件清单。不同版本的入口可能不同，可参考 [OpenAI 插件安装说明](https://developers.openai.com/plugins/build/plugins)。

没有 CLI 时，可以把仓库作为项目打开，在支持本地 marketplace 的桌面端插件目录中选择 **Scientific Reading**，找到本插件并安装。如果你的版本没有这个入口，可先用 [手动安装 Skill 的方法](docs/INSTALL.md)。

本项目通过这个仓库分发；发布到 GitHub 不代表已经上架官方插件目录。


## 简单办法：直接复制该网址给Codex，注意在Codex先安装对应的插件！！

## 开始前准备什么

最少需要一个能运行 Skill 的 Codex 环境，以及一个允许 Codex 写入的 Obsidian 库。其他来源按你实际使用的工具接入，不用一次全部配齐。

| 你想整理的内容 | 需要准备什么 |
|---|---|
| Zotero 里的论文和分类 | 可用的 Zotero 连接工具，或你导出的书目文件 |
| 小绿鲸笔记和备注 | 登录小绿鲸网页版，并让 Codex 有可用的网页读取工具；已有导出文件也可以用 |
| ChatGPT 里的论文讨论 | 指定相关对话，并有能读取它的工具；也可以直接提供摘录或导出 |
| 论文汇报 PPT | 告诉 Codex 文件位置；图片和公式内容需要能查看相应页面 |

安装这个插件不会自动让 Codex 获得上述账户或文件的访问权限。第一次使用时，它会先检查哪些来源能读取。

普通使用不需要你运行 Python。只有手动初始化或检查档案时，才需要 Python 3.10 及以上版本。

## 第一次怎么用

把下面这段发给 Codex，改成你自己的路径即可。不用的来源删掉就行。

```text
使用 $scientific-research-reading-workflow-skills 帮我整理阅读笔记。

我的 Obsidian 库在：【填写路径】
我主要用 Zotero 和小绿鲸读论文。
论文总结 PPT 在：【填写路径，没有就删掉这行】
这次相关的 ChatGPT 对话是：【填写对话或提供摘录】

先检查哪些资料能读取，再帮我整理。
沿用原文件夹分类，保留我自己的判断，不操作桌面客户端。
```

首次配置会保存在你自己的库里，之后不用每次重复填写。小绿鲸需要重新登录时，由你完成扫码；不用把密码或登录信息写进配置。

## 之后怎么用

可以直接说：

```text
更新我的阅读笔记。
```

也可以加上你这次想做的事：

```text
整理最近两周新读的论文，把上次没读到的笔记也检查一下。
只整理小绿鲸“我的研究方向”文件夹里的笔记。
把这段论文问答补进对应笔记，保留我原来的看法。
检查这些论文有没有用在指定 PPT 里，并标出页码。
只检查文献库结构，先不要修改内容。
```

每次整理完，Codex 会告诉你更新了哪些论文、笔记放在哪里，以及还有哪些内容没读到。

## 整理后的笔记在哪里

默认入口是 Obsidian 库里的 `Reading/INDEX.md`：

- `papers/`：一篇论文一份笔记。
- `collections/`：按原文件夹找到论文。
- `discussions/` 和 `presentations/`：相关讨论和汇报记录。
- `updates/`：每次整理的变化和待补内容。

已经有自己的笔记格式也没关系，告诉 Codex 沿用即可。更详细的字段约定放在 [档案说明](skills/scientific-research-reading-workflow-skills/references/schema.md) 中。



## 想改成自己的ai大脑

直接编辑文件就可以：

| 想改什么 | 改哪个文件 |
|---|---|
| 中文介绍、使用说明、示例 | `README.md` |
| 英文介绍和使用说明 | `README.en.md` |
| Codex 整理笔记时的做法 | `skills/scientific-research-reading-workflow-skills/SKILL.md` |
| 给新用户的默认配置示例 | `skills/scientific-research-reading-workflow-skills/assets/workflow.example.json` |
| 自己的库路径、PPT 和来源范围 | 私人库中的 `Reading/workflow.json` |



## 几点注意事项

这套流程在你发出指令后运行，不会一直在后台自动同步。小绿鲸目前的验证主要覆盖网页笔记文字和列表备注；图片、手写内容及 PDF 批注要看实际能读取到多少。

AI 整理出的解释会和你的判断分开。PPT 文字搜索没找到某篇论文时，也不会直接把它标成“没做过汇报”。没有读全的地方，会保留说明。

你的真实笔记、聊天记录、论文和 PPT 留在自己的资料库里，不要跟这个公开仓库一起上传。


[维护和检查](docs/MAINTAINING.md) · [验证记录](docs/VALIDATION.md) · [发布到 GitHub](docs/PUBLISHING.md)

## 许可

采用 [MIT License](LICENSE)。欢迎按自己的阅读习惯修改和分享。
