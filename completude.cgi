#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# Copyright (C) 2006, 2007 Kim Gerdes
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

import time, re, cgitb, cgi, sha, Cookie, os, sys
import session
from random import choice
from frenchLinguist import FrenchLinguist
from rogers import Rogers
from analyste import Elizia

cgitb.enable()

# Some hosts will need to have document_root appended
# to sys.path to be able to find user modules
#sys.path.append(os.environ['DOCUMENT_ROOT'])

machine = "elizia.net"
cefichier = "supervision.cgi"
stylesheet = "/eliziastyle.css" # avec chemin depuis machine


sess = session.Session(expires=365*24*60*60, cookie_path='/')





e = Elizia(sess)


print sess.cookie
print "Content-Type: text/html\n" # blank line : end of headers


print """<html>
	<head><title>Supervision Elizia - test de complétude </title>
	<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">"""
print """<style type="text/css">
	td { border:thin solid #ddd; }
	</style>"""
print	'<link href="http://' + machine +stylesheet+ '" rel="stylesheet" type="text/css"></head>'
print "<body OnLoad='document.entree.probleme.focus();'> <h1> Supervision d'<a href='http://elizia.net'>Elizia</a></h1>"



# get already saved special cases
specialKeys = sess.data.get('specialKeys')
specialAnswers = sess.data.get('specialAnswers')




form = cgi.FieldStorage()
probleme = ""



allkeys = []
allwords = []



if not form.has_key("probleme") :
	if os.environ.get("HTTP_REFERER", "<not present>").endswith(cefichier) :
		print "<p class = 'vous'>Vous :",probleme,"</p>"
		print "<p class = 'elizia'>Elizia :",e.analyse(probleme,sess),"</p>"
	else : 
		print "<p class = 'elizia'>Elizia : Mettez-vous à l'aise et parlez-moi ouvertement de vos problèmes !</p>"
else  :
	probleme = form["probleme"].value
	print "<p class = 'vous'>Vous :",probleme,"</p>"
	print "<p class = 'elizia'>Elizia :",e.analyse(probleme,sess),"</p>"
	

if not e.fini: print '<form method="post" action="'+cefichier+'" name="entree"><input  name="probleme" class="probleme" ></form>'

print "<p><br><br>"

l = FrenchLinguist()
for cas,keyw in e.rogers.keywords.iteritems(): 
	for key in keyw:
		if key in allkeys:
			print "double key '",key,"'",cas,"<br>"
	allkeys+=keyw
print "<p>ici</p>"
#print 1/0
for cas,answers in e.rogers.answers.iteritems(): 
	print "--- new case",cas,"<br>"
	for answer in answers:
		print "- new answer"#,answer,"<br>"
		print answer,"<br>"
		answer = l.nettoyerTexte(answer.lower())
		lemmas = l.getLemmas(answer)
		print lemmas,"<br>"
		#words=answer.split()
		for word in lemmas:
			
			ok = False
			if word.lower() in allkeys+["de","la","le","d","que","qu","ne","n","l","ai","as","a","il","elle","?","!"]:
				continue
			#print word
			#lemmas = l.getLemmas(word)
			#for lemma in lemmas:
			#if lemma in allkeys:
				#ok=True
			if not ok:
				allwords += [word]
			#print word,"**"
			#word = l.nettoyerTexte(word.lower())
			#word = word.encode("utf-8")
			#allwords+= word.lower().split(",")
			#for w in word:
				#print w.split("'")
				
	
print "<p>____________________________words from the answers that are not understood:</p>"

wlist = list(set(allwords)-set(allkeys))
wlist.sort()
for word in wlist:
	print word#.encode("utf-8")
print "<br><br>------------------"
print "keys <br>"
allkeys.sort()
for word in allkeys:
	print word


print "<br><br>"
