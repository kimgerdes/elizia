#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# Copyright (C) 2006-2015 Kim Gerdes
# kim AT gerdes.fr
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
# See the GNU General Public License (www.gnu.org) for more details.
#
# You can retrieve a copy of the GNU General Public License
# from http://www.gnu.org/.  For a copy via US Mail, write to the
#     Free Software Foundation, Inc.
#     59 Temple Place - Suite 330,
#     Boston, MA  02111-1307
#     USA
####

from sqlite3  import connect
import cgitb, sys, codecs, time, re







def makeFormLemmaCode(infile="lefff.txt", outfile="formlemmacode.txt"):
	"""
	finds words with a lemma _different_ from the form (the token)
	puts them in search tree dictionary
	dumps the tab separated form-lemma table in the outfile
	"""
	ti = time.time()
	
	renotword=re.compile("\W|\+|\&|\<|\>|\@|\%|\$|\/|\=",re.U)

	count = 0
	ll=(None, None, None) # last entry
	
	with codecs.open(infile,"r","utf-8") as inf, codecs.open(outfile,"w","utf-8") as outf:
		for li in inf :
			# example:
			# mégisseront	100	v	[pred='mégisser_____1<Suj:cln|scompl|sinf|sn,Obj:(cla|sn)>',@pers,cat=v,@F3p]	mégisser_____1	Default	F3p	%actif
			
			els = li.lower().split("\t") # lower !!!!!!
			# els[0]=token, els[2]=cat, ...
			
			tok, _, cat, pred = els[:4]
			
			#filtering: cours qui a comme lemme : donner cours etc...
			if cat in ["cf","cfi","pri","prel"]:
				continue
			if pred.startswith("[pred='"):
				lemma=pred[7:].split("__")[0].replace("_"," ")
				code=pred.split("@")[-1][:-1]
			else: continue
			#if pred in ["pouvoir","devoir","falloir"]:
				#els[2]="auxMod"
			###
			if cat in ["poncts","ponctw","parentf","parento","ilimp","epsilon"] or cat.startswith("cl") or cat.endswith(";") or renotword.search(tok[0]) or (lemma==tok and (not "m" in code)) or (tok,lemma,code)==ll :
				continue # only keep lemmas that are different from the token or multiword expressions! or (not renotword.search(lemma))
			
			#if  tok[0]!="z":
				#continue
			
			outf.write(tok+"\t"+lemma+"\t"+code+"\n")
			
			ll=(tok,lemma,code)
			count += 1
			if not count%10000: print count,li
				
	print "____",time.time()-ti,"seconds for",count,"entries"
	
makeFormLemmaCode()

def writeFileIntoDB(lefffile = 'formlemmacode.txt', dbpath="formlemmacode.sqlite"):
	db = connect(dbpath)
	cursor = db.cursor()
	cursor.execute ("DROP TABLE IF EXISTS words")
        cursor.execute ("""
		CREATE TABLE words
		(
		form TEXT,
		lemma TEXT,
		code TEXT
		);""")
	cursor.execute ("""
		CREATE INDEX frm ON words(form);
		""")
        print "table created"
        print "inserting file..."
	
	counter=0
	with codecs.open(lefffile,"r","utf-8") as infile:
		for line in infile:
			line = line.strip()
			if line: 
				f,l,c = line.split("\t")
				cursor.execute("insert or ignore into words VALUES (?,?,?);",(f,l,c,))
				counter+=1
	db.commit()
	db.close()	
	print counter,"forms inserted into", dbpath

    
writeFileIntoDB()

def makeFormLemma(infile="lefff.txt", outfile="formlemma.txt"):
	"""
	finds words with a lemma _different_ from the form (the token)
	puts them in search tree dictionary
	dumps the tab separated form-lemma table in the outfile
	"""
	ti = time.time()
	
	renotword=re.compile("\W|\+|\&|\<|\>|\@|\%|\$|\/|\=",re.U)

	count = 0
	ll=[None, None] # last entry
	
	with codecs.open(infile,"r","utf-8") as inf, codecs.open(outfile,"w","utf-8") as outf:
		for li in inf :
			# example:
			# mégisseront	100	v	[pred='mégisser_____1<Suj:cln|scompl|sinf|sn,Obj:(cla|sn)>',@pers,cat=v,@F3p]	mégisser_____1	Default	F3p	%actif
			
			els = li.lower().split("\t") # lower !!!!!!
			# els[0]=token, els[2]=cat, ...
			
			tok, _, cat, pred = els[:4]
			
			#filtering: cours qui a comme lemme : donner cours etc...
			if cat in ["cf","cfi","pri","prel"]:
				continue
			if pred.startswith("[pred='"):
				lemma=pred[7:].split("__")[0].replace("_"," ")
			else: continue
			#if pred in ["pouvoir","devoir","falloir"]:
				#els[2]="auxMod"
			###
			if cat in ["poncts","ponctw","parentf","parento","ilimp","epsilon"] or cat.startswith("cl") or cat.endswith(";") or renotword.search(tok[0]) or lemma== tok or (tok,lemma)==ll :
				continue # only keep lemmas that are different from the token or multiword expressions! or (not renotword.search(lemma))
			
			#if  tok[0]!="z":
				#continue
			
			outf.write(tok+"\t"+lemma+"\n")
			
			ll=(tok,lemma)
			count += 1
			if not count%10000: print count,li
				
	print "____",time.time()-ti,"seconds for",count,"entries"
	
#makeFormLemma()

def buildlexicon(formlemmafile="formlemma.txt"):
	"""
	voir README dans le dossier lemmm
	
	Tu utilises buildlexicon
	1) pour fabriquer xa.fsa, xa.tbl
	2) pour exploiter ces fichiers


	1) Pour fabriquer: build
	buildlexicon -d <dossier-ou-se-trouve-les fichiers-xa> -p <nom-des-fichiers> build < fichier lexique

	2) Pour exploiter: consult
	buildlexicon -d <dossier-ou-se-trouve-les fichiers-xa> -p <nom-des-fichiers> consult < mots


	exemple
	$ cat > detruire
	forma mot1
	forma mot2
	formb mot3
	CtrlD

	$ ./buildlexicon -d . -p detruire build < detruire
	...
	$ ./buildlexicon -d . -p detruire consult
	forma
	formb
	CtrlD
	"""
	
		
	import subprocess

	args=["./buildlexicon -d . -p lemmdico build < "+formlemmafile]
	pipe = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE)
	pipe.stdout
	stdout, stderr = pipe.communicate()
	
	print stdout, stderr

#buildlexicon()	
