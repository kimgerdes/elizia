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
stylesheet = "eliziastyle.css" # avec chemin depuis machine


sess = session.Session(expires=365*24*60*60, cookie_path='/')
# expires can be reset at any moment:
#sess.set_expires('')
# or changed:
#sess.set_expires(30*24*60*60)
# Session data is a dictionary like object


def connaissance(total_seconds):

	if total_seconds <1 :
		return "On est en train de faire connaissance"
	else :
		seconds = total_seconds % 60
		total_minutes = total_seconds / 60
		minutes = total_minutes % 60
		total_hours = total_minutes / 60
		hours = total_hours % 24
		total_days = total_hours / 24
		days = total_days % 365
		years = total_days / 365
		text = "On se connait depuis plus de "
		per = [years, days, hours, minutes, seconds]
		pernom = ['année', 'mois', 'heure', 'minute', 'seconde']
		for i in range(len(per)):
			if per[i] :  
				text+= str(per[i]) + " "+pernom[i]
				if per[i]>1 : text+= "s"
				break
		return text
	





e = Elizia(sess)

#DBmessage = e.linguist.dataBaseStatus

print sess.cookie
print "Content-Type: text/html\n" # blank line : end of headers


print """<html>
	<head><title>Supervision Elizia </title>
	<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">"""
print	'<link href="' +stylesheet+ '" rel="stylesheet" type="text/css"></head>'
print """<style type="text/css">
	td { border:thin solid #ddd; }
	.title {
	width 100%;
	font-family:verdana,helvetica,arial,sans-serif;
	border-bottom:4px solid #aaa; padding-bottom:0px; margin:2px; 
	}
	.container {
	width 100%;
	padding:3px;
	}
	.tech {
	color:#666666;
	background:white;
	font-size:9px;
	font-family:verdana,helvetica,arial,sans-serif;
	padding:3px;
	}
	.info {font-size:10px;
	width:23%;
	margin:4px;
	float: left;
	color:#666666;
	border-style:solid;
	border-width:1px;
	border-color:#eee;
	text-align:left;
	font-family:verdana,helvetica,arial,sans-serif;
	}
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

print "<body OnLoad='document.qqq.problem.focus();'>"
print "<div class=title><h1> Supervision d'<a href='http://elizia.net'>Elizia</a></h1></div>"
print "<div class=container ><div class=info><p>Bienvenue sur la page de <a href='http://en.wikipedia.org/wiki/Clinical_supervision'>supervision</a> d'<a href='http://elizia.net'>Elizia</a>.</p><p> &nbsp; </p>"
print "<p> Ici, on peut changer les réponses d'<a href='http://elizia.net'>Elizia</a> :</p><p>Les déclencheurs des <b>cas spéciaux</b> sont codés en dur, donc non-modifiables ici. Par contre, on peut changer les réponses et d'autres paramètres. </p><p>Les <b>cas normaux</b> sont basés sur la reconnaissance des mots clés</p>"
print "<p><a href='http://elizia.net'>Elizia</a> choisit parmi les cas reconnus ayant la plus haute <b>qualité</b>. Si plusieurs cas possibles ont la même qualité, elle choisit par hasard.</p>"

print "</div><div class=info><p>Si on coche la case <i>ce cas sort les réponses dans l'ordre donné</i>, les réponses sont choisies dans un ordre fixe, comme par exemple pour le cas 'Salutation'. Sinon, les réponses sont données dans un ordre arbitraire, en essayant d'éviter des répétitions directe. </p>"
print "<p>Si on coche la case <i>ce cas arrête tout quand les réponses sont épuisées</i>, <a href='http://elizia.net'>Elizia</a> prend congé quand elle est arrivée à l'avant-dernière réponse, par exemple pour le cas 'Insulte'. Sinon, elle boucle.</p>"
print "<p>Quand on coche <i>ce cas arrête la discussion tout de suite</i>, <a href='http://elizia.net'>Elizia</a> prend congé dès qu'elle reconnaît ce cas.</p>"


print "<p>Dans la section <b>'cas normaux'</b> vous pouvez changer les mots clés déclencheurs ainsi que les réponses. Les mots clés contenant des espaces sont reconnus même s'ils ne sont pas entourés des espaces&nbsp;!</p>"
print "</div><div class=info>"
print "<p>Si 'Reprise' est le cas choisi, <a href='http://elizia.net'>Elizia</a> choisit un cas alternatif parmi les cas reconnus précédemment dans la thérapie pour lesquels la case <i>ce cas peut être repris</i> est cochée. Elle essaie donc de ramener la discussion à un sujet connu. Dans les réponses, 'xxx' est remplacé par le nom du cas alternatif. Le nom d'une section est donc important.</p>"
print "<p>Tout en bas, on peut créer un <b>nouveau cas</b> avec des mots clés et des réponses de votre choix. Il n'est pas possible d'effacer un cas, par contre, on peut donner à un cas une valeur inférieur à tous les autres (par exemple -1) et il ne sera jamais choisi (car le cas 'Retour' est toujours possible).</p>"
print "<p>N'oubliez pas de cliquer sur <b>'Mettre à jour'</b> quand vous avez changé quelque chose. Ne seront pris en compte que les changements du cas que vous avez mis au jour. Les changements sur d'autres cas seront perdus. </p>"
print "</div><div class=info><p>Dans le champ d'Eliza ci-dessous, vous pouvez <b>tester</b> si tout marche comme vous le souhaitez. Les changements ne s'appliquent que pour vous (vous avez un cookie grâce auquel <a href='http://elizia.net'>Elizia</a> vous reconnaît) mais ils sont enrégistrés et si vos idées sont bonnes, on s'en inspirera..."
print "</p><p>Il est possible d'utiliser une autre fenêtre d'Elizia 'habituelle' pour tester vos changements. </p><p>Si une phrase commence par ':::' <a href='http://elizia.net'>Elizia</a> indique les cas reconnus dans l'historique</p><p>'all:' au début de la phrase donne une liste en ordre alphabétique de tous les mots que <a href='http://elizia.net'>Elizia</a> teste contre les mots clés.</p></p><p>'lemmas:' donne juste une liste des lemmes par mot.</p><p>'words:' rend les mots.</div></div>"
print '<p style="clear: left;"><br><br></p>'




# get already saved personalized cases
personalizedKeys = sess.data.get('personalizedKeys')
personalizedAnswers = sess.data.get('personalizedAnswers')
personalizedQuality = sess.data.get('personalizedQuality')
personalizedLists = sess.data.get('personalizedLists')
if personalizedKeys : 
	for c in personalizedKeys.keys(): e.rogers.keywords[c]= personalizedKeys[c]
else :  personalizedKeys={}
if personalizedAnswers : 
	for c in personalizedAnswers.keys(): e.rogers.answers[c]= personalizedAnswers[c]
else :	personalizedAnswers={}
if personalizedQuality : 
	for c in personalizedQuality.keys(): e.rogers.quality[c]= personalizedQuality[c]
else :	personalizedQuality={}
if personalizedLists : e.rogers.noRecall,e.rogers.ordered,e.rogers.noCycle,e.rogers.stop = personalizedLists
##############




form = cgi.FieldStorage()
probleme = ""

if form.has_key("cas") : # a case was changed
	keys = None
	cas = form["cas"].value
	if form.has_key("problem") : probleme = form["problem"].value
	
	noRecall = not form.has_key("recall")
	ordered = form.has_key("ordered")
	noCycle = form.has_key("noCycle")
	stop = form.has_key("stop")
	
	if form.has_key("keys") : keys = [k.strip() for k in form["keys"].value.split("\n") if k.strip()]
	answers = [a.strip() for a in form["answers"].value.split("\n") if a.strip()]
	try : 	quality = int(form["quality"].value)
	except: quality = -1
	
	if keys : e.rogers.keywords[cas]= keys
	e.rogers.answers[cas]=answers
	e.rogers.quality[cas]=quality
	
	if noRecall and cas not in e.rogers.noRecall: e.rogers.noRecall+=[cas]
	elif not noRecall and cas in e.rogers.noRecall: e.rogers.noRecall.remove(cas)
	if ordered and cas not in e.rogers.ordered: e.rogers.ordered+=[cas]
	elif not ordered and cas in e.rogers.ordered: e.rogers.ordered.remove(cas)
	if noCycle and cas not in e.rogers.noCycle: e.rogers.noCycle+=[cas]
	elif not noCycle and cas in e.rogers.noCycle: e.rogers.noCycle.remove(cas)
	if stop and cas not in e.rogers.stop: e.rogers.stop+=[cas]
	elif not stop and cas in e.rogers.stop: e.rogers.stop.remove(cas)
	
	if keys :personalizedKeys[cas]= keys
	personalizedAnswers[cas]=answers
	personalizedQuality[cas]=quality
	personalizedLists=(e.rogers.noRecall,e.rogers.ordered,e.rogers.noCycle,e.rogers.stop)
	sess.data['personalizedLists'] = personalizedLists
	sess.data['personalizedQuality'] = personalizedQuality
	if personalizedKeys : sess.data['personalizedKeys'] = personalizedKeys
	if personalizedAnswers : sess.data['personalizedAnswers'] = personalizedAnswers

if form.has_key("problem")  : # a new problem was sent to analyze
	probleme = form["problem"].value
	print "<p class = 'vous'>Vous :",probleme,"</p>"
	print "<p class = 'elizia'>Elizia :",e.analyse(probleme),"</p>"

else : # no new problem => use old problem, or start session
	if os.environ.get("HTTP_REFERER", "<not present>").endswith(cefichier) : # old problem
		print "<p class = 'vous'>Vous :",probleme,"</p>"
		print "<p class = 'elizia'>Elizia :",e.analyse(probleme),"</p>"
	else : # start session
		print "<p class = 'elizia'>Elizia : Mettez-vous à l'aise et parlez-moi ouvertement de vos problèmes !</p>"


def checkbox(name,test,sentence):
	s= '<input type="checkbox" name="'+name+'" value="true" '
	if eval(test): s+= "checked"
	s+= '>'+sentence+'<br>'
	return s
def textarea(name,lis):
	s= '<textarea name="'+name+'" style="font-size: x-small; height:100%; width:100%;" rows="8">'
	for rep in lis:
		s+= rep+"\n"
	s+= '</textarea>'
	return s

def printForm(cas,cefichier,probleme,quality,keywords,answers):
	print '<form method="post" action="'+cefichier+'" name="xentree">'
	print '<input type="hidden" name="problem" value="'+probleme+'">'
	print "<table style='border:thin solid red; border-spacing:5px ;font-size: small; empty-cells:show; width:100%'>"
	if cas: 
		print "<tr><td><b>"+cas+"</b></td>"
		print '<input type="hidden" name="cas" value="'+cas+'">'
	else: print "<tr><td><b>Nom du nouveau cas :<input name='cas'></b>"
	print "<td></td><td>qualité <input name='quality' size = 1 value='"+str(quality)+"'></td></tr>"
	print '<tr><td style="width:30%;" >'
	if keywords:print textarea("keys",keywords)
	else:print "<span style='font-size: 8px;'>pas de mots clés, parce que ce cas est codé en dur</span>"
	print "</td><td style='width:50%;' class='elizia'>"
	print textarea("answers",answers)
	print '</td><td style=" font-size: x-small;">'
	print checkbox("recall","cas not in e.rogers.noRecall","ce cas peut être repris")
	print checkbox("ordered","cas in e.rogers.ordered","ce cas sort les réponses dans l'ordre donné (eg. Salutation)")
	print checkbox("noCycle","cas in e.rogers.noCycle","ce cas arrête tout quand les réponses sont épuisées (eg. Insultes)")
	print checkbox("stop","cas in e.rogers.stop","ce cas arrête la discussion tout de suite (eg. Fin)")
	print '<br><input type="submit" value=" Mettre à jour"; style="border:thin solid white; border-spacing:10px;width:100%">'
	print "</td></tr></table>"
	print "</form>"
	
	

if not e.fini: 
	print '<form method="post" action="'+cefichier+'" name="qqq">'
	print '<input  name="problem" class="problem"  value="'+probleme+'"></form>'

print "<p><br><br>"

print "<br><br><h2><u>Cas spéciaux :</u></h2>"

for cas in e.rogers.answers.keys(): # print personalized cases
	if cas in e.rogers.keywords.keys():
		continue
	printForm(cas,cefichier,probleme,e.rogers.quality[cas],None,e.rogers.answers[cas])

print "<br><br><h2><u>Cas normaux :</u></h2>"
for cas in sorted(e.rogers.keywords, key=str.lower): # print common cases (with keywords)
	printForm(cas,cefichier,probleme,e.rogers.quality[cas],e.rogers.keywords[cas],e.rogers.answers[cas])

print "<br><br><h2><u>Nouveau cas :</u></h2>"
printForm(None,cefichier,probleme,0,["les mots clés (effacer cette ligne)"],["au moins deux réponses (effacer cette ligne)"])

print "<br><br>"
print '<div class="tech">'
print "<hr>"
print "<p><b><u>trucs techniques :</u></b></p>"
memoire = sess.data.get('memoireinputsPatient')
if e.cas : print "<p><b>Cas : </b>",e.cas,"</p>"
print "<p><b>Conversation : </b></p>"	
try:
	if "memoireReponses" in sess.data.keys():
		for i in range(len(sess.data["memoireReponses"])):
			print  "<p>"+time.asctime(time.localtime(float(sess.data["memoireTemps"][i]))),
			print " : "+sess.data["memoireinputsPatient"][i]+" - ",
			print sess.data["memoireReponses"][i],
			print "("+sess.data["memoireCas"][i]+")</p>"
except:
	print "Oh, j'ai trop fumé. J'ai tout oublié !"

firstvisit = sess.data.get('firstvisit')
lastvisit = sess.data.get('lastvisit')
if firstvisit and lastvisit : 
	therapyduration = float(lastvisit)-float(firstvisit)
	message = '<p>Welcome back. Your last visit was on ' + 	time.asctime(time.localtime(float(lastvisit))) +"</p>"
	print "<p>Your first visit was on " + time.asctime(time.localtime(float(firstvisit))) +"</p>"
	print "<p>", connaissance(int(therapyduration)),"</p>"
else : 
	therapyduration = float(0)
	message = '<p>New session</p>'
	sess.data['firstvisit'] = repr(time.time())
	firstvisit = repr(time.time())
	lastvisit = repr(time.time())

# Save the current time in the session
sess.data['lastvisit'] = repr(time.time())
print message
#print DBmessage+"<br>"
print "<p>sess.cookie : "+str(sess.cookie)+"</p>"
print "<hr>"
for i in sess.data.keys():
	print  "<p><b>"+i+": </b>"+str(sess.data[i])+"</p>"

print "<p><b>Referer:</b>", os.environ.get("HTTP_REFERER", "<not present>")
print "<p><b>User Agent:</b>", os.environ.get("HTTP_USER_AGENT", "<unknown>")
ipnum = os.environ.get("REMOTE_ADDR", "<not present>")
sess.data['ipnum'] = ipnum
print "<p><b>IP:</b>", ipnum
print '</div>'
sess.close()
print "</body></html>"

