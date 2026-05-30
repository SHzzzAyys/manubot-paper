#!/usr/bin/env python
"""Export markdown evidence tables from structured CSV files."""

from __future__ import annotations

import csv
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "data"
GENERATED = REPO / "docs" / "generated"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def to_markdown(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    rule = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(row.get(column, "").replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, rule, *body])


def write_table(title: str, rows: list[dict[str, str]], columns: list[str], outfile: Path) -> None:
    outfile.parent.mkdir(parents=True, exist_ok=True)
    content = [f"# {title}", "", to_markdown(rows, columns), ""]
    outfile.write_text("\n".join(content), encoding="utf-8")


def main() -> None:
    direct_rows = read_csv(DATA / "cat_toxo_vaccine_direct_studies.csv")
    support_rows = read_csv(DATA / "cat_toxo_vaccine_support_studies.csv")
    review_rows = read_csv(DATA / "cat_toxo_vaccine_reviews.csv")

    write_table(
        "Direct Cat Studies",
        direct_rows,
        [
            "year",
            "study_id",
            "vaccine_or_intervention",
            "cat_scale",
            "immunization_program",
            "challenge_design",
            "immunology_summary",
            "oocyst_summary",
            "evidence_grade",
            "notes",
        ],
        GENERATED / "direct-cat-studies.md",
    )

    write_table(
        "Support Studies",
        support_rows,
        [
            "year",
            "study_id",
            "study_type",
            "cat_scale",
            "design_summary",
            "key_finding",
            "evidence_grade",
            "notes",
        ],
        GENERATED / "support-studies.md",
    )

    write_table(
        "Review Studies",
        review_rows,
        ["year", "study_id", "focus", "key_value"],
        GENERATED / "review-studies.md",
    )

    print("Generated markdown tables in docs/generated")


if __name__ == "__main__":
    main()
