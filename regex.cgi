#!/usr/bin/python
# -*- coding: UTF-8 -*-

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

machine = "http://elizia.net"

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
	exp = re.compile(stri, re.UNICODE)
	
	#color: rgb(51, 102, 102)
	regsCibleString =  "<span class='vous'>" 
	if border : regsCibleString+="|>"
	regsCibleString += r"\1" 
	if border : regsCibleString+="<|"
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

#######################################""

print "Content-Type: text/html\n" # blank line : end of headers


print """<html>
	<head><title>Exercices sur les expressions régulières et la segmentation </title>
	
	<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
"""
print """<style type="text/css">
	td { border:thin solid #ddd; }
	</style>"""
print	'<link href="' + machine + '/eliziastyle.css" rel="stylesheet" type="text/css"></head>'
print "<body OnLoad='document.entree.exp.focus();'> <h1> Exercices sur les expressions régulières et la segmentation </h1>"

print """
<span style="font-style: italic; width:100%">
Certaines personnes, lorsqu&rsquo;elles sont confront&eacute;es &agrave; un probl&egrave;me, se disent &ldquo;Je sais, je vais utiliser les expressions r&eacute;guli&egrave;res.&rdquo; Et l&agrave;, elles ont maintenant deux probl&egrave;mes.
</span>
<p style='font-size: small;'>
Jamie Zawinski, dans comp.lang.emacs cit&eacute; d'apr&egrave;s
<a target="_blank" href="http://diveintopython.adrahon.org/">
diveintopython (Plongez au coeur de Python)
</p></a><br>
"""

form = cgi.FieldStorage()

texte = ""
exp = ""
preps = ""
dets = ""
segsdevant = ""

if form.has_key("texte") : texte = form["texte"].value.strip()

if form.has_key("exp") : exp = form["exp"].value.strip()
if form.has_key("preps") : preps = form["preps"].value.strip()
if form.has_key("dets") : dets = form["dets"].value.strip()
if form.has_key("segsdevant") : segsdevant = form["segsdevant"].value.strip()

border = form.has_key("border")


if texte == "" : texte = """L'euthanasie bouscule les candidats\nBLOG\nLa plume et le bistouri • \n«On veut savoir si on va changer la loi?», demande Marie Humbert, qui avait plaidé pour l'euthanasie de son fils, tétraplégique après un accident de voiture. L’occasion pour les candidats de prendre position dans ce débat relancé par un manifeste signé par 2000 médecins et infirmières. """
unitexte = unicode(texte,"utf-8")
spacetexte = space(unitexte).encode("utf-8")
unispacetexte = unicode(spacetexte,"utf-8")
#<span style="border: thin solid white; color: red;  "></span>
if exp == "" : exp = "[abc]"
if preps == "" : preps = "( de|par )"
if dets == "" : dets = "la"
if segsdevant == "" : segsdevant = "pour? l?"

print '<form method="post" action="regex.cgi" name="entree">'
print '<textarea name="texte" cols="30" rows="8" style="  width:100%;">'
print texte
print '</textarea>'
print """<div style="border: thin solid light grey; color: red; text-align:justify; width: 100%;">
<input value="Ziva !" style="border: thin solid white; cursor:pointer;color: red; width: 85%;" type="submit">

<input name="border" value="border" style="width: 20pt;"
 """
if border : print ' checked="checked" '
print ' type="checkbox">Frontière</div>'

print "<u>Le text espacé en minuscule - qui servira pour les analyses suivantes :</u><br> <p class = 'texte'>"
print linebreak(spacetexte)
print "</p>"

print "<br><u>Expression régulière :</u><br>"
print '<input name="exp" style="width:100%; color:red; border:thin solid red; border-spacing:10px ;  width:100%" value = "'+exp+'" >'
print "Résultat pour cette expression régulière :<br> <p class = 'texte'>"
print linebreak(mark(unispacetexte,exp)).encode("utf-8")
print "</p>"

print """Regardez aussi <a target="_blank" href="http://elizia.net/regex1.html">cet exercice</a><br>"""

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


	
