# 情報工学入門

[![PDFをビルドしてPagesへ公開](https://github.com/tsuji-tomonori/cs-doc/actions/workflows/build-pdf.yml/badge.svg)](https://github.com/tsuji-tomonori/cs-doc/actions/workflows/build-pdf.yml)

新卒アプリケーションエンジニア向けに、物理からアプリまでを一つの出来事として描く技術書原稿です。
利用者がAIアプリへ「注文番号1234はいつ届きますか」と送ってから応答を受け取るまでを追い、電気信号、CPU、言語、OS、データ、設計、分散網、要求配送、LLM、ブラウザ描画へ順に視点を移します。

## 公開版

- [PDFを読む](https://tsuji-tomonori.github.io/cs-doc/information-engineering-basics.pdf)
- [閲覧ページを開く](https://tsuji-tomonori.github.io/cs-doc/)

PDFはA4縦で、「はじめに」、第1〜9章、付録、参考文献、索引を収録します。
`main`ブランチへのpush時に、GitHub ActionsがLuaLaTeXで再生成し、GitHub Pagesへ公開します。
Pull Requestでは組版と品質検証だけを実行します。

## 物語としての構成

各章は「はじめに」と到達目標から始まり、要求がいまどこにいるかを示します。
節は前の節で残った問いから次の概念を導き、章末は結論で閉じず、まだ見えていない層を次章へ渡します。用語の説明は流れの中へ置き、手順、観測、問いのように順序や区別が必要な箇所だけを列挙します。
第8章で同じ応答を画面まで戻します。
第9章では、遅延、メモリ、通信、描画、設計、AI品質の問題が起きたときに、物語のどこへ戻るかを扱います。

| 範囲 | 節数 | 主題 |
| --- | ---: | --- |
| はじめに | 5 | 一つの送信、見えない層、九つの場面、読み進め方 |
| 第1章 信号から計算へ | 20 | 電気信号から論理回路、記憶、CPUまで |
| 第2章 コードから命令へ | 16 | ソースコードからAST、機械語、実行順序まで |
| 第3章 プログラムが動く場所 | 21 | OS、メモリ、型、データ構造による実行の舞台 |
| 第4章 変更を支える設計 | 23 | 変更を局所化する境界、モデル、テスト |
| 第5章 インターネットという分散網 | 17 | IP、AS、BGP、DNSから成る網の網 |
| 第6章 要求が届くまで | 16 | TCP、QUIC、TLS、HTTPによる配送 |
| 第7章 言葉が応答になるまで | 36 | 文字列からトークン、Transformer、生成、評価まで |
| 第8章 応答が画面になるまで | 11 | DOM、CSSOM、レイアウト、ペイント、合成 |
| 第9章 一つの応答をたどる | 21 | 全経路の再統合、観測、障害調査、総合演習 |
| 付録・参考文献・索引 | 4区分 | 環境、解答、根拠資料、用語の検索 |

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

`make verify`は、組版警告、A4判定、ページ数、本文量、外部リンク、書体埋め込み、カタログの186節と600用語、文体規則を検査します。

## リポジトリ構成

- `main.tex`：書籍全体のエントリーポイント
- `chapters/`：章ごとのLaTeX原稿
- `tex/preamble.tex`：A4ページ、書体、配色、共通レイアウト
- `tex/macros.tex`：章の導入、到達目標、要点、用語、出典の共通部品
- `assets/`：画像と生成記録
- `docs/coverage.md`：改訂カタログと本文の対応
- `docs/writing-guide.md`：です・ます調と用語定義の執筆規約
- `site/`：公開ページ
- `.github/workflows/build-pdf.yml`：ビルド、検証、Pages公開
- `.workspace/`：執筆時の目次、参照資料一覧、デザイン規定

## 組版とデザイン

本文はA4縦で、可読性を優先した明朝体です。
見出し、図中の文字、コードにはゴシック体または等幅書体を使います。
背景は白、本文はディープネイビー、アクセントはくすんだ紫と桃色に限定し、背景装飾、グラデーション、強い影は使いません。

表紙と各章の概念図は画像生成を用いて作成しました。
生成条件とプロンプトは[画像記録](assets/README.md)に残しています。
本文の構成図、回路図、グラフはTeX/TikZで作成しています。

## 参考資料

参考文献章から、大学の公開教材、言語の公式仕様、IETFのRFC、原著論文を参照できます。
外部PDFはリポジトリへ転載せず、リンクと独自の要約だけを収録しています。
