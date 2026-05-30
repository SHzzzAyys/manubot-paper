#!/usr/bin/env python
"""Build a literature intelligence layer from evidence files, daily reports, and branch notes."""

from __future__ import annotations

import csv
import datetime as dt
import json
import re
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
INTEL = REPO / "docs" / "intelligence"
REGISTRY_JSON = INTEL / "literature-note-registry.json"
WRITING_BRANCH = "writing-everyday"
SEARCH_DIR = Path(r"D:\ToxoVault\ResearchProject\outputs\daily-search")
SCAN_ROOTS = [REPO / "content", REPO / "data", REPO / "docs" / "generated"]
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")


def run_git_text(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def run_git_bytes(*args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(REPO), *args],
        check=True,
        capture_output=True,
    )
    return result.stdout


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def extract_dois(text: str) -> set[str]:
    return {match.rstrip(".") for match in DOI_RE.findall(text)}


def load_main_index() -> dict[str, set[str]]:
    index = {"doi": set(), "pmid": set(), "text": set()}
    for root in SCAN_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix.lower() not in {".md", ".csv", ".yaml", ".yml", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            lowered = text.lower()
            index["text"].add(lowered)
            index["doi"].update(doi.lower() for doi in extract_dois(text))
            index["pmid"].update(re.findall(r"\b\d{7,8}\b", text))
    return index


def list_branch_notes() -> list[str]:
    output = run_git_bytes("ls-tree", "-r", "-z", "--name-only", WRITING_BRANCH, "--", "daily-writing")
    paths = [item.decode("utf-8") for item in output.split(b"\x00") if item]
    return sorted(path for path in paths if "文献笔记" in Path(path).name)


def show_branch_file(path: str) -> str:
    return run_git_text("show", "--textconv", f"{WRITING_BRANCH}:{path}")


def extract_first(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_block(title: str, text: str) -> str:
    pattern = rf"## {re.escape(title)}\s+(.+?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    if not match:
        return ""
    return re.sub(r"\n{2,}", "\n", match.group(1).strip())


def classify_topics(text: str) -> list[str]:
    lower = text.lower()
    topics: list[str] = []
    mapping = {
        "猫模型与卵囊": ["cat", "cats", "feline", "oocyst", "entero-epithelial", "definitive host"],
        "阶段转换与包囊": ["bradyzoite", "tachyzoite", "cyst", "conversion", "differentiation", "stage"],
        "检测与方法": ["rt-qpcr", "assay", "marker", "detection", "viability", "bioassay"],
        "顶质体与靶点": ["apicoplast", "thioredoxin", "kinase", "target", "drug"],
        "疫苗与免疫": ["vaccine", "vaccin", "immun", "attenuated", "adjuvant", "mucosal"],
    }
    for label, keywords in mapping.items():
        if any(keyword in lower for keyword in keywords):
            topics.append(label)
    return topics or ["其他支撑资料"]


def classify_priority(text: str) -> str:
    lower = text.lower()
    has_cat = any(token in lower for token in ["cat", "cats", "feline", "oocyst", "definitive host"])
    has_vaccine = any(token in lower for token in ["vaccine", "vaccin", "immun", "attenuated", "adjuvant"])
    has_support = any(
        token in lower
        for token in ["bradyzoite", "cyst", "apicoplast", "thioredoxin", "marker", "viability", "kinase", "drug"]
    )
    if has_cat and has_vaccine:
        return "high"
    if has_cat or has_support or has_vaccine:
        return "medium"
    return "background"


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def derive_main_status(note: dict[str, str], index: dict[str, set[str]]) -> tuple[str, str]:
    doi = note.get("doi", "").lower()
    pmid = note.get("pmid", "")
    title_key = normalize_text(note["title"])
    if doi and doi in index["doi"]:
        return "已进入主库", "可进一步补到正文或核心表"
    if pmid and pmid in index["pmid"]:
        return "已进入主库", "建议核对正文和数据层是否一致"
    if title_key and any(title_key in blob for blob in index["text"]):
        return "已进入主库", "建议核对正文和数据层是否一致"
    if note["priority"] == "high":
        return "待提升", "优先评估是否进入主数据库与正文"
    if note["priority"] == "medium":
        return "待筛选", "保留在外围资料层，视需要再提升"
    return "背景保留", "仅在补背景或方法学时调用"


def parse_note(path: str, index: dict[str, set[str]]) -> dict[str, str]:
    content = show_branch_file(path)
    title = extract_first(r"^#\s+文献笔记[:：]\s*(.+)$", content) or Path(path).stem
    journal = extract_first(r"^- 期刊[:：]\*?(.+?)\*?$", content)
    year = extract_first(r"^- 时间[:：](.+)$", content) or extract_first(r"^- 发表时间[:：](.+)$", content)
    doi = extract_first(r"^- DOI[:：]`?(.+?)`?$", content)
    pmid = extract_first(r"^- PMID[:：]`?(.+?)`?$", content)
    summary = extract_block("一句话总结", content).splitlines()[0] if extract_block("一句话总结", content) else ""
    topics = classify_topics(content)
    priority = classify_priority(content)
    note_date_match = re.match(r"daily-writing/(\d{4}-\d{2}-\d{2})", path)
    note_date = note_date_match.group(1) if note_date_match else ""
    note = {
        "path": path,
        "title": title,
        "journal": journal,
        "year": year,
        "doi": doi,
        "pmid": pmid,
        "summary": summary or "未提取到一句话总结。",
        "topics": topics,
        "priority": priority,
        "note_date": note_date,
    }
    status, action = derive_main_status(note, index)
    note["main_status"] = status
    note["next_action"] = action
    return note


def parse_daily_reports() -> list[dict[str, str]]:
    reports = []
    if not SEARCH_DIR.exists():
        return reports
    for path in sorted(SEARCH_DIR.glob("*-toxo-vaccine-search.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        hit_count = extract_first(r"## 命中文献（共 (\d+) 篇）", text) or "0"
        reports.append({"path": str(path), "date": path.stem.replace("-toxo-vaccine-search", ""), "hit_count": hit_count})
    return reports


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    rule = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |" for row in rows
    ]
    return "\n".join([header, rule, *body]) if rows else "\n".join([header, rule])


def build_index(notes: list[dict[str, str]], reports: list[dict[str, str]], index: dict[str, set[str]]) -> str:
    topic_counter = Counter()
    for note in notes:
        for topic in note["topics"]:
            topic_counter[topic] += 1
    promoted = sum(1 for note in notes if note["main_status"] == "已进入主库")
    return "\n".join(
        [
            "# 文献情报系统总览",
            "",
            f"- 生成日期：`{dt.date.today().isoformat()}`",
            f"- 分支文献笔记数：`{len(notes)}`",
            f"- 主库扫描 DOI 数：`{len(index['doi'])}`",
            f"- 已进入主库的分支笔记：`{promoted}`",
            f"- D 盘检索日报数：`{len(reports)}`",
            "",
            "## 入口",
            "",
            "- [主题地图](./01-topic-map.md)",
            "- [优先处理队列](./02-priority-board.md)",
            "- [文献笔记目录](./03-note-catalog.md)",
            "- [近 7 天摘要](./04-weekly-digest.md)",
            "- [提升路径](./05-promotion-pipeline.md)",
            "",
            "## 当前主题分布",
            "",
            *[f"- `{topic}`：{count}" for topic, count in topic_counter.most_common()],
            "",
        ]
    )


def build_topic_map(notes: list[dict[str, str]]) -> str:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for note in notes:
        for topic in note["topics"]:
            grouped[topic].append(note)
    lines = ["# 主题地图", ""]
    for topic in sorted(grouped):
        lines.append(f"## {topic}")
        lines.append("")
        rows = [
            {
                "日期": note["note_date"] or "未标记",
                "标题": note["title"],
                "优先级": note["priority"],
                "主库状态": note["main_status"],
            }
            for note in sorted(grouped[topic], key=lambda item: item["note_date"], reverse=True)
        ]
        lines.append(markdown_table(rows, ["日期", "标题", "优先级", "主库状态"]))
        lines.append("")
    return "\n".join(lines)


def build_priority_board(notes: list[dict[str, str]]) -> str:
    order = {"high": 0, "medium": 1, "background": 2}
    rows = [
        {
            "优先级": note["priority"],
            "日期": note["note_date"] or "未标记",
            "标题": note["title"],
            "主题": "、".join(note["topics"]),
            "主库状态": note["main_status"],
            "建议动作": note["next_action"],
        }
        for note in sorted(notes, key=lambda item: (order[item["priority"]], item["note_date"]), reverse=False)
    ]
    return "\n".join(["# 优先处理队列", "", markdown_table(rows, ["优先级", "日期", "标题", "主题", "主库状态", "建议动作"]), ""])


def build_note_catalog(notes: list[dict[str, str]]) -> str:
    rows = [
        {
            "日期": note["note_date"] or "未标记",
            "标题": note["title"],
            "期刊": note["journal"] or "未提取",
            "时间": note["year"] or "未提取",
            "DOI": note["doi"] or "未提取",
            "PMID": note["pmid"] or "未提取",
            "摘要": note["summary"],
        }
        for note in sorted(notes, key=lambda item: item["note_date"], reverse=True)
    ]
    return "\n".join(["# 文献笔记目录", "", markdown_table(rows, ["日期", "标题", "期刊", "时间", "DOI", "PMID", "摘要"]), ""])


def build_weekly_digest(notes: list[dict[str, str]], reports: list[dict[str, str]]) -> str:
    today = dt.date.today()
    recent_notes = [note for note in notes if note["note_date"] and (today - dt.date.fromisoformat(note["note_date"])).days <= 7]
    recent_reports = [
        report for report in reports if report["date"] and (today - dt.date.fromisoformat(report["date"])).days <= 7
    ]
    lines = ["# 近 7 天摘要", "", "## D 盘检索日报", ""]
    if recent_reports:
        for report in recent_reports:
            lines.append(f"- `{report['date']}`：命中 `{report['hit_count']}` 篇，文件 `{report['path']}`")
    else:
        lines.append("- 最近 7 天没有日报文件。")
    lines.extend(["", "## 新增文献笔记", ""])
    if recent_notes:
        for note in sorted(recent_notes, key=lambda item: item["note_date"], reverse=True):
            lines.append(
                f"- `{note['note_date']}` {note['title']} | 主题：{'、'.join(note['topics'])} | 优先级：{note['priority']} | 状态：{note['main_status']}"
            )
    else:
        lines.append("- 最近 7 天没有新增文献笔记。")
    lines.append("")
    return "\n".join(lines)


def build_promotion_pipeline(notes: list[dict[str, str]]) -> str:
    lines = [
        "# 提升路径",
        "",
        "## 判定原则",
        "",
        "1. 先写分支笔记：进入 `writing-everyday/daily-writing`。",
        "2. 再看主题和主库状态：猫模型、卵囊、直接免疫评价优先进入主数据库。",
        "3. 方法学、阶段转换、顶质体和支撑机制先留在外围资料层，必要时再进入正文。",
        "",
        "## 当前候选",
        "",
    ]
    rows = [
        {
            "标题": note["title"],
            "优先级": note["priority"],
            "主库状态": note["main_status"],
            "建议动作": note["next_action"],
        }
        for note in notes
    ]
    lines.append(markdown_table(rows, ["标题", "优先级", "主库状态", "建议动作"]))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    main_index = load_main_index()
    notes = [parse_note(path, main_index) for path in list_branch_notes()]
    reports = parse_daily_reports()

    write(INTEL / "00-index.md", build_index(notes, reports, main_index))
    write(INTEL / "01-topic-map.md", build_topic_map(notes))
    write(INTEL / "02-priority-board.md", build_priority_board(notes))
    write(INTEL / "03-note-catalog.md", build_note_catalog(notes))
    write(INTEL / "04-weekly-digest.md", build_weekly_digest(notes, reports))
    write(INTEL / "05-promotion-pipeline.md", build_promotion_pipeline(notes))
    write(REGISTRY_JSON, json.dumps(notes, ensure_ascii=False, indent=2))
    print(f"Built intelligence docs in {INTEL}")
    print(f"分支笔记数：{len(notes)}")
    print(f"D 盘日报数：{len(reports)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
