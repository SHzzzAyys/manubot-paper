# 科研写作工具链说明

本仓库除 Manubot 主文稿外，还包含一个可复用的小型科研写作工具链，主要由三部分构成：

## 1. 文稿主线

- `content/`
  Manubot 主文稿与补充材料说明。
- `content/06.core-table.md`
  核心比较表。
- `content/09.study-matrix.md`
  逐篇研究矩阵。
- `content/10.supplementary-notes.md`
  补充材料表注与缩略词说明。

## 2. 结构化证据库

- `data/cat_toxo_vaccine_direct_studies.csv`
- `data/cat_toxo_vaccine_support_studies.csv`
- `data/cat_toxo_vaccine_reviews.csv`
- `docs/evidence-data-dictionary.md`

这部分数据用于沉淀单篇研究的结构化信息，便于后续写作、扩展综述或迁移到数据库工具中。

## 3. 自动化脚本

- `scripts/export_evidence_tables.py`
  从 `data/` 目录中的 CSV 生成 `docs/generated/` 下的 markdown 表格。
- `scripts/validate_manuscript.py`
  做轻量级校验，目前会检查：
  - `metadata.yaml` 是否缺标题和作者
  - 作者单位是否仍为占位符
  - 证据库 CSV 是否存在且非空

## 推荐使用方式

1. 先更新 `data/` 中的结构化证据文件。
2. 运行 `scripts/export_evidence_tables.py`，刷新可读表格。
3. 根据导出的表格更新 `content/06.core-table.md` 或 `content/09.study-matrix.md`。
4. 运行 `scripts/validate_manuscript.py` 做轻量级检查。
5. 运行 `manubot process` 检查章节编排与引用纳入。

## Windows 下示例命令

```powershell
py scripts\export_evidence_tables.py
py scripts\validate_manuscript.py
```

如需继续扩展，可在后续加入：

- 自动生成 supplement markdown
- 自动比较当前正文和结构化数据是否一致
- 投稿前检查脚本
