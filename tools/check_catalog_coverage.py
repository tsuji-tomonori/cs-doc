#!/usr/bin/env python3
"""Validate chapter/term coverage against the attached revision catalog."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs" / "revision-catalog" / "term_index_candidates.md"
REPORT_JSON = ROOT / "build" / "catalog-coverage.json"
REPORT_MD = ROOT / "build" / "catalog-coverage.md"

CHAPTER_FILES = {
    "00": ROOT / "chapters" / "00-introduction.tex",
    "01": ROOT / "chapters" / "01-digital-computer.tex",
    "02": ROOT / "chapters" / "02-language.tex",
    "03": ROOT / "chapters" / "03-runtime-data.tex",
    "04": ROOT / "chapters" / "04-software-engineering.tex",
    "05": ROOT / "chapters" / "05-internet.tex",
    "06": ROOT / "chapters" / "06-request-delivery.tex",
    "07": ROOT / "chapters" / "07-language-model.tex",
    "08": ROOT / "chapters" / "08-browser.tex",
    "09": ROOT / "chapters" / "09-practice.tex",
    "A": ROOT / "chapters" / "90-appendix-environment.tex",
}

# Appendix terms are intentionally split across the environment and answer chapters.
APPENDIX_EXTRA = ROOT / "chapters" / "91-appendix-answers.tex"


def parse_terms() -> dict[str, list[str]]:
    terms: dict[str, list[str]] = defaultdict(list)
    row = re.compile(r"^\|\s*(00|0[1-9]|A)\s*\|[^|]*\|\s*([^|]+?)\s*\|")
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        match = row.match(line)
        if match:
            terms[match.group(1)].append(match.group(2).strip())
    return terms


def normalize_tex(text: str) -> str:
    replacements = {
        r"\_": "_",
        r"\&": "&",
        r"\%": "%",
        r"\#": "#",
        r"\texttt{": "",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    return text


def bold_terms(text: str) -> set[str]:
    return {
        normalize_tex(term.strip())
        for term in re.findall(r"\\term\{([^{}]+)\}", text)
    }


def main() -> int:
    expected = parse_terms()
    details: dict[str, object] = {}
    missing: list[dict[str, str]] = []
    all_text = "\n".join(
        path.read_text(encoding="utf-8") for path in CHAPTER_FILES.values()
    )
    all_text += "\n" + APPENDIX_EXTRA.read_text(encoding="utf-8")
    all_text += "\n" + "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "chapters" / "terms").glob("*.tex"))
    )
    normalized = normalize_tex(all_text)
    bold = bold_terms(all_text)

    # The catalog intentionally repeats cross-cutting terms in several chapters.
    # A technical textbook should define a term once at the first responsible
    # chapter, then use the same spelling thereafter.
    first_owner: dict[str, str] = {}
    for chapter, terms in expected.items():
        for term in terms:
            first_owner.setdefault(term, chapter)

    for chapter, terms in expected.items():
        unique_terms = list(dict.fromkeys(terms))
        covered = [term for term in unique_terms if term in normalized and term in bold]
        details[chapter] = {
            "catalog_rows": len(terms),
            "unique_terms": len(unique_terms),
            "defined_somewhere": len(covered),
        }

    for term, chapter in first_owner.items():
        if term not in normalized or term not in bold:
            missing.append({"chapter": chapter, "term": term})

    report = {
        "catalog_rows": sum(len(items) for items in expected.values()),
        "unique_terms": len(first_owner),
        "missing_count": len(missing),
        "chapters": details,
        "missing": missing,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# 改訂カタログ用語網羅レポート",
        "",
        f"- カタログ行数：{report['catalog_rows']}",
        f"- 未網羅：{report['missing_count']}",
        "",
        "| 章 | カタログ行 | 章内の固有用語 | 本文中で定義済み |",
        "| --- | ---: | ---: | ---: |",
    ]
    for chapter, item in details.items():
        lines.append(
            f"| {chapter} | {item['catalog_rows']} | {item['unique_terms']} | {item['defined_somewhere']} |"
        )
    if missing:
        lines.extend(["", "## 未網羅", ""])
        lines.extend(f"- {item['chapter']}：{item['term']}" for item in missing)
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if missing:
        print(f"catalog coverage failed: {len(missing)} missing terms")
        for item in missing[:40]:
            print(f"- chapter {item['chapter']}: {item['term']}")
        return 1

    print(f"catalog coverage passed: {report['catalog_rows']} term rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
