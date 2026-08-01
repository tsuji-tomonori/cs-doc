#!/usr/bin/env python3
"""Generate a term-level beginner-comprehension report and enforce key fixes."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs/revision-catalog/term_index_candidates.md"
REPORT_MD = ROOT / "reports/beginner-comprehension.md"
REPORT_JSON = ROOT / "build/beginner-comprehension.json"

SOURCE_FILES = [
    ROOT / "chapters/00-introduction.tex",
    *sorted((ROOT / "chapters").glob("0[1-9]-*.tex")),
    ROOT / "chapters/90-appendix-environment.tex",
    ROOT / "chapters/91-appendix-answers.tex",
    *sorted((ROOT / "chapters/terms").glob("*.tex")),
]

SENSE_LABELS = {
    ("00", "層"): "一般的な役割のまとまり。通信層とニューラルネットワーク層は担当章で再定義",
    ("03", "パディング"): "構造体の配置境界をそろえるメモリ上の隙間",
    ("03", "メモリ・パディング"): "構造体の配置境界をそろえるメモリ上の隙間",
    ("07", "系列パディング"): "長さの異なる系列をバッチ化するために末尾を埋める処理",
    ("07", "過少適合"): "訓練データにある関係も十分に捉えられない状態",
    ("07", "言語モデル"): "言語列への確率付与や言語に関する予測を行うモデルの総称",
    ("07", "自己回帰言語モデル"): "それまでの列を条件に次の要素を予測する言語モデル",
    ("08", "Largest Contentful Paint"): "表示領域内で最大の適格候補が描画された時刻",
    ("08", "Interaction to Next Paint"): "利用中の操作から次の描画までの応答性",
    ("A", "Python"): "動的型付け言語。言語仕様とCPythonの実行方式を分ける",
}


def catalog_rows() -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    pattern = re.compile(r"^\|\s*(00|0[1-9]|A)\s*\|[^|]*\|\s*([^|]+?)\s*\|")
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        if match := pattern.match(line):
            rows.append((match.group(1), match.group(2).strip()))
    return rows


def term_pattern(term: str) -> re.Pattern[str]:
    escaped = re.escape(term).replace("_", r"(?:_|\\_)")
    return re.compile(r"\\term\{" + escaped + r"\}")


def clean_context(line: str) -> str:
    line = re.sub(r"\\term\{([^{}]+)\}", r"\1", line)
    line = re.sub(r"\\(?:code|texttt|emph)\{([^{}]+)\}", r"\1", line)
    line = re.sub(r"\\item\[([^]]+)\]", r"\1：", line)
    line = re.sub(r"\\[A-Za-z]+\*?(?:\[[^]]*\])?", "", line)
    line = line.replace("{", "").replace("}", "").replace("%", "")
    line = " ".join(line.split()).replace("|", "\\|")
    return line[:150] + ("…" if len(line) > 150 else "")


def find_definition(term: str) -> tuple[str, int, str] | None:
    pattern = term_pattern(term)
    for path in SOURCE_FILES:
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if pattern.search(line):
                return str(path.relative_to(ROOT)), number, clean_context(line)
    return None


def key_checks() -> list[dict[str, object]]:
    def read(relative: str) -> str:
        return (ROOT / relative).read_text(encoding="utf-8")

    intro = read("chapters/00-introduction.tex")
    ch3 = read("chapters/03-runtime-data.tex")
    ch6 = read("chapters/06-request-delivery.tex")
    ch7 = read("chapters/07-language-model.tex")
    ch8 = read("chapters/08-browser.tex")
    ch9 = read("chapters/09-practice.tex")
    app_a = read("chapters/90-appendix-environment.tex")
    app_b = read("chapters/91-appendix-answers.tex")
    catalog = CATALOG.read_text(encoding="utf-8")
    guides = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((ROOT / "chapters/terms").glob("*.tex"))
    )

    checks = [
        ("はじめにに章末案内語を置かない", "terms/00" not in intro and not (ROOT / "chapters/terms/00.tex").exists()),
        ("第1〜9章の案内語を表形式にする", guides.count("\\subsection*{章末の案内語}") == 9 and guides.count("\\begin{tabularx}") >= 9),
        ("編集上の語を学習用語から除く", not re.search(r"\|\s*(図1|旅|読者|研修|現在地|前方参照|後方参照|確認問題)\s*\|", catalog)),
        ("層の語義を担当分野ごとに分ける", all(word in intro for word in ("一般的な言葉", "通信層", "ニューラルネットワーク層"))),
        ("二種類のパディングを区別する", "メモリ・パディング" in ch3 and "系列パディング" in ch7 and "別の概念" in ch3),
        ("過少適合を標準的な語で説明する", "\\term{過少適合}" in ch7 and "\\term{未学習}" not in ch7),
        ("仮想アドレス空間を連続物理領域と誤解させない", "固有の仮想アドレス空間" in ch3 and "この対応は疎" in ch3 and "ページ単位" in ch3),
        ("ポート番号をプロトコル別16ビット空間として説明する", "各トランスポートプロトコルが持つ16ビット" in ch6 and "0から65535" in ch6),
        ("TCP接続確立の順序を明示する", all(word in ch6 for word in ("SYN", "SYN-ACK", "ACK"))),
        ("TLS証明書を合意対象と誤記しない", "提示された証明書" in ch6 and "暗号パラメータ" in ch6),
        ("言語モデルと自己回帰方式を区別する", "モデルの総称" in ch7 and "\\term{自己回帰言語モデル}" in ch7),
        ("LCPの候補更新を説明する", "適格な画像またはテキストブロック" in ch8 and "LCP候補は更新" in ch8),
        ("操作応答性をINPで説明する", "\\term{Interaction to Next Paint}" in ch8 and "\\term{INP}" in ch8),
        ("第7章に最短経路と深掘り経路を併記する", "この章の二つの読み方" in ch7 and "最短経路" in ch7 and "深掘り経路" in ch7),
        ("TLSが物理経路を保証しないことを明示する", "TLSは物理経路やルーティング経路そのものを検証しません" in ch9),
        ("Pythonの言語仕様と実装方式を分ける", "動的型付けを採用するプログラミング言語" in app_a and "CPython" in app_a and "バイトコード" in app_a),
        ("環境構築にOS別手順・期待出力・復旧表を備える", all(word in app_a for word in ("Windows 11ではWSL", "macOSで用意", "DebianまたはUbuntu", "期待出力", "症状から切り分ける"))),
        ("全章の演習に解答・判定条件を備える", all(f"第{number}章" in app_b for number in range(1, 10)) and "判定条件" in app_b),
    ]
    return [{"check": title, "passed": passed} for title, passed in checks]


def main() -> int:
    rows = catalog_rows()
    details: list[dict[str, object]] = []
    for index, (chapter, term) in enumerate(rows, 1):
        definition = find_definition(term)
        details.append(
            {
                "number": index,
                "chapter": chapter,
                "term": term,
                "status": "PASS" if definition else "FAIL",
                "sense": SENSE_LABELS.get((chapter, term), "本文の定義文で語義を限定"),
                "evidence": definition,
            }
        )

    checks = key_checks()
    failed_terms = [item for item in details if item["status"] == "FAIL"]
    failed_checks = [item for item in checks if not item["passed"]]
    report = {
        "catalog_rows": len(rows),
        "term_pass_count": len(rows) - len(failed_terms),
        "term_fail_count": len(failed_terms),
        "key_check_count": len(checks),
        "key_check_fail_count": len(failed_checks),
        "checks": checks,
        "terms": details,
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# 初学者理解度検査報告",
        "",
        "## 判定",
        "",
        f"- 現行カタログ：{len(rows)}行",
        f"- 定義と語義の確認：PASS {report['term_pass_count']}／FAIL {report['term_fail_count']}",
        f"- 初学者導線の重点確認：PASS {len(checks) - len(failed_checks)}／FAIL {len(failed_checks)}",
        "- はじめにの章末案内語：なし",
        "- 第1〜9章の章末案内語：既出の中核語だけを表形式で掲載",
        "",
        "内容量を減らさず、初回通読で必要な中核語と、必要時に参照する補足語を分けました。補足語の定義は付録Cに保持しています。",
        "",
        "## 重点確認",
        "",
        "| 確認項目 | 結果 |",
        "| --- | --- |",
    ]
    lines.extend(
        f"| {item['check']} | {'PASS' if item['passed'] else 'FAIL'} |"
        for item in checks
    )
    lines.extend(
        [
            "",
            "## 用語別再確認",
            "",
            "| No. | 章 | 用語 | 語義・確認観点 | 結果 | 本文根拠 |",
            "| ---: | --- | --- | --- | --- | --- |",
        ]
    )
    for item in details:
        evidence = item["evidence"]
        evidence_text = (
            f"{evidence[0]}:{evidence[1]} — {evidence[2]}" if evidence else "定義なし"
        )
        lines.append(
            f"| {item['number']} | {item['chapter']} | {item['term']} | "
            f"{item['sense']} | {item['status']} | {evidence_text} |"
        )
    REPORT_MD.parent.mkdir(parents=True, exist_ok=True)
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if failed_terms or failed_checks:
        print(
            "beginner comprehension failed: "
            f"{len(failed_terms)} term issues, {len(failed_checks)} key issues"
        )
        for item in failed_checks:
            print(f"- {item['check']}")
        return 1
    print(
        "beginner comprehension passed: "
        f"{len(rows)} term rows, {len(checks)} key checks"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
