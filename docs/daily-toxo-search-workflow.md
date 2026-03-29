# 弓形虫疫苗每日检索工作流

## 1. 可复制的每日检索指令模板

每天你只要发我这一句即可：

```text
查最近 24 小时到 7 天内与弓形虫疫苗相关的新文献。优先 PubMed 和主流寄生虫/疫苗期刊。请输出：
1. 新文献清单
2. 高/中/低优先级
3. 哪些值得做文献笔记
4. 哪些值得更新进 GitHub 数据库
5. 若有高优先级，直接生成文献笔记并推到 writing-everyday/daily-writing
```

如果你想缩小范围，可以直接用：

```text
查最近 7 天内与猫弓形虫疫苗、卵囊排出、猫模型免疫相关的新文献，并按优先级整理。
```

## 2. 本地自动检索脚本

仓库里已经提供了自动检索脚本：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\run_daily_toxo_search.ps1"
```

默认会：

- 查询最近 `7` 天的 PubMed 新记录
- 生成一份当日 Markdown 报告
- 输出到 `docs/daily-search/`

输出示例路径：

```text
C:\Users\zheng shang\manubot-paper\docs\daily-search\2026-03-29-toxo-vaccine-search.md
```

如果你只想查最近 `1` 天：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\run_daily_toxo_search.ps1" -Days 1
```

## 3. 自动定时运行

仓库里也准备了注册 Windows 定时任务的脚本：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\register_daily_toxo_search_task.ps1"
```

默认设置：

- 任务名：`DailyToxoVaccineSearch`
- 每天运行时间：`08:30`
- 检索窗口：最近 `7` 天

如果你想改成每天 `07:00`，并只查最近 `1` 天：

```powershell
powershell -ExecutionPolicy Bypass -File "C:\Users\zheng shang\manubot-paper\scripts\register_daily_toxo_search_task.ps1" -Time "07:00" -Days 1
```

## 4. 推荐工作流

推荐你这样用：

1. 让本地定时任务每天自动生成检索报告
2. 你每天把报告发给我，或者直接说“处理今天的弓形虫疫苗检索报告”
3. 我再做第二层人工筛选：
   - 判断哪些真值得保留
   - 生成文献笔记
   - 推送到 `writing-everyday`
   - 需要时再更新主数据库和综述正文

## 5. 当前限制

- 这套自动化脚本当前使用的是 `PubMed`，不是所有期刊官网都逐站抓取
- 但对弓形虫疫苗这类生物医学主题，`PubMed` 已经能覆盖绝大多数高价值新文献
- 如果以后你要，我可以再把这套脚本扩展到 `Crossref`、`OpenAlex` 或特定期刊 RSS
