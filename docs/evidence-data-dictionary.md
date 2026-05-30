# 证据库字段说明

本文件说明 `data/` 目录下结构化证据文件的字段含义。

## `cat_toxo_vaccine_direct_studies.csv`

- `year`
  论文年份。
- `study_id`
  便于脚本和表格引用的稳定标识。
- `category`
  当前固定为 `direct_cat_study`。
- `vaccine_or_intervention`
  候选疫苗或免疫干预名称。
- `cat_scale`
  猫只规模或分组信息。
- `immunization_program`
  免疫程序、剂量、途径和时间安排摘要。
- `challenge_design`
  攻毒设计，包括虫株、剂量、攻毒途径和观察窗口。
- `immunology_summary`
  论文中报告的主要免疫学结果。
- `oocyst_summary`
  卵囊排出相关核心定量结果。
- `evidence_grade`
  采用与正文一致的 `A/B/C` 分级。
- `notes`
  额外说明，如样本量限制、仅摘要可见等。

## `cat_toxo_vaccine_support_studies.csv`

- `study_type`
  支撑性研究类型，如持续性、机理、攻毒模型等。
- `design_summary`
  研究设计摘要。
- `key_finding`
  核心结论。

## `cat_toxo_vaccine_reviews.csv`

- `focus`
  综述文章的主题定位。
- `key_value`
  该综述对当前项目的主要价值。

## `cat_toxo_research_gap_matrix.csv`

- `gap_id`
  研究空白的稳定编号。
- `gap_title`
  空白点标题。
- `current_evidence`
  当前文献对该问题的支持现状。
- `main_limitation`
  当前证据的主要限制。
- `research_opportunity`
  对应可形成的后续研究问题、证据补强方向或综述扩展切入点。

## 维护原则

- 结构化证据库优先保留原始文献直接给出的量化结果。
- 若仅能获得摘要或期刊页面可见信息，应在 `notes` 中显式标注。
- 结构化数据更新后，应同步检查 `content/06.core-table.md`、`content/09.study-matrix.md` 与 `content/10.supplementary-notes.md` 是否需要刷新。
