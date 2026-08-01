# 生成画像の記録

## `cover-progression.png`

- 生成日：2026-07-28
- 生成方法：Codex 組み込み `image_gen`（既定モード）
- 用途：表紙の概念イラスト
- 後処理：1904×826へ中央基準でトリミングし、PNGのメタデータを除去

プロンプト：

```text
Use case: scientific-educational
Asset type: cover illustration for a Japanese computer-science training textbook
Primary request: a refined visual progression from electronic switching to modern AI: transistor and logic gate, CPU and memory, source structure and runtime, networked computers exchanging packets, then a compact neural network and browser response
Scene/backdrop: perfectly plain off-white background, color #F7F6F1
Subject: five clearly separated but connected stages, left to right: a transistor switch and logic gate; a CPU chip beside memory cells; source code becoming a small abstract syntax tree; two networked computers exchanging packets; a compact neural-network motif representing machine learning
Style/medium: clean flat vector-like educational illustration, precise thin lines, restrained geometry
Composition/framing: wide horizontal composition, centered vertically, generous outer margins, each stage similar visual weight, one thin continuous connector showing progression
Color palette: deep navy #2B3A4A, muted blue #5E7E96, pale gray #9AA4AD, very light blue-gray accents only
Constraints: no text, no letters, no numbers, no logos, no watermark; no gradients; no shadows; no glow; no 3D; no decorative dots, bubbles, waves, patterns, border ornaments, or background motifs; scientifically recognizable simplified objects; high visual clarity at small print size
Avoid: dense infographic, photographic realism, colorful accents, purple, pink, orange, strong primary colors, decorative background
```

## 2026年7月28日再生成の章扉画像

次の画像は、Codex 組み込み `image_gen` の既定モードで生成しました。
いずれも16:9、画像内の生成文字なし、人物なしの章扉用概念イラストです。
生成後に1200×675へ中央基準でトリミングし、PNGのメタデータを除去しました。
日本語の説明は画像へ焼き込まず、`tex/macros.tex`によって図の一部として組版します。
この方法により、生成文字の誤字を避け、検索可能な日本語としてPDFへ埋め込みます。
本文中の厳密な回路、木構造、プロトコル順序は、画像生成の解釈に依存させずTeXまたは表で示します。

| ファイル | 用途 |
| --- | --- |
| `ch00-overview.png` | 一要求を九つの場面で追う全体像 |
| `ch01-signals.png` | 信号、論理回路、記憶、CPU |
| `ch02-code.png` | ソースコードから命令への変換 |
| `ch03-runtime.png` | OS、プロセス、スレッド、仮想メモリ、ヒープ、GC |
| `ch04-design.png` | モジュール、境界、テスト、変更 |
| `ch05-internet.png` | 分散網、複数経路、名前解決 |
| `ch06-delivery.png` | 接続、暗号化、HTTP、キャッシュ |
| `ch07-language-model.png` | 学習、Attention、生成、評価 |
| `ch08-browser.png` | DOM、CSSOM、レイアウト、描画 |
| `ch09-observability.png` | 観測点、仮説、切り分け |

共通プロンプトは次の形式です。

```text
Use case: scientific-educational
Asset type: 16:9 chapter opener for a Japanese computer science textbook
Primary request: [表の用途欄に示す章ごとの概念を、左から右へつながる構成で表現]
Scene/backdrop: flat off-white #F6F3F6 with generous whitespace
Style/medium: precise flat editorial vector-style educational illustration, thin geometric lines
Color palette: #E8CDDD #71618E #5C4D7A #493D5E #2C2437
Constraints: no readable words, letters, numbers, logos, people, photorealism, gradients, decorative patterns, watermark; print-sharp
```

## 2026年7月28日再生成の本文挿絵

次の画像は、Codex組み込み`image_gen`の既定モードで生成しました。
長い章の途中で概念を整理し、読者が文章から厳密な図へ進むための足場として使います。
短い章とTikZ図が十分にある箇所には追加せず、視覚的な区切りが有効な5箇所に限定しました。
章扉画像と同じく、日本語の説明はTeXで図中へ組版します。

| ファイル | 挿入箇所 | 主なプロンプト |
| --- | --- | --- |
| `ch03-data-structures.png` | 第3章「データ構造の選択」 | 同じデータを連続領域、参照の鎖、キーによる格納へ分け、操作の違いを示す |
| `ch04-change-safety.png` | 第4章「テスト」 | 変更を一つのモジュールへ局所化し、複数の検査を通して全体へ戻す |
| `ch07-training-inference.png` | 第7章「学習と推論」 | 多くの例で内部を調整する学習と、固定したモデルを一度使う推論を対比する |
| `ch07-attention-generation.png` | 第7章「文章生成」 | 文脈内を異なる強さで参照し、新しい要素を列へ加えて生成を反復する |
| `ch09-evidence-correlation.png` | 第9章「観測と仮説」 | ログ、トレース、メトリクスを同じ時点へそろえ、異常境界を絞り込む |

共通指定は次のとおりです。

```text
Use case: scientific-educational
Asset type: 16:9 mid-chapter editorial illustration for a Japanese computer science textbook
Scene/backdrop: flat off-white #F6F3F6 with generous whitespace
Style/medium: clean editorial vector-style technology illustration, soft SaaS presentation aesthetic
Color palette: #E8CDDD #71618E #5C4D7A #493D5E #2C2437
Constraints: no words, letters, numbers, logos, people, photorealism, gradients, decorative patterns, watermark; print-sharp
```

## 日本語説明の対応

図中の日本語説明は、生成画像の見た目と本文の概念を対応付ける短い経路として記載します。
章扉では、例えば「電気信号 → デジタル信号 → 論理回路 → 記憶 → 演算 → CPU」のように、章内で扱う順序を示します。
本文挿絵では、「学習」と「推論」や、「メトリクス」「ログ」「トレース」の役割を対比します。
OSI参照モデル、プロセスとスレッド、並行と並列、GCの到達可能性は、正確な対応関係が必要なためTikZで作成しました。
