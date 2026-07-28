# 第8章 応答が画面になるまで 改訂設計メモ

## 章の狙い

サーバーから返った応答が、ブラウザのプロセス内でHTML解析、DOM、CSSOM、スタイル計算、レイアウト、描画、合成、JavaScript実行、イベントループ、fetch、DOM更新を経て画面になるまでを扱います。

## 本文で必ず書くこと

- ブラウザもOS上のプロセスであり、第3章のプロセス・メモリの上で動くアプリケーションだと確認します。
- HTML解析とDOMは、第2章の字句解析・構文解析・木構造との対応を意識して説明します。
- CSSOM、スタイル計算、レイアウト、ペイント、合成は、画素へ色が付くまでの段階として扱い、第1章の信号へ戻る構図にします。
- JavaScriptエンジン、JIT、イベントループ、非同期処理は、送信ボタンのクリックやfetchの完了がどう処理されるかに絞って説明します。
- 初回表示と更新時の再計算コストを、体感速度・jank・DevTools観測と結びます。

## 節別執筆メモ

| 節 | 見出し | 扱い | 書くべきこと |
| --- | --- | --- | --- |
| 8.1 | 応答を受け取るブラウザ | 新 | 【新】 応答を受け取るブラウザを、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.2 | HTML解析とDOM | 新 | 【新】 HTML解析とDOMを、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.3 | CSSOMとスタイル計算 | 新 | 【新】 CSSOMとスタイル計算を、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.4 | レイアウト | 新 | 【新】 レイアウトを、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.5 | 描画と合成 | 新 | 【新】 描画と合成を、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.6 | JavaScriptエンジン | 新 | 【新】 JavaScriptエンジンを、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.7 | イベントループと非同期処理 | 新 | 【新】 イベントループと非同期処理を、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.8 | fetchとDOM更新 | 新 | 【新】 fetchとDOM更新を、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.9 | 初回表示とその後の更新 | 新 | 【新】 初回表示とその後の更新を、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.10 | 手を動かす：開発者ツールで描画を観測する | 新 | 【新】 手を動かす：開発者ツールで描画を観測するを、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |
| 8.11 | 旅をたどり直す | 新 | 【新】 旅をたどり直すを、返ってきた応答がブラウザで解析・実行・描画され画面になる工程として説明する。 |

## 主要資料リンク

| 資料 | 大学・機関 | 種別 | URL | 本文での使い方 |
| --- | --- | --- | --- | --- |
| HTML Living Standard | WHATWG | living standard | https://html.spec.whatwg.org/ | HTML解析、DOM構築、イベントループ |
| DOM Standard | WHATWG | living standard | https://dom.spec.whatwg.org/ | DOMノード、イベント、ツリー |
| CSS Object Model (CSSOM) | W3C | working draft/specification | https://www.w3.org/TR/cssom-1/ | CSSOM、スタイル表現 |
| Critical rendering path | MDN Web Docs | technical guide | https://developer.mozilla.org/docs/Web/Performance/Critical_rendering_path | DOM、CSSOM、レンダーツリー、レイアウト、ペイント |
| Populating the page: how browsers work | MDN Web Docs | technical guide | https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work | style, layout, paint, compositing |
| V8 documentation | Google / V8 Project | official docs | https://v8.dev/docs | JavaScriptエンジン、JIT、GC |
| Chrome DevTools Performance monitor | Chrome for Developers | official documentation | https://developer.chrome.com/docs/devtools/performance-monitor | CPU、JS heap、DOM nodes、layout/sec |

## 用語候補（初出太字化対象）

- ブラウザ、レンダリングエンジン、プロセス、タブ、HTML、HTMLパーサ、トークン化、DOM、ノード、要素、属性、テキストノード
- CSS、CSSOM、カスケード、セレクタ、スタイル計算、computed style、render tree、レイアウト、box model、viewport、reflow、paint
- rasterize、compositing、layer、GPU、JavaScriptエンジン、V8、インタプリタ、JIT、ガベージコレクション、イベントループ、タスク、マイクロタスク
- Promise、async/await、コールバック、非同期処理、fetch、DOM更新、再スタイル計算、再レイアウト、再描画、jank、FPS、First Contentful Paint
- Largest Contentful Paint、DevTools、Network、Performance、Elements

## 図表・演習候補

- DevToolsのNetwork、Performance、Elementsを開き、fetch後にDOMが更新され、style/layout/paintが発生する様子を観測します。

## 執筆上の注意

- 参考資料の図表は転載せず、本文用の独自図・表として描き直します。
- 専門用語は、初出で太字にし、略語は正式名称・役割・本書での使い方の順で説明します。
- 断定は適用範囲を添え、仕様・実装・観測結果・教材上の簡略化を区別します。
- 各節は前節で残った問いへの回答として始め、章末で次章へ残る問いを渡します。
