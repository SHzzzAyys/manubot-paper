#!/usr/bin/env python
"""Replace configured wording with milder alternatives in repository docs and D-drive outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
LEGACY_RULES_PATH = REPO / "data" / "wording_substitutions.json"
PROFILE_DIR = REPO / "data" / "wording-profiles"

ACADEMIC_TARGETS = [
    REPO / "content",
    REPO / "docs" / "intelligence",
    REPO / "docs" / "daily-toxo-search-workflow.md",
    REPO / "docs" / "research-hub-workflow.md",
    Path(r"D:\ToxoVault\ResearchProject\outputs\daily-search"),
    Path(r"D:\ToxoVault\ResearchProject\outputs\research-hub")
]

DAILY_TARGETS = [
    REPO / "docs" / "daily-toxo-search-workflow.md",
    REPO / "docs" / "research-hub-workflow.md",
    Path(r"D:\ToxoVault\ResearchProject\outputs\daily-search"),
    Path(r"D:\ToxoVault\ResearchProject\outputs\research-hub")
]

TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".csv"}


def load_rules(profile: str) -> list[tuple[str, str]]:
    profile_path = PROFILE_DIR / f"{profile}.json"
    if profile_path.exists():
        rules = json.loads(profile_path.read_text(encoding="utf-8"))
    else:
        rules = json.loads(LEGACY_RULES_PATH.read_text(encoding="utf-8"))
    # Longer keys first to avoid partial replacement before specific replacement.
    return sorted(rules.items(), key=lambda item: len(item[0]), reverse=True)


def default_targets(profile: str) -> list[Path]:
    if profile == "daily":
        return DAILY_TARGETS
    return ACADEMIC_TARGETS


def iter_files(targets: list[Path]) -> list[Path]:
    files: list[Path] = []
    for target in targets:
        if not target.exists():
            continue
        if target.is_file():
            if target.suffix.lower() in TEXT_SUFFIXES:
                files.append(target)
            continue
        for path in target.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                files.append(path)
    return sorted(set(files))


def sanitize_text(text: str, rules: list[tuple[str, str]]) -> tuple[str, int]:
    count = 0
    for old, new in rules:
        hits = text.count(old)
        if hits:
            text = text.replace(old, new)
            count += hits
    return text, count


def main() -> int:
    parser = argparse.ArgumentParser(description="Replace configured wording with milder alternatives.")
    parser.add_argument(
        "--profile",
        choices=["academic", "daily"],
        default="academic",
        help="Replacement profile. academic is more suitable for formal writing; daily is more relaxed.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report replacements without writing files.")
    parser.add_argument("targets", nargs="*", help="Optional file or directory targets.")
    args = parser.parse_args()

    targets = [Path(item) for item in args.targets] if args.targets else default_targets(args.profile)
    rules = load_rules(args.profile)
    total_files = 0
    total_replacements = 0

    for path in iter_files(targets):
        text = path.read_text(encoding="utf-8", errors="ignore")
        updated, replaced = sanitize_text(text, rules)
        if replaced == 0:
            continue
        total_files += 1
        total_replacements += replaced
        if not args.dry_run:
            path.write_text(updated, encoding="utf-8")
        print(f"{path}: {replaced}")

    mode = "Dry run" if args.dry_run else "Updated"
    print(f"{mode} {total_files} files with {total_replacements} replacements using profile={args.profile}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
