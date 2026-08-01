#!/usr/bin/env python3
"""Generate and validate the section-to-authoritative-source registry."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs/section-evidence.md"
REPORT = ROOT / "build/section-evidence.json"

CHAPTERS = [
    ("H", "はじめに", "00-introduction.tex"),
    ("1", "第1章", "01-digital-computer.tex"),
    ("2", "第2章", "02-language.tex"),
    ("3", "第3章", "03-runtime-data.tex"),
    ("4", "第4章", "04-software-engineering.tex"),
    ("5", "第5章", "05-internet.tex"),
    ("6", "第6章", "06-request-delivery.tex"),
    ("7", "第7章", "07-language-model.tex"),
    ("8", "第8章", "08-browser.tex"),
    ("9", "第9章", "09-practice.tex"),
]

SOURCES = {
    "REPO": ("本書のスコープと学習設計", "一次資料", "https://github.com/tsuji-tomonori/cs-doc"),
    "MIT6004": ("MIT 6.004 Computation Structures", "大学公式教材", "https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/"),
    "IEEE754": ("IEEE 754-2019", "国際標準", "https://standards.ieee.org/ieee/754/6210/"),
    "UNICODE": ("The Unicode Standard 17.0", "公式仕様", "https://www.unicode.org/versions/Unicode17.0.0/core-spec/"),
    "RISCV": ("RISC-V Instruction Set Manual", "公式仕様", "https://github.com/riscv/riscv-isa-manual"),
    "LLVM": ("LLVM Tutorial: My First Language Frontend", "公式文書", "https://llvm.org/docs/tutorial/"),
    "MIT6006": ("MIT 6.006 Introduction to Algorithms", "大学公式教材", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/"),
    "OSTEP": ("Operating Systems: Three Easy Pieces", "大学公開教科書", "https://pages.cs.wisc.edu/~remzi/OSTEP/"),
    "GOSPEC": ("The Go Programming Language Specification", "公式仕様", "https://go.dev/ref/spec"),
    "GOGC": ("A Guide to the Go Garbage Collector", "公式文書", "https://go.dev/doc/gc-guide"),
    "PYDATA": ("Python Data Model", "公式仕様", "https://docs.python.org/3/reference/datamodel.html"),
    "PARNAS": ("On the Criteria To Be Used in Decomposing Systems into Modules", "原著論文", "https://doi.org/10.1145/361598.361623"),
    "DIJKSTRA": ("Notes on Structured Programming", "原著資料", "https://www.cs.utexas.edu/~EWD/transcriptions/EWD02xx/EWD249.html"),
    "UML": ("OMG UML 2.5.1", "公式仕様", "https://www.omg.org/spec/UML/2.5.1/PDF"),
    "SWEBOK": ("SWEBOK Guide", "専門団体公式", "https://www.computer.org/education/bodies-of-knowledge/software-engineering"),
    "ISO25010": ("ISO/IEC 25010:2023", "国際標準", "https://www.iso.org/standard/78176.html"),
    "X200": ("ITU-T X.200 OSI Basic Reference Model", "国際標準", "https://www.itu.int/rec/T-REC-X.200/en"),
    "RFC1122": ("RFC 1122 — Requirements for Internet Hosts", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc1122.html"),
    "RFC8200": ("RFC 8200 — IPv6", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc8200.html"),
    "RFC4271": ("RFC 4271 — BGP-4", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc4271.html"),
    "RFC1034": ("RFC 1034 — Domain Names", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc1034.html"),
    "RFC6335": ("RFC 6335 — Service Names and Port Numbers", "Best Current Practice", "https://www.rfc-editor.org/rfc/rfc6335.html"),
    "RFC9293": ("RFC 9293 — TCP", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc9293.html"),
    "RFC768": ("RFC 768 — UDP", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc768.html"),
    "RFC9000": ("RFC 9000 — QUIC", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc9000.html"),
    "RFC9110": ("RFC 9110 — HTTP Semantics", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc9110.html"),
    "RFC9111": ("RFC 9111 — HTTP Caching", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc9111.html"),
    "RFC8446": ("RFC 8446 — TLS 1.3", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc8446.html"),
    "RFC5280": ("RFC 5280 — X.509 PKI", "インターネット標準", "https://www.rfc-editor.org/rfc/rfc5280.html"),
    "CS229": ("Stanford CS229 Machine Learning", "大学公式教材", "https://cs229.stanford.edu/"),
    "D2L": ("Dive into Deep Learning", "査読付き公開教科書", "https://d2l.ai/"),
    "PERCEPTRON": ("The Perceptron", "原著論文", "https://doi.org/10.1037/h0042519"),
    "BACKPROP": ("Learning representations by back-propagating errors", "原著論文", "https://doi.org/10.1038/323533a0"),
    "TRANSFORMER": ("Attention Is All You Need", "原著論文", "https://proceedings.neurips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html"),
    "CS224N": ("Stanford CS224N", "大学公式教材", "https://web.stanford.edu/class/cs224n/"),
    "NISTGENAI": ("NIST AI 600-1 Generative AI Profile", "政府公式文書", "https://doi.org/10.6028/NIST.AI.600-1"),
    "HTML": ("HTML Living Standard", "公式仕様", "https://html.spec.whatwg.org/"),
    "DOM": ("DOM Living Standard", "公式仕様", "https://dom.spec.whatwg.org/"),
    "CSSOM": ("CSS Object Model", "公式仕様", "https://drafts.csswg.org/cssom/"),
    "FETCH": ("Fetch Standard", "公式仕様", "https://fetch.spec.whatwg.org/"),
    "ECMA262": ("ECMAScript Language Specification", "公式仕様", "https://tc39.es/ecma262/"),
    "LCP": ("Largest Contentful Paint", "公式仕様", "https://www.w3.org/TR/largest-contentful-paint/"),
    "INP": ("Interaction to Next Paint", "ブラウザ公式文書", "https://web.dev/articles/inp"),
    "OTEL": ("OpenTelemetry Specification", "公式仕様", "https://opentelemetry.io/docs/specs/otel/"),
    "SRE": ("Site Reliability Engineering", "公式実務書", "https://sre.google/sre-book/table-of-contents/"),
}


def source_ids(chapter: str, title: str) -> list[str]:
    if chapter == "H":
        return ["PARNAS"] if title == "見えない層" else ["REPO"]
    if chapter == "1":
        if "ビット列" in title:
            return ["UNICODE", "IEEE754"]
        return ["MIT6004"]
    if chapter == "2":
        if re.search(r"命令セット|機械語|高級言語|実行方式", title):
            return ["RISCV"]
        if re.search(r"コンパイル|字句解析|構文解析|抽象構文木|AST|式を木|プロセスへ", title):
            return ["LLVM"]
        return ["MIT6006"]
    if chapter == "3":
        if "Python" in title:
            return ["PYDATA"]
        if re.search(r"Go|型|サイズ|値渡し|スライス|append|マップ", title):
            return ["GOSPEC"]
        if re.search(r"計算量|配列|データ構造|置き方", title):
            return ["MIT6006"]
        if re.search(r"GC|ガベージ", title):
            return ["GOGC"]
        return ["OSTEP"]
    if chapter == "4":
        if re.search(r"クラス図|シーケンス図|モデル", title):
            return ["UML"]
        if "品質" in title:
            return ["ISO25010"]
        if re.search(r"テスト|危機|ケース|変更要求", title):
            return ["SWEBOK"]
        if re.search(r"構造化|分割統治", title):
            return ["DIJKSTRA"]
        return ["PARNAS"]
    if chapter == "5":
        if "DNS" in title:
            return ["RFC1034"]
        if re.search(r"IPアドレス|CIDR", title):
            return ["RFC8200"]
        if re.search(r"ルーティング|網の網|経路制御|耐障害", title):
            return ["RFC4271"]
        if re.search(r"OSI|階層化", title):
            return ["X200"]
        return ["RFC1122"]
    if chapter == "6":
        if "ポート" in title:
            return ["RFC6335"]
        if re.search(r"TCP|フロー制御|輻輳制御", title):
            return ["RFC9293"]
        if "UDP" in title:
            return ["RFC768"]
        if "QUIC" in title:
            return ["RFC9000"]
        if title == "TLS":
            return ["RFC8446"]
        if "証明書" in title:
            return ["RFC5280", "RFC8446"]
        if "サーバーの手前" in title:
            return ["RFC9111"]
        return ["RFC9110"]
    if chapter == "7":
        if re.search(r"Attention|Query|Key|Value|位置情報|Transformer", title):
            return ["TRANSFORMER"]
        if re.search(r"トークン|プロンプト|コンテキスト|文章生成|次トークン", title):
            return ["CS224N"]
        if re.search(r"データ漏洩|偏り|分布変化|ハルシネーション|評価", title):
            return ["NISTGENAI"]
        if "誤差逆伝播" in title:
            return ["BACKPROP"]
        if "パーセプトロン" in title:
            return ["PERCEPTRON"]
        if re.search(r"ニューロン|順伝播|系列データ|ベクトル|行列", title):
            return ["D2L"]
        return ["CS229"]
    if chapter == "8":
        if "初回表示" in title:
            return ["LCP", "INP"]
        if "fetch" in title:
            return ["FETCH"]
        if re.search(r"JavaScript|イベントループ", title):
            return ["ECMA262", "HTML"]
        if "CSSOM" in title:
            return ["CSSOM"]
        if re.search(r"HTML|DOM", title):
            return ["DOM", "HTML"]
        return ["HTML"]
    if chapter == "9":
        if re.search(r"通信経路|通信障害", title):
            return ["RFC8446", "RFC9293"]
        if "コードから実行" in title:
            return ["LLVM", "OSTEP"]
        if "メモリ" in title:
            return ["GOGC", "OSTEP"]
        if re.search(r"機械学習|AI品質", title):
            return ["NISTGENAI"]
        if "描画" in title:
            return ["LCP", "INP"]
        if re.search(r"観測|遅延|障害調査|評価方法", title):
            return ["OTEL", "SRE"]
        if "変更容易性" in title:
            return ["ISO25010"]
        return ["SRE"]
    raise ValueError(chapter)


def main() -> int:
    rows: list[dict[str, object]] = []
    for prefix, chapter_name, filename in CHAPTERS:
        text = (ROOT / "chapters" / filename).read_text(encoding="utf-8")
        for index, match in enumerate(
            re.finditer(r"^\\section\{([^}]+)\}", text, flags=re.MULTILINE), 1
        ):
            title = match.group(1)
            ids = source_ids(prefix, title)
            rows.append(
                {
                    "section": f"{prefix}.{index}.",
                    "chapter": chapter_name,
                    "title": title,
                    "source_ids": ids,
                }
            )

    failures = [
        {"section": row["section"], "source": source_id}
        for row in rows
        for source_id in row["source_ids"]
        if source_id not in SOURCES
    ]
    report = {
        "section_count": len(rows),
        "source_count": len(SOURCES),
        "failure_count": len(failures),
        "rows": rows,
        "failures": failures,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# 節ごとの根拠対応表",
        "",
        "第1〜9章と「はじめに」の各節について、内容を照合する第一候補の公式仕様、標準、原著論文、大学公式教材を示します。本文の流れを重くしないため、根拠の追跡情報をここへ集約しています。複数資料を示す節では、保証範囲が異なるため両方を確認します。",
        "",
        "| 節 | 区分 | 節名 | 主要根拠 | 資料種別 | 照合観点 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        source_links = []
        source_types = []
        for source_id in row["source_ids"]:
            title, source_type, url = SOURCES[source_id]
            source_links.append(f"[{title}]({url})")
            source_types.append(source_type)
        lines.append(
            f"| {row['section']} | {row['chapter']} | {row['title']} | "
            f"{' / '.join(source_links)} | {' / '.join(source_types)} | "
            "定義・保証範囲・因果関係 |"
        )
    lines.extend(
        [
            "",
            "## 運用ルール",
            "",
            "- 節を追加または改名したときは、この表を再生成し、根拠の空欄がないことを確認します。",
            "- 実装依存の説明には公式実装文書を、相互運用上の保証には標準仕様を優先します。",
            "- 学習順序の判断には大学公式教材を使い、規範要件の代わりにはしません。",
        ]
    )
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if failures or len(rows) != 186:
        print(
            f"section evidence failed: {len(rows)} sections, {len(failures)} source errors"
        )
        return 1
    print(f"section evidence passed: {len(rows)} sections, {len(SOURCES)} sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
