# 情報工学入門

[![PDFをビルドしてPagesへ公開](https://github.com/tsuji-tomonori/cs-doc/actions/workflows/build-pdf.yml/badge.svg)](https://github.com/tsuji-tomonori/cs-doc/actions/workflows/build-pdf.yml)

新卒アプリケーションエンジニア向けに、コンピュータからAIまでを一冊の流れとして説明する技術書原稿です。
電気信号と論理回路から始め、CPU、プログラミング言語、OS、データ構造、ソフトウェア工学、ネットワーク、機械学習、LLMまでを扱います。

## 公開版

- [PDFを読む](https://tsuji-tomonori.github.io/cs-doc/information-engineering-basics.pdf)
- [閲覧ページを開く](https://tsuji-tomonori.github.io/cs-doc/)

PDFはA4縦の95ページです。
`main`ブランチへのpush時に、GitHub ActionsがLuaLaTeXで再生成し、GitHub Pagesへ公開します。
Pull Requestでは組版と品質検証だけを実行します。

## 読み物としての構成

各章は、概要と「この章で学ぶこと」から始まります。
本文は、定義、仕組み、成立条件、実務での観測方法を文章でつなぎ、図表を本文から参照する構成です。用語の説明は行内から始まる段落とし、手順、演習、確認問題のように順序や項目の区別が必要な箇所だけを列挙します。
章末には要点、確認問題、または手を動かす実習を置いています。

| 範囲 | 本文ページ | 主題 |
| --- | ---: | --- |
| はじめに | ii–iii | 本書の目的、対象読者、全体像、読み進め方 |
| 第1章 | 1–10 | 電気信号、2進表現、論理回路、記憶、CPU |
| 第2章 | 11–18 | 機械語、コンパイラ、AST、再帰、DFS、BFS |
| 第3章 | 19–29 | OS、仮想メモリ、型、計算量、配列、スライス、マップ |
| 第4章 | 30–41 | ソフトウェア危機、抽象化、モジュール、UML、設計原則 |
| 第5章 | 42–52 | 階層化、IP、DNS、TCP、UDP、QUIC、TLS、HTTP |
| 第6章 | 53–69 | 数学、回帰、分類、ニューラルネット、Transformer、LLM |
| 第7章 | 70–78 | 全階層の統合、障害調査、学習ガイド、総合演習 |
| 参考文献 | 79–83 | 大学教材、公式仕様、RFC、原著論文へのリンク |

推奨目次との対応は[網羅表](docs/coverage.md)に記録しています。

## ローカルビルド

LuaLaTeX、latexmk、Noto CJKフォント、Popplerが必要です。

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

`make verify`は、組版警告、A4判定、ページ数、本文量、外部リンク、書体埋め込み、Beamer命令の残存を検査します。

## リポジトリ構成

- `main.tex`：書籍全体のエントリーポイント
- `chapters/`：章ごとのLaTeX原稿
- `tex/preamble.tex`：A4ページ、書体、配色、共通レイアウト
- `tex/macros.tex`：章導入、学習内容、要点、出典の共通部品
- `assets/`：画像と生成記録
- `docs/coverage.md`：推奨目次と本文の対応
- `site/`：公開ページ
- `.github/workflows/build-pdf.yml`：ビルド、検証、Pages公開
- `.workspace/`：執筆時の目次、参照資料一覧、デザイン規定

## 組版とデザイン

本文はA4縦で、可読性を優先した明朝体です。
見出し、図中の文字、コードにはゴシック体または等幅書体を使います。
背景は白、本文はディープネイビー、アクセントはくすんだ青に限定し、背景装飾、グラデーション、強い影は使いません。

表紙の概念図は画像生成を用いて作成しました。
生成条件とプロンプトは[画像記録](assets/README.md)に残しています。
本文の構成図、回路図、グラフはTeX/TikZで作成しています。

## 参考資料

参考文献章から、大学の公開教材、言語の公式仕様、IETFのRFC、原著論文を参照できます。
外部PDFはリポジトリへ転載せず、リンクと独自の要約だけを収録しています。
