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

import time, re, cgitb, cgi,sha, Cookie, os,sys
cgitb.enable()
import session

#machine = "http://elizia.net"

def space(text):
    regsSourceString = "([^\w])"
    regSourceExp = re.compile(regsSourceString, re.UNICODE)
    regsCibleString = " "+ r"\1"+" "
    chaine = " "+regSourceExp.sub(regsCibleString,text).lower()+" "
    while "  " in chaine :
        chaine = chaine.replace("  "," ")
    return chaine

def linebreak(text):
	return text.replace("\n","<br>")

def mark(text,regex):
	stri = u'('+unicode(regex,"utf-8")+u')'
	exp = re.compile(stri, re.UNICODE+re.MULTILINE)
	
	#color: rgb(51, 102, 102)
	regsCibleString =  "<span class='vous'>" 
	if border : 
		if leftborder[-1]==";":regsCibleString+="&"
		regsCibleString+=leftborder
	#"&rsaquo;"
	regsCibleString += r"\1" 
	if border : 
		if rightborder[-1]==";":regsCibleString+="&"
		regsCibleString+=rightborder
	#"&lsaquo;"
	regsCibleString += "</span>"
	text = exp.sub(regsCibleString,text)   
	while "  " in text :
		text = text.replace("  "," ") 
	   
	return text

def chunkdevant(text,regex):
	stri = u'('+unicode(regex,"utf-8")+u')'
	exp = re.compile(stri, re.UNICODE)
	regsCibleString =  "<span class='vous'> |> </span>" + r"\1" 
	text = exp.sub(regsCibleString,text)   
	while "  " in text :
		text = text.replace("  "," ")    
	return text

#print sess.cookie
print "Content-Type: text/html\n" # blank line : end of headers


print """<html>
	<head><title>Exercices sur les expressions régulières et la segmentation </title>
	
	<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
"""
print """<style type="text/css">
	td { border:thin solid #ddd; }
	</style>
		<script type="text/javascript">

	  var _gaq = _gaq || [];
	  _gaq.push(['_setAccount', 'UA-19440362-1']);
	  _gaq.push(['_trackPageview']);

	  (function() {
	    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
	    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
	    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
	  })();

	</script>
	"""
print	'<link href="../eliziastyle.css" rel="stylesheet" type="text/css"></head>'
print '<script type="text/javascript" language="JavaScript" src="script.js"></script>'
print "<body OnLoad='document.entree.exp.focus();'> <h1> Exercices sur les expressions régulières et la segmentation </h1>"



print """
<span style="font-style: italic; width:100%">
Certaines personnes, lorsqu&rsquo;elles sont confront&eacute;es &agrave; un probl&egrave;me, se disent &ldquo;Je sais, je vais utiliser les expressions r&eacute;guli&egrave;res.&rdquo; Et l&agrave;, elles ont maintenant deux probl&egrave;mes.
</span><p style='font-size: small;'>
Jamie Zawinski, dans comp.lang.emacs cit&eacute; d'apr&egrave;s
<a target="_blank" href="http://diveintopython.adrahon.org/">
diveintopython (Plongez au coeur de Python)
</p></a><br>

<a
 style="font-style: italic;" href="explications.html" target="_blank"><h3 style="font-family: Helvetica,Arial,sans-serif; color: rgb(152, 122, 168);">
 Cliquez ici pour voir des explications pour comprendre cette page.</h3></a><br>
"""

form = cgi.FieldStorage()

texte = ""
exp = ""
preps = ""
dets = ""
segsdevant = ""
leftborder = ""
rightborder = ""

if form.has_key("texte") : texte = form["texte"].value.strip()
if form.has_key("exp") : exp = form["exp"].value.strip()
if form.has_key("preps") : preps = form["preps"].value.strip()
if form.has_key("dets") : dets = form["dets"].value.strip()
if form.has_key("segsdevant") : segsdevant = form["segsdevant"].value.strip()
border = form.has_key("border")
if form.has_key("leftborder") : leftborder = form["leftborder"].value.strip()
if form.has_key("rightborder") : rightborder = form["rightborder"].value.strip()


if texte.strip() == "" : texte = """A l’image de ses manières affectées, tout en lui était artificiel ; toutefois, ses yeux enfiévrés semblaient avides de compassion.\nA la fin de la série de valses, il la conduisit vers une table isolée sans le lui avoir proposé. Ce n’était pas nécessaire : d’avance, elle connaissait la suite et se réjouit qu’il commande du champagne. La lumière tamisée du salon rendait l’endroit agréable, et chaque table avait son propre espace d’intimité. """
texte=texte.replace("\r","")
unitexte = unicode(texte,"utf-8")
spacetexte = space(unitexte).encode("utf-8")
unispacetexte = unicode(spacetexte,"utf-8")

if exp == "" : exp = "[abc]"
if preps == "" : preps = "( de|par )"
if dets == "" : dets = "la"
if segsdevant == "" : segsdevant = "pour? l?"
if leftborder == "" : leftborder = "rsaquo;"
if rightborder == "" : rightborder = "lsaquo;"


print '<form method="post" action="index.cgi" name="entree">'
print '<textarea name="texte" title="Mettez ici le texte que vous voulez analyser"  cols="30" rows="8" style="  width:100%;">'+texte+ '</textarea>'
print """
<div style="border: thin solid light grey; color: red; text-align:justify; width: 100%;"  >
<input value="Ziva !" style="font-size:x-large; border: thin solid white; cursor:pointer;color: red; width: 100%;" type="submit">
</div>
"""




print """
<table  width="100%">

<tr  class="row" onClick="ouvre(1,125)" onMouseOver="dessus(1)" onMouseOut="parti(1)">
	<td width="33%"></td><td class="row" id=name1 width="34%" style="border-right-color: #FFFFFF;border-left-color: #FFFFFF;">
	[Options]
	</td><td width="33%"></td>
</tr>

<tr style="display:none" id="idRow1" >
	   <td  colspan="3" >
	   <input name="border" value="border" style="width: 20pt;"
 """
if border : print ' checked="checked" '
print 'onclick="document.entree.submit();" type="checkbox">Montrer les frontières des correspondances <br>'
print ' Frontière gauche : <input name="leftborder"  value = "'+leftborder+'" >'
print "<br>"
print  ' Frontière droite : <input name="rightborder"  value = "'+rightborder+'" >'
print "<span style='font-size:xx-small;'>(Les caractère spéciaux HTML s'écrivent sans '&' avec un ';' à la fin)</span></td></tr>"

print "</table>"


print "<u>Le text espacé en minuscule - qui servira pour les analyses suivantes :</u><br> <p class = 'texte'>"
print linebreak(spacetexte)
print "</p>"


print "<br><u>Expression régulière :</u><br>"
print '<input name="exp" title="votre expression régulière"   style="width:100%; color:red; border:thin solid red; border-spacing:10px ;  width:100%" value = "'+exp+'" >'
print "Résultat pour cette expression régulière :<br> <p class = 'texte'>"
print linebreak(mark(unispacetexte,exp)).encode("utf-8")
print "</p>"


print "<br><u>Expression régulière pour trouver les prépositions :</u><br>"
print '<input name="preps" style="width:100%; color:red; border:thin solid red; border-spacing:10px ;  width:100%" value = "'+preps+'" >'
print "Résultat pour les prépositions :<br> <p class = 'texte'>"

print linebreak(mark(unispacetexte,preps)).encode("utf-8")
print "</p>"

print "<br><u>Expression régulière pour trouver les déterminants potentiels :</u><br>"
print '<input name="dets" style="width:100%; color:red; border:thin solid red; border-spacing:10px ;  width:100%" value = "'+dets+'" >'
print "Résultat pour les déterminants potentiels :<br> <p class = 'texte'>"
print linebreak(mark(unispacetexte,dets)).encode("utf-8")
print "</p>"

print "<br><u>Expression régulière pour trouver les frontières de segments potentielles :</u><br>"
print '<input name="segsdevant" style="width:100%; color:red; border:thin solid red; border-spacing:10px ;  width:100%" value = "'+segsdevant+'" >'
print "Résultat pour les segments potentiels :<br> <p class = 'texte'>"
print linebreak(chunkdevant(unispacetexte,segsdevant)).encode("utf-8")
print "</p>"

print """<p style="color:white;">(( dans| de| pour| après| par) (la|le|l|les|ce|un|son)?\\b)|(( dans| de| pour| après| par)? (la|le|l|les|ce|un|son)\\b)</p>"""

print "</body></html>"


	
