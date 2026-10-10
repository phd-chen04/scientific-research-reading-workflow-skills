# 档案约定

这是新库的最小约定；已有库先映射字段，不强制迁移。数据存入用户自己的 vault，公开仓库只保存流程、模板和虚构测试。

## 论文身份

一篇论文一份主档案，标题变化不改变身份。优先使用 `zotero_library`＋父条目 `zotero_key`，附件 key 不替代论文 key。DOI 辅助匹配，同 DOI 多版本/重复条目保留歧义，不自动合并。

未匹配 Zotero 但有明确论文归属时，可使用 `paper_id: "xiaolvjing:document:<documentId>"` 并把 Zotero 字段设为 null。后来匹配成功，保留旧来源 ID 和文件链接，先检查是否已有主档案。仅状态片段或归属不明的文字先存来源及待处理项。

以下为虚构结构示例，不能直接作为真实论文发布：

```yaml
---
type: paper
title: "示例论文（虚构）"
paper_id: "zotero:example-library:EXAMPLE1"
zotero_library: "example-library"
zotero_key: "EXAMPLE1"
doi: null
reading_status: activity_recorded
verification_status: unchecked
has_presentation: null
---
```

审计脚本只解析身份字段的单行字符串/null：字符串建议 JSON 双引号格式，也接受简单不带引号的值。它不是完整 YAML 解析器；身份字段使用多行、标签、锚点或复杂 YAML 时报告格式问题，不静默猜测。

## 正文与状态

按现有格式保留资料入口、阅读理由、整理草稿、用户判断、问答与核验、汇报应用及理解变化。没有材料的区块不补造。

- 来源定位：实际文件/来源 ID、采集时间、章节/页码/回合；PDF 页序号与印刷页码分开。
- `activity_recorded` 仅表示存在实质活动；明确读完可记 `read_confirmed_by_user`。访问、收藏、空模板和百分比不推断深度。
- `has_presentation` 为 true/false/null，正文记录检查范围与页码；只做文字检索未命中保持 null。
- 摘录、AI 解释、译文和用户判断分别标识；AI 回答默认待核，局部核验不升级为整篇论文已核验。
- 更新时间是编辑时间，不替代未知阅读时间；不把整理结果自动写成科研项目进展。

## 分类

在 `Reading/collections/` 保存原软件文件夹映射。Zotero 使用集合 key＋完整路径；小绿鲸保存原生显示名及实际核实层级。文件名可安全转义，但属性保留原名。两来源不自动视为相同分类。

多个分类只链接同一论文。研究问题可另外放在 `Reading/topics/`；未归类明确标识，不凭标题擅自归类。

## 来源处理状态

`Reading/_state/processed.json`：

```json
{
  "schema_version": 1,
  "source_status": {},
  "processed_sources": {},
  "pending": [],
  "output_sha256": {}
}
```

每条已处理来源记录稳定 `source_id`、实际定位、内容哈希/可靠版本、规范化策略、`paper_ids`、输出路径、已读范围及成功处理时间。记录时间和读完时间分开。

同来源新版先比较正文，修正保留原因。跨论文讨论/PPT 保留一份共享记录。相同哈希不跳过此前未读部分；未配置、失效登录和读取失败不刷新成功游标。仅成功验证的部分进入处理记录，其余仍 pending。

`output_sha256` 是以 vault 为根的相对文件路径到 SHA-256 的映射，仅跟踪生成结果；不把 state 文件自身纳入。先保留人工编辑、完成内容核对，再更新预期哈希。

## 写入与检查

改写前备份、检查并发变化，再原子替换；没有整批原子事务时，记录部分成功和可恢复位置。验证后更新状态，不用历史发布脚本覆盖当前库。

审计脚本扫描 `Reading/papers/**/*.md` 和 `Reading/` 内 Markdown，跳过 `_backups/` 与符号链接。链接使用 vault 相对或当前文件相对路径，如 `[[Reading/papers/example]]`，可带别名/标题锚点；脚本检查文件存在，不检查锚点。

脚本忽略代码块、行内代码、HTML 注释中的链接，不实现 Obsidian 全局短文件名搜索。采用此类语法的旧库可另做映射核验，不能把脚本限制解释为源文件损坏。结构检查不能核验内容真实性。
