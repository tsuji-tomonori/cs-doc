#!/usr/bin/env python3
"""Verify that generated figures carry readable labels inside the image area."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = sorted((ROOT / "chapters").glob("0[0-9]-*.tex"))
EXPECTED_SPECIALS = {
    "ch04-design.png",
    "ch07-attention-generation.png",
    "ch09-evidence-correlation.png",
}


def main() -> int:
    macros = (ROOT / "tex" / "macros.tex").read_text(encoding="utf-8")
    failures: list[str] = []

    if r"\newcommand{\BookAnnotatedImage}" not in macros:
        failures.append("BookAnnotatedImage macro is missing")
    if r"\colorbox{OffWhite}" in macros:
        failures.append("legacy below-image annotation box remains in macros")

    invocations: list[tuple[str, str, str]] = []
    pattern = re.compile(
        r"\\(?:chapterimage|sectionimage)\[([^]]+)\]"
        r"\{([^}]+\.png)\}\{([^}]+)\}\{[^}]+\}"
    )
    for path in CHAPTERS:
        source = path.read_text(encoding="utf-8")
        for annotation, image, caption in pattern.findall(source):
            invocations.append((annotation.strip(), image, caption.strip()))

    if len(invocations) != 15:
        failures.append(f"expected 15 annotated generated figures, found {len(invocations)}")

    for annotation, image, caption in invocations:
        if not annotation:
            failures.append(f"{image}: in-figure annotation is empty")
        if not caption:
            failures.append(f"{image}: caption is empty")

    for image in EXPECTED_SPECIALS:
        if f"\\ifstrequal{{#2}}{{{image}}}" not in macros:
            failures.append(f"{image}: dedicated in-figure labels are missing")

    if failures:
        print("figure annotation check failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "figure annotation check passed: "
        f"{len(invocations)} generated figures use in-figure labels"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
