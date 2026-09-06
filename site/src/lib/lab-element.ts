import {defaults,result,maxSteps,labs} from './labs.mjs';
import {registerStep} from './models.mjs';
export class CSLab extends HTMLElement {
 kind='';values:Record<string,any>={};state={step:0,q:0,transient:false,message:''};
 initialized=false;timer:ReturnType<typeof setTimeout>|undefined;
 connectedCallback(){
  if(this.initialized)return;this.initialized=true;this.kind=this.dataset.kind!;this.values=defaults(this.kind);
  this.addEventListener('input',this.onInput);this.addEventListener('change',this.onInput);this.addEventListener('click',this.onClick);
  if(matchMedia('(prefers-reduced-motion: reduce)').matches){
   this.classList.add('paused');
   const button=this.querySelector<HTMLButtonElement>('[data-action="motion"]');
   if(button){button.disabled=true;button.textContent='端末の設定によりアニメーションを停止';}
  }
  this.draw();
 }
 disconnectedCallback(){clearTimeout(this.timer);}
 valid(){
  const invalid=[...this.querySelectorAll<HTMLInputElement>('input')].find(x=>!x.validity.valid||!Number.isFinite(x.valueAsNumber));
  const error=this.querySelector<HTMLElement>('.lab-error')!;error.hidden=!invalid;
  error.textContent=invalid?'指定された範囲と刻みで数値を入力してください。結果は直前の有効な値です。':'';
  return !invalid;
 }
 onInput=(event:Event)=>{
  if(!(event.target instanceof HTMLInputElement||event.target instanceof HTMLSelectElement)||!this.valid())return;
  for(const input of this.querySelectorAll<HTMLInputElement|HTMLSelectElement>('input[name],select[name]')){
   const spec=labs[this.kind as keyof typeof labs].fields.find(f=>f.key===input.name);
   this.values[input.name]=typeof spec?.value==='number'?Number(input.value):input.value;
  }
  this.state.step=0;if(this.kind==='mos')this.values.gate=this.values.vg===3.3?1:0;this.draw();
 };
 onClick=(event:Event)=>{
  if(!(event.target instanceof Element))return;
  const button=event.target.closest<HTMLButtonElement>('button');if(!button||!this.contains(button))return;
  const key=button.dataset.toggle;
  if(key){
   const before=this.values[key];this.values[key]=1-before;this.state.step=0;
   if(this.kind==='mos'&&key==='gate'){this.values.vg=this.values.gate?3.3:0;this.querySelector<HTMLInputElement>('[name="vg"]')!.value=String(this.values.vg);}
   if(this.kind==='mos'&&key==='input'){clearTimeout(this.timer);this.state.transient=true;this.timer=setTimeout(()=>{this.state.transient=false;this.draw();},1600);}
   if(this.kind==='register'){
    if(key==='clock'){
     this.state.q=registerStep(this.state.q,this.values.data,before,this.values.clock);
     this.state.message=this.values.clock?`0 → 1：D = ${this.values.data} を取り込みました。`:'1 → 0：保持したQは変わりません。';
    }else this.state.message='Dが変わりました。次のクロックの立ち上がりまでQを保持します。';
   }
  }
  if(button.dataset.bit!==undefined){
   this.values.a=(this.values.a^(2**Number(button.dataset.bit)))%(2**this.values.width);
   this.querySelector<HTMLInputElement>('[name="a"]')!.value=String(this.values.a);
  }
  const action=button.dataset.action;
  if(action==='next'&&this.valid())this.state.step=Math.min(this.state.step+1,maxSteps(this.kind,this.values));
  if(action==='reset')this.state.step=0;
  if(action==='motion'){
   const paused=this.classList.toggle('paused');button.setAttribute('aria-pressed',String(paused));button.textContent=paused?'アニメーションを再開':'アニメーションを一時停止';return;
  }
  const focusBit=button.dataset.bit;this.draw();
  if(focusBit!==undefined)this.querySelector<HTMLButtonElement>(`[data-bit="${focusBit}"]`)?.focus();
 };
 draw(){
  this.querySelector<HTMLElement>('.lab-result')!.innerHTML=result(this.kind,this.values,this.state);
  for(const button of this.querySelectorAll<HTMLButtonElement>('[data-toggle]')){
   const on=!!this.values[button.dataset.toggle!];button.setAttribute('aria-pressed',String(on));button.querySelector('span')!.textContent=on?'1 / ON':'0 / OFF';
  }
  const next=this.querySelector<HTMLButtonElement>('[data-action="next"]');if(next)next.disabled=this.state.step>=maxSteps(this.kind,this.values);
 }
}
if(!customElements.get('cs-lab'))customElements.define('cs-lab',CSLab);
