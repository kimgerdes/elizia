# -*- coding: UTF-8 -*-

import re, codecs


def lefff2lemmma(lefff,lefffamlgm=None, lemmafile="lemmm.txt"):
	catinfo=re.compile(ur"__\w+", re.M+re.U)
	form2lem={}
	count=0
	with codecs.open(lefff, 'r','iso-8859-15') as f, codecs.open(lemmafile, 'w','utf-8') as out:
		ll=""
		for li in f:
			li=li.strip()
			if not li or li[0]=="#": continue
			count += 1
			if not count%100000:	print count, li
			els = li.split("\t")
			
			#filtering:"nc",
			if els[2] in ["np","cf","cfi"]: continue
		
			lem=els[4].split(u"_")[0]
			
			# corrections
			if lem in ["cln", "clr", "cll", "ilimp"]: lem=els[0]
			if lem in ["j'", "t'", "l'", "s'", "c'", "d'", "m'", "n'"]: lem=lem[0]+"e"
			
			nl = els[0]+"\t"+lem+"\n"
			
			# repetition:
			if nl==ll: continue
		
			out.write(nl)
			form2lem[els[0]]=lem
			ll=nl
			#break
		with codecs.open(lefffamlgm, 'r','iso-8859-15') as g:
			for li in g:
				li=li.strip()
				if not li or li[0]=="#": continue
				els = li.split("\t")
				val=catinfo.sub("",els[1])
				val=val.replace("_"," ")
				val=" ".join([form2lem.get(w,w) for w in val.split()])
				out.write(els[0]+"\t"+val+"\n")

			
lefff2lemmma("lefff-ext-3.2.txt","lefff-ext-3.2.amlgm.txt")