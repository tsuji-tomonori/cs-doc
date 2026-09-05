#!/usr/bin/env python3
"""Verify that generated figures are complete 16:9 infographic slides."""

from __future__ import annotations

import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = sorted((ROOT / "chapters").glob("0[0-9]-*.tex"))
EXPECTED_SLIDES = {
    "ch00-overview.png",
    "ch01-signals.png",
    "ch02-code.png",
    "ch03-runtime.png",
    "ch03-data-structures.png",
    "ch04-design.png",
    "ch04-change-safety.png",
    "ch05-internet.png",
    "ch06-delivery.png",
    "ch07-language-model.png",
    "ch07-training-inference.png",
    "ch07-attention-generation.png",
    "ch08-browser.png",
    "ch09-observability.png",
    "ch09-evidence-correlation.png",
}


def png_size(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a valid PNG")
    return struct.unpack(">II", header[16:24])


def main() -> int:
    failures: list[str] = []
    macros = (ROOT / "tex" / "macros.tex").read_text(encoding="utf-8")
    readme = (ROOT / "assets" / "README.md").read_text(encoding="utf-8")

    for legacy in (r"\BookAnnotatedImage", "diagramlabel"):
        if legacy in macros:
            failures.append(f"legacy overlay mechanism remains: {legacy}")

    invocations: list[tuple[str, str, str]] = []
    pattern = re.compile(
        r"\\(?:chapterimage|sectionimage)"
        r"\{([^}]+\.png)\}\{([^}]+)\}\{([^}]+)\}"
    )
    for path in CHAPTERS:
        source = path.read_text(encoding="utf-8")
        if re.search(r"\\(?:chapterimage|sectionimage)\[", source):
            failures.append(f"{path.name}: legacy optional annotation remains")
        invocations.extend(pattern.findall(source))

    actual = {image for image, _, _ in invocations}
    if not EXPECTED_SLIDES.issubset(actual):
        missing = sorted(EXPECTED_SLIDES - actual)
        if missing:
            failures.append(f"missing slide references: {', '.join(missing)}")

    for chapter in CHAPTERS:
        source = chapter.read_text(encoding="utf-8")
        if r"\begin{tikzpicture}" in source:
            failures.append(f"{chapter.name}: a non-imagegen diagram remains")
        for filename in re.findall(r"\\inlineimage\{([^}]+)\}", source):
            invocations.append((filename, "本文内の図", "fig:inline"))

    for image, caption, label in invocations:
        path = ROOT / "assets" / image
        if not path.is_file():
            failures.append(f"{image}: file is missing")
            continue
        try:
            size = png_size(path)
        except ValueError as exc:
            failures.append(f"{image}: {exc}")
            continue
        if min(size) < 900 or abs(size[0] / size[1] - 16 / 9) > 0.01:
            failures.append(
                f"{image}: expected approximately 16:9 with at least 900px height, "
                f"found {size[0]}x{size[1]}"
            )
        if path.stat().st_size < 150_000:
            failures.append(f"{image}: unexpectedly small generated asset")
        if not caption.strip():
            failures.append(f"{image}: caption is empty")
        if not label.startswith("fig:"):
            failures.append(f"{image}: figure label must start with fig:")
        if image.startswith("generated/"):
            prompt = ROOT / "assets/image-prompts" / (Path(image).stem + ".txt")
            if not prompt.is_file():
                failures.append(f"{image}: generation prompt is missing")
        elif f"`{image}`" not in readme:
            failures.append(f"{image}: generation record is missing")

    if failures:
        print("figure slide check failed")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "figure slide check passed: "
        f"{len(invocations)} infographic slides meet 16:9 dimensions and generation-record checks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
