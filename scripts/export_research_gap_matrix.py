#!/usr/bin/env python
"""Export public research-gap markdown from the research gap matrix."""

from __future__ import annotations

import csv
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data" / "cat_toxo_research_gap_matrix.csv"
OUTPUT = REPO / "docs" / "generated" / "research-gap-matrix.md"


def main() -> None:
    with DATA.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    columns = ["gap_id", "gap_title", "current_evidence", "main_limitation", "research_opportunity"]
    header = "| " + " | ".join(columns) + " |"
    rule = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(row[column].replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(["# Research Gap Matrix", "", header, rule, *body, ""]), encoding="utf-8")
    print(f"Generated {OUTPUT}")


if __name__ == "__main__":
    main()
