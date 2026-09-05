# 生成画像の記録

## 2026年9月5日の改訂

本文中の57点のTeX図を、Codex組み込みimagegenで生成したPNGへ置き換えました。
探索、配列拡張、通信、学習などの動作を追う図も12点追加しました。
使用画像は `generated/`、生成指示は `image-prompts/` に保存します。
`diagram-manifest.json` は旧図と置換先の対応記録です。
既存の15点の概念図と表紙もimagegen由来です。概念図のうち8点を今回再生成しました。
今回作成した77点の採用画像とプロンプト、ハッシュ値は `image-prompts/generation-record.json` に記録しています。

参考資料は、ローカルの `rag-guide/assets/image-prompts/README.md` と図版です。
16:9、オフホワイトの背景、ネイビーの文字、青の矢印、意味ごとにまとめた配置を参考にしました。
工程図は入力、途中状態、出力を追える構成とし、数値は教材用の例として示します。
生成後は、計算値、矢印、用語、縮小時の文字を確認します。確認結果は `reports/pdf-review.md` に記録します。

## 共通方針

章扉と本文挿絵は、2026年8月27日に Codex 組み込みの image-gen 2.0 で再制作しました。
参考にしたのは `tsuji-tomonori/rag-guide` の読み物向けスライドです。

- 16:9（1672×941 px）
- オフホワイト `#F7F6F1`、ディープネイビー `#2B3A4A`、くすんだ青 `#5E7E96`
- 「章ラベル → 要点を言い切るタイトル → 3〜5個の意味ブロック → 結論」の順に読む構成
- 工程名、比較軸、関係ラベルを対象と同じカードまたはレーンの中へ配置
- 画像下の説明帯、空のラベル欄、交差する配線、装飾だけの要素を使用しない
- A4本文へ縮小しても読める文字サイズと線幅を確保
- 生成原版から64色へ最適化し、文字と線の見た目を保ったままPDF容量を抑制

本文の `\chapterimage` と `\sectionimage` は完成したスライド画像をそのまま配置します。
旧方式のように TeX で画像下端へ注釈を重ねません。キャプションは図の参照と本文からの導線に限ります。

## 図版一覧

| ファイル | 図中の要点タイトル |
| --- | --- |
| `ch00-overview.png` | 一つの要求を追うと、情報工学の全体がつながる |
| `ch01-signals.png` | 電気の連続変化を二値へ区切ると、論理と計算が作れる |
| `ch02-code.png` | コンパイラは、コードを実行用の命令へ変換する |
| `ch03-runtime.png` | OSとランタイムは、異なる範囲を管理する |
| `ch03-data-structures.png` | データ構造は、使う操作から選ぶ |
| `ch04-design.png` | 境界を明確にすると、変更を小さく閉じ込められる |
| `ch04-change-safety.png` | 変更は小さく分け、段階ごとに確かめる |
| `ch05-internet.png` | ネットワークをつなぎ、名前から宛先を調べる |
| `ch06-delivery.png` | Web配信は、接続・保護・転送・処理を層として重ねる |
| `ch07-language-model.png` | 言語モデルは、文字列を確率へ変換し、次のトークンを選ぶ |
| `ch07-training-inference.png` | 学習はパラメータを変え、推論は固定したパラメータを使う |
| `ch07-attention-generation.png` | 次のトークンを選び、入力の列へ追加する |
| `ch08-browser.png` | 文書とスタイルから、画面を組み立てる |
| `ch09-observability.png` | 境界ごとに観測すると、障害箇所を段階的に絞り込める |
| `ch09-evidence-correlation.png` | 同じ要求と時刻で、観測結果を照らし合わせる |

## 生成プロンプトの骨格

```text
Use case: scientific-educational
Asset type: finished Japanese textbook infographic slide, 16:9 landscape
Layout: safe outer margins; small section label; takeaway title; short accent rule;
        3–5 clearly separated semantic cards or lanes; integrated takeaway callout
Palette: #F7F6F1, #2B3A4A, #5E7E96, pale blue-gray, #9AA4AD
Typography: readable Noto Sans JP-like sans serif with consistent hierarchy
Constraints: exact specified Japanese text; labels inside their semantic blocks;
             no detached legend, no bottom annotation strip, no crossing connectors;
             no gradients, shadows, 3D, decorative bubbles, logo, or watermark
```

工程図・比較図・二層構造・証拠の集約図は同じテンプレートへ押し込まず、内容に合うレイアウトを個別指定しました。
生成後は各画像を原寸とPDFへの縮小表示で目視し、文字欠落、誤字、線の衝突、ラベルと対象の分離がないことを確認します。

## 表紙画像

`cover-progression.png` は2026年7月28日に生成した表紙用概念イラストです。
トランジスタ、CPU、ソース構造、ネットワーク、言語モデルへの進行を、文字なしの横長線画で表しています。

### 2026-09-05 概念図の再確認

8点の概念図を再生成しました。OSとランタイムの担当範囲、DNSの階層、DOMとCSSOMの合流を描き分けています。トークンの説明を本文に合わせ、測定していない数値や効果の保証を取り除きました。
