#!/usr/bin/env python
"""Fetch recent Toxoplasma vaccine papers from PubMed and write a daily report."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO / "docs" / "daily-search"

NCBI = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

QUERIES = [
    (
        "core_vaccine",
        '("Toxoplasma gondii"[Title/Abstract] OR toxoplasma[Title/Abstract]) '
        'AND (vaccine*[Title/Abstract] OR vaccination[Title/Abstract] OR immuniz*[Title/Abstract])',
    ),
    (
        "feline_oocyst",
        '("Toxoplasma gondii"[Title/Abstract] OR toxoplasma[Title/Abstract]) '
        'AND (cat[Title/Abstract] OR cats[Title/Abstract] OR feline[Title/Abstract] '
        'OR oocyst*[Title/Abstract] OR "definitive host"[Title/Abstract]) '
        'AND (vaccine*[Title/Abstract] OR immuniz*[Title/Abstract] OR attenuated[Title/Abstract])',
    ),
    (
        "platforms",
        '("Toxoplasma gondii"[Title/Abstract] OR toxoplasma[Title/Abstract]) '
        'AND ("DNA vaccine"[Title/Abstract] OR "subunit vaccine"[Title/Abstract] '
        'OR "live attenuated"[Title/Abstract] OR mRNA[Title/Abstract] OR recombinant[Title/Abstract])',
    ),
]


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as response:
        return json.load(response)


def fetch_text(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as response:
        return response.read().decode("utf-8")


def esearch(term: str, days: int) -> list[str]:
    params = {
        "db": "pubmed",
        "retmode": "json",
        "retmax": "50",
        "sort": "pub date",
        "reldate": str(days),
        "datetype": "pdat",
        "term": term,
    }
    url = f"{NCBI}/esearch.fcgi?{urllib.parse.urlencode(params)}"
    data = fetch_json(url)
    return data.get("esearchresult", {}).get("idlist", [])


def chunked(items: list[str], size: int) -> list[list[str]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def clean_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def first_article_id(pubmed_data: ET.Element) -> str:
    for article_id in pubmed_data.findall(".//PubmedData/ArticleIdList/ArticleId"):
        if article_id.attrib.get("IdType") == "doi":
            return article_id.text or ""
    return ""


def extract_abstract(article: ET.Element) -> str:
    parts = []
    for node in article.findall(".//Abstract/AbstractText"):
        label = node.attrib.get("Label")
        body = "".join(node.itertext()).strip()
        if not body:
            continue
        parts.append(f"{label}: {body}" if label else body)
    return clean_whitespace(" ".join(parts))


def extract_pub_date(article: ET.Element) -> str:
    article_date = article.find(".//PubDate")
    if article_date is None:
        return ""
    year = article_date.findtext("Year", default="")
    month = article_date.findtext("Month", default="")
    day = article_date.findtext("Day", default="")
    return "-".join(part for part in [year, month, day] if part)


def extract_authors(article: ET.Element) -> str:
    names = []
    for author in article.findall(".//AuthorList/Author"):
        last_name = author.findtext("LastName", default="")
        initials = author.findtext("Initials", default="")
        collective = author.findtext("CollectiveName", default="")
        if collective:
            names.append(collective)
        elif last_name:
            names.append(f"{last_name} {initials}".strip())
        if len(names) >= 3:
            break
    return ", ".join(names)


def efetch(pmids: list[str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for batch in chunked(pmids, 20):
        params = {
            "db": "pubmed",
            "retmode": "xml",
            "id": ",".join(batch),
        }
        url = f"{NCBI}/efetch.fcgi?{urllib.parse.urlencode(params)}"
        root = ET.fromstring(fetch_text(url))
        for article in root.findall(".//PubmedArticle"):
            citation = article.find(".//MedlineCitation")
            article_data = article.find(".//Article")
            if citation is None or article_data is None:
                continue
            pmid = citation.findtext("PMID", default="")
            title = clean_whitespace("".join(article_data.findtext("ArticleTitle", default="")))
            journal = clean_whitespace(article_data.findtext(".//Journal/Title", default=""))
            abstract = extract_abstract(article)
            pub_date = extract_pub_date(article)
            doi = first_article_id(article)
            authors = extract_authors(article)
            records.append(
                {
                    "pmid": pmid,
                    "title": title,
                    "journal": journal,
                    "date": pub_date,
                    "doi": doi,
                    "authors": authors,
                    "abstract": abstract,
                    "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
                }
            )
    return records


def score_priority(record: dict[str, str]) -> str:
    text = " ".join([record.get("title", ""), record.get("abstract", "")]).lower()
    high_terms = ["cat", "cats", "feline", "oocyst", "definitive host", "transmission-blocking"]
    medium_terms = ["vaccine", "vaccination", "attenuated", "subunit", "dna vaccine", "recombinant"]
    if any(term in text for term in high_terms) and any(term in text for term in medium_terms):
        return "high"
    if any(term in text for term in medium_terms):
        return "medium"
    return "background"


def score_reason(priority: str) -> str:
    if priority == "high":
        return "直接涉及猫模型、卵囊排出或关键结局，优先处理。"
    if priority == "medium":
        return "与弓形虫疫苗平台或候选抗原直接相关，可纳入后备清单。"
    return "与弓形虫相关，但更偏背景、方法或外围支持信息。"


def format_record(record: dict[str, str]) -> str:
    abstract = record.get("abstract", "")
    abstract = textwrap.shorten(abstract, width=280, placeholder="...")
    doi = record.get("doi", "")
    doi_line = f"- DOI: `{doi}`" if doi else "- DOI: 未检出"
    return "\n".join(
        [
            f"### {record['title']}",
            f"- 优先级：`{record['priority']}`",
            f"- 原因：{record['reason']}",
            f"- 期刊：{record['journal'] or '未检出'}",
            f"- 日期：{record['date'] or '未检出'}",
            f"- 作者：{record['authors'] or '未检出'}",
            f"- PMID: `{record['pmid']}`",
            doi_line,
            f"- PubMed: {record['pubmed_url']}",
            f"- 摘要摘录：{abstract or '未检出'}",
            "",
        ]
    )


def build_report(records: list[dict[str, str]], days: int) -> str:
    today = dt.date.today().isoformat()
    lines = [
        f"# 弓形虫疫苗每日检索报告 {today}",
        "",
        f"- 检索窗口：最近 `{days}` 天",
        "- 数据源：PubMed",
        "- 说明：这是自动初筛结果，后续可再人工筛选并生成文献笔记。",
        "",
        "## 检索式",
        "",
    ]
    for name, query in QUERIES:
        lines.append(f"- `{name}`: `{query}`")
    lines.extend(["", f"## 命中记录（共 {len(records)} 篇）", ""])
    if not records:
        lines.append("本次没有检索到新记录。")
        lines.append("")
        return "\n".join(lines)
    for record in records:
        lines.append(format_record(record))
    lines.extend(
        [
            "## 建议后续动作",
            "",
            "1. 优先处理 `high` 项，制作文献笔记并推送到 `writing-everyday/daily-writing`。",
            "2. 对 `medium` 项判断是否进入主数据库或综述正文。",
            "3. 对 `background` 项仅在需要补背景时保留。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a daily Toxoplasma vaccine report from PubMed.")
    parser.add_argument("--days", type=int, default=7, help="Search window in days.")
    args = parser.parse_args()

    pmids: list[str] = []
    for _, query in QUERIES:
        for pmid in esearch(query, args.days):
            if pmid not in pmids:
                pmids.append(pmid)

    records = efetch(pmids)
    for record in records:
        record["priority"] = score_priority(record)
        record["reason"] = score_reason(record["priority"])
    records.sort(key=lambda item: ({"high": 0, "medium": 1, "background": 2}[item["priority"]], item["date"]), reverse=False)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outfile = OUTPUT_DIR / f"{dt.date.today().isoformat()}-toxo-vaccine-search.md"
    outfile.write_text(build_report(records, args.days), encoding="utf-8")

    print(f"Wrote {outfile}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
