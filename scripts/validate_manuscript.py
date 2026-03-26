#!/usr/bin/env python
"""Lightweight repository checks for the manuscript workspace."""

from __future__ import annotations

import csv
from pathlib import Path

import yaml


REPO = Path(__file__).resolve().parent.parent
CONTENT = REPO / "content"
DATA = REPO / "data"


def require(path: Path) -> None:
    if not path.exists():
        raise SystemExit(f"Missing required file: {path}")


def validate_metadata() -> list[str]:
    warnings: list[str] = []
    metadata_path = CONTENT / "metadata.yaml"
    require(metadata_path)
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))

    if not metadata.get("title"):
        warnings.append("metadata.yaml: missing title")

    authors = metadata.get("authors", [])
    if not authors:
        warnings.append("metadata.yaml: missing authors")
    else:
        for idx, author in enumerate(authors, start=1):
            if not author.get("affiliations") or author.get("affiliations") == ["Add primary affiliation here"]:
                warnings.append(f"metadata.yaml: author {idx} affiliation still placeholder or missing")

    return warnings


def validate_data_files() -> list[str]:
    warnings: list[str] = []
    for filename in [
        "cat_toxo_vaccine_direct_studies.csv",
        "cat_toxo_vaccine_support_studies.csv",
        "cat_toxo_vaccine_reviews.csv",
    ]:
        path = DATA / filename
        require(path)
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if not rows:
            warnings.append(f"{filename}: no rows found")
    return warnings


def main() -> None:
    warnings = []
    warnings.extend(validate_metadata())
    warnings.extend(validate_data_files())

    print("Validation complete.")
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("No warnings.")


if __name__ == "__main__":
    main()
