import {readFile} from 'node:fs/promises';
import assert from 'node:assert/strict';
const root=new URL('../dist/pagefind/',import.meta.url).pathname;
globalThis.fetch=async input=>new Response(await readFile(root+new URL(input,'https://example.test').pathname.split('/pagefind/')[1]));
const pagefind=await import(root+'pagefind.js');
await pagefind.options({basePath:'/pagefind/',baseUrl:'/cs-doc/',language:'ja'});
for(const word of ['トランジスタ','2の補数','NAND','DNS','Attention','レイアウト']){
 const found=await pagefind.search(word);assert.ok(found.results.length,`No result for ${word}`);
 const first=await found.results[0].data();assert.ok(first.excerpt&&first.meta.title&&first.url.startsWith('/cs-doc/'));
 console.log(`${word}: ${found.results.length} results`);
}
