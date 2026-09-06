import html
import json
import re
import unittest
from html.parser import HTMLParser
from prepare_book import ROOT,PREAMBLE,clean_source,pandoc

class CodeParser(HTMLParser):
    def __init__(self):super().__init__();self.blocks=[];self.active=False
    def handle_starttag(self,tag,attrs):
        if tag=='pre':self.active=True;self.blocks.append('')
    def handle_endtag(self,tag):
        if tag=='pre':self.active=False
    def handle_data(self,text):
        if self.active:self.blocks[-1]+=text

class ContentTests(unittest.TestCase):
    def test_listings_protect_percent_and_tex_literals(self):
        source=r'''\chapter{試験}
\section{表と式}
\term{条件}を保ちます。$x^2 + 1$です。
\begin{tabularx}{\textwidth}{@{}p{30mm}Y@{}}
名前 & 説明 \\
A & 値です。 \\
\end{tabularx}
\begin{lstlisting}[language=Python]
print(13 % 2)
print("100% and \\newpage")
\end{lstlisting}
'''
        cleaned=clean_source(source);self.assertIn('13 % 2',cleaned);self.assertIn('100% and',cleaned)
        doc=json.loads(pandoc(PREAMBLE+cleaned,'latex','json'));self.assertIn('Table',[b['t'] for b in doc['blocks']])
        self.assertIn('print(13 % 2)',next(b for b in doc['blocks'] if b['t']=='CodeBlock')['c'][1])

    def test_every_section_term_and_listing_survives(self):
        book=json.loads((ROOT/'site/src/data/book.json').read_text())
        expected=re.findall(r'\\input\{(chapters/[^}]+)\}',(ROOT/'main.tex').read_text());self.assertEqual(len(book),len(expected))
        for chapter in book:
            source=(ROOT/chapter['source']).read_text();rendered=''.join(p['html'] for p in chapter['parts'])
            sections=re.findall(r'\\section\*?\{([^}]+)\}',source)
            self.assertEqual(sections,[h['text'] for h in chapter['headings'] if h['depth']==2],chapter['slug'])
            listings=re.findall(r'\\begin\{lstlisting\}(?:\[[^]]*\])?\s*\n(.*?)\\end\{lstlisting\}',source,re.S)
            parser=CodeParser();parser.feed(rendered)
            self.assertEqual([x.strip() for x in listings],[x.strip() for x in parser.blocks],chapter['slug'])
            for term in re.findall(r'\\term\{([^{}]+)\}',source):
                if '\\' not in term and '$' not in term:self.assertTrue(html.escape(term,quote=False) in rendered,term)
if __name__=='__main__':unittest.main()
