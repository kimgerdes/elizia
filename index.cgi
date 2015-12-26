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

import time, cgitb, cgi, Cookie, os
import session
from analyste import Elizia

# web debug output:
cgitb.enable()


def connaissance(total_seconds):
	"""
	traduit un nombre de secondes en phrase de durée
	"""
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
				if per[i]>1 and i!=1: text+= "s" # pluriel de "mois" est "mois"
				break
		return text+". Ça va déjà mieux ?"


def readPersonalizedAnswers(sess,elizia):
	# get already saved personalized cases
	personalizedKeys = 	sess.data.get('personalizedKeys')
	personalizedAnswers = 	sess.data.get('personalizedAnswers')
	personalizedQuality = 	sess.data.get('personalizedQuality')
	personalizedLists = 	sess.data.get('personalizedLists')
	if personalizedKeys : 
		for c in personalizedKeys.keys(): elizia.rogers.keywords[c]= personalizedKeys[c]
	else :  personalizedKeys={}
	if personalizedAnswers : 
		for c in personalizedAnswers.keys(): elizia.rogers.answers[c]= personalizedAnswers[c]
	else :	personalizedAnswers={}
	if personalizedQuality : 
		for c in personalizedQuality.keys(): elizia.rogers.quality[c]= personalizedQuality[c]
	else :	personalizedQuality={}
	if personalizedLists : elizia.rogers.noRecall,elizia.rogers.ordered,elizia.rogers.noCycle,elizia.rogers.stop = personalizedLists
	##############

def computeAnswer(problem):
	"""
	returns html output for a given problem
	"""
	master=False
	if problem.startswith(":::hypnosis"): # erases memory
		problem=problem[11:]
		sess.data["memory"]=None
		sess.data["dejaDitelizia"]=None
		sess.data["sex"]="unknown"
		
		
		master=True
	if problem.startswith("lemmas:"): # gives complete information
		master=True
	if problem.startswith(":::") : 
		problem=problem[3:]
		master=True
	readPersonalizedAnswers(sess,e)
	answer = e.analyse(problem)
	if e.special: master=True
	
	html= """
	<p class = 'vous'>Vous : {problem}</p>
	<p class = 'elizia' id = 'eli'>Elizia : </p>
	<script type="text/javascript">
		<!--
		answer = '{answer}';
		//-->
	</script>""".format(problem=problem, answer=answer.replace("'","\\'"))
	
	return html, master


if os.environ.has_key('REQUEST_URI') : cefichier = os.environ['REQUEST_URI']
else : cefichier = "index.cgi"
referer=os.environ.get("HTTP_REFERER", "no referer")
ipnum = os.environ.get("REMOTE_ADDR", "<not present>")

sess = session.Session(expires=365*24*60*60, cookie_path='/')
# expires can be reset at any moment: sess.set_expires('') or changed: sess.set_expires(30*24*60*60) Session data is a dictionary like object
firstvisit = sess.data.get('firstvisit',0)
lastvisit = sess.data.get('lastvisit',0)


print sess.cookie

print """Content-Type: text/html\n
	<html>
	<head><title> ElizIA </title>
	<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
	<LINK REL="SHORTCUT ICON" href="images/favicon.ico">
	<script type="text/javascript">
	<!--
	function bouge() 
	{
		document.getElementsByName("tetebox")[0].style.background = "url('images/elizia"+(Math.floor(Math.random()*3)+1).toString()+".gif')";
		setTimeout("bouge()",Math.floor(Math.random()*5000)+1000);
	}
	function loadPictures()
	{	elizia1= new Image(200,181); elizia1.src='images/elizia1.gif'; 
		elizia2= new Image(200,181); elizia2.src='images/elizia2.gif'; 
		elizia3= new Image(200,181); elizia3.src='images/elizia3.gif';
	}
	var error=false;	
	
	function writeLetter(ii)	
	{
		if (answer.length == 0) return;
		var ch = answer.charAt(ii);
		eli = document.getElementById("eli");
		if (error) eli.innerHTML=eli.innerHTML.substr(0,eli.innerHTML.length-1)+ch;
		else eli.innerHTML=eli.innerHTML+ch;
		error = false;
		if (ii<answer.length)	{
			var fo = "writeLetter("+(ii+1)+")";
			var du = Math.floor(Math.random()*100)+10;
			if (Math.random()<0.05){
				eli.innerHTML=eli.innerHTML+answer.charAt(Math.random()*answer.length);
				error = true;
				du = du+280;
				}
			if (ch == " ") du = du+30;
			setTimeout(fo,du);
			}
	};
	answer="";
	
	// google analytics stuff:
		(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
		(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
		m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
		})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

		ga('create', 'UA-19440362-1', 'auto');
		ga('send', 'pageview');

	//-->
	</script>
	<script src="jquery-1.11.1.min.js"></script>
	<link href="eliziastyle.css" rel="stylesheet" type="text/css">
	</head>
	
	<body OnLoad='writeLetter(0);document.entree.problem.focus();loadPictures();'> 
	"""


form = cgi.FieldStorage()
problem = ""


e = Elizia(sess)

if form.has_key("problem") : # a problem sentence was sent
	vouselizia, master=computeAnswer(form["problem"].value)
else:
	master=False # not more information
	if referer.endswith(cefichier) : 
		# an empty problem sentence was sent or some other strange thing 
		vouselizia = "<p class = 'vous'>Vous :{problem}</p><p class = 'elizia'>Elizia :{answer}</p>".format(problem=problem, answer=e.analyse(problem))
	else :  # first arrival or reloading the page with the address line
		vouselizia = "<p class = 'elizia'>Elizia : Mettez-vous à l'aise et parlez-moi ouvertement de vos problèmes !</p><p>&nbsp;</p>"

print """
	<div id="analyzebox">
		<h2> Relaxez-vous &#150; vous êtes chez Elizia </h2>
		{vouselizia}
		{form}
		<div id="tetebox" name="tetebox">
		</div>
		<script type="text/javascript">
			setTimeout("bouge()",1000);
		</script>
	</div>
	<br>
	""".format(vouselizia=vouselizia,form='' if e.fini else '<form method="post" action="'+cefichier+'" name="entree" style="height:30px;"><input type="text" name="problem" class="problem" id="prob"></form>') # only give input box if elizia isn't mad

	
history=""
memory=sess.data.get("memory",None)
if memory:
	if master: 	mem=memory 
	else:		mem=memory[:-1]
	if mem:
		history = "<span style='font-size:14'>L'historique de votre thérapie:</span>"
		for (inp, outp, case, tim) in mem:
			history +=  "<p><span class = 'temps'>{time} : &nbsp;&nbsp;&nbsp;&nbsp;</span><span class = 'vous'>{inp} </span>–<span class = 'elizia'>{outp} </span>{case}</p>".format(time=time.asctime(time.localtime(float(tim))), inp=inp, outp=outp, case="("+case+")" if master else "")
if master and e.sex: history+= "<p>sex: "+e.sex+"</p>"
if firstvisit and lastvisit: 	history +=  "<p>"+connaissance(int(float(lastvisit)-float(firstvisit)))+"</p>"
else :				sess.data['firstvisit'] = repr(time.time())


#print "<br><br><br><br><br><br><br><br><br><br>",sess.data

print """
		<div class='history'>
		{history}
		</div>
		<br><br>
		<div id="bottombox"><a  href="cerveau/">Le cerveau d'Elizia</a>
			&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;<a href="supervision.cgi">La supervision</a> 
			&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;<a href="regex/">Un exercice sur les expressions régulières</a> 		
		</div>
		<div id="cervobox"></div>
	</body>
	</html>
	""".format(history=history)
	
	

sess.data['lastvisit'] = repr(time.time())
sess.data['ipnum'] = ipnum
if not (referer.endswith(cefichier) or referer=="no referer"): sess.data['referer'] = referer

sess.close()