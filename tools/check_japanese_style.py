#!/usr/bin/env python3
"""Check the enforceable rules in docs/writing-guide.md."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "build" / "japanese-style.json"
CHAPTERS = [
    "00-introduction.tex",
    "01-digital-computer.tex",
    "02-language.tex",
    "03-runtime-data.tex",
    "04-software-engineering.tex",
    "05-internet.tex",
    "06-request-delivery.tex",
    "07-language-model.tex",
    "08-browser.tex",
    "09-practice.tex",
    "90-appendix-environment.tex",
    "91-appendix-answers.tex",
]
PROHIBITED = {
    "full_width_digit": re.compile(r"[０-９]"),
    "redundant_capability": re.compile(r"することができます"),
    "empty_preview": re.compile(r"見ていきます"),
    "em_dash": re.compile(r"[—―]{2,}"),
}


def strip_non_prose(text: str) -> str:
    for environment in (
        "lstlisting",
        "figure",
        "table",
        "tikzpicture",
        "tabular",
        "tabularx",
        "longtable",
        "learninggoals",
        "align",
        "align*",
        "equation",
        "equation*",
    ):
        text = re.sub(
            rf"\\begin\{{{re.escape(environment)}\}}.*?"
            rf"\\end\{{{re.escape(environment)}\}}",
            "",
            text,
            flags=re.DOTALL,
        )
    text = re.sub(r"\\\[.*?\\\]", "", text, flags=re.DOTALL)
    text = re.sub(
        r"(?m)^\s*\\(?:chapter|section|subsection|label|input|source|"
        r"chapterimage|begin|end|takeaway)\b.*$",
        "",
        text,
    )
    text = re.sub(r"(?m)^\s*%.*$", "", text)
    return text


def main() -> int:
    issues = []
    long_sentences = []
    multi_term_sentences = []
    files = [ROOT / "chapters" / filename for filename in CHAPTERS]
    files.extend(sorted((ROOT / "chapters" / "terms").glob("*.tex")))

    for path in files:
        text = path.read_text(encoding="utf-8")
        relative = str(path.relative_to(ROOT))
        for line_number, line in enumerate(text.splitlines(), 1):
            for rule, pattern in PROHIBITED.items():
                if pattern.search(line):
                    issues.append(
                        {"file": relative, "line": line_number, "rule": rule}
                    )

        prose = strip_non_prose(text)
        for sentence in re.split(r"(?<=[。！？])", prose):
            terms = re.findall(r"\\term\{([^{}]+)\}", sentence)
            if len(terms) > 1:
                multi_term_sentences.append(
                    {"file": relative, "terms": terms}
                )
            plain = re.sub(r"\\[A-Za-z]+(?:\[[^]]*\])?", "", sentence)
            plain = re.sub(r"[{}$]", "", plain)
            plain = " ".join(plain.split())
            if len(plain) > 90:
                long_sentences.append(
                    {
                        "file": relative,
                        "length": len(plain),
                        "sentence": plain,
                    }
                )

    report = {
        "prohibited_expression_count": len(issues),
        "multi_term_sentence_count": len(multi_term_sentences),
        "long_sentence_review_count": len(long_sentences),
        "issues": issues,
        "multi_term_sentences": multi_term_sentences,
        "long_sentences_for_review": long_sentences,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if issues or multi_term_sentences:
        print(
            "Japanese style failed: "
            f"{len(issues)} prohibited expressions, "
            f"{len(multi_term_sentences)} multi-term sentences"
        )
        return 1
    print(
        "Japanese style passed: "
        f"{len(long_sentences)} long sentences recorded for review"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
