# cs-doc 改訂目次案 調査・執筆設計資料

作成日: 2026-07-28

このフォルダは、`情報工学入門 改訂目次案` を `cs-doc` に反映する前段の設計資料です。章ごとに、信頼できる大学・研究機関・標準化団体・公式仕様へのリンク、本文で書くべきこと、初出管理すべき用語候補を整理しています。

## ファイル

| 章 | タイトル | Markdown | 節数 | 用語数 |
| --- | --- | --- | --- | --- |
| 00 | はじめに | 00_introduction.md | 5 | 29 |
| 01 | 第1章 信号から計算へ | 01_signal_to_computation.md | 20 | 67 |
| 02 | 第2章 コードから命令へ | 02_code_to_instruction.md | 16 | 54 |
| 03 | 第3章 プログラムが動く場所 | 03_runtime_place.md | 21 | 69 |
| 04 | 第4章 変更を支える設計 | 04_design_for_change.md | 23 | 56 |
| 05 | 第5章 インターネットという分散網 | 05_internet_distributed_network.md | 17 | 62 |
| 06 | 第6章 要求が届くまで | 06_request_delivery.md | 16 | 59 |
| 07 | 第7章 言葉が応答になるまで | 07_language_to_response.md | 36 | 80 |
| 08 | 第8章 応答が画面になるまで | 08_response_to_screen.md | 11 | 53 |
| 09 | 第9章 一つの応答をたどる | 09_trace_one_response.md | 21 | 49 |
| A | 付録・参考文献・索引 | appendix_references_index.md | 4 | 29 |

## 編集方針

- 既存教材の「一つの送信を追う」物語線を維持します。
- 第5章を分散網、第6章を接続・HTTP・TLSへ分割します。
- 第8章としてブラウザ描画を新設し、第9章で全層を再統合します。
- 外部PDF・外部図表は転載せず、URL、出典の役割、独自の要約・図表だけを収録します。
- 各章の用語候補は索引および本文初出の太字化候補として扱います。

## Excel

`chapter_source_term_catalog.xlsx` に、Overview / Sections / Sources / Terms / Workplan の5シートで同じ内容を表形式に整理しています。
