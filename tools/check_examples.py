#!/usr/bin/env python3
"""Run textbook listings and compare their output with the printed answers."""

from __future__ import annotations

import difflib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
ANSWERS = "91-appendix-answers.tex"


def section(root: Path, filename: str, title: str) -> str:
    source = (root / "chapters" / filename).read_text(encoding="utf-8")
    sections = list(re.finditer(r"^\\section\{([^}]+)\}", source, re.MULTILINE))
    matches = [i for i, match in enumerate(sections) if match[1] == title]
    if len(matches) != 1:
        raise ValueError(f"{filename}: expected one section {title!r}")
    i = matches[0]
    end = sections[i + 1].start() if i + 1 < len(sections) else len(source)
    return source[sections[i].end():end]


def listings(source: str, language: str, count: int) -> list[str]:
    blocks = []
    for options, body in re.findall(
        r"\\begin\{lstlisting\}\[([^\]]+)\]\s*\n(.*?)\\end\{lstlisting\}",
        source, re.DOTALL,
    ):
        if re.search(r"(?:^|,)\s*language\s*=\s*" + re.escape(language) + r"\s*(?:,|$)", options):
            blocks.append(body.strip() + "\n")
    if len(blocks) != count:
        raise ValueError(f"expected {count} {language} listings, found {len(blocks)}")
    return blocks


def expected_output(source: str) -> str:
    block, = listings(source, "bash", 1)
    # The AST example prints its shell command before the expected stdout.
    return "\n".join(line for line in block.splitlines() if not line.startswith("$ "))


def compare_output(name: str, actual: str, expected: str) -> None:
    if actual.strip() != expected.strip():
        diff = "\n".join(difflib.unified_diff(
            expected.strip().splitlines(), actual.strip().splitlines(),
            fromfile="printed answer", tofile="execution", lineterm="",
        ))
        raise ValueError(f"{name}: output mismatch\n{diff}")
    print(f"PASS {name}: output matches the printed answer", flush=True)


def run(command: list[str], directory: Path) -> str:
    result = subprocess.run(
        command, cwd=directory, text=True, capture_output=True, timeout=180,
        env={**os.environ, "GOWORK": "off", "GOTOOLCHAIN": "local", "GOPROXY": "off"},
    )
    if result.returncode:
        raise ValueError(
            f"{' '.join(command)} exited {result.returncode}\n"
            f"{result.stdout}{result.stderr}"
        )
    return result.stdout


def check_python(root: Path, work: Path, chapter: str, title: str, answer: str) -> None:
    code, = listings(section(root, chapter, title), "Python", 1)
    path = work / "exercise.py"
    path.write_text(code, encoding="utf-8")
    compare_output(title, run([sys.executable, str(path)], work),
                   expected_output(section(root, ANSWERS, answer)))


def check_go(root: Path, work: Path) -> None:
    answer = section(root, ANSWERS, "第2章：式を木にする")
    code, driver = listings(answer, "Go", 2)
    ast_dir = work / "ast"
    ast_dir.mkdir()
    (ast_dir / "ast.go").write_text(code + driver, encoding="utf-8")
    compare_output("Go AST answer", run(["go", "run", "ast.go"], ast_dir),
                   expected_output(answer))

    # Exercise the shorter implementation printed in chapter 2 as well.
    # Reuse the answer's AST construction so the two versions receive the same input.
    basic, = listings(section(root, "02-language.tex", "手を動かす：式を木にする"), "Go", 1)
    marker = "    value, err := Eval(ast)"
    if driver.count(marker) != 1:
        raise ValueError("AST driver changed: review how the chapter 2 input is constructed")
    basic_driver = driver.split(marker)[0] + "    fmt.Println(Eval(ast))\n}\n"
    (ast_dir / "basic.go").write_text('package main\nimport "fmt"\n' + basic + basic_driver,
                                     encoding="utf-8")
    match = re.search(r"^value: (-?\d+) error: <nil>$", expected_output(answer), re.MULTILINE)
    if not match:
        raise ValueError("AST answer must contain a successful value line")
    compare_output("Go AST exercise", run(["go", "run", "basic.go"], ast_dir), match[1])

    benchmark, = listings(section(root, "03-runtime-data.tex", "手を動かす：置き方と速さ"), "Go", 1)
    package, = listings(section(root, ANSWERS, "第3章：置き方と速さ"), "Go", 1)
    bench_dir = work / "lookup-bench"
    bench_dir.mkdir()
    (bench_dir / "lookup_test.go").write_text(package + benchmark, encoding="utf-8")
    run(["go", "mod", "init", "example.com/lookup-bench"], bench_dir)
    output = run(["go", "test", "-bench=.", "-benchmem", "-count=5", "-benchtime=100ms"], bench_dir)
    for name in ("BenchmarkSliceIndex", "BenchmarkMapLookup"):
        rows = re.findall(r"^" + name + r"(?:-\d+)?\s+\d+\s+[\d.]+\s+ns/op\b", output, re.MULTILINE)
        if len(rows) != 5:
            raise ValueError(f"{name}: expected five measurements\n{output}")
    print("PASS Go benchmarks: five measurements each (timings are not assertions)", flush=True)
    print(output, end="", flush=True)


def main() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="cs-doc-examples-") as directory:
            work = Path(directory)
            check_python(ROOT, work, "01-digital-computer.tex", "手を動かす：数の表現", "第1章：数の表現")
            check_python(ROOT, work, "07-language-model.tex", "手を動かす：学習と汎化", "第7章：学習と汎化")
            check_go(ROOT, work)
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        print(f"Exercise verification failed: {exc}", file=sys.stderr)
        return 1
    print("Exercise verification passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
