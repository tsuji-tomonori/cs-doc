#!/usr/bin/env python3
"""Reject centered blocks that continue an open prose paragraph."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def previous_content(lines: list[str], index: int) -> tuple[int, str] | None:
    for previous in range(index - 1, -1, -1):
        content = lines[previous].strip()
        if content and not content.startswith("%"):
            return previous + 1, content
    return None


def starts_fresh_block(content: str) -> bool:
    return (
        content.startswith(r"\begingroup")
        or content.startswith(r"\begin{figure}")
        or content.startswith(r"\begin{center}")
        or content == "{"
        or r"\par" in content
    )


def main() -> int:
    failures: list[tuple[Path, int, int, str]] = []
    unsplittable_failures: list[tuple[Path, int]] = []
    for path in sorted((ROOT / "chapters").glob("*.tex")):
        lines = path.read_text(encoding="utf-8").splitlines()
        samepage_depth = 0
        for index, line in enumerate(lines):
            stripped = line.strip()
            if stripped == r"\begin{samepage}":
                samepage_depth += 1
            elif stripped == r"\end{samepage}":
                samepage_depth -= 1

            if stripped == r"\begin{center}" and samepage_depth == 0:
                unsplittable_failures.append((path.relative_to(ROOT), index + 1))

            if line.strip() != r"\centering":
                continue
            previous = previous_content(lines, index)
            if previous is None:
                continue
            previous_line, content = previous
            if not starts_fresh_block(content):
                failures.append(
                    (path.relative_to(ROOT), index + 1, previous_line, content)
                )

    if failures or unsplittable_failures:
        print(
            "layout source check failed: "
            f"{len(failures)} centered blocks continue an open paragraph; "
            f"{len(unsplittable_failures)} prose-centered blocks can split across pages"
        )
        for path, line, previous_line, content in failures:
            print(
                f"- {path}:{line}: add \\\\par before \\\\centering "
                f"(previous content at line {previous_line}: {content})"
            )
        for path, line in unsplittable_failures:
            print(
                f"- {path}:{line}: wrap the prose and centered block "
                "in a samepage environment"
            )
        return 1

    print(
        "layout source check passed: centered blocks start in fresh paragraphs "
        "and prose-centered blocks stay on one page"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
