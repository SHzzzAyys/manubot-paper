from __future__ import annotations


def build_title_slug(title: str) -> str:
    """Build a simple slug for demo purposes."""
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
