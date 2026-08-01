#!/usr/bin/env python3
"""Validate that each chapter-end guide only summarizes already defined core terms."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "build" / "chapter-guide-check.json"

CHAPTER_FILES = {
    1: "01-digital-computer.tex",
    2: "02-language.tex",
    3: "03-runtime-data.tex",
    4: "04-software-engineering.tex",
    5: "05-internet.tex",
    6: "06-request-delivery.tex",
    7: "07-language-model.tex",
    8: "08-browser.tex",
    9: "09-practice.tex",
}

FORBIDDEN = re.compile(
    r"図\s*\d+|前方参照|後方参照|確認問題|現在地|旅|研修|読者|実務|演習|索引|参考文献|リンク切れ"
)


def section_before(text: str, position: int) -> str | None:
    sections = list(
        re.finditer(r"^\\section\{([^}]+)\}", text[:position], flags=re.MULTILINE)
    )
    return sections[-1].group(1) if sections else None


def main() -> int:
    failures: list[dict[str, object]] = []
    chapters: list[dict[str, object]] = []

    intro = (ROOT / "chapters" / "00-introduction.tex").read_text(encoding="utf-8")
    if "\\input{chapters/terms/00}" in intro or (ROOT / "chapters/terms/00.tex").exists():
        failures.append({"chapter": "はじめに", "rule": "no_introduction_guide"})

    for number, filename in CHAPTER_FILES.items():
        body_path = ROOT / "chapters" / filename
        guide_path = ROOT / "chapters" / "terms" / f"{number:02d}.tex"
        body = body_path.read_text(encoding="utf-8")
        guide = guide_path.read_text(encoding="utf-8")
        marker = f"\\input{{chapters/terms/{number:02d}}}"
        marker_positions = [match.start() for match in re.finditer(re.escape(marker), body)]
        last_section = max(
            (match.start() for match in re.finditer(r"^\\section\{", body, re.MULTILINE)),
            default=-1,
        )

        chapter_failures: list[str] = []
        if len(marker_positions) != 1:
            chapter_failures.append("guide_input_must_appear_once")
        elif marker_positions[0] < last_section:
            chapter_failures.append("guide_must_follow_last_section")
        if "\\subsection*{章末の案内語}" not in guide:
            chapter_failures.append("missing_guide_heading")
        if "\\begin{tabularx}" not in guide:
            chapter_failures.append("guide_must_be_table")

        rows = re.findall(
            r"\\guideterm\{([^{}]+)\}\s*&\s*([^&]+?)\s*&",
            guide,
        )
        if not 8 <= len(rows) <= 10:
            chapter_failures.append(f"core_term_count_{len(rows)}")

        term_details: list[dict[str, object]] = []
        for display, section_cell in rows:
            if FORBIDDEN.search(display):
                chapter_failures.append(f"editorial_term:{display}")
            defined_terms = display.split("／")
            actual_sections: list[str] = []
            for term in defined_terms:
                match = re.search(r"\\term\{" + re.escape(term) + r"\}", body)
                if match is None:
                    chapter_failures.append(f"not_defined_in_chapter:{term}")
                    continue
                actual = section_before(body, match.start())
                if actual is None:
                    chapter_failures.append(f"defined_before_first_section:{term}")
                    continue
                actual_sections.append(actual)
                if actual not in section_cell:
                    chapter_failures.append(
                        f"first_section_mismatch:{term}:{actual}:{section_cell.strip()}"
                    )
            term_details.append(
                {
                    "display": display,
                    "declared_first_section": section_cell.strip(),
                    "actual_first_sections": list(dict.fromkeys(actual_sections)),
                }
            )

        if chapter_failures:
            failures.extend(
                {"chapter": number, "rule": rule} for rule in chapter_failures
            )
        chapters.append(
            {
                "chapter": number,
                "guide_terms": len(rows),
                "passed": not chapter_failures,
                "terms": term_details,
            }
        )

    report = {
        "introduction_guide": False,
        "chapter_count": len(chapters),
        "guide_term_count": sum(item["guide_terms"] for item in chapters),
        "failure_count": len(failures),
        "chapters": chapters,
        "failures": failures,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    if failures:
        print(f"chapter guide check failed: {len(failures)} issues")
        for item in failures:
            print(f"- chapter {item['chapter']}: {item['rule']}")
        return 1
    print(
        "chapter guide check passed: "
        f"9 tables, {report['guide_term_count']} previously defined core terms"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
