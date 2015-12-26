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


import time, re, cgitb, cgi,sha, Cookie, os,sys,shelve
cgitb.enable()
import session



if os.environ.has_key('HTTP_HOST') : machine = os.environ['HTTP_HOST']
else : machine = "elizia.net" # pour style sheet and links
if os.environ.has_key('REQUEST_URI') : cefichier = os.environ['REQUEST_URI']
else : cefichier = "histoire.cgi"
stylesheet = "/eliziastyle.css" # avec chemin depuis machine


def Walk( root, recurse=0, pattern='*', return_folders=0 ):
	import fnmatch, string
	
	# initialize
	result = []

	# must have at least root folder
	try:
		names = os.listdir(root)
	except os.error:
		return result

	# expand pattern
	pattern = pattern or '*'
	pat_list = string.splitfields( pattern , ';' )
	
	# check each file
	for name in names:
		fullname = os.path.normpath(os.path.join(root, name))

		# grab if it matches our pattern and entry type
		for pat in pat_list:
			if fnmatch.fnmatch(name, pat):
				if os.path.isfile(fullname) or (return_folders and os.path.isdir(fullname)):
					result.append(fullname)
				continue
				
		# recursively scan other folders, appending results
		if recurse:
			if os.path.isdir(fullname) and not os.path.islink(fullname):
				result = result + Walk( fullname, recurse, pattern, return_folders )
			
	return result
			
			
def outputForRogers(cas,keywords,answers):
	res = "keywords['"+cas+"'] = ["
	for key in keywords:
		res += '"' +key+ '", '
	res = res[:-2]+"]<br>"
	res += "answers['"+cas+"'] = ["
	for ans in answers:
		res += '"' +ans+ '", '
	res = res[:-2]+"]"
	return res

print "Content-Type: text/html\n" # blank line : end of headers

print """<html>
	<head>
	<title> Histoire d'Elizia </title><META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
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
print	'<link href="http://' + machine + stylesheet+'" rel="stylesheet" type="text/css"></head>'

print "<body > <h1> L'histoire d'elizia </h1>"

emptyerase=False
form = cgi.FieldStorage()
if form.has_key("erase") : # case: erasing a session
	filename = form["erase"].value
	if filename=="allempty":
		print "erasing empty files"
		emptyerase=True
	elif os.path.isfile(filename):
		os.remove(filename)
		print filename+" erased."
	else : print "problem erasing "+filename

#files = Walk(os.environ['DOCUMENT_ROOT'] + '/session', 0, 'sess*', 1)
files = Walk( 'session', 0, 'sess*', 1)
toErase = []
print '<h3>Nous avons %s sessions de thérapie enregistrées:</h3>' % len(files)
date2text = {}
goodSessionNumber=0
listOfEmptySessions = []
for file in files:
		sid = file[-40:]
	#try:
		#data = shelve.open(os.environ['DOCUMENT_ROOT'] + '/session'+'/sess_' + sid, writeback=False)
		try:
			data = shelve.open( 'session/sess_' + sid, writeback=False)
		except:
			print "can't open",'session/sess_' + sid
		personalizedAnswers = data.get('personalizedAnswers')
		#print "***",personalizedAnswers,data
		text = ""
		datenumber=None
		if "memoireReponses" in data.keys():
			goodSessionNumber+=1
			text+= "<hr><br>"
			datenumber = 0
			#if not personalizedKeys :continue	
			if data.get('firstvisit') :
				datenumber = time.localtime(float(data["firstvisit"]))
				text+= "Session "+str(goodSessionNumber)+" commencée le "+time.asctime(datenumber)
			if "ipnum" in data.keys() :
				text+= " --- numéro IP : "+data["ipnum"]
			if "referer" in data.keys() :
				text+= " --- referer : "+data["referer"]
			text+= " --- sid: " +sid + "<br>"
		elif "memory" in data.keys():
			
			goodSessionNumber+=1
			text+= "<hr><br>"
			datenumber = 0
			#if not personalizedKeys :continue	
			if data.get('firstvisit') :
				datenumber = time.localtime(float(data["firstvisit"]))
				text+= "Session "+str(goodSessionNumber)+" commencée le "+time.asctime(datenumber)
			if "ipnum" in data.keys() :
				text+= " --- numéro IP : "+data["ipnum"]
			if "referer" in data.keys() :
				text+= " --- referer : "+data["referer"]
			text+= " --- sid: " +sid + "<br>"
			
			
		else : 
			if data.has_key("firstvisit"):	listOfEmptySessions.append( time.asctime(time.localtime(float(data["firstvisit"]))) )
			toErase+=[file]
		shit=False
		personalizedKeys = data.get('personalizedKeys')
		personalizedQuality = data.get('personalizedQuality')
		if personalizedAnswers :
			
			for c in personalizedAnswers.keys():
				text+=  """<tr>
				<table style='border:thin solid red; border-spacing:5px ;font-size: small; empty-cells:show; width:100%'>"""
				text+= "<tr><td>: : : "+c+"</td><td>"
				try: text+=str(personalizedQuality[c])
				except: pass
				
				personalizedLists = data.get('personalizedLists')
				
				if personalizedLists : noRecall,ordered,noCycle,stop = personalizedLists
				else:noRecall,ordered,noCycle,stop=[],[],[],[]
				if c in noRecall: text+= " noRecall "
				if c in ordered: text+= " ordered "
				if c in noCycle: text+= " noCycle "
				if c in stop: text+= " stop "
				text+="</td></tr>"
		
				text+= '<tr><td>'
				if personalizedKeys and c in personalizedKeys.keys():
					text+= '<textarea name="keys" cols="30" rows="8" style=" font-size: x-small; height:100%; width:100%;">'
					for key in personalizedKeys[c]:
						text+= key+"\n"
						if "href=" in key or "href =" in key: shit=True
					text+= '</textarea>'
				else : text+= "cléfs personnalisées"
				text+= "</td><td class='elizia'>"
				text+= '<textarea name="answers" cols="80" rows="8" >'
				for rep in personalizedAnswers[c]:
					text+= rep+"\n"
				text+= '</textarea></td></tr>'
				text+= '<tr><td colspan="2" >'
				if  personalizedKeys and c in personalizedKeys.keys():
					text+= "<p style='font-size: xx-small; color:grey;'>"+outputForRogers(c,personalizedKeys[c],personalizedAnswers[c])+"</p>"
				text+= '</td></tr>'
				
				text+= '</table></tr>'
		allinput=""
		try:
			if "memoireReponses" in data.keys():
				text+=  "<table style='border:thin solid red; border-spacing:10px ; empty-cells:show; width:100%'>"
				#try:
				for i in range(len(data["memoireReponses"])):
					text+= "<tr>"
					text+= "<td class='tech' style='width:115px'>"+time.asctime(time.localtime(float(data["memoireTemps"][i])))
					text+= " : </td><td><span class='vous' >"+data["memoireinputsPatient"][i]+"</span> </td><td> <span class='elizia'>"
					text+= data["memoireReponses"][i]
					text+= "<td class='tech' style='width:77px'>"+data["memoireCas"][i]+"</td></tr>"
					allinput+=data["memoireinputsPatient"][i]
				text+= "</table>"
				
			elif "memory" in data.keys():
				text+=  "<table style='border:thin solid red; border-spacing:10px ; empty-cells:show; width:100%'>"
				#try:
				for i,o,c,t in data["memory"]:
					text+= "<tr>"
					text+= "<td class='tech' style='width:115px'>"+time.asctime(time.localtime(float(t)))
					text+= " : </td><td><span class='vous' >"+i+"</span> </td><td> <span class='elizia'>"
					text+= o
					text+= "<td class='tech' style='width:77px'>"+c+"</td></tr>"
					allinput+=i
				text+= "</table>"
		except:
			print "Oh, j'ai trop fumé. J'ai tout oublié !"
			#text+= "------ erreur"
		
		
		if shit or not allinput.strip():
			if data.has_key("firstvisit"):	listOfEmptySessions.append( time.asctime(time.localtime(float(data["firstvisit"]))) )
			toErase+=[file]
		
		text+= '<form method="post" action="'+cefichier+'" name="erase" style="border: thin solid white;">'
		text+= '<input type="hidden" name="erase" value="'+file+'">'
		text+= """<input value="Erase !" style="float: right;  border: thin solid white; cursor:pointer;" type="submit">
		</form>"""
		if datenumber: date2text[datenumber] = text
	#except:
		
		#print "problem reading",file,"!\n<br>"
		
		
		
	
dates = 	date2text.keys()
dates.sort()
dates.reverse()
#print dates
for date in dates:
	print date2text[date]

if listOfEmptySessions!=[] : print "<h4>"+str(len(listOfEmptySessions))+" sessions vides :</h4>"
for date in listOfEmptySessions:
	print date+" --- "

if listOfEmptySessions!=[] : 
	print """
	<form method="post" action='"""+cefichier+"""' name="erase" style="border: thin solid white;">
	<input type="hidden" name="erase" value="allempty">
	<input value="Erase all empty files!" style="float: right;  border: thin solid white; cursor:pointer;" type="submit">
	</form>"""

print "<br><br><br><P></p>"
print '<div class="tech">'
print "<p><b><u>trucs techniques :</u></b></p>"

if emptyerase:
	for f in toErase:
		try:
			os.remove(f)
			print f," was erased.<br>"
		except:
			print "failed to erase",f

#print "<p><b>Referer:</b>", os.environ.get("HTTP_REFERER", "<not present>")
print "<p><b>User Agent:</b>", os.environ.get("HTTP_USER_AGENT", "<unknown>")
ipnum = os.environ.get("REMOTE_ADDR", "<not present>")
print "<p><b>IP:</b>", ipnum
referer = os.environ.get("HTTP_REFERER", "no referer")
print "<p><b>referer:</b>", referer
print '</div>'
print "</body></html>"