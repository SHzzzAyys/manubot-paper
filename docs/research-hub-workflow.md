# 科研资料中台工作流

## 目标

这套工作流把三层内容连在一起：

1. D 盘日报
2. 仓库内文献情报层
3. thesis-ready 章节资产与数据层总览

这样你每天不需要分别更新三个地方，只要跑一次入口脚本，就会同步刷新。

## 入口脚本

### 每日检索入口

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\run_daily_toxo_search.ps1"
```

这条命令现在会连续完成：

1. 生成或更新 D 盘日报
2. 重建 `docs/intelligence/`
3. 重建 D 盘 `research-hub/`
4. 自动把设定词表中的偏硬表述替换成更普通的词汇

### 仅刷新情报层和中台

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\run_research_hub.ps1"
```

适合你当天没有重新抓文献，只想把已有笔记和资产重新汇总的情况。

## D 盘输出位置

中台输出目录：

```text
D:\ToxoVault\ResearchProject\outputs\research-hub\
```

当前会生成：

- `00-dashboard.md`
  总览页，适合每天先看。
- `01-daily-search-log.md`
  日报台账。
- `02-literature-note-log.md`
  分支文献笔记台账。
- `03-thesis-assets-log.md`
  thesis-ready 资产清单。
- `04-data-assets-log.md`
  数据层和输出层清单。
- `research-hub.json`
  机器可读版本，后续还能继续接脚本。

## 自动替换器

论文版词汇替换规则放在：

```text
C:\Users\zheng shang\manubot-paper\data\wording-profiles\academic.json
```

日常版词汇替换规则放在：

```text
C:\Users\zheng shang\manubot-paper\data\wording-profiles\daily.json
```

清洗脚本：

```text
C:\Users\zheng shang\manubot-paper\scripts\sanitize_wording.py
```

默认会处理：

- `content/`
- `docs/thesis-ready/`
- `docs/intelligence/`
- `docs/daily-toxo-search-workflow.md`
- `docs/research-hub-workflow.md`
- `D:\ToxoVault\ResearchProject\outputs\daily-search\`
- `D:\ToxoVault\ResearchProject\outputs\research-hub\`

如果你只想单独跑一次论文版替换：

```powershell
& "C:\Users\zheng shang\manubot-paper\.venv\Scripts\python.exe" "C:\Users\zheng shang\manubot-paper\scripts\sanitize_wording.py" --profile academic
```

如果你只想单独跑一次日常版替换：

```powershell
& "C:\Users\zheng shang\manubot-paper\.venv\Scripts\python.exe" "C:\Users\zheng shang\manubot-paper\scripts\sanitize_wording.py" --profile daily
```

如果只想先看会替换哪些内容：

```powershell
& "C:\Users\zheng shang\manubot-paper\.venv\Scripts\python.exe" "C:\Users\zheng shang\manubot-paper\scripts\sanitize_wording.py" --profile academic --dry-run
```

## 推荐使用方式

1. 让定时任务每天先跑 `run_daily_toxo_search.ps1`。
2. 你有空时直接看 `D:\ToxoVault\ResearchProject\outputs\research-hub\00-dashboard.md`。
3. 需要做笔记或提升主库时，再把具体条目交给我继续处理。

## 当前边界

- 中台默认汇总的是仓库已有内容和 D 盘已有输出。
- 它不会自行决定删除或清理 D 盘旧资料。
- 自动替换器只按词表做文本替换，不会判断上下文语气是否最优，所以词表需要按你的使用习惯逐步调。
- 如果后续要接入更多目录，例如 `reflect everyday`、`plan everyday` 或 `knowledge`，可以在这个基础上继续扩展。
