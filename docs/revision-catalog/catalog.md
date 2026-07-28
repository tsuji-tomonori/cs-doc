# 改訂設計カタログ

| 章 | タイトル | 扱い | Markdown | 節数 | 資料数 | 用語数 | 章の狙い |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00 | はじめに | 改訂方針 | 00_introduction.md | 5 | 4 | 29 | 一つの送信を起点に、物理層・実行環境・設計・分散網・LLM・ブラウザ描画までを一続きの旅として読者に示します。既存教材の物語線を維持しつつ、章の分割と新設に合わせて場面数と図の責務を更新します。 |
| 01 | 第1章 信号から計算へ | 現行を細分化 | 01_signal_to_computation.md | 20 | 5 | 67 | 電圧の揺らぎを0/1として扱うところから、NAND、加算器、記憶回路、メモリ階層、CPUの命令実行までを、アプリの一要求が最終的には物理信号で動くという視点で説明します。 |
| 02 | 第2章 コードから命令へ | 現行を維持しつつ順序整理 | 02_code_to_instruction.md | 16 | 5 | 54 | 人間が書くソースコードが、トークン、構文、AST、評価順、機械語・実行方式へ変換される流れを扱います。第1章のCPU命令と、第3章のプロセス実行を接続します。 |
| 03 | 第3章 プログラムが動く場所 | 現行を細分化 | 03_runtime_place.md | 21 | 7 | 69 | 実行中のプログラムを、OS、プロセス、システムコール、仮想メモリ、型、データ構造、計算量の観点から説明します。コードがCPU命令になるだけでは不十分で、どこで、どの資源を使って動くかを扱います。 |
| 04 | 第4章 変更を支える設計 | 現行を拡張 | 04_design_for_change.md | 23 | 6 | 56 | 動くプログラムを、変更し続けられるソフトウェアへ育てるための設計原則を扱います。ソフトウェア危機から、分割統治、情報隠蔽、抽象化、UML、OOP、関数型、テスト、品質維持へ進めます。 |
| 05 | 第5章 インターネットという分散網 | 改：現行第5章前半を再編 | 05_internet_distributed_network.md | 17 | 7 | 62 | ネットワークを、単なる通信手順ではなく、パケット交換・階層化・IP・ルーティング・AS・IX・BGP・DNS・エンドツーエンド原則によって成り立つ分散網として説明します。 |
| 06 | 第6章 要求が届くまで | 改：現行第5章後半を独立 | 06_request_delivery.md | 16 | 8 | 59 | 第5章の分散網の上で、アプリケーションの一要求がポート、TCP/UDP/QUIC、TLS、HTTP、キャッシュ、プロキシ、CDNを経てサーバーへ届くまでを説明します。 |
| 07 | 第7章 言葉が応答になるまで | 現行第6章を移動、一部結び改 | 07_language_to_response.md | 36 | 7 | 80 | 数学、機械学習、ニューラルネットワーク、Transformer、トークン化、生成、評価、漏洩・偏り・分布変化・ハルシネーションまでを、注文確認AIが自然言語応答を生成する道筋として説明します。 |
| 08 | 第8章 応答が画面になるまで | 新設 | 08_response_to_screen.md | 11 | 7 | 53 | サーバーから返った応答が、ブラウザのプロセス内でHTML解析、DOM、CSSOM、スタイル計算、レイアウト、描画、合成、JavaScript実行、イベントループ、fetch、DOM更新を経て画面になるまでを扱います。 |
| 09 | 第9章 一つの応答をたどる | 現行第7章を拡張 | 09_trace_one_response.md | 21 | 6 | 49 | 第1章から第8章までの層を再統合し、一要求を観測・仮説・切り分け・検証の流れで追えるようにします。遅延、メモリ、通信、描画、AI品質、変更容易性の問題を、戻るべき層と観測点に対応させます。 |
| A | 付録・参考文献・索引 | 新設・改 | appendix_references_index.md | 4 | 6 | 29 | 環境構築、手を動かす節の解答例、参考文献の章別整理、索引をまとめます。外部資料は転載せず、リンク・出典の役割・本文で使う観点を記録します。 |

## 主要資料一覧

| 章 | 資料 | 機関 | 種別 | URL | 本文での使い方 |
| --- | --- | --- | --- | --- | --- |
| 00 | ACM/IEEE-CS/AAAI CS2023 Computer Science Curricula | ACM / IEEE Computer Society / AAAI | curriculum homepage | https://csed.acm.org/ | 全体構成・知識領域の妥当性確認 |
| 00 | MIT 6.033 Computer System Engineering | MIT OpenCourseWare | course homepage | https://ocw.mit.edu/courses/6-033-computer-system-engineering-spring-2018/ | システムを層と境界で捉える導入 |
| 00 | CS50x 2026: Introduction to Computer Science | Harvard University | course homepage | https://cs50.harvard.edu/x/ | 入門者向けの語り方・抽象化 |
| 00 | UC Berkeley CS61C course description | UC Berkeley EECS | course homepage | https://www2.eecs.berkeley.edu/Courses/CS61C/ | 機械構造から高級言語・OSへの橋渡し |
| 01 | MIT 6.004 Computation Structures | MIT OpenCourseWare | course homepage | https://ocw.mit.edu/courses/6-004-computation-structures-spring-2009/ | トランジスタ、論理回路、CPUの骨格 |
| 01 | Nand2Tetris official course | Nand2Tetris / MIT Press book | course homepage | https://www.nand2tetris.org/ | NANDからコンピュータを作る教材設計 |
| 01 | Nand2Tetris Projects | Nand2Tetris | project homepage | https://www.nand2tetris.org/course | Boolean logic, arithmetic, memory, CPU |
| 01 | CMU 15-213 Introduction to Computer Systems | Carnegie Mellon University | course homepage | https://www.cs.cmu.edu/~213/ | 整数・浮動小数点・メモリ階層 |
| 01 | IEEE 754-2019 Floating-Point Arithmetic | IEEE | standard homepage | https://standards.ieee.org/standard/754-2019.html | 浮動小数点と丸め誤差 |
| 02 | Stanford CS143: Compilers | Stanford University | course archive | https://web.stanford.edu/class/archive/cs/cs143/cs143.1128/ | 字句解析・構文解析・型検査・コード生成 |
| 02 | Stanford CS143 bulletin entry | Stanford University | course catalog | https://bulletin.stanford.edu/courses/1056721 | コンパイラ・インタプリタの範囲確認 |
| 02 | The Go Programming Language Specification | Go Project | language specification | https://go.dev/ref/spec | EBNF、型、文法、構文 |
| 02 | LLVM Kaleidoscope tutorial | LLVM Project | official tutorial | https://llvm.org/docs/tutorial/ | ASTからコード生成まで |
| 02 | Nand2Tetris Projects 6,10,11 | Nand2Tetris | project homepage | https://www.nand2tetris.org/course | アセンブラ・構文解析・コード生成 |
| 03 | MIT xv6, a simple Unix-like teaching operating system | MIT PDOS / CSAIL | course/resource homepage | https://pdos.csail.mit.edu/6.828/2025/xv6.html | OS、プロセス、仮想メモリ、システムコール |
| 03 | xv6 book RISC-V | MIT PDOS / CSAIL | PDF | https://pdos.csail.mit.edu/6.828/2025/xv6/book-riscv-rev5.pdf | ページテーブル、トラップ、システムコール |
| 03 | CMU CS:APP curriculum | Carnegie Mellon University | course/book homepage | https://csapp.cs.cmu.edu/3e/curriculum.html | プログラム実行、メモリ、ネットワーク、並行性 |
| 03 | Princeton Algorithms, Part I | Princeton University | course homepage | https://online.princeton.edu/algorithms-part-i | 基本データ構造と計算量 |
| 03 | Algorithms, 4th Edition | Princeton University | book companion | https://algs4.cs.princeton.edu/home/ | データ構造・計算量・演習 |
| 03 | Python Data Model | Python Software Foundation | official documentation | https://docs.python.org/3/reference/datamodel.html | identity, type, value, object model |
| 03 | The Go Programming Language Specification | Go Project | language specification | https://go.dev/ref/spec | 型、サイズ、アラインメント、値渡し |
| 04 | SWEBOK Guide V4 | IEEE Computer Society | official guide homepage | https://www.computer.org/education/bodies-of-knowledge/software-engineering | ソフトウェア工学の知識体系 |
| 04 | NATO Software Engineering Report 1968 | NATO / Newcastle University ePrints | PDF metadata/homepage | https://eprints.ncl.ac.uk/158767 | ソフトウェア危機の歴史的背景 |
| 04 | On the Criteria To Be Used in Decomposing Systems into Modules | D. L. Parnas / ACM / CMU | paper homepage | https://doi.org/10.1145/361598.361623 | 情報隠蔽、モジュール分割 |
| 04 | UML official page | Object Management Group | specification homepage | https://www.omg.org/uml/ | クラス図・シーケンス図・モデリング |
| 04 | ISO/IEC 19505 UML | ISO | standard homepage | https://www.iso.org/standard/32624.html | UMLの国際標準 |
| 04 | Go To Statement Considered Harmful | E. W. Dijkstra / CWI archive | paper PDF | https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf | 構造化プログラミングの背景 |
| 05 | RFC 791: Internet Protocol | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc791 | IPデータグラム、フラグメンテーション、ベストエフォート |
| 05 | RFC 8200: IPv6 Specification | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc8200 | IPv6の基本ヘッダーと配送 |
| 05 | RFC 4271: Border Gateway Protocol 4 | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc4271 | BGP、AS、経路広告 |
| 05 | RFC 1034: Domain Names - Concepts and Facilities | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc1034 | DNSの概念、委任、キャッシュ |
| 05 | RFC 1035: Domain Names - Implementation and Specification | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc1035 | DNSメッセージと実装仕様 |
| 05 | End-to-End Arguments in System Design | MIT / ACM TOCS | paper PDF | https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf | エンドツーエンド原則 |
| 05 | CAIDA AS Rank | CAIDA / UC San Diego | research project homepage | https://www.caida.org/projects/as-rank/ | AS・インターネット構造の観測 |
| 06 | RFC 9293: Transmission Control Protocol | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc9293 | TCP接続、順序、再送、制御 |
| 06 | RFC 9000: QUIC | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc9000 | QUICのUDP上の多重化・暗号化接続 |
| 06 | RFC 9110: HTTP Semantics | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc9110 | HTTPメソッド、ステータス、意味論 |
| 06 | RFC 9112: HTTP/1.1 | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc9112 | HTTP/1.1メッセージ構文 |
| 06 | RFC 9113: HTTP/2 | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc9113 | HTTP/2の多重化 |
| 06 | RFC 9114: HTTP/3 | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc9114 | HTTP/3とQUIC |
| 06 | RFC 8446: TLS 1.3 | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc8446 | TLSハンドシェイクと暗号化 |
| 06 | Service workers and the Cache Storage API | web.dev / Google | official guide | https://web.dev/learn/pwa/serving | Service Workerとキャッシュ |
| 07 | Stanford CS229 Machine Learning | Stanford University | course homepage | https://see.stanford.edu/Course/CS229 | 機械学習の基礎、回帰、分類、最適化 |
| 07 | Dive into Deep Learning | D2L.ai / university authors | book homepage | https://d2l.ai/ | ニューラルネットワーク、Transformer、実装 |
| 07 | Deep Learning | MIT Press | book homepage | https://mitpress.mit.edu/9780262035613/deep-learning/ | 深層学習の体系 |
| 07 | Stanford CS224N: NLP with Deep Learning | Stanford University | course homepage | https://web.stanford.edu/class/cs224n/ | Transformer、Attention、言語モデル |
| 07 | Speech and Language Processing draft | Stanford / University of Colorado | book homepage | https://web.stanford.edu/~jurafsky/slp3/ | 言語モデル、Transformer、評価 |
| 07 | Attention Is All You Need | Google Brain / Google Research / University of Toronto | paper PDF | https://arxiv.org/pdf/1706.03762 | Transformerの原典 |
| 07 | NIST AI Risk Management Framework 1.0 | NIST | PDF | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf | AIのリスク、評価、信頼性 |
| 08 | HTML Living Standard | WHATWG | living standard | https://html.spec.whatwg.org/ | HTML解析、DOM構築、イベントループ |
| 08 | DOM Standard | WHATWG | living standard | https://dom.spec.whatwg.org/ | DOMノード、イベント、ツリー |
| 08 | CSS Object Model (CSSOM) | W3C | working draft/specification | https://www.w3.org/TR/cssom-1/ | CSSOM、スタイル表現 |
| 08 | Critical rendering path | MDN Web Docs | technical guide | https://developer.mozilla.org/docs/Web/Performance/Critical_rendering_path | DOM、CSSOM、レンダーツリー、レイアウト、ペイント |
| 08 | Populating the page: how browsers work | MDN Web Docs | technical guide | https://developer.mozilla.org/en-US/docs/Web/Performance/Guides/How_browsers_work | style, layout, paint, compositing |
| 08 | V8 documentation | Google / V8 Project | official docs | https://v8.dev/docs | JavaScriptエンジン、JIT、GC |
| 08 | Chrome DevTools Performance monitor | Chrome for Developers | official documentation | https://developer.chrome.com/docs/devtools/performance-monitor | CPU、JS heap、DOM nodes、layout/sec |
| 09 | Google SRE Books | Google SRE | book homepage | https://sre.google/books/ | 監視、信頼性、インシデント、SLO |
| 09 | OpenTelemetry Documentation | OpenTelemetry | official documentation | https://opentelemetry.io/docs/ | traces, metrics, logs, instrumentation |
| 09 | Chrome DevTools Performance panel | Chrome for Developers | official documentation | https://developer.chrome.com/docs/devtools/performance | 描画・JS・ネットワークの調査 |
| 09 | The USE Method | Brendan Gregg | method homepage | https://www.brendangregg.com/usemethod.html | Utilization, Saturation, Errors |
| 09 | NIST AI RMF 1.0 | NIST | PDF | https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf | AI品質・リスク調査 |
| 09 | RFC 9110: HTTP Semantics | IETF | RFC | https://datatracker.ietf.org/doc/html/rfc9110 | HTTP観測・障害切り分け |
| A | Go installation docs | Go Project | official docs | https://go.dev/doc/install | Goのインストールと確認 |
| A | Python setup and usage | Python Software Foundation | official docs | https://docs.python.org/3/using/ | Pythonのインストールと起動 |
| A | Python Tutorial | Python Software Foundation | official docs | https://docs.python.org/3/tutorial/ | Pythonの動作確認 |
| A | everything curl | curl project | official book/docs | https://everything.curl.dev/ | curlの使い方 |
| A | BIND 9 dig documentation | Internet Systems Consortium | official docs | https://bind9.readthedocs.io/ | digとDNS問い合わせ |
| A | Chrome DevTools documentation | Chrome for Developers | official docs | https://developer.chrome.com/docs/devtools | Network/Performance/Elements |