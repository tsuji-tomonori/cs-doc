# 生成画像の記録

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
| `ch02-code.png` | ソースコードは段階的な変換を経て、CPUが実行できる命令になる |
| `ch03-runtime.png` | OSは実行単位とメモリを分離し、資源を安全に共有する |
| `ch03-data-structures.png` | データ構造は、速くしたい操作から選ぶ |
| `ch04-design.png` | 境界を明確にすると、変更を小さく閉じ込められる |
| `ch04-change-safety.png` | 変更は小さく作り、複数の検査を通して安全に反映する |
| `ch05-internet.png` | 異なる管理主体の網をつなぎ、複数経路で到達可能にする |
| `ch06-delivery.png` | Web配信は、接続・保護・転送・処理を層として重ねる |
| `ch07-language-model.png` | 言語モデルは、文字列を確率へ変換し、次のトークンを選ぶ |
| `ch07-training-inference.png` | 学習はパラメータを変え、推論は固定したパラメータを使う |
| `ch07-attention-generation.png` | 生成は、文脈を参照して次の一語を選ぶ反復で進む |
| `ch08-browser.png` | 文書とスタイルを配置・描画し、画面を組み立てる |
| `ch09-observability.png` | 境界ごとに観測すると、障害箇所を段階的に絞り込める |
| `ch09-evidence-correlation.png` | 時刻をそろえると、三つの証拠が同じ障害を指す |

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
