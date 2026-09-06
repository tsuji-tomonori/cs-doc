# 本文Web版の保守

PDF閲覧専用だった公開入口をAstro + Starlightへ変更します。RAGガイドの `handson/aws-rag/` を参考に、左の章一覧、右のページ内目次、日本語全文検索をそろえます。

## 本文の正本

`main.tex` の章順と `chapters/` を正本として、`site/scripts/prepare_book.py` がPandocで構文を解析します。独自マクロを意味のあるHTMLへ対応付け、組版上の配置指定を除きます。PDFを画像化する方式ではありません。

はじめに、第1〜9章、付録A〜C、参考文献の14ページを生成します。数式はMathML、表はHTML table、プログラムは強調表示付きのコードです。補足用語と出典も取り込み、用語から説明へ戻れる索引を生成します。索引は太字語から作るため、見出し的な強調語も一部含みます。

`site/src/data/book.json`、`site/public/book-assets/`、`site/dist/` は生成物です。更新は原稿と生成処理へ行います。`make site` はPDFを作った後でWeb版を生成し、両方を同じコミットにそろえます。PDFのURLは `/cs-doc/information-engineering-basics.pdf` のままです。

## 操作教材の配置

| 章 | 変更して観察する内容 |
| --- | --- |
| 1 | 電圧の保証範囲、2進数、2の補数、NMOS・CMOS、真理値表、NAND構成、全加算器、固定幅演算、レジスタ、LRUキャッシュ、CPU命令 |
| 2 | ASTの部分木からの評価 |
| 3 | 線形探索の途中状態と比較回数 |
| 4 | インタフェースによる変更の局所化 |
| 5 | DNSのキャッシュ有無と問い合わせ |
| 6 | TCPの欠落・再送・順序保証 |
| 7 | 勾配降下、温度とsoftmax確率 |
| 8 | 幅による折り返しと配置 |
| 9 | 直列工程の遅延と内訳 |

合計20教材です。`prepare_book.py` の `LABS` が節名に対応付けます。節名の変更で配置が失われると生成を停止します。実験がある節の元の図は補足として開く形にし、操作と本文を組み合わせます。他の図は説明を保つため残します。

`Lab.astro` は初期結果をHTMLへ出力します。`lab-element.ts` が入力を受け、`labs.mjs` が説明と図を更新し、`models.mjs` が純粋な計算を行います。外部APIや任意コード実行は使いません。JavaScriptを無効にしても本文と初期例を読めます。

入力にはラベル、範囲、刻みを設けます。不正な数値では直前の結果を保持し、修正方法を示します。スイッチはキーボード操作と `aria-pressed`、結果はライブ領域に対応します。回路アニメーションには停止操作があり、端末の `prefers-reduced-motion` にも対応します。図と表は狭い画面では局所的に横スクロールできます。

## 回路のモデルと根拠

NMOSはソース・基板を0 Vとし、`VGS > VT` でチャネルができるモデルです。チャネルがあっても `VDS = 0` なら電流は0です。ゲートから酸化膜を貫く電流は描きません。慣用的な電流をDからSへ描き、電子は逆方向であることを説明します。

電流は長チャネル近似で `k = 1 mA/V²`、`VT = 1 V` と仮定します。線形領域は `ID = k[(VGS − VT)VDS − VDS²/2]`、飽和領域は `ID = k(VGS − VT)²/2` です。実素子のシミュレーターではありません。

CMOSは入力LowでpMOS、HighでnMOSをオンにします。充放電は入力の切り替え時だけアニメーションで示します。安定後も電源からGNDへ流れ続ける表現は使いません。漏れ電流や切り替え中の同時導通は説明文で範囲を明示します。時間は観察用に引き延ばします。

確認資料（2026-09-05）：

- [MIT 6.004 CMOS Technology](https://computationstructures.org/lectures/cmos/cmos.html)：電界制御、相補接続、電力と容量
- [MIT 6.012 MOSFETモデル](https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/eeb94eab00ebb62a3fde0eec1484bc08_MIT6_012F09_lec11_gradual.pdf)：線形・飽和領域の電流近似
- [Starlight custom pages](https://starlight.astro.build/guides/pages/)：独自データからの本文生成と目次

## 検証と公開

`npm test` は全加算器の全入力、固定幅演算、オーバーフロー、NMOSのしきい値と電圧差、softmaxの数値安定性、記憶更新、キャッシュ、勾配降下、全教材の途中状態を検証します。原稿の全節・用語・コード本文がHTMLに残ることも照合します。コード内の `%` をTeXコメントとして失わないことを回帰テストします。

`npm run test:site` は生成HTMLのローカルリンク、アンカー、画像、スクリプト、重複ID、数式、20教材、本文量、PDFの同梱を検査します。Pagefindの実インデックスへ日本語検索を行います。これらは実ブラウザでの見た目や操作感の評価を代替するものではありません。

CIは既存のPDF品質検査とPython・Go演習検証を維持します。PRではWeb版とPDFをArtifactsに保存し、mainへ反映後に `site/dist/` をGitHub Pagesへ公開します。

## スキルの移設

直下の二重フォルダーを `skills/japanese-tech-writing-desumasu/` へ移設しました。既存の `skills/cs-textbook-review/` と同じ配置です。SKILL、チェックリスト、出典、統合版、履歴、READMEは内容を保持し、ルートREADMEの参照を更新します。
