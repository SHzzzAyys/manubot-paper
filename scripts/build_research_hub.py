#!/usr/bin/env python
"""Build a research hub that summarizes public reports, notes, and data assets."""

from __future__ import annotations

import csv
import datetime as dt
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
OUTPUTS = Path(r"D:\ToxoVault\ResearchProject\outputs")
HUB = OUTPUTS / "research-hub"
INTEL = REPO / "docs" / "intelligence"
DAILY_SEARCH = OUTPUTS / "daily-search"
DATA = REPO / "data"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def load_registry() -> list[dict[str, str]]:
    path = INTEL / "literature-note-registry.json"
    if not path.exists():
        return []
    return json.loads(read_text(path))


def list_daily_reports() -> list[dict[str, str]]:
    reports = []
    if not DAILY_SEARCH.exists():
        return reports
    for path in sorted(DAILY_SEARCH.glob("*-toxo-vaccine-search.md"), reverse=True):
        text = read_text(path)
        hit_match = re.search(r"## 命中文献（共 (\d+) 篇）", text)
        reports.append(
            {
                "date": path.stem.replace("-toxo-vaccine-search", ""),
                "path": str(path),
                "hit_count": hit_match.group(1) if hit_match else "0",
            }
        )
    return reports


def data_counts() -> list[dict[str, str]]:
    rows = []
    for path in sorted(DATA.glob("*.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            count = max(sum(1 for _ in csv.reader(handle)) - 1, 0)
        rows.append({"file": path.name, "rows": str(count)})
    return rows


def output_inventory() -> list[dict[str, str]]:
    rows = []
    for path in sorted(OUTPUTS.iterdir()):
        if not path.is_dir():
            continue
        count = sum(1 for _ in path.rglob("*") if _.is_file())
        rows.append({"folder": path.name, "files": str(count), "path": str(path)})
    return rows


def markdown_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    rule = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, rule, *body]) if rows else "\n".join([header, rule])


def build_dashboard(registry: list[dict[str, str]], reports: list[dict[str, str]]) -> str:
    pending_notes = [note for note in registry if note.get("main_status") != "已进入主库"]
    recent_reports = reports[:5]
    recent_notes = sorted(registry, key=lambda item: item.get("note_date", ""), reverse=True)[:5]
    lines = [
        f"# 科研资料中台总览 {dt.date.today().isoformat()}",
        "",
        "## 当前快照",
        "",
        f"- D 盘日报数：`{len(reports)}`",
        f"- 分支文献笔记数：`{len(registry)}`",
        f"- 待提升笔记数：`{len(pending_notes)}`",
        f"- 主库 CSV 数：`{len(data_counts())}`",
        "",
        "## 最近日报",
        "",
    ]
    if recent_reports:
        for report in recent_reports:
            lines.append(f"- `{report['date']}`：命中 `{report['hit_count']}` 篇，文件 `{report['path']}`")
    else:
        lines.append("- 暂无日报。")
    lines.extend(["", "## 最近笔记", ""])
    if recent_notes:
        for note in recent_notes:
            lines.append(
                f"- `{note.get('note_date') or '未标记'}` {note['title']} | 主题：{'、'.join(note.get('topics', []))} | 状态：{note.get('main_status', '未标记')}"
            )
    else:
        lines.append("- 暂无分支文献笔记。")
    return "\n".join(lines)


def build_daily_log(reports: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# D 盘日报清单",
            "",
            markdown_table(reports, ["date", "hit_count", "path"]),
            "",
        ]
    )


def build_note_log(registry: list[dict[str, str]]) -> str:
    rows = [
        {
            "date": note.get("note_date", ""),
            "title": note.get("title", ""),
            "topics": "、".join(note.get("topics", [])),
            "priority": note.get("priority", ""),
            "main_status": note.get("main_status", ""),
            "path": note.get("path", ""),
        }
        for note in sorted(registry, key=lambda item: item.get("note_date", ""), reverse=True)
    ]
    return "\n".join(["# 文献笔记台账", "", markdown_table(rows, ["date", "title", "topics", "priority", "main_status", "path"]), ""])


def build_data_log(data_rows: list[dict[str, str]], inventory_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 数据层与输出层清单",
            "",
            "## 主库 CSV",
            "",
            markdown_table(data_rows, ["file", "rows"]),
            "",
            "## D 盘输出目录",
            "",
            markdown_table(inventory_rows, ["folder", "files", "path"]),
            "",
        ]
    )


def main() -> int:
    HUB.mkdir(parents=True, exist_ok=True)
    registry = load_registry()
    reports = list_daily_reports()
    data_rows = data_counts()

    write(HUB / "00-dashboard.md", build_dashboard(registry, reports))
    write(HUB / "01-daily-search-log.md", build_daily_log(reports))
    write(HUB / "02-literature-note-log.md", build_note_log(registry))

    # Two-pass write so the research-hub folder count reflects the files written by this script.
    for _ in range(2):
        inventory_rows = output_inventory()
        write(HUB / "03-data-assets-log.md", build_data_log(data_rows, inventory_rows))
        write(
            HUB / "research-hub.json",
            json.dumps(
                {
                    "generated_on": dt.date.today().isoformat(),
                    "daily_reports": reports,
                    "literature_notes": registry,
                    "data_rows": data_rows,
                    "output_inventory": inventory_rows,
                },
                ensure_ascii=False,
                indent=2,
            ),
        )
    print(f"Wrote research hub to {HUB}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
