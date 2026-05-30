#!/usr/bin/env python
"""Fetch recent Toxoplasma literature from PubMed and write a layered daily report."""

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


OUTPUT_DIR = Path(r"D:\ToxoVault\ResearchProject\outputs\daily-search")
NCBI = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

QUERIES = [
    (
        "core_vaccine",
        "核心疫苗",
        '("Toxoplasma gondii"[Title/Abstract] OR toxoplasma[Title/Abstract]) '
        'AND (vaccine*[Title/Abstract] OR vaccination[Title/Abstract] OR immuniz*[Title/Abstract])',
    ),
    (
        "cat_oocyst",
        "猫模型与卵囊",
        '("Toxoplasma gondii"[Title/Abstract] OR toxoplasma[Title/Abstract]) '
        'AND (cat[Title/Abstract] OR cats[Title/Abstract] OR feline[Title/Abstract] '
        'OR oocyst*[Title/Abstract] OR "definitive host"[Title/Abstract] '
        'OR "sexual stage"[Title/Abstract])',
    ),
    (
        "attenuation_platforms",
        "减毒与平台",
        '("Toxoplasma gondii"[Title/Abstract] OR toxoplasma[Title/Abstract]) '
        'AND (attenuated[Title/Abstract] OR "live attenuated"[Title/Abstract] '
        'OR recombinant[Title/Abstract] OR "DNA vaccine"[Title/Abstract] '
        'OR "subunit vaccine"[Title/Abstract] OR adjuvant[Title/Abstract] '
        'OR mucosal[Title/Abstract])',
    ),
    (
        "stage_conversion",
        "阶段转换与包囊",
        '("Toxoplasma gondii"[Title/Abstract] OR toxoplasma[Title/Abstract]) '
        'AND (bradyzoite*[Title/Abstract] OR tachyzoite*[Title/Abstract] '
        'OR cyst*[Title/Abstract] OR differentiation[Title/Abstract] '
        'OR conversion[Title/Abstract])',
    ),
    (
        "apicoplast_targets",
        "顶质体与靶点",
        '("Toxoplasma gondii"[Title/Abstract] OR toxoplasma[Title/Abstract]) '
        'AND (apicoplast[Title/Abstract] OR thioredoxin[Title/Abstract] '
        'OR kinase[Title/Abstract] OR target*[Title/Abstract] OR drug*[Title/Abstract])',
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


def first_article_id(article: ET.Element, id_type: str) -> str:
    for article_id in article.findall(".//PubmedData/ArticleIdList/ArticleId"):
        if article_id.attrib.get("IdType") == id_type:
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
    pub_date = article.find(".//PubDate")
    if pub_date is None:
        return ""
    year = pub_date.findtext("Year", default="")
    month = pub_date.findtext("Month", default="")
    day = pub_date.findtext("Day", default="")
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
        params = {"db": "pubmed", "retmode": "xml", "id": ",".join(batch)}
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
            records.append(
                {
                    "pmid": pmid,
                    "title": title,
                    "journal": journal,
                    "date": extract_pub_date(article),
                    "doi": first_article_id(article, "doi"),
                    "pmc": first_article_id(article, "pmc"),
                    "authors": extract_authors(article),
                    "abstract": extract_abstract(article),
                    "pubmed_url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
                    "matched_queries": [],
                }
            )
    return records


def score_priority(record: dict[str, str]) -> str:
    text = " ".join([record.get("title", ""), record.get("abstract", "")]).lower()
    cat_terms = ["cat", "cats", "feline", "oocyst", "definitive host", "sexual stage", "hap2"]
    vaccine_terms = ["vaccine", "vaccination", "immuniz", "attenuated", "dna vaccine", "subunit", "adjuvant"]
    support_terms = [
        "bradyzoite",
        "cyst",
        "differentiation",
        "conversion",
        "apicoplast",
        "thioredoxin",
        "kinase",
        "marker",
        "viability",
    ]
    if any(term in text for term in cat_terms) and any(term in text for term in vaccine_terms):
        return "high"
    if any(term in text for term in vaccine_terms) or any(term in text for term in support_terms) or any(
        term in text for term in cat_terms
    ):
        return "medium"
    return "background"


def score_reason(priority: str) -> str:
    if priority == "high":
        return "与猫模型、卵囊结局或直接免疫评价关系紧密，宜优先人工核对。"
    if priority == "medium":
        return "与阶段转换、检测方法、顶质体或支撑性机制相关，适合纳入外围跟踪。"
    return "与弓形虫主题有关，但更偏背景信息，可按需保留。"


def format_record(record: dict[str, str]) -> str:
    abstract = textwrap.shorten(record.get("abstract", ""), width=320, placeholder="...")
    matched = "、".join(record.get("matched_queries", [])) or "未标记"
    doi = record.get("doi") or "未检出"
    pmc = record.get("pmc") or "未检出"
    return "\n".join(
        [
            f"### {record['title']}",
            f"- 优先级：`{record['priority']}`",
            f"- 原因：{record['reason']}",
            f"- 命中分组：{matched}",
            f"- 期刊：{record['journal'] or '未检出'}",
            f"- 日期：{record['date'] or '未检出'}",
            f"- 作者：{record['authors'] or '未检出'}",
            f"- PMID：`{record['pmid']}`",
            f"- DOI：`{doi}`",
            f"- PMCID：`{pmc}`",
            f"- PubMed：{record['pubmed_url']}",
            f"- 摘要摘录：{abstract or '未检出'}",
            "",
        ]
    )


def build_report(records: list[dict[str, str]], days: int) -> str:
    today = dt.date.today().isoformat()
    lines = [
        f"# 弓形虫每日检索报告 {today}",
        "",
        f"- 检索窗口：最近 `{days}` 天",
        "- 数据源：PubMed",
        "- 结构：核心检索 + 外围补充检索",
        "- 说明：这是自动初筛结果，后续仍需人工判断是否值得做文献笔记或纳入主库。",
        "",
        "## 检索分组",
        "",
    ]
    for key, label, query in QUERIES:
        lines.append(f"- `{key}` / {label}：`{query}`")
    lines.extend(["", f"## 命中文献（共 {len(records)} 篇）", ""])
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
            "1. 优先处理 `high` 条目，必要时直接生成文献笔记。",
            "2. 对 `medium` 条目判断是否进入主数据库、正文或外围资料层。",
            "3. `background` 条目仅在补背景或方法学时保留。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a daily Toxoplasma literature report from PubMed.")
    parser.add_argument("--days", type=int, default=7, help="Search window in days.")
    args = parser.parse_args()

    query_hits: dict[str, list[str]] = {}
    all_pmids: list[str] = []
    for key, label, query in QUERIES:
        ids = esearch(query, args.days)
        query_hits[key] = ids
        for pmid in ids:
            if pmid not in all_pmids:
                all_pmids.append(pmid)

    records = efetch(all_pmids)
    by_pmid = {record["pmid"]: record for record in records}
    for _, label, _ in QUERIES:
        pass
    for key, label, _ in QUERIES:
        for pmid in query_hits.get(key, []):
            if pmid in by_pmid:
                by_pmid[pmid]["matched_queries"].append(label)

    for record in records:
        record["priority"] = score_priority(record)
        record["reason"] = score_reason(record["priority"])

    priority_order = {"high": 0, "medium": 1, "background": 2}
    records.sort(key=lambda item: (priority_order[item["priority"]], item["date"] or ""), reverse=False)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outfile = OUTPUT_DIR / f"{dt.date.today().isoformat()}-toxo-vaccine-search.md"
    outfile.write_text(build_report(records, args.days), encoding="utf-8")
    print(f"Wrote {outfile}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
