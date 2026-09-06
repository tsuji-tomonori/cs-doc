import {readFileSync,existsSync,readdirSync} from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {createWindow} from '@mixmark-io/domino';
import {labs} from '../src/lib/labs.mjs';
const root=path.resolve('dist'),files=[];
function collect(dir){for(const f of readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,f.name);if(f.isDirectory())collect(p);else if(f.name.endsWith('.html'))files.push(p);}}
collect(root);
const documents=new Map(files.map(p=>[p,createWindow(readFileSync(p,'utf8')).document]));
const errors=[];let experiments=0,math=0,chars=0;
for(const [file,doc] of documents){
 const ids=new Set();for(const node of doc.querySelectorAll('[id]')){if(ids.has(node.id))errors.push(`${file}: duplicate #${node.id}`);ids.add(node.id);}
 for(const el of doc.querySelectorAll('a[href],img[src],script[src],link[href]')){
  const href=el.getAttribute('href')||el.getAttribute('src');if(!href||/^(https?:|mailto:|data:)/.test(href))continue;
  const url=new URL(href,'https://local.invalid/cs-doc/'+path.relative(root,file));
  if(!url.pathname.startsWith('/cs-doc/')){errors.push(`${file}: outside base ${href}`);continue;}
  let target=path.join(root,decodeURIComponent(url.pathname.slice('/cs-doc/'.length)));
  if(target.endsWith('/')||!path.extname(target))target=path.join(target,'index.html');
  if(!existsSync(target)){errors.push(`${file}: missing ${href}`);continue;}
  if(url.hash&&documents.has(target)&&!documents.get(target).getElementById(decodeURIComponent(url.hash.slice(1))))errors.push(`${file}: missing anchor ${href}`);
 }
 for(const lab of doc.querySelectorAll('cs-lab')){experiments++;assert.ok(labs[lab.getAttribute('data-kind')]);assert.ok(lab.querySelector('.lab-result').textContent.length>20);assert.ok(lab.querySelector('noscript'));}
 math+=doc.querySelectorAll('math').length;chars+=(doc.querySelector('.book-body')?.textContent||'').length;
}
assert.deepEqual(errors,[]);assert.equal(experiments,20);assert.ok(math>200);assert.ok(chars>80000);
assert.ok(existsSync('dist/pagefind/pagefind.js'));assert.ok(existsSync('dist/information-engineering-basics.pdf'));
console.log(`Verified ${files.length} pages, ${experiments} experiments, ${math} equations, ${chars} text characters; all local links and anchors resolve.`);
