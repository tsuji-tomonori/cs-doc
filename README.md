# 情報工学の基礎

[![PDFをビルドしてPagesへ公開](https://github.com/tsuji-tomonori/cs-doc/actions/workflows/build-pdf.yml/badge.svg)](https://github.com/tsuji-tomonori/cs-doc/actions/workflows/build-pdf.yml)

新卒アプリケーションエンジニア向けの社内研修教材です。
電気信号と論理回路から始め、CPU、プログラミング言語、OS、データ構造、ソフトウェア工学、ネットワーク、機械学習、LLMまでを一つの流れで扱います。

## 公開版

- [PDFを開く](https://tsuji-tomonori.github.io/cs-doc/information-engineering-basics.pdf)
- [閲覧ページ](https://tsuji-tomonori.github.io/cs-doc/)

`main`ブランチへのpush時に、GitHub ActionsがLuaLaTeXでPDFを再生成し、GitHub Pagesへ公開します。Pull Requestでは組版と品質検証だけを実行します。

## 教材の構成

| 範囲 | ページ | 主題 |
| --- | ---: | --- |
| 序章 | 1–4 | 研修の目的、全体像、学習方法 |
| 第1章 | 5–25 | 電気信号、2進表現、論理回路、記憶、CPU |
| 第2章 | 26–42 | 機械語、コンパイラ、AST、再帰、DFS、BFS |
| 第3章 | 43–64 | OS、仮想メモリ、型、計算量、配列、スライス、マップ |
| 第4章 | 65–88 | ソフトウェア危機、抽象化、モジュール、UML、設計原則 |
| 第5章 | 89–112 | 階層化、IP、DNS、TCP、UDP、QUIC、TLS、HTTP |
| 第6章 | 113–149 | 数学、回帰、分類、ニューラルネット、Transformer、LLM |
| 終章 | 150–169 | 全階層の統合、障害調査、学習ガイド、総合演習 |
| 参考文献 | 170–177 | 大学教材、公式仕様、RFC、原著論文へのリンク |

目次との詳しい対応は[網羅表](docs/coverage.md)に記録しています。

## ローカルビルド

LuaLaTeX、latexmk、Noto Sans CJK JPが必要です。

Ubuntuでは、次のパッケージ構成でビルドできます。

```bash
sudo apt-get install latexmk texlive-luatex texlive-lang-japanese \
  texlive-latex-extra texlive-fonts-recommended fonts-noto-cjk poppler-utils
```

```bash
make pdf
make verify
make site
```

主な生成物は次のとおりです。

- `build/information-engineering-basics.pdf`：配布用PDF
- `site/information-engineering-basics.pdf`：GitHub Pages用PDF

`make verify`は、組版警告、ページ数、外部リンク注釈を検査します。

## リポジトリ構成

- `main.tex`：エントリーポイント
- `chapters/`：章ごとの本文
- `tex/preamble.tex`：配色、書体、共通レイアウト
- `assets/`：画像と生成記録
- `docs/coverage.md`：推奨目次と教材の対応
- `site/`：公開ページ
- `.github/workflows/build-pdf.yml`：ビルド、検証、Pages公開
- `.workspace/`：執筆時の目次、参照資料一覧、デザイン規定

## デザイン

ページは16:9です。
背景はオフホワイト、本文はディープネイビー、アクセントはくすんだ青に固定しています。
背景装飾、グラデーション、強い影は使いません。

表紙の概念図は画像生成を用いて作成しました。生成条件とプロンプトは[画像記録](assets/README.md)に残しています。本文の構成図、回路図、グラフはTeX/TikZで作成しています。

## 参考資料

教材内の参考文献章から、大学の公開教材、言語の公式仕様、IETFのRFC、原著論文を参照できます。外部PDFはリポジトリへ転載せず、リンクと独自の要約だけを収録しています。
