# 付録・参考文献・索引 改訂設計メモ

## 章の狙い

環境構築、手を動かす節の解答例、参考文献の章別整理、索引をまとめます。外部資料は転載せず、リンク・出典の役割・本文で使う観点を記録します。

## 本文で必ず書くこと

- 付録AはGo、Python、dig、curl、traceroute、ブラウザ開発者ツールの準備とバージョン確認をOS別にまとめます。
- 付録Bは各章の『手を動かす』の期待出力、よくある失敗、確認観点を置きます。
- 参考文献は章別に整理し、大学教材、標準仕様、RFC、原著論文、公式ドキュメントを区別します。
- 索引は専門用語の初出節、関連章、略語展開を持たせ、本文の初出太字化と整合させます。

## 節別執筆メモ

| 節 | 見出し | 扱い | 書くべきこと |
| --- | --- | --- | --- |
| 付録A | 環境構築 | 新 | 【新】 環境構築は、本文の演習・参照・用語管理を再現可能にするための補助資料として整備する。 |
| 付録B | 「手を動かす」の解答例と期待出力 | 新 | 【新】 「手を動かす」の解答例と期待出力は、本文の演習・参照・用語管理を再現可能にするための補助資料として整備する。 |
| 参考文献 | 資料の選び方と章別リンク | 改 | 【改】 資料の選び方と章別リンクは、本文の演習・参照・用語管理を再現可能にするための補助資料として整備する。 |
| 索引 | 専門用語の初出管理 | 新 | 【新】 専門用語の初出管理は、本文の演習・参照・用語管理を再現可能にするための補助資料として整備する。 |

## 主要資料リンク

| 資料 | 大学・機関 | 種別 | URL | 本文での使い方 |
| --- | --- | --- | --- | --- |
| Go installation docs | Go Project | official docs | https://go.dev/doc/install | Goのインストールと確認 |
| Python setup and usage | Python Software Foundation | official docs | https://docs.python.org/3/using/ | Pythonのインストールと起動 |
| Python Tutorial | Python Software Foundation | official docs | https://docs.python.org/3/tutorial/ | Pythonの動作確認 |
| everything curl | curl project | official book/docs | https://everything.curl.dev/ | curlの使い方 |
| BIND 9 dig documentation | Internet Systems Consortium | official docs | https://bind9.readthedocs.io/ | digとDNS問い合わせ |
| Chrome DevTools documentation | Chrome for Developers | official docs | https://developer.chrome.com/docs/devtools | Network/Performance/Elements |

## 用語候補（初出太字化対象）

- 環境構築、Go、Python、pip、venv、dig、traceroute、curl、ブラウザ開発者ツール、PATH、バージョン確認、インストール
- OS別手順、期待出力、エラー、トラブルシュート、WSL、macOS、Windows、Linux、サンプルコード、解答例、索引、参考文献
- DOI、RFC、標準仕様、ライセンス、リンク切れ

## 図表・演習候補

- 各章末演習の入力・期待出力・確認ポイント・失敗時の切り分けを統一フォーマットで収録します。

## 執筆上の注意

- 参考資料の図表は転載せず、本文用の独自図・表として描き直します。
- 専門用語は、初出で太字にし、略語は正式名称・役割・本書での使い方の順で説明します。
- 断定は適用範囲を添え、仕様・実装・観測結果・教材上の簡略化を区別します。
- 各節は前節で残った問いへの回答として始め、章末で次章へ残る問いを渡します。
