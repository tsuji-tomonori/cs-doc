import {fixedWidth,fullAdder,nmos,softmax,gradientStep,cacheTrace} from './models.mjs';
export const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const number=(key,label,value,min,max,step=1)=>({key,label,value,min,max,step,type:'number'});
const range=(...args)=>({...number(...args),type:'range'});
const select=(key,label,value,options)=>({key,label,value,options,type:'select'});
const toggle=(key,label,value=0)=>({key,label,value,type:'toggle'});
const width=select('width','ビット幅',8,[4,8,16]);
export const labs={
 voltage:{title:'電圧を動かして論理値を読む',intro:'入力電圧を変え、0と1を保証できる範囲を調べます。',fields:[range('voltage','入力電圧（V）',1.5,0,3.3,.1)],note:'説明用の3.3 V回路です。VIL = 0.8 V、VIH = 2.0 Vと仮定します。実際の保証範囲は回路ごとに異なります。'},
 binary:{title:'ビットを切り替えて数を作る',intro:'10進数を入力するか各桁を押してください。桁の重みと合計が連動します。',fields:[width,number('a','10進数（符号なし）',13,0,65535)],note:'指定幅に収まらない値は下位ビットで表示し、入力との差も示します。'},
 complement:{title:'反転して1を足す',intro:'2の補数を作り、符号付きと符号なしの読み方を比べます。',fields:[width,number('a','整数',5,-32768,65535)],note:'入力を指定幅で表してから符号を反転します。符号付きの範囲は −2ⁿ⁻¹ 〜 2ⁿ⁻¹−1 です。最小値の符号反転は範囲を超えます。'},
 bits:{title:'ビット演算と固定幅の計算機',intro:'数値と演算を変え、桁ごとの結果、桁上がり、符号付きオーバーフローを比べます。',fields:[width,number('a','A（整数）',13,-32768,65535),number('b','B（整数）',5,-32768,65535),select('operation','演算','AND',['AND','OR','XOR','NOT','ADD','SUB','SHL','SHR'])],note:'SHLとSHRは1ビットの論理シフトです。入力は指定幅に丸めます。NOT・SHL・SHRはAだけを使います。'},
 mos:{title:'ゲート電圧で電気の通り道を作る',intro:'ゲートをオンにし、次にドレイン電圧を0 Vにしてください。チャネルの有無と電流の有無を分けて観察できます。',fields:[toggle('gate','ゲートを3.3 Vにする'),range('vg','ゲート電圧 VG（V）',0,0,3.3,.1),range('vd','ドレイン電圧 VD（V）',3.3,0,3.3,.1),toggle('input','CMOSの入力をHighにする')],note:'nMOSのソース・基板は0 V、しきい値VT = 1 Vです。電流は長チャネル近似（k = 1 mA/V²）で、漏れ電流・基板効果は省略します。図の寸法と動作時間は説明用です。'},
 gates:{title:'スイッチと真理値表を結び付ける',intro:'AとBを切り替えると、真理値表の対応する行と出力が変わります。',fields:[toggle('a','入力A'),toggle('b','入力B')],note:'LowまたはHighとして入力が安定した後の論理値を示します。'},
 nand:{title:'NANDだけでNOT・AND・ORを作る',intro:'入力を変え、中間のNAND出力から最終出力まで追います。',fields:[toggle('a','入力A'),toggle('b','入力B')],note:'NANDは二つの入力が1のときだけ0を返します。'},
 adder:{title:'1桁の和と桁上がりを作る',intro:'二つのビットと、下の桁からの桁上がりを切り替えます。',fields:[toggle('a','A'),toggle('b','B'),toggle('cin','入力の桁上がり Cin')],note:'全加算器です。A + B + Cin = 2 × Cout + S を確かめてください。'},
 register:{title:'クロックの立ち上がりで記憶する',intro:'Dを切り替え、クロックを上げ下げします。Qが更新される瞬間を確認します。',fields:[toggle('data','入力 D'),toggle('clock','クロック CLK')],note:'立ち上がりエッジで取り込む理想的な1ビットレジスタです。セットアップ時間とホールド時間は省略します。'},
 cache:{title:'キャッシュの中身を1回ずつ追う',intro:'参照列 A → B → A → C → A → B を追います。容量を変えてヒット数を比べます。',fields:[select('capacity','保持できる項目数',2,[1,2,3])],actions:true,note:'LRU（最も長く使っていない項目を追い出す）方式の説明用モデルです。実CPUのキャッシュ構成は再現しません。'},
 cpu:{title:'命令を取り出し、解読し、実行する',intro:'R0に5を入れ、3を加える二つの命令を追います。「次へ」で内部状態が変わります。',fields:[],actions:true,note:'説明用のCPUです。PCは命令番号で示し、パイプラインは省略します。'},
 ast:{title:'式を木として評価する',intro:'a + b × c の値を変え、掛け算の部分木から足し算へ評価する順序を追います。',fields:[number('a','a',2,-100,100),number('b','b',3,-100,100),number('c','c',4,-100,100)],actions:true,note:'通常の演算子の優先順位に従う整数式です。'},
 search:{title:'線形探索の比較を追う',intro:'配列 [7, 12, 19, 31, 42] を先頭から調べます。見つからない数も試してください。',fields:[number('target','探す値',31,0,99)],actions:true,note:'添字は0から数えます。見つかれば、その後の要素は比較しません。'},
 coupling:{title:'変更が伝わる範囲を見る',intro:'保存方式を変更したとき、どの部品が変更対象になるか比較します。',fields:[toggle('boundary','保存をインタフェースの後ろに隠す',1)],note:'保存方式だけが変わり、契約は維持する例です。契約まで変われば呼び出し側にも影響します。'},
 dns:{title:'名前を解決する問い合わせを追う',intro:'example.comのアドレスを求めます。キャッシュがある場合とない場合を比べます。',fields:[toggle('cached','有効なキャッシュがある')],actions:true,note:'再帰リゾルバーが反復問い合わせを行う例です。委任情報のキャッシュ、CNAME、DNSSECは省略します。'},
 transport:{title:'欠けたデータを待って順序を戻す',intro:'三つのデータ片を送ります。二つ目を失うと、受信側がどこまでアプリへ渡せるか観察します。',fields:[toggle('loss','二つ目のデータ片を失う',1)],actions:true,note:'TCPの順序保証と再送の概念図です。番号は説明用で、実際のシーケンス番号はバイト単位です。再送の検出方法やタイマーは省略します。'},
 gradient:{title:'勾配に沿って損失を下げる',intro:'L(w) = (w − 3)² の最小値を探します。学習率を大きくしたときも比べてください。',fields:[number('start','初期値 w',-2,-10,10,.5),range('rate','学習率 η',.2,.05,1.2,.05)],actions:true,note:'w ← w − η × 2(w − 3) を繰り返します。1変数の二次関数の例で、一般の学習の収束を保証するものではありません。'},
 softmax:{title:'スコアから候補の確率を作る',intro:'三つのlogitと温度を変え、softmaxで得られる確率分布を観察します。',fields:[number('a','候補Aのlogit',2,-20,20,.1),number('b','候補Bのlogit',1,-20,20,.1),number('c','候補Cのlogit',0,-20,20,.1),range('temperature','温度 T',1,.1,3,.1)],note:'pᵢ = exp(zᵢ/T) / Σⱼ exp(zⱼ/T) です。温度は正の値で比べます。抽選前の確率分布を示します。'},
 layout:{title:'利用できる幅が配置を変える',intro:'親要素の幅を変え、3枚のカードの折り返しと行数を観察します。',fields:[range('width','親要素の幅（CSS px）',480,200,640,10)],note:'カードの幅は140 px、間隔は12 pxです。狭い画面では横へスクロールできます。'},
 latency:{title:'応答の待ち時間を分解する',intro:'各工程の時間を変え、全体の遅延と最も時間を使う工程を調べます。',fields:[number('network','通信（ms）',80,0,2000),number('server','サーバー処理（ms）',40,0,2000),number('model','モデル推論（ms）',600,0,5000),number('render','画面描画（ms）',30,0,2000)],note:'4工程が直列に実行される仮想例です。並列処理、ストリーミング、計測の重複区間は含みません。'},
};
export const defaults=kind=>Object.fromEntries(labs[kind].fields.map(f=>[f.key,f.value]));
export function controls(kind) {
 return labs[kind].fields.map(f=>{
  const id=`${kind}-${f.key}`,common=`id="${id}" name="${f.key}"`;
  if(f.type==='toggle')return `<button type="button" data-toggle="${f.key}" aria-pressed="${!!f.value}">${f.label}：<span>${f.value?'1 / ON':'0 / OFF'}</span></button>`;
  if(f.type==='select')return `<label for="${id}">${f.label}<select ${common}>${f.options.map(x=>`<option ${x===f.value?'selected':''}>${x}</option>`).join('')}</select></label>`;
  return `<label for="${id}">${f.label}<input ${common} type="${f.type}" value="${f.value}" min="${f.min}" max="${f.max}" step="${f.step}" required /></label>`;
 }).join('');
}
const bits=(n,w)=>n.toString(2).padStart(w,'0');
const formula=s=>`<p class="lab-formula">${s}</p>`;
const box=(label,value)=>`<div class="state-box"><span>${label}</span><strong>${value}</strong></div>`;
const states=content=>`<div class="states">${content}</div>`;
const table=(heads,rows)=>`<div class="table-scroll"><table><thead><tr>${heads.map(x=>`<th scope="col">${x}</th>`).join('')}</tr></thead><tbody>${rows.map(row=>`<tr>${row.map(x=>`<td>${x}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
const stages=(names,index)=>`<ol class="stages">${names.map((x,i)=>`<li ${i===index?'aria-current="step"':''}>${x}</li>`).join('')}</ol>`;
export function maxSteps(kind,v) {
 if(kind==='cache'||kind==='cpu')return 6;
 if(kind==='ast')return 3;
 if(kind==='dns')return v.cached?2:5;
 if(kind==='transport')return v.loss?4:3;
 if(kind==='gradient')return 12;
 if(kind==='search'){const i=[7,12,19,31,42].indexOf(v.target);return i<0?5:i+1;}
 return 0;
}
export function result(kind,v,s={step:0,q:0,transient:false}) {
 const step=s.step||0;
 if(kind==='voltage')return formula(`${v.voltage.toFixed(1)} V → ${v.voltage<=.8?'Low / 0':v.voltage>=2?'High / 1':'論理値を保証しない領域'}`)+`<div class="voltage-scale"><span>Low ≤ 0.8 V</span><span>保証なし</span><span>High ≥ 2.0 V</span><i style="left:${v.voltage/3.3*100}%"></i></div>`;
 if(kind==='binary') {
  const r=fixedWidth(v.a,0,v.width,'OR');
  return `<div class="bit-grid">${bits(r.x,v.width).split('').map((b,i)=>`<button type="button" data-bit="${v.width-i-1}" aria-label="2の${v.width-i-1}乗のビットを反転" aria-pressed="${b==='1'}"><small>2<sup>${v.width-i-1}</sup></small><b>${b}</b><small>${2**(v.width-i-1)}</small></button>`).join('')}</div>`+formula(`${bits(r.x,v.width)}₂ = ${r.x}₁₀ = 0x${r.x.toString(16).toUpperCase()}`)+`<p>${Array.from({length:v.width},(_,i)=>`${(r.x>>i)&1} × ${2**i}`).reverse().join(' + ')} = ${r.x}</p><p>${v.a!==r.x?`下位${v.width}ビットを表示しています。入力 ${v.a} との差は ${v.a-r.x} です。`:'指定幅に収まっています。'}</p>`;
 }
 if(kind==='complement') {
  const a=fixedWidth(v.a,0,v.width,'OR'),b=fixedWidth(v.a,0,v.width,'NOT'),c=fixedWidth(b.value,1,v.width,'ADD');
  return table(['操作','ビット列','符号なし'],[['元の値',bits(a.x,v.width),a.x],['全ビットを反転',b.binary,b.value],['1を足す',c.binary,c.value]])+formula(`符号付きで読むと ${c.signed}`)+`<p>${a.x===2**(v.width-1)?'最小値の符号反転は範囲を超え、同じビット列が残ります。':`下位${v.width}ビットで、元の値と結果の和は0です。`}</p>`;
 }
 if(kind==='bits') {
  const r=fixedWidth(v.a,v.b,v.width,v.operation);
  return table(['値',`${v.width}ビット`,'符号なし'],[['A',bits(r.x,v.width),r.x],['B',bits(r.y,v.width),r.y],['結果',r.binary,r.value]])+formula(`${v.operation} → ${r.binary}₂`)+states(box('符号付きの結果',r.signed)+box('桁上がり',r.carry?'あり':'なし')+box('借り',r.borrow?'あり':'なし')+box('符号付きオーバーフロー',r.overflow?'あり':'なし'))+`<p>A: ${v.a} → ${r.x}、B: ${v.b} → ${r.y}（指定幅の入力）</p>`;
 }
 if(kind==='mos')return mosResult(v,s);
 if(kind==='gates')return formula(`A = ${v.a}、B = ${v.b}`)+table(['A','B','NOT A','AND','OR','XOR','NAND'],[0,1,2,3].map(i=>{const a=i>>1,b=i&1;return [a,b,1-a,a&b,a|b,a^b,1-(a&b)].map(x=>a===v.a&&b===v.b?`<strong class="active-value">${x}</strong>`:x);}));
 if(kind==='nand'){
  const na=1-v.a,nb=1-v.b,nab=1-(v.a&v.b);
  return table(['回路','途中の値','出力'],[['NOT A = NAND(A,A)',`NAND(${v.a},${v.a})`,na],['AND = NAND(NAND(A,B),NAND(A,B))',`NAND(A,B) = ${nab}`,1-nab],['OR = NAND(NAND(A,A),NAND(B,B))',`NOT A = ${na}、NOT B = ${nb}`,1-(na&nb)]]);
 }
 if(kind==='adder'){
  const r=fullAdder(v.a,v.b,v.cin);
  return states(box('A XOR B',v.a^v.b)+box('和 S',r.sum)+box('桁上がり Cout',r.carry))+formula(`${v.a} + ${v.b} + ${v.cin} = ${r.carry}${r.sum}₂ = ${v.a+v.b+v.cin}₁₀`)+`<p>S = A XOR B XOR Cin<br/>Cout = (A AND B) OR (Cin AND (A XOR B))</p>`;
 }
 if(kind==='register')return states(box('入力 D',v.data)+box('クロック CLK',v.clock)+box('保持する値 Q',s.q||0))+`<p>${escape(s.message||'クロックの0 → 1でDをQへ取り込みます。Dだけを変えてもQは保持します。')}</p>`;
 if(kind==='cache'){
  const trace=cacheTrace(['A','B','A','C','A','B'],v.capacity).slice(0,step),last=trace.at(-1);
  return formula(`現在のキャッシュ：${last?last.cache.join(' | '):'空'}（左が最近の参照）`)+table(['参照','判定','追い出す値','参照後'],trace.map(x=>[x.address,x.hit?'HIT':'MISS',x.evicted||'—',x.cache.join(' | ')]))+`<p>${step} / 6 回。ヒット ${trace.filter(x=>x.hit).length} 回、ミス ${trace.filter(x=>!x.hit).length} 回です。</p>`;
 }
 if(kind==='cpu'){
  const rows=[[0,'—',0],[0,'MOV R0, 5',0],[0,'R0に5を入れる',0],[1,'MOV 完了',5],[1,'ADD R0, 3',5],[1,'R0と3を加える',5],[2,'ADD 完了',8]],r=rows[Math.min(step,6)];
  return stages(['フェッチ','デコード','実行'],step?(step-1)%3:-1)+states(box('PC',r[0])+box('R0',r[2]))+formula(r[1])+`<p>${step} / 6 工程。メモリ[0] = MOV R0, 5 ／ メモリ[1] = ADD R0, 3</p>`;
 }
 if(kind==='ast')return `<div class="diagram-scroll"><svg viewBox="0 0 500 270" role="img" aria-label="根が足し算で、右の子が掛け算の抽象構文木"><path d="M220 55 L100 130 M220 55 L330 130 M330 150 L250 230 M330 150 L420 230" class="wire"/><g class="tree-node"><circle cx="220" cy="40" r="32"/><circle cx="100" cy="130" r="30"/><circle cx="330" cy="130" r="30"/><circle cx="250" cy="230" r="30"/><circle cx="420" cy="230" r="30"/></g><g text-anchor="middle"><text x="220" y="47">＋</text><text x="100" y="137">${v.a}</text><text x="330" y="137">×</text><text x="250" y="237">${v.b}</text><text x="420" y="237">${v.c}</text></g></svg></div>`+formula(`${v.a} + ${v.b} × ${v.c}`)+`<p>${['まず子の値を調べます。',`掛け算の葉は ${v.b} と ${v.c} です。`,`部分木の値は ${v.b} × ${v.c} = ${v.b*v.c} です。`,`根の足し算は ${v.a} + ${v.b*v.c} = ${v.a+v.b*v.c} です。`][Math.min(step,3)]}</p>`;
 if(kind==='search'){
  const values=[7,12,19,31,42],found=values.slice(0,step).indexOf(v.target);
  return states(values.map((x,i)=>box(`添字 ${i}`,i<step?`<mark>${x} ${x===v.target?'一致':'≠'}</mark>`:x)).join(''))+formula(found>=0?`添字 ${found} で発見（${step}回比較）`:step===5?'5回比較し、見つかりませんでした':`${step}回比較。次は添字 ${step} を調べます。`);
 }
 if(kind==='coupling')return states(box('注文の処理',v.boundary?'変更を局所化':'変更対象')+box('検索の処理',v.boundary?'変更を局所化':'変更対象')+box('保存アダプター','変更対象'))+`<p>${v.boundary?'呼び出し側は契約を使い、実装の変更をアダプターへ集めます。':'各処理が保存方式の詳細を使うため、それぞれの呼び出しを調べて直します。'}</p>`;
 if(kind==='dns'){
  const flow=v.cached?['ブラウザ → リゾルバー：example.comを問い合わせる','リゾルバー → ブラウザ：キャッシュのアドレスを返す']:['ブラウザ → リゾルバー：example.comを問い合わせる','リゾルバー ↔ ルート：.comの委任先を得る','リゾルバー ↔ .com：example.comの権威サーバーを得る','リゾルバー ↔ 権威サーバー：アドレスを得る','リゾルバー → ブラウザ：アドレスを返す'];
  return stages(flow,step-1)+`<p>${step?flow[step-1]:'まだ問い合わせを始めていません。'} ${step===flow.length?'名前解決が完了しました。':''}</p>`;
 }
 if(kind==='transport'){
  const received=step===0?[]:step===1?[1]:step===2?(v.loss?[1]:[1,2]):step===3?(v.loss?[1,3]:[1,2,3]):[1,2,3],delivered=received.includes(2)?received:received.filter(x=>x===1);
  return states(box('受信済み',received.join(', ')||'なし')+box('アプリへ渡せる連続部分',delivered.join(', ')||'なし'))+formula(v.loss&&step===3?'3が届いても、欠けた2を待ちます':v.loss&&step===4?'2を再送し、1・2・3の順序がそろいます':`転送の段階 ${step}`)+stages(['1を受信',v.loss?'2を喪失':'2を受信','3を受信',...(v.loss?['2を再送']:[])],step-1);
 }
 if(kind==='gradient'){
  let w=v.start;const rows=[['初期値',w.toFixed(4),((w-3)**2).toFixed(4)]];
  for(let i=0;i<step;i++){w=gradientStep(w,v.rate);rows.push([i+1,w.toFixed(4),((w-3)**2).toFixed(4)]);}
  return formula(`w = ${w.toFixed(4)} ／ L(w) = ${((w-3)**2).toFixed(4)} ／ η = ${v.rate}`)+table(['更新回数','w','損失 L(w)'],rows)+`<p>${v.rate<1?'この例では0 < η < 1で最小値へ近づきます。':v.rate===1?'η = 1では最小値をまたいで同じ距離を往復します。':'η > 1では最小値からの距離が拡大します。'}</p>`;
 }
 if(kind==='softmax'){
  const p=softmax([v.a,v.b,v.c],v.temperature);
  return `<div class="probabilities">${p.map((x,i)=>`<div><span>候補${'ABC'[i]}</span><meter min="0" max="1" value="${x}" aria-label="候補${'ABC'[i]}の確率"></meter><b>${(x*100).toFixed(2)}%</b></div>`).join('')}</div>`+formula(`温度 ${v.temperature.toFixed(1)} ／ 確率の合計 ${(p.reduce((a,b)=>a+b,0)*100).toFixed(2)}%`);
 }
 if(kind==='layout'){
  const columns=Math.min(3,Math.floor((v.width+12)/152));
  return `<div class="diagram-scroll"><div class="layout-window" style="width:${v.width}px">${['注文番号','配送状況','到着予定'].map(x=>`<div>${x}</div>`).join('')}</div></div>`+formula(`幅 ${v.width} px → ${columns}列・${Math.ceil(3/columns)}行`)+`<p>2列には 140 × 2 + 12 = 292 px、3列には 140 × 3 + 12 × 2 = 444 px 必要です。</p>`;
 }
 if(kind==='latency'){
  const vals=[v.network,v.server,v.model,v.render],names=['通信','サーバー','モデル','描画'],total=vals.reduce((a,b)=>a+b,0);
  return formula(`合計 ${total} ms`)+`<div class="latency-bar">${vals.map((x,i)=>`<span style="flex:${x||.001}" title="${names[i]} ${x} ms"></span>`).join('')}</div>`+table(['工程','時間','割合'],vals.map((x,i)=>[names[i],`${x} ms`,`${total?(x/total*100).toFixed(1):0}%`]))+`<p>${total?`最も時間を使う工程は${names[vals.indexOf(Math.max(...vals))]}です。`:'すべて0 msと設定されています。'}</p>`;
 }
 throw new Error('Unknown experiment '+kind);
}
function mosResult(v,s){
 const m=nmos(v.vg,v.vd),on=m.current>0,pOn=!v.input;
 return formula(`VGS = ${v.vg.toFixed(1)} V ／ VDS = ${v.vd.toFixed(1)} V ／ ID ≈ ${m.current.toFixed(3)} mA`)+
 `<div class="diagram-scroll"><svg viewBox="0 0 540 340" role="img" aria-label="nMOSの断面。ゲート電圧でソースとドレインの間にチャネルができます。">
 <rect x="40" y="175" width="460" height="120" rx="6" class="substrate"/><text x="270" y="278" text-anchor="middle">p型の基板（0 V）</text>
 <rect x="75" y="175" width="85" height="65" class="terminal"/><rect x="380" y="175" width="85" height="65" class="terminal"/><text x="117" y="203" text-anchor="middle">n⁺</text><text x="422" y="203" text-anchor="middle">n⁺</text>
 <rect x="165" y="147" width="210" height="17" class="oxide"/><text x="270" y="140" text-anchor="middle">酸化膜（絶縁体）</text>
 <rect x="165" y="90" width="210" height="22" class="gate"/><path d="M270 90 V55" class="wire"/><text x="270" y="40" text-anchor="middle">ゲート G：${v.vg.toFixed(1)} V</text>
 <path d="M115 175 V110 H55 M425 175 V110 H485" class="wire"/><text x="80" y="80" text-anchor="middle">S：0 V</text><text x="450" y="80" text-anchor="middle">D：${v.vd.toFixed(1)} V</text>
 <path d="M160 186 H380" class="channel ${m.channel?'channel-on':''}"/>
 ${m.channel?'<path d="M215 115 V168 M270 115 V168 M325 115 V168" class="field"/>':''}
 <path d="M420 224 H115" class="current ${on?'flow':''}" opacity="${on?1:.15}"/>
 <text x="270" y="252" text-anchor="middle">${on?'← 慣用的な電流：DからSへ':'電流は0（近似モデル）'}</text>
 <text x="270" y="325" text-anchor="middle">${m.channel?'チャネルあり：電子の通り道ができる':'チャネルなし：通り道がつながらない'}</text></svg></div>
 <p>${m.channel?(on?'ゲートの電界で電子が酸化膜の下へ集まり、通り道ができます。DとSの電圧差があるため電流が流れます。':'通り道はありますが、DとSの電圧差が0 Vなので電流は流れません。'):'VGSがしきい値以下なので、チャネルを通る電流はこのモデルでは0です。'} ゲートから酸化膜を貫く電流は描きません。電子の移動方向は慣用的な電流と逆です。</p>
 <h4>CMOSインバーターの切り替え</h4>
 <div class="diagram-scroll"><svg viewBox="0 0 540 350" role="img" aria-label="pMOSはVDD側、nMOSはGND側。片方がオンになり出力が反転します。">
 <text x="295" y="27" text-anchor="middle">VDD：3.3 V</text><path d="M295 38 V65" class="wire"/>
 <rect x="225" y="65" width="140" height="55" class="${pOn?'switch-on':'switch-off'}"/><text x="295" y="98" text-anchor="middle">pMOS ${pOn?'ON':'OFF'}</text>
 <path d="M295 120 V225 M295 175 H465 M295 280 V318" class="wire"/>
 <rect x="225" y="225" width="140" height="55" class="${pOn?'switch-off':'switch-on'}"/><text x="295" y="258" text-anchor="middle">nMOS ${pOn?'OFF':'ON'}</text>
 <path d="M80 175 H165 V92 H225 M165 175 V252 H225" class="wire"/><text x="105" y="158" text-anchor="middle">入力 ${v.input}</text><text x="440" y="157" text-anchor="middle">出力 ${1-v.input}</text>
 <path d="M400 175 V204 M380 204 H420 M380 216 H420 M400 216 V318 H295" class="wire"/><text x="460" y="242" text-anchor="middle">負荷容量</text><text x="295" y="343" text-anchor="middle">GND：0 V</text>
 ${s.transient?`<path d="${pOn?'M295 38 V175 H400 V204':'M400 204 V175 H295 V318'}" class="current flow transient"/>`:''}</svg></div>
 ${states(box('pMOS',pOn?'導通':'遮断')+box('nMOS',pOn?'遮断':'導通')+box('出力',pOn?'High / 1':'Low / 0'))}
 <p>${s.transient?(pOn?'pMOS側から負荷容量を充電して出力が上がる様子を、時間を引き延ばして示します。':'負荷容量をnMOS側へ放電して出力が下がる様子を、時間を引き延ばして示します。'):'安定後は充放電が終わり、理想モデルではVDDからGNDへ流れ続ける電流はありません。'} 実回路には漏れ電流があり、切り替え中に両方が一時的に導通する場合もあります。</p>
 <p class="lab-source">出典：<a href="https://computationstructures.org/lectures/cmos/cmos.html">MIT 6.004 CMOS Technology</a>、<a href="https://ocw.mit.edu/courses/6-012-microelectronic-devices-and-circuits-fall-2009/eeb94eab00ebb62a3fde0eec1484bc08_MIT6_012F09_lec11_gradual.pdf">MIT 6.012 MOSFETモデル</a></p>`;
}
