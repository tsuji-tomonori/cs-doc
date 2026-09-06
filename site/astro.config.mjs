import {defineConfig} from 'astro/config';
import starlight from '@astrojs/starlight';
import book from './src/data/book.json' with {type:'json'};
export default defineConfig({
 site:'https://tsuji-tomonori.github.io',base:'/cs-doc',
 integrations:[starlight({
  title:'情報工学入門',description:'物理からアプリまで、読みながら動かして学ぶ情報工学',
  locales:{root:{label:'日本語',lang:'ja'}},
  social:[{icon:'github',label:'GitHub',href:'https://github.com/tsuji-tomonori/cs-doc'}],
  customCss:['./src/styles/book.css'],tableOfContents:{minHeadingLevel:2,maxHeadingLevel:2},
  sidebar:[
   {label:'学習を始める',link:'/'},
   {label:'本文',items:book.filter(p=>Number(p.slug.slice(0,2))<90).map(p=>({label:p.title,link:`/guide/${p.slug}/`}))},
   {label:'付録と参考資料',items:book.filter(p=>Number(p.slug.slice(0,2))>=90).map(p=>({label:p.title,link:`/guide/${p.slug}/`}))},
   {label:'用語索引',link:'/term-index/'},{label:'PDFを読む',link:'/information-engineering-basics.pdf'}
  ]
 })]
});
