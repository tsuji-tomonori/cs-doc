# 生成画像の記録

## `cover-progression.png`

- 生成日：2026-07-15
- 生成方法：Codex 組み込み `image_gen`（既定モード）
- 用途：表紙の概念イラスト
- 後処理：なし

プロンプト：

```text
Use case: scientific-educational
Asset type: cover illustration for a Japanese computer-science training textbook
Primary request: a simple visual progression from electronic switching to modern AI
Scene/backdrop: perfectly plain off-white background, color #F7F6F1
Subject: five clearly separated but connected stages, left to right: a transistor switch and logic gate; a CPU chip beside memory cells; source code becoming a small abstract syntax tree; two networked computers exchanging packets; a compact neural-network motif representing machine learning
Style/medium: clean flat vector-like educational illustration, precise thin lines, restrained geometry
Composition/framing: wide horizontal composition, centered vertically, generous outer margins, each stage similar visual weight, one thin continuous connector showing progression
Color palette: deep navy #2B3A4A, muted blue #5E7E96, pale gray #9AA4AD, very light blue-gray accents only
Constraints: no text, no letters, no numbers, no logos, no watermark; no gradients; no shadows; no glow; no 3D; no decorative dots, bubbles, waves, patterns, border ornaments, or background motifs; scientifically recognizable simplified objects; high visual clarity at small print size
Avoid: dense infographic, photographic realism, colorful accents, purple, pink, orange, strong primary colors, decorative background
```

## 2026年7月28日改訂の章扉画像

次の画像は、Codex 組み込み `image_gen` の既定モードで生成しました。
いずれも16:9、文字なし、人物なしの章扉用概念イラストです。
本文中の厳密な回路、木構造、プロトコル順序は、画像生成の解釈に依存させずTeXまたは表で示します。

| ファイル | 用途 |
| --- | --- |
| `ch00-overview.png` | 一要求を九つの場面で追う全体像 |
| `ch01-signals.png` | 信号、論理回路、記憶、CPU |
| `ch02-code.png` | ソースコードから命令への変換 |
| `ch03-runtime.png` | OS、プロセス、仮想メモリ、データ構造 |
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
Primary request: [章ごとの概念を、左から右へつながる構成で表現]
Scene/backdrop: flat off-white #F6F3F6 with generous whitespace
Style/medium: clean editorial vector-style technology illustration, soft SaaS presentation aesthetic
Color palette: #E8CDDD #71618E #5C4D7A #493D5E #2C2437
Constraints: no words, letters, numbers, logos, people, photorealism, gradients, decorative patterns, watermark; print-sharp
```
