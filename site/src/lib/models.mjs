/** Deterministic teaching models; never evaluate user-provided code. */
export function fixedWidth(a,b,width,operation) {
 const mod=2**width,mask=mod-1,wrap=n=>((n%mod)+mod)%mod,signed=n=>n>=mod/2?n-mod:n,x=wrap(a),y=wrap(b);
 const raw={AND:()=>x&y,OR:()=>x|y,XOR:()=>x^y,NOT:()=>(~x)&mask,ADD:()=>x+y,SUB:()=>x-y,SHL:()=>x*2,SHR:()=>Math.floor(x/2)}[operation]();
 const value=wrap(raw),mathematical=operation==='ADD'?signed(x)+signed(y):signed(x)-signed(y);
 return {x,y,raw,value,signed:signed(value),carry:raw>=mod,borrow:raw<0,overflow:['ADD','SUB'].includes(operation)&&(mathematical< -mod/2||mathematical>=mod/2),binary:value.toString(2).padStart(width,'0')};
}
export const fullAdder=(a,b,cin)=>({sum:a^b^cin,carry:(a&b)|(cin&(a^b))});
export function nmos(vg,vd,vt=1) {
 const u=vg-vt;
 // Source/body grounded, long-channel approximation, k=1 mA/V².
 return {channel:u>0,current:u<=0||vd===0?0:vd<u?u*vd-vd*vd/2:u*u/2};
}
export function softmax(logits,temperature) {
 const max=Math.max(...logits),exp=logits.map(x=>Math.exp((x-max)/temperature)),sum=exp.reduce((a,b)=>a+b,0);
 return exp.map(x=>x/sum);
}
export const gradientStep=(w,rate)=>w-rate*2*(w-3);
export const registerStep=(q,data,before,after)=>before===0&&after===1?data:q;
export function cacheTrace(addresses,capacity) {
 const cache=[];
 return addresses.map(address=>{const at=cache.indexOf(address),hit=at>=0;if(hit)cache.splice(at,1);cache.unshift(address);const evicted=cache.length>capacity?cache.pop():null;return {address,hit,evicted,cache:[...cache]};});
}
