# coding: UTF-8

import sys
import re
import codecs

## config ##
doc = [
r"""\documentclass[a4j]{jarticle}
\usepackage{listings,ascmac}
\usepackage[dvips]{graphicx}
\usepackage{slashbox}
\usepackage{multirow}
\lstset{language=C, numbers=left, breaklines=true, breakindent=10pt, frame=ltrb, basicstyle=\small\ttfamily }

\begin{document}
""",
r"""
\end{document}
"""
]
bf = [r"\bf{",r"}\rm{}"]
ul = [r"\underline{",r"}\rm{}"]
ilcode = [r"\verb`",r"`"]
hl = "\\noindent \\rule{\\textwidth}{0.1mm}\n"
qt = ["\\begin{quote}\n","\\end{quote}\n"]
item = ["\\begin{itemize}\n","\\end{itemize}\n","\\item "]
enum = ["\\begin{enumerate}\n","\\end{enumerate}\n","\\item "]
desc = ["\\begin{description}\n","\\end{description}\n","\\item"]
## constant ##
begin = 0
end = 1
prefix = 2

## functions ##
def toTex(line,ex):
	r = re.compile(ex).search(line)
	if r != None:
		str = r.group(0);
		post = r.string[r.end():]
		pre = r.string[:r.start()]
		line = pre + "\\" + str + toTex(post,ex)
	return line

def bold(line):
	r = re.compile("##[^#]+?##").search(line)
	if r != None:
		str = r.group(0);
		post = r.string[r.end():]
		pre = r.string[:r.start()]
		r = re.compile("[^#]+").search(str)
		str = bf[begin] + r.group(0) + bf[end]
		line = pre + str + bold(post)
	return line

def uline(line):
	r = re.compile("__[^#]+?__").search(line)
	if r != None:
		str = r.group(0);
		post = r.string[r.end():]
		pre = r.string[:r.start()]
		r = re.compile("[^_]+").search(str)
		str = ul[begin] + r.group(0) + ul[end]
		line = pre + str + uline(post)
	return line

def code(line):
	r = re.compile("`[^`]+?`").search(line)
	if r != None:
		str = r.group(0);
		post = r.string[r.end():]
		pre = r.string[:r.start()]
		r = re.compile("[^`]+").search(str)
		str = ilcode[begin] + r.group(0) + ilcode[end]
		line = pre + str + code(post)
	return line
def hline(line):
	r = re.compile("^(-{3,}?)").search(line)
	if r != None:
		line = hl + "\n"
	return line

def header(line):
	r = re.compile("^#+")
	m = r.search(line)
	if m != None:
		sharp = m.group(0)
		post = m.string[m.end():]
		r = re.compile("\r|\n")
		m = r.search(post)
		section_title = m.string[:m.start()]
		section_depth = len(sharp)
		if section_depth == 2:
			line = "\\section{" + section_title +"}\n"
		elif section_depth>2:
			depth = section_depth - 2
			sub = ""
			while depth:
				sub += "sub"
				depth -= 1
			line = "\\" + sub + "section{" + section_title + "}\n"
	return line
def image(line):
	r = re.compile("^!\[\s*.+\s*\]\(\s*.+\s*\)")
	m = r.search(line)
	if m != None:
		r = re.compile("\[\s*")
		m = r.search(line)
		str = m.string[m.end():]
		r = re.compile("\s*\]")
		m = r.search(str)
		caption = m.string[:m.start()]
		str = m.string[m.end():]
		r = re.compile("\(\s*")
		m = r.search(str)
		str = m.string[m.end():]
		r = re.compile("\s*\)")
		m = r.search(str)
		url = m.string[:m.start()]
		line = """\\begin{figure}[htbp]
\\begin{center}
\\includegraphics[width=150mm]{"""+url+"""}
\\caption{{\\bf """+caption+"""}}
\\label{default}
\\end{center}
\\end{figure}"""
	return line
def inline(line):
	line = bold(line)
	line = uline(line)
	line = code(line)
	line = hline(line)
	line = header(line)
	line = image(line)
	return line
depth = 0
block = "none"
def isQuote(line):
	r = re.compile("^\s?>\s+")
	m = r.search(line)
	return m != None
def isItem(line):
	r = re.compile("^\t?[*|+|-]\s+")
	m = r.search(line)
	return m != None
def isEnum(line):
	r = re.compile("^\t?[0-9]+\.\s+")
	m = r.search(line)
	return m != None
def isDesc(line):
	r = re.compile("^\t?[^0-9]+\.\s+")
	m = r.search(line)
	return m != None
def isCode(line):
	r = re.compile("^\`{3}\s*")
	m = r.search(line)
	return m != None
def codeHead(line):
	r = re.compile("^\`{3}\s*")
	m = r.search(line)
	if m != None:
		str = m.string[m.end():]
		r = re.compile("\s*:\s*")
		m = r.search(str)
		lang = m.string[:m.start()]
		str = m.string[m.end():]
		r = re.compile("\r|\n")
		m = r.search(str)
		caption = m.string[:m.start()]
		line = "\\begin{lstlisting}[language="+lang+",caption="+caption+"]\n"
	return line
def isScreen(line):
	r = re.compile("^\*{3,}\s?")
	m = r.search(line)
	return m != None
def isItemBox(line):
	r = re.compile("={3,}\s?")
	m = r.search(line)
	return m != None
def itemBoxHead(line):
	r = re.compile("[^=]+\s?")
	m = r.search(line)
	if m != None:
		head = m.group(0).rstrip()
		pre = m.string[:m.start()]
		post = m.string[m.end():]
		pos = ""
		if len(pre) == 0:
			pos = "l"
		elif len(post) == 0:
			pos = "r"
		else:
			pos = "c"
		line = "\\begin{itembox}["+pos+"]"+"{"+head+"}\n"
	return line
def isMath(line):
	r = re.compile("^\${3}")
	m = r.search(line)
	return m != None
def _analyze(line):
	global block
	global depth
	status = "analyze"
	next = True
	if isQuote(line):
		line = qt[begin]
		status = "quote"
		next = False
	elif isItem(line):
		line = ""
		block = "item"
		status = "item"
		next = False
	elif isEnum(line):
		line = ""
		block = "enum"
		status = "enum"
		next = False
	elif isDesc(line):
		line = ""
		block = "desc"
		status = "desc"
		next = False
	elif isCode(line):
		line = codeHead(line)
		status = "code"
	elif isScreen(line):
		line = "\\begin{screen}\n"
		block = "screen"
		status = "screen"
		depth = 1
	elif isItemBox(line):
		line = itemBoxHead(line)
		block = "itembox"
		status = "itembox"
		depth = 1
	elif isMath(line):
		line = "\\begin{eqnarray}\n"
		status = "math"
	else:
		line = inline(line)
		if depth > 0:
			status = block
	return (line,status,next)
def _quote(line):
	status = "quote"
	next = True
	r = re.compile("^\s?>\s+")
	m = r.search(line)
	if m != None:
		post = m.string[m.end():]
		line = inline(post).rstrip() + " \\\\\n";
	else:
		line = qt[end]
		status = 'analyze'
		next = False
	return (line,status,next)
def _item(line):
	status = "item"
	next = True
	global depth
	r = re.compile("^\t?[*|+|-]\s+")
	m = r.search(line)
	d = len(re.compile("^\t?").search(line).group(0)) + 1
	if m != None:
		post = m.string[m.end():]
		if d == depth:
			(post,status,next) = _analyze(post)
			line = item[prefix] + post
		elif d > depth:
			line = item[begin]
			depth = d
			next = False
		else :
			line = item[end]
			depth = d
			next = False
	else:
		if d > depth:
			line = ""
		else :
			line = item[end]
			depth = depth - 1
		status = 'analyze'
		next = False
		
	return (line,status,next)
def _enum(line):
	status = "enum"
	next = True
	global depth
	r = re.compile("^\t?[0-9]+\.\s+")
	m = r.search(line)
	d = len(re.compile("^\t?").search(line).group(0)) + 1
	if m != None:
		post = m.string[m.end():]
		if d == depth:
			(post,status,next) = _analyze(post)
			line = enum[prefix] + post
		elif d > depth:
			line = enum[begin]
			depth = d
			next = False
		else :
			line = enum[end]
			depth = d
			next = False
	else:
		if d > depth:
			line = ""
		else :
			line = enum[end]
			depth = depth - 1
		status = 'analyze'
		next = False
	return (line,status,next)
def _desc(line):
	status = "desc"
	next = True
	global depth
	r = re.compile("^\t?[^0-9]+\.\s+")
	m = r.search(line)
	d = len(re.compile("^\t?").search(line).group(0)) + 1
	if m != None:
		post = m.string[m.end():]
		if d == depth:
			m = re.compile("^\t?").search(m.group(0))
			pre = re.compile(".\s+?").sub("",m.string[m.end():])
			(post,status,next) = _analyze(post)
			line = desc[prefix] + "[" + pre + "]" + post
		elif d > depth:
			line = desc[begin]
			depth = d
			next = False
		else :
			line = desc[end]
			depth = d
			next = False
	else:
		if d > depth:
			line = ""
		else :
			line = desc[end]
			depth = depth - 1
		status = 'analyze'
		next = False
	return (line,status,next)
def _code(line):
	status = "code"
	next = True
	r = re.compile("^\`{3}\s*")
	m = r.search(line)
	if m != None:
		line = "\\end{lstlisting}\n"
		status = 'analyze'
	return (line,status,next)
math_count = 0
def _math(line):
	global math_count
	status = "math"
	next = True
	r = re.compile("^\${3}")
	m = r.search(line)
	if m != None:
		line = "\\end{eqnarray}\n"
		status = 'analyze'
		math_count = 0
	else :
		if math_count != 0:
			line = "\\\\\n" + line
		math_count = math_count + 1
	return (line,status,next)
def _screen(line):
	status = "screen"
	next = True
	r = re.compile("^\*{3,}\s?")
	m = r.search(line)
	if m == None:
		(line,status,next) = _analyze(line)
	else :
		line = "\\end{screen}\n"
		status = 'analyze'
		depth = 0
	return (line,status,next)
def _itembox(line):
	status = "itembox"
	next = True
	r = re.compile("={3,}\s?")
	m = r.search(line)
	if m == None:
		(line,status,next) = _analyze(line)
	else :
		line = "\\end{itembox}\n"
		status = 'analyze'
		depth = 0
	return (line,status,next)
def _table(line):
	return (line,status,next)
struct_functions = {
'analyze':_analyze,
'quote':_quote,
'item':_item,
'enum':_enum,
'desc':_desc,
'code':_code,
'math':_math,
'screen':_screen,
'itembox':_itembox,
'table':_table,
}
def struct(f,o,line,status,next):
	if next:
		line = f.readline()
	if line:
		(l,s,n) = struct_functions.get(status)(line)
		o.write(l)
		struct(f,o,line,s,n)
	else:
		return

## main ##
argvs = sys.argv
argc = len(argvs)
if (argc != 2):
	print 'Usage: # python %s filename' % argvs[0]
	quit()
 
f = open(argvs[1])
o = open("out.tex","w")

o.write(doc[begin])
status = "analyze"
struct(f,o,"",status,True)
o.write(doc[end])
f.close
o.close





