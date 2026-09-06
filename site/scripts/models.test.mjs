import test from 'node:test';
import assert from 'node:assert/strict';
import {fixedWidth,fullAdder,nmos,softmax,gradientStep,cacheTrace,registerStep} from '../src/lib/models.mjs';
import {labs,defaults,result,maxSteps} from '../src/lib/labs.mjs';
test('全加算器の全入力で和と桁上がりが一致する',()=>{
 for(let a=0;a<2;a++)for(let b=0;b<2;b++)for(let c=0;c<2;c++){const r=fullAdder(a,b,c);assert.equal(2*r.carry+r.sum,a+b+c);}
});
test('固定幅の全4ビット入力と符号付き境界を検証する',()=>{
 for(let a=0;a<16;a++)for(let b=0;b<16;b++){
  assert.equal(fixedWidth(a,b,4,'AND').value,a&b);assert.equal(fixedWidth(a,b,4,'XOR').value,a^b);
  const r=fixedWidth(a,b,4,'ADD');assert.equal(r.value,(a+b)%16);assert.equal(r.carry,a+b>=16);
 }
 assert.equal(fixedWidth(127,1,8,'ADD').signed,-128);assert.equal(fixedWidth(127,1,8,'ADD').overflow,true);
 assert.equal(fixedWidth(255,1,8,'ADD').overflow,false);assert.equal(fixedWidth(-1,0,8,'OR').value,255);
 assert.equal(fixedWidth(0,1,8,'SUB').borrow,true);assert.equal(fixedWidth(65535,0,16,'SHL').value,65534);
 assert.equal(fixedWidth(128,0,8,'SHR').value,64);
});
test('NMOSはしきい値と電圧差の両方を必要とする',()=>{
 assert.equal(nmos(1,3.3).current,0);assert.equal(nmos(0,3.3).channel,false);
 assert.equal(nmos(3.3,0).channel,true);assert.equal(nmos(3.3,0).current,0);
 assert.equal(nmos(2,.5).current,.375);assert.equal(nmos(2,2).current,.5);
 assert.ok(nmos(3.3,3.3).current>0);
 const v=defaults('mos');assert.ok(!result('mos',v).includes('current flow transient'));
 assert.ok(result('mos',{...v,input:1},{transient:true}).includes('current flow transient'));
});
test('softmaxは数値的に安定し温度で集中度が変わる',()=>{
 const p=softmax([1000,999,998],1);assert.ok(p.every(Number.isFinite));assert.ok(Math.abs(p.reduce((a,b)=>a+b)-1)<1e-12);
 assert.ok(softmax([2,1,0],.2)[0]>softmax([2,1,0],2)[0]);assert.deepEqual(softmax([0,0,0],1),[1/3,1/3,1/3]);
});
test('キャッシュ容量とクロックの立ち上がりを検証する',()=>{
 const refs=['A','B','A','C','A','B'];assert.equal(cacheTrace(refs,1).filter(x=>x.hit).length,0);
 assert.equal(cacheTrace(refs,2).filter(x=>x.hit).length,2);assert.equal(cacheTrace(refs,3).filter(x=>x.hit).length,3);
 assert.equal(registerStep(0,1,0,1),1);assert.equal(registerStep(1,0,1,0),1);assert.equal(registerStep(1,0,1,1),1);
});
test('勾配降下の収束・振動・発散を区別する',()=>{
 assert.ok(Math.abs(gradientStep(-2,.2)-3)<5);assert.equal(gradientStep(-2,1),8);assert.ok(Math.abs(gradientStep(-2,1.2)-3)>5);
});
test('全教材の初期値・途中・最終段階に不正数値がない',()=>{
 for(const kind of Object.keys(labs)){const v=defaults(kind);for(let step=0;step<=maxSteps(kind,v);step++)assert.doesNotMatch(result(kind,v,{step,q:0}),/NaN|undefined|Infinity/);}
});
test('TCPは欠けた2を待ち、探索は発見時に終了する',()=>{
 assert.match(result('transport',{loss:1},{step:3}),/欠けた2/);assert.match(result('transport',{loss:1},{step:4}),/1・2・3/);
 assert.equal(maxSteps('search',{target:7}),1);assert.equal(maxSteps('search',{target:31}),4);assert.equal(maxSteps('search',{target:99}),5);
 assert.equal(maxSteps('dns',{cached:1}),2);assert.equal(maxSteps('dns',{cached:0}),5);
});
