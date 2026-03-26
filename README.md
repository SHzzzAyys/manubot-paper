# 猫弓形虫疫苗综述工作区

本仓库基于 Manubot，用于撰写并维护综述《猫的弓形虫疫苗研究进展》。
当前仓库已经不再只是一个空模板，而是同时承载 3 项工作：

1. 综述投稿定稿工程
2. 猫弓形虫疫苗证据库工程
3. 自动化科研写作工具链工程

另外，仓库现在还包含一套可直接服务毕业论文写作的资产库：

- `docs/thesis/00-index.md`
- `docs/thesis/01-chapter-background-significance.md`
- `docs/thesis/02-chapter-review-status.md`
- `docs/thesis/03-chapter-gaps-objectives.md`
- `docs/thesis/04-paragraph-bank.md`
- `docs/thesis/05-figure-table-bank.md`
- `docs/thesis/06-gap-matrix.md`
- `docs/thesis/07-defense-and-review-qa.md`

以及三套更接近直接使用状态的重交付：

- `docs/thesis-ready/`
  接近可直接拼接进毕业论文的文献综述章节初稿。
- `docs/proposal/`
  开题报告资产包。
- `docs/defense/`
  答辩资产包。

## 仓库入口

- `content/`
  Manubot 主文稿、主表、时间轴、研究矩阵和补充材料说明。
- `data/`
  结构化证据库 CSV 文件。
- `scripts/`
  证据表导出和轻量级校验脚本。
- `docs/`
  投稿清单、文稿结构地图、字段说明、工具链说明和生成表格。

## 主文稿结构

- `content/01.abstract.md`
- `content/02.introduction.md`
- `content/03.methods.md`
- `content/04.results.md`
- `content/05.discussion.md`
- `content/08.conclusion.md`

## 表格与补充材料

- `content/06.core-table.md`
  核心证据表。
- `content/07.timeline.md`
  研究演化时间轴。
- `content/09.study-matrix.md`
  逐篇研究矩阵。
- `content/10.supplementary-notes.md`
  补充材料说明、缩略词和数据口径。

## 证据库文件

- `data/cat_toxo_vaccine_direct_studies.csv`
- `data/cat_toxo_vaccine_support_studies.csv`
- `data/cat_toxo_vaccine_reviews.csv`

字段解释见：

- `docs/evidence-data-dictionary.md`

## 常用文档

- `docs/submission-checklist.md`
  投稿前逐项检查。
- `docs/manuscript-map.md`
  当前主文、主表、补充材料的结构地图。
- `docs/toolchain.md`
  工具链说明。

## 常用命令

在本机可直接使用已配置好的 Python 与 Manubot 环境。

导出结构化证据表：

```powershell
& "C:\Users\zheng shang\.venvs\manubot\Scripts\python.exe" scripts\export_evidence_tables.py
```

运行轻量级校验：

```powershell
& "C:\Users\zheng shang\.venvs\manubot\Scripts\python.exe" scripts\validate_manuscript.py
```

运行 Manubot 编排检查：

```powershell
$env:TZ='Etc/UTC'
$env:LC_ALL='en_US.UTF-8'
$env:PATH = "C:\Users\zheng shang\.venvs\manubot\Scripts;" + $env:PATH
& "C:\Users\zheng shang\.venvs\manubot\Scripts\manubot.exe" process --content-directory=content --output-directory=output --cache-directory=ci/cache --skip-citations --log-level=INFO
```

## 当前已知待补项

- `content/metadata.yaml` 中作者单位仍为占位符，正式投稿前需要补全。
- HTML/PDF 最终导出仍受 `pandoc-fignos` 等依赖缺失影响，但不影响当前文稿内容与结构验证。
