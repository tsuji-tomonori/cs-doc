#!/usr/bin/env python3
"""Validate chapter sections against the attached revision catalog."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "build" / "structure-coverage.json"

FILES = {
    "00": ("00_introduction.md", "00-introduction.tex"),
    "01": ("01_signal_to_computation.md", "01-digital-computer.tex"),
    "02": ("02_code_to_instruction.md", "02-language.tex"),
    "03": ("03_runtime_place.md", "03-runtime-data.tex"),
    "04": ("04_design_for_change.md", "04-software-engineering.tex"),
    "05": ("05_internet_distributed_network.md", "05-internet.tex"),
    "06": ("06_request_delivery.md", "06-request-delivery.tex"),
    "07": ("07_language_to_response.md", "07-language-model.tex"),
    "08": ("08_response_to_screen.md", "08-browser.tex"),
    "09": ("09_trace_one_response.md", "09-practice.tex"),
}


def catalog_sections(chapter: str, filename: str) -> list[str]:
    text = (ROOT / "docs" / "revision-catalog" / filename).read_text(encoding="utf-8")
    prefix = str(int(chapter))
    row = re.compile(rf"^\|\s*{prefix}\.(\d+)\s*\|\s*([^|]+?)\s*\|")
    return [
        match.group(2).strip()
        for line in text.splitlines()
        if (match := row.match(line))
    ]


def tex_sections(filename: str) -> list[str]:
    text = (ROOT / "chapters" / filename).read_text(encoding="utf-8")
    return re.findall(r"^\\section\{([^}]+)\}", text, flags=re.MULTILINE)


def main() -> int:
    chapters = {}
    failures = []
    for chapter, (catalog_file, tex_file) in FILES.items():
        expected = catalog_sections(chapter, catalog_file)
        actual = tex_sections(tex_file)
        chapters[chapter] = {
            "expected": expected,
            "actual": actual,
            "matched": expected == actual,
        }
        if expected != actual:
            failures.append(chapter)

    report = {
        "catalog_section_count": sum(
            len(item["expected"]) for item in chapters.values()
        ),
        "failed_chapters": failures,
        "chapters": chapters,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if failures:
        print("structure coverage failed: " + ", ".join(failures))
        return 1
    print(f"structure coverage passed: {report['catalog_section_count']} sections")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
