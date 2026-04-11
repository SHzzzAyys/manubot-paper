"""Demo-only helper for PR workflow examples.

This script is intentionally minimal and is not a production slug utility.
"""

from __future__ import annotations


def build_title_slug(title: str) -> str:
    """Build a simple demo-only slug from a title.

    This helper exists only to keep the PR example self-contained.
    Do not reuse it for branch names, file names, or URLs.
    """
    normalized = title.strip().lower()
    return normalized.replace(" ", "-")


def main() -> None:
    examples = [
        "Cat Toxo Vaccine Review",
        "Evidence Table Update",
    ]
    for title in examples:
        print(f"{title} -> {build_title_slug(title)}")


if __name__ == "__main__":
    main()
