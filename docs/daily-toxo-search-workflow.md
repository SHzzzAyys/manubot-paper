# 弓形虫每日检索工作流

## 1. 可复制的每日指令模板
每天只需要对我说一句：

```text
检查最近 24 小时到 7 天内与弓形虫相关的新文献。请分成两层：1. 核心检索：疫苗、免疫、减毒、抗原、佐剂、猫模型、卵囊结局。2. 外围补充检索：缓殖子、包囊、阶段转换、顶质体、关键靶点、检测方法、药物诱导变化。请输出：新文献清单、优先级、哪些值得做笔记、哪些值得更新 GitHub 主数据库。
```

如果只想看更窄的一层，可以说：

```text
检查最近 7 天内与猫弓形虫、卵囊结局、猫模型免疫相关的新文献，并按优先级整理。
```

## 2. 本地自动检索脚本
仓库里已经提供自动检索脚本：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\run_daily_toxo_search.ps1"
```

默认行为：

- 检查最近 `7` 天的 PubMed 记录
- 生成当日 Markdown 报告
- 输出到 `D:\ToxoVault\ResearchProject\outputs\daily-search\`

输出示例：

```text
D:\ToxoVault\ResearchProject\outputs\daily-search\2026-03-29-toxo-vaccine-search.md
```

如果只查最近 `1` 天：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\run_daily_toxo_search.ps1" -Days 1
```

## 3. 自动定时运行
定时任务注册脚本：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\register_daily_toxo_search_task.ps1"
```

默认设置：

- 任务名：`DailyToxoVaccineSearch`
- 每天运行时间：`08:30`
- 检索窗口：最近 `7` 天

例如改成每天 `07:00`，只查最近 `1` 天：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\register_daily_toxo_search_task.ps1" -Time "07:00" -Days 1
```

## 4. 推荐用法
建议固定这样用：

1. 本地定时任务每天生成 D 盘日报。
2. 你每天对我说“处理今天的弓形虫检索报告”。
3. 我再做第二层人工筛选：
   - 判断哪些值得保留
   - 生成文献笔记
   - 推到 `writing-everyday`
   - 需要时再提升到主数据库和正文

## 5. 当前边界

- 这套自动化当前使用 `PubMed`，不是逐站抓取所有期刊官网。
- 对弓形虫这种生物医学主题，`PubMed` 已经覆盖大多数高价值新文献。
- 后续如果需要，可以再扩到 `Crossref`、`OpenAlex` 或特定期刊的 `RSS`。
