"""Derive semantic HTML from the PDF's authoritative TeX with Pandoc.

Only project macros and print layout are adapted; unknown TeX stops the build.
"""
from pathlib import Path
import collections
import html
import json
import re
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
SITE=ROOT/'site'
BASE='/cs-doc'
PREAMBLE=r'''
\newcommand{\ChapterRef}[1]{\ref{#1}}
\newcommand{\term}[1]{\textbf{#1}}
\newcommand{\guideterm}[1]{\textbf{#1}}
\newcommand{\code}[1]{\texttt{#1}}
\newcommand{\takeaway}[1]{\begin{quote}\textbf{要点}\quad #1\end{quote}}
\newcommand{\source}[1]{\begin{quote}出典：#1\end{quote}}
\newcommand{\materialref}[3]{\paragraph{\href{#1}{#2}} #3\par}
\newcommand{\chapterimage}[3]{\begin{figure}\includegraphics{assets/#1}\caption{#2}\label{#3}\end{figure}}
\newcommand{\sectionimage}[3]{\begin{figure}\includegraphics{assets/#1}\caption{#2}\label{#3}\end{figure}}
\newcommand{\inlineimage}[1]{\includegraphics{assets/#1}}
'''
LABS={
 '01-digital-computer':{'電圧と論理値':'voltage','2進数':'binary','負数と2の補数':'complement','トランジスタ':'mos','論理ゲート':'gates','NANDによる回路構成':'nand','加算器':'adder','多ビット加算とALU':'bits','クロックとレジスタ':'register','メモリ階層':'cache','CPUの命令実行':'cpu'},
 '02-language':{'ASTの評価':'ast'},'03-runtime-data':{'計算量の評価軸':'search'},
 '04-software-engineering':{'情報隠蔽':'coupling'},'05-internet':{'DNS':'dns'},
 '06-request-delivery':{'TCPのデータ転送':'transport'},
 '07-language-model':{'勾配降下法':'gradient','次トークン予測':'softmax'},
 '08-browser':{'レイアウト':'layout'},'09-practice':{'遅延の調査':'latency'},
}

def pandoc(source,source_format,target,extra=()):
    r=subprocess.run(['pandoc','--from',source_format,'--to',target,*extra],input=source,text=True,capture_output=True,cwd=ROOT)
    if r.returncode or r.stderr.strip(): raise RuntimeError(r.stderr)
    return r.stdout

def expand_inputs(text):
    def expand(m):
        p=ROOT/(m[1] if m[1].endswith('.tex') else m[1]+'.tex')
        return expand_inputs(p.read_text())
    return re.sub(r'\\input\{([^}]+)\}',expand,text)

def clean_source(text):
    text=expand_inputs(text)
    listings=[]
    def protect(m):
        listings.append(m[0]);return f'CSLISTINGPLACEHOLDER{len(listings)-1}END'
    text=re.sub(r'\\begin\{lstlisting\}.*?\\end\{lstlisting\}',protect,text,flags=re.S)
    text=re.sub(r'(?<!\\)%[^\n]*','',text)
    text=re.sub(r'\\(?:begin|end)\{(?:chapterabstract|samepage|center)\}','\n',text)
    text=text.replace(r'\begin{learninggoals}',r'\paragraph{到達目標}\begin{itemize}').replace(r'\end{learninggoals}',r'\end{itemize}')
    text=re.sub(r'\\begin\{minipage\}(?:\[[^]]*\])?\{[^}]*\}','',text).replace(r'\end{minipage}','')
    text=re.sub(r'\\(?:vspace|hspace)\*?\{[^}]*\}','',text)
    text=re.sub(r'\\(?:begingroup|endgroup|medskip|smallskip|bigskip|centering|noindent|clearpage|newpage|raggedright|footnotesize|small|normalsize|FloatBarrier)\b','',text)
    text=re.sub(r'\\addcontentsline\{[^}]*\}\{[^}]*\}\{[^}]*\}','',text)
    text=re.sub(r'\\BookIndex\{[^}]*\}\{[^}]*\}','',text)
    def table(m):
        spec=re.sub(r'@\{[^}]*\}|>\{[^}]*\}','',m[1])
        spec=re.sub(r'p\{[^}]*\}','l',spec).replace('Y','l').replace('X','l')
        return r'\begin{tabular}{'+spec+'}'
    text=re.sub(r'\\begin\{tabularx\}\{\\(?:linewidth|textwidth)\}\{((?:[^{}]|\{[^{}]*\})*)\}',table,text)
    text=text.replace(r'\end{tabularx}',r'\end{tabular}')
    for i,listing in enumerate(listings):text=text.replace(f'CSLISTINGPLACEHOLDER{i}END',listing)
    return text

def walk(value):
    if isinstance(value,dict):
        yield value
        for v in value.values():yield from walk(v)
    elif isinstance(value,list):
        for v in value:yield from walk(v)

def plain(n):
    if isinstance(n,list):return ''.join(plain(x) for x in n)
    if not isinstance(n,dict):return ''
    t=n.get('t');c=n.get('c')
    if t=='Str':return c
    if t in ('Space','SoftBreak','LineBreak'):return ' '
    if t in ('Code','Math'):return c[-1]
    if t in ('Link','Image','Span'):return plain(c[1])
    return plain(c)

def main():
    files=re.findall(r'\\input\{(chapters/[^}]+)\}',(ROOT/'main.tex').read_text())
    definitions='\n'.join(p.read_text().split(r'\subsection')[0] for p in sorted((ROOT/'chapters/terms').glob('*.tex')))
    records=[];labels={};label_text={};unknown=collections.Counter()
    for filename in files:
        path=ROOT/(filename+'.tex');slug=path.stem;source=clean_source(path.read_text())
        doc=json.loads(pandoc(PREAMBLE+(definitions if slug.startswith('92-') else '')+source,'latex','json'))
        title=next(plain(n['c'][2]) for n in doc['blocks'] if n['t']=='Header')
        if 1<=int(slug[:2])<=9:title=f'第{int(slug[:2])}章　{title}'
        for n in walk(doc):
            t=n.get('t');c=n.get('c')
            if t in ('RawInline','RawBlock') and c[0]=='latex':unknown[c[1]]+=1
            if t=='Header' and c[1][0]:
                labels[c[1][0]]=(slug,c[1][0]);label_text[c[1][0]]=title if c[0]==1 else plain(c[2])
            elif t in ('Span','Div','Figure') and c[0][0]:
                labels[c[0][0]]=(slug,c[0][0])
                if t=='Figure':label_text[c[0][0]]=plain(c[1])
        records.append({'slug':slug,'title':title,'source':str(path.relative_to(ROOT)),'doc':doc})
    for cmd in list(unknown):
        if re.fullmatch(r'\\(?:index|label)\{[^}]*\}',cmd):del unknown[cmd]
    if unknown:raise RuntimeError('Unsupported TeX: '+str(unknown))
    output=[]
    for record in records:
        doc=record.pop('doc');slug=record['slug'];terms=[]
        def rewrite(v):
            if isinstance(v,list):return [rewrite(x) for x in v]
            if not isinstance(v,dict):return v
            t=v.get('t');c=v.get('c')
            if t in ('RawInline','RawBlock') and c[0]=='latex':return {'t':'Str','c':''} if t=='RawInline' else {'t':'Null'}
            if t=='Image':
                src=c[2][0];asset=ROOT/src
                if not src.startswith('assets/') or not asset.is_file():raise ValueError('Missing image '+src)
                c[2][0]=BASE+'/book-assets/'+src.removeprefix('assets/')
                if not c[1]:c[1]=[{'t':'Str','c':'本文の補足図（'+asset.stem+'）'}]
                c[0][2].extend([['loading','lazy'],['decoding','async']])
            if t=='Link' and c[2][0].startswith('#'):
                key=c[2][0][1:]
                if key not in labels:raise ValueError('Unresolved reference '+key)
                target,anchor=labels[key];c[2][0]=f'{BASE}/guide/{target}/#{anchor}'
                if key in label_text:c[1]=[{'t':'Str','c':'「'+label_text[key]+'」'}]
            return {k:rewrite(x) for k,x in v.items()}
        doc=rewrite(doc)
        counter=0
        for node in walk(doc):
            if node.get('t')=='CodeBlock':
                counter+=1
                if not node['c'][0][0]:node['c'][0][0]=f'code-{slug}-{counter}'
        headings=[];parts=[];blocks=[];active_lab=None;section='';seen=set()
        def flush():
            figures=[]
            if active_lab:
                for block in blocks[:]:
                    if block['t']=='Figure' or (block['t']=='Para' and all(n['t'] in ('Image','Space','SoftBreak') for n in block['c'])):
                        figures.append(block);blocks.remove(block)
            def render(chunk):return pandoc(json.dumps({**doc,'blocks':chunk}),'json','html5',('--mathml','--wrap=none'))
            if blocks:parts.append({'html':render(blocks.copy()),'lab':''});blocks.clear()
            if active_lab:
                parts.append({'html':'','lab':active_lab})
                headings.append({'depth':3,'slug':'lab-'+active_lab,'text':'動かして確かめる'})
            if figures:parts.append({'html':'<details class="reference-diagram"><summary>本文の補足図を開く</summary>'+render(figures)+'</details>','lab':''})
        for n in doc['blocks']:
            if n['t']=='Header':
                level,attr,ins=n['c'];text=plain(ins)
                if level in (1,2):flush();active_lab=LABS.get(slug,{}).get(text);seen.add(text)
                if level==1:
                    blocks.append({'t':'RawBlock','c':['html',f'<span id="{html.escape(attr[0],quote=True)}"></span>']});continue
                n['c'][0]=min(3,level);headings.append({'depth':n['c'][0],'slug':attr[0],'text':text})
                if level==2:section=attr[0]
            for child in walk(n):
                if child.get('t')=='Strong':terms.append({'text':plain(child['c']),'anchor':section})
            blocks.append(n)
        flush()
        if set(LABS.get(slug,{}))-seen:raise ValueError('Missing lab section in '+slug)
        record.update(headings=headings,parts=parts,terms=terms);output.append(record)
    target=SITE/'src/data/book.json';target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
    shutil.copytree(ROOT/'assets',SITE/'public/book-assets',dirs_exist_ok=True,ignore=shutil.ignore_patterns('image-prompts','*.md','*.json'))
    pdf=ROOT/'build/information-engineering-basics.pdf'
    if pdf.exists():shutil.copy2(pdf,SITE/'public/information-engineering-basics.pdf')
    print(f'Prepared {len(output)} chapters; {sum(bool(p["lab"]) for r in output for p in r["parts"])} experiments')

if __name__=='__main__':main()
