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

import time, re, cgitb, cgi,sha, Cookie, os,sys
cgitb.enable()
import session
from random import choice
from frenchLinguist import FrenchLinguist
from lookup import lookup
from rogers import Rogers


class Elizia:

	
    listeInterro=["pourquoi","quand","comment"]
    fini = False
    dicoDejaDitElizia = {}

    cas = None # contient le mot clé trouvé   
    
    
    
    def __init__(self,session):
	    
	    self.sess = session
	    self.memory = session.data.get('memory',None)
	    #if not self.memory: self.memory=[([],[],[],[])]
	    if self.memory:self.memoProblems,self.memoAnswers,self.memoCases,self.memoTimes = zip(*self.memory)
	    else:self.memoProblems,self.memoAnswers,self.memoCases,self.memoTimes=[],[],[],[]
	    #session.data.get('memoireinputsPatient',[])
	    #self.avantCas = session.data.get('memoireCas',[])
	    self.dicoDejaDitElizia = session.data.get('dejaDitelizia',{})
	    self.sex = session.data.get('sex',"unknown")
	    self.rogers = Rogers()
	    self.goodCases=[c for c in self.memoCases if c not in self.rogers.noRecall]
	    self.linguist = FrenchLinguist()
	    self.problem = "???" # devrait être écrasé par le vrai input

    
    def analyse(self,problem):
	""" ici se fait tout le boulot. """
	
	self.problemBase=problem.strip()
	
	#first letter of sentence lower key:
	if len(self.problemBase)>1 : self.problemBase = self.problemBase[0].lower()+self.problemBase[1:]
	self.special=self.problemBase.split(":")[0]
	#print "***",self.problemBase.split(":"),self.special
	if self.special in ["words","lemmas","all"]:self.problemBase=" ".join(self.problemBase.split(":")[1:])
	else:self.special=None
	#self.problem = self.problemBase
	self.problem = self.linguist.decontracte(self.problemBase)
	if self.special=="words":return "words: "+self.problem
	
	self.cas = [] # contains (quality,case) couples
	inputPropre = self.linguist.nettoyerTexte(self.problem)
	inputSplit = inputPropre.split()
	
	#print inputSplit
	
	if self.special=="lemmas":	return "lemmas: "+" / ".join(lookup(inputPropre))
	lemmas = lookup(inputPropre) # list of lemmas (that are different from the form)
	sex = self.linguist.guesssex(self.problem)
	if sex != "unknown":
		self.sess.data['sex'] = sex
	 	if self.sex != "unknown" and sex != self.sex:
			c="votre identité sexuelle"
			self.cas += [(self.rogers.quality[c],c)]
			#return self.repo()
		self.sex = sex
	#for lemma in lemmas:
		#print lemma,"-"
	allKeys = list(set(inputSplit + lemmas))
	allKeys.sort()
	if self.special=="all": return "all: "+" / ".join(allKeys)
	
	
	# special cases:
	if len(self.problem) > 0 and self.cleTrouvee(self.rogers.keywords['vos SMS'],self.problem,self.problem.split()):
		c="vos SMS"
		self.cas += [(self.rogers.quality.get(c,0),c)]
	#voir si le patient a dit qqch
	if len(inputSplit)==0:
	#if len(self.patientInput) > 0:
		c="Vide"
		self.cas += [(self.rogers.quality.get(c,0),c)]
		return self.repo()
	# voir si le patient a pê posé une question :
	# donc si ça commence avec un mot interrogatif ou termine sur un point d'interrogation
	if inputSplit[0] in self.listeInterro or self.problem[-1]=="?":
		c="Question"
		self.cas += [(self.rogers.quality.get(c,0),c)]
	elif self.problemBase in self.memoProblems :
		c="Répétition"
		self.cas += [(self.rogers.quality.get(c,0),c)]
		
	# regular cases:
	for nom in self.rogers.keywords.keys(): # pour chaque clé		
		if self.cleTrouvee(self.rogers.keywords[nom],inputPropre,allKeys):
			self.cas += [(self.rogers.quality[nom],nom)]
	#voir si le patient est très bref
	if len(inputSplit)==1:
		c="Bref"
		self.cas += [(self.rogers.quality.get(c,0),c)]				
	c="Retour"
	self.cas += [(self.rogers.quality.get(c,0),c)]

	return self.repo()

    def cleTrouvee(self,cles,texte,liste):
        """ 
	cherche une liste cles dans un self.texte (string) et dans la liste de mots correspondante
	deux cas : clé est un mot : il doit apparaître entouré de blancs 
	ou clé contient des espaces : peu importe, tant qu'il apparaît
	"""
	
        for c in cles :
		if " " in c and c in texte:
			return True
		elif c in liste :
			return True
        return False

  
   
    def repo(self):
	""" fonction importante qui rend la réponse et gêre les mémoires """
	
	ordered,reponse,cases,maxiq = False,"",[],0
	for q,c in self.cas:
		if q>maxiq:
			cases=[c]
			maxiq=q
		elif q==maxiq:cases+=[c]
	#print cases
	nomcas=choice(cases) # take one of the maxi cases by chance
	#print nomcas

	memoire =  self.dicoDejaDitElizia.get(nomcas,[])
	#if nomcas in self.dicoDejaDitElizia.keys() : memoire =  self.dicoDejaDitElizia[nomcas]
	#else : memoire = []	
	
	
	
	ordered = nomcas in self.rogers.ordered  #== "Insulte" ,...
	# if (ordered, no more answers and no cycle) or end case: end it all
	self.fini = (nomcas in self.rogers.ordered and len(memoire) >= len(self.rogers.answers[nomcas])-2 and nomcas in self.rogers.noCycle ) or nomcas == "Fin"
	
	#if case is worse than 1, we do have good cases, come back to old cases from time to time    (nomcas=="Retour" )
	if maxiq<1 and self.goodCases and 0 == choice([0,1]) :  
		nomcas = "Reprise"
		casRepris = self.goodCases[-1]
		#print self.goodCases,self.memoCases
		if 0 == choice([0,1,2]): # parfois (1/3) on ajoute une réponse de l'ancien cas
			if casRepris in self.dicoDejaDitElizia.keys() : memoReprise =  self.dicoDejaDitElizia[casRepris]
			else : memoReprise = []
			reponse = " \n "+self.choisirReponse(casRepris,memoReprise,False)
	
	reponse = self.choisirReponse(nomcas,memoire,ordered) + reponse
	
	if nomcas == "Reprise" : reponse = reponse.replace("xxx",casRepris)
	
	if nomcas == "Retour" and " xxx" in reponse:
		reponse = reponse.replace("xxx","")
		reponse = reponse + self.linguist.phraseEnchassee(self.problem,self.sex)
	# se souvenir de ce qu'on a dit
	try:
		self.sess.data['memory']  = (self.sess.data.get('memory') or [])+[( self.problemBase,reponse,nomcas,repr(time.time())  )]
	except:
		print "Putain, j'ai un problème de mémoire !"#.encode("utf-8")
		
	return self.linguist.beautifier(reponse,self.sex)

    def choisirReponse(self,casActuel,memoireActuel,ordered):
	# le [:] permet de faire une copie
        #       - pour qu'on ne touche pas à la liste originale
        listeReponseLocale=self.rogers.answers[casActuel][:]

        for rep in memoireActuel:
		if rep in listeReponseLocale: # normalement, ça devrait tjrs être dedans
			listeReponseLocale.remove(rep) # on enlève ce qu'on a déjà dit
        if ordered : 	reponse = listeReponseLocale[0]
	else : 		reponse = choice(listeReponseLocale) # choix par hasard parmi le reste
	
	memoireCas=memoireActuel+[reponse] # on retient la réponse (sans phrase du patient en cas Retour)
	
	# vider le mémoire sauf la dernière réponse au cas où on a déjà	utilisé toutes les réponses proposées
	
	if len(memoireCas) >= len(self.rogers.answers[casActuel]):
            while len(memoireCas)>1:
                memoireCas.pop(0)
		
	self.dicoDejaDitElizia[casActuel]=memoireCas
	
	
	
	self.sess.data['dejaDitelizia'] = self.dicoDejaDitElizia
	
	return reponse
	
	