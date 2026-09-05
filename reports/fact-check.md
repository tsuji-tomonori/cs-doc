# ファクトチェック記録

確認日：2026年9月5日。

第1〜9章、付録、用語解説、84枚の図版を読み、定義、成立条件、式、数値例、演習との整合を確認した。疑義のある主張は、下記の公式仕様・原著論文・大学教材の該当箇所と照合して修正した。本文の学習順序と、注文確認AIの一要求を追う構成は維持した。

全186節の[根拠対応表](../docs/section-evidence.md)は資料を探すための索引である。この記録では、実際に照合した主張と検証方法を示す。資料の登録数や自動検査の合格を、全記述の正しさの証明として扱わない。

## 主な修正と根拠

| 対象 | 確認した問題と修正 | 照合した資料・箇所 |
| --- | --- | --- |
| 第1章・文字 | 見た目の一文字、コードポイント、Unicodeスカラー値を区別。UTF-8の対象範囲を明記。 | [Unicode 17.0, §3.9, D76・D92](https://www.unicode.org/versions/Unicode17.0.0/core-spec/chapter-3/) |
| 第1章・トランジスタ | ゲートとソースの電圧差で動くこと、High/Lowによる説明の接続条件を明記。 | [MIT 6.004, CMOS Technology](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c3/c3s1/) |
| 第1章・記憶とCPU | ラッチと、エッジで入力を取り込むフリップフロップを区別。クロックを先に説明。ADDは説明用表記とし、一命令と一クロック周期の混同を解消。 | [MIT 6.004, Sequential Logic](https://ocw.mit.edu/courses/6-004-computation-structures-spring-2017/pages/c5/c5s1/) |
| 第2章・探索 | 前順・間順・後順の説明を二分木に限定。DFSの記憶量を実装別に説明。BFSの最短距離の条件を同じ正の重みに限定。ASTの後順評価は対象の四則演算に限定。 | [MIT 6.006, Lecture Notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/lecture-notes/)（探索・計算量） |
| 第3章・並行性 | 並行な仕事の交互実行と並列実行を区別。図中の「軽量に並列処理」を改訂。スレッドのスタックも同じアドレス空間にあることを補足。 | [OSTEP, Concurrency: An Introduction, pp.1–3](https://pages.cs.wisc.edu/~remzi/OSTEP/threads-intro.pdf) |
| 第3章・仮想メモリ | ページフォールトの後に処理を再開する場合と、不正なアクセスとして処理する場合を区別。 | [OSTEP, Beyond Physical Memory: Mechanisms](https://pages.cs.wisc.edu/~remzi/OSTEP/vm-beyondphys.pdf) |
| 第3章・計算量 | O記法を増え方の上限として説明。図の操作回数と一般的な上限を区別。アクセスと挿入を別表に保ち、平均と償却の条件を修正。 | [MIT 6.006, Lecture 1](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/pages/lecture-notes/)、[CMU 15-122, Hash Tables, §§5–6](https://www.cs.cmu.edu/~15122/handouts/lectures/12-hashing.pdf) |
| 第3章・Go | appendは容量が足りれば元配列を再利用する。容量不足時の要素コピーと、要素内の参照先の共有を区別。ハッシュ図は連鎖法の例と明記。 | [Go specification: Appending and copying slices](https://go.dev/ref/spec#Appending_and_copying_slices)、[Go Slices: usage and internals](https://go.dev/blog/slices-intro) |
| 第4章・設計 | RESTをURLの命名方法だけで定義せず、アーキテクチャの制約として説明。純粋関数の説明では外部状態の読み取りも区別。全組合せの関係数には前提を付記。 | [Fielding, dissertation, chapter 5](https://ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm)、[Hughes, Why Functional Programming Matters, §1](https://www.cs.kent.ac.uk/people/staff/dat/miranda/whyfp90.pdf) |
| 第4章・シーケンス図 | 利用者まで結果が戻る本文に合わせ、APIから利用者への最後の応答矢印を追加。 | 本文の注文処理の手順と、図中の①〜⑥の送受信者を照合。 |
| 第5章・DNSと経路 | DNSのTTLをキャッシュ保持時間の上限として説明。定期更新の周期との混同を解消。経路選択とパケット転送を区別。 | [RFC 1035, §3.2.1](https://www.rfc-editor.org/rfc/rfc1035.html#section-3.2.1)、[RFC 1812, §5](https://www.rfc-editor.org/rfc/rfc1812.html#section-5) |
| 第5章・設計原則 | エンドツーエンド原則を原著へ結び付け、端点での確認と途中の補助機能を併記。 | [Saltzer, Reed, Clark, End-to-End Arguments in System Design](https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf) |
| 第6章・通信 | ACKの次に期待する番号を明確化。HTTP/1.1の開始行・ヘッダーとバイナリのボディを区別。TCPの後にTLSを行う例と、QUICにTLSを組み込む例を分けた。 | [RFC 9293, §3.1](https://www.rfc-editor.org/rfc/rfc9293.html#section-3.1)、[RFC 9112, §2.1](https://www.rfc-editor.org/rfc/rfc9112.html#section-2.1)、[RFC 9001, §4](https://www.rfc-editor.org/rfc/rfc9001.html#section-4) |
| 第7章・最小二乗と正則化 | 目的関数は残差二乗和の「半分」と修正。重みが一意に求まる列の独立性を明記。L2ノルムと、その二乗を使う罰則を区別。 | [Stanford CS229, Supervised Learning, Part I](https://cs229.stanford.edu/notes-spring2019/cs229-notes1.pdf)、[D2L, Weight Decay](https://d2l.ai/chapter_linear-regression/weight-decay.html) |
| 第7章・確率と評価 | ベイズの式でクラス・観測値・正の周辺確率を明記。F1の式と分母が0の場合の扱いを補足。回帰演習の評価対象を、ノイズのない元の関数に修正。 | [Stanford CS229, Generative Learning Algorithms, p.1](https://cs229.stanford.edu/notes-spring2019/cs229-notes2.pdf)、[scikit-learn: F1 score / zero_division](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.f1_score.html)、数式の再計算とPython演習の再実行。 |
| 第7章・Attention | ベクトル次元を固定した計算量と、行列を保存するメモリ量を区別。FlashAttentionの説明を追加。位置情報もマスクもない場合の並べ替えの性質に限定。 | [Attention Is All You Need, §§3.2・3.5・4](https://arxiv.org/html/1706.03762v7)、[FlashAttention, §3](https://arxiv.org/abs/2205.14135) |
| 第7章・因果マスク | 自分と過去の位置を参照し、訓練時も使うことを本文・表・図で統一。図のsoftmax式へマスクMを追加し、Mの値を本文で説明。 | [Attention Is All You Need, §3.2.3](https://arxiv.org/html/1706.03762v7) |
| 第8章・描画 | computed styleとレイアウトで使う寸法を区別。fetchのResponse取得と、ボディ取得完了を分けて説明。Promiseを導入してから反応処理へ接続。 | [CSS Cascade 5, §4](https://www.w3.org/TR/css-cascade-5/#value-stages)、[Fetch Standard, §§5.3・5.6](https://fetch.spec.whatwg.org/)、[HTML event loop](https://html.spec.whatwg.org/multipage/webappapis.html#event-loop-processing-model) |
| 第9章・仮説検証 | 反証を「仮説から予測した結果と合わない観測」と修正。支持する観測だけで原因が確定するという飛躍を解消。 | [SRE, Effective Troubleshooting: Hypothesize / Test and Treat](https://sre.google/sre-book/effective-troubleshooting/) |
| 第9章・性能 | 総時間の加算を、順に進む重複しない区間に限定。並列処理では完了を決める依存経路を見る。CLSは最長5秒の区間ごとの合計の最大値と修正。 | 各区間の開始・終了時刻による整合確認。[CLS: session window](https://web.dev/articles/cls) |
| 付録B・実行手順 | Goモジュール作成を追加。本文と付録のベンチマーク入力・実行回数を統一。架空の通信時間を例と明記。モデル選択用データと最終テストを区別。 | [Go: Create a module](https://go.dev/doc/tutorial/create-module)、下記の実行検証。 |

## 図表と文章

本文の22個のネイティブ表をPDFで確認した。比較軸、列幅、セルの改行、行間、ページ内の収まりを確認した。表本文は周囲の本文と同程度のサイズで、表を一括縮小する指定はない。第3章の表は、アクセスと挿入の区別を保って条件を修正した。第4・7章の一部コード例にあった約7ポイントの個別縮小指定は外した。第7章のPythonコードは、関数の途中で改ページされないよう、一つのページへまとめた。

画像84枚では、数値例、矢印、処理順、本文の説明との対応を目視した。2進変換、加算器、DFS/BFS、配列の添字、append、最長接頭辞一致、TCPのACK、BPEの結合回数、パーセプトロン更新、勾配と損失、Attentionの加重和、サンプリングの確率を照合した。

次の3枚は組み込みのimage_genで編集し、生成後に再確認した。元画像は保持した。編集プロンプトも保存した。

- [プロセスとスレッド](../assets/generated/03-diagram-02-reviewed.png)／[プロンプト](../assets/image-prompts/03-diagram-02-reviewed.txt)
- [シーケンス図](../assets/generated/04-diagram-05-reviewed.png)／[プロンプト](../assets/image-prompts/04-diagram-05-reviewed.txt)
- [自己注意の計算](../assets/generated/07-diagram-09-reviewed.png)／[プロンプト](../assets/image-prompts/07-diagram-09-reviewed.txt)

文章は、初出の説明、一文の主題、同じ節の接続詞、肯定形への言い換えを確認した。科学的な否定や条件の限定は残した。制作・組版・プロンプト指示の転記に当たる文章は本文の検索と通読で確認した。執筆方針は[スキル](../skills/cs-textbook-review/SKILL.md)と[執筆規約](../docs/writing-guide.md)へ保存した。

## 実行検証

実行環境はLinux amd64、Python 3.12.9、NumPy 2.5.2、Go 1.27.1。本文のコードブロックを抽出して実行し、付録の出力と照合した。

| 検証 | 結果 |
| --- | --- |
| 第1章のビット演算・浮動小数点 | 付録Bの8行と一致。 |
| 第2章のGoによるAST評価 | 値24、0除算、未知演算子の3出力と一致。 |
| 第3章のGoベンチマーク | 専用モジュールで両例を各5回実行してPASS。検証時は `-benchtime=100ms` を追加。時間の大小や具体値を合否条件にしなかった。 |
| 第7章の多項式回帰 | 4行すべて、付録Bの小数6桁まで一致。 |
| スキルの形式 | `quick_validate.py skills/cs-textbook-review` が合格。 |
| 書籍全体 | `make verify` が合格。201ページ、186節、600用語、84図版、67資料の索引。組版警告・文字欠落・はみ出しは検出されなかった。 |

回帰の実測結果：

```text
次数 訓練MSE 元の関数に対するMSE
0    0.559948 0.520170
1    0.322496 0.195771
3    0.039028 0.011542
9    0.005280 0.029639
```

再現時はライブラリの版も記録する。[NumPyの乱数互換性方針](https://numpy.org/doc/stable/reference/random/compatibility.html)に従い、シードだけであらゆる環境の結果が固定されるとは扱わない。

## 確認の範囲

継続検証として、`make verify-examples`で本文と付録のコードを直接実行し、付録の期待出力と照合する。第2章は本文の簡潔な実装と付録のエラー処理付き実装を両方実行する。第3章は各ベンチマークの5回の完走を確認する。PRとmainへのpushで、演習検証と既存の`make verify`を別ジョブで実行する。Pages公開は両ジョブの成功を条件とする。環境の版と再現手順は[README](../README.md#演習の検証)に記録した。

DNS・traceroute・curlの実通信と、読者のブラウザでの開発者ツール操作は、この検証では再実行していない。これらは仕様、観測値の意味、手順の整合を確認した。Windows環境のセットアップも未実行である。PDFは画面上で確認しており、紙への試し刷りは行っていない。

今回確認した範囲と根拠を記録し、将来の仕様変更や改訂時に同じ観点で追跡できるようにした。
