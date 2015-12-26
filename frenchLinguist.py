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
#### @TODO : reinsert guess sex after having doing a better lexicon including features

import string
import lefffDB
from lookup import lookup
import re,urllib
#telnetlib

#lemmaHost = "lionel-clement.dyndns.org"
#lemmaPort = 54322

class FrenchLinguist:

	lefff = lefffDB.Lefff()
	motsPasApresQue = ["mais","enfin","bon"]
	personalAdjTriggers =["suis","étais","ai été","ai pas été","serais","fus",
				"suis devenu","suis pas devenu","deviens",
					"me a","me as rendu","me as pas rendu","me as","me avez","me ont",
					"me sens","me sentais","me sentirai","suis senti",
					"me trouve","me trouvent","me trouvez", "me ont trouvé", "me avez trouvé"]
	motsFemme = ["une","folle","belle","vieille","conne","blanche","bonne"] #,"une femme","une fille"
	motsPasFemme=["une personne","une bonne personne"]
	lightAdv = ["pas","jamais","peu","ni","très","tout à fait","vraiment","toujours","souvent","également"]

	listeClitiques=["je","j","me","m","tu","il","ils","elles","le","l",
				"la","ne","n",
				"te","t","en","y","lui","se","s","vous","nous","leur"]
	dicClitPersSource = {1:["je","j","nous"],2:["tu","vous"]}
	##    dicClitPersCible = {1:"je",2:"vous"}
	listeElis = ["je","te","me","se","le","la","ne","que","ce","de"]
	
	remplacements12 = [("je vous","vous me"),("je ne vous","vous ne me"),
				("vous vous","je me"),("vous ne vous","je ne me"),("nous nous","vous vous"),
				("nous vous","vous me"),("nous ne vous","vous ne me"),
				("je me","vous vous"),("je ne me","vous ne vous"),
				("nous","vous"),
				("je","vous"),("me","vous"),("mon","votre"),("mes","vos"),
				("ma","votre"),("vous","je"),("votre","ma")]
	# attention : l'ordre de ces entrées est important - on remplace d'abord les premiéres
	#               entrées et les autres seulement quand les premières ne se sont pas
	#               appliquées !
    
    
	
		
	def guesssex(self,textinput):
		#print "ggggggggggggggg"
		for trigger in self.personalAdjTriggers:
			if trigger+" " in textinput: # if i found a trigger:
				#print "ggggggggggggggg", trigger
				rest = textinput.split(trigger)[-1].strip() # take rest after last occurrence of trigger
				for adv in self.lightAdv:
					if rest.startswith(adv): 
						rest = " ".join(rest.split()[1:])
				for adj in self.motsFemme:
					if rest.startswith(adj): 
						retu=True
						for m in self.motsPasFemme:
							if rest.startswith(m):retu=False
						if retu:return "F"
				
				for lem,cod in self.lefff.lookupDico(rest.split()[0]):
					if "f" in cod:
						return "F"
					if "m" in cod:
						return "M"
				
		return "unknown"
	
	def changePersonne(self,liste):
		""" fonction qui remplace les verbes par la personne contraire
		(la personne de l'interlocuteur ou du locuteur respectivement)
		et les pronoms qui vont avec.
		- c'est un peu un bricolage pas très élégant - il n'y a rien
		d'universel ou de profondement linguistique dans cette fonction...
		(le plus difficile est de remplacer la suite de pronoms une fois
		et ne pas une deuxième fois, même si la liste de remplacment le
		permettait...)
		"""
		#  on trouve les verbes à la 1ère personne qu'il faudra remplacer
		indexVerbes1 = self.candidatsVerbaux(self.dicClitPersSource[1],liste)
		
		# et on les remplace
		for i in indexVerbes1:
			liste[i] = self.lefff.changePersonne(liste[i],1,2)
	
		#  on trouve les verbes à  la 2e personne qu'il faudra remplacer
		indexVerbes2 = self.candidatsVerbaux(self.dicClitPersSource[2],liste)
		# et on les remplace (si ce n'est pas déjà  le résultat d'un remplacement)
		for i in indexVerbes2:
			if i not in indexVerbes1:
				liste[i] = self.lefff.changePersonne(liste[i],2,1,pluriel=False)
	
		# on passe aux pronoms :
		nouvelleListe=["" for mot in liste]
	
		for cle,valeur in self.remplacements12: # chaque remplacement
			listeMotsAvant = cle.split()
			listeMotsApres = valeur.split()
			neuf = self.remplaceSousListe(listeMotsAvant,listeMotsApres,liste)
			# copier tout ce qui est nouveau s'il n'y a pas déjà un remplacement
			for index, mot in enumerate(liste):
				if nouvelleListe[index] == "" and mot != neuf[index]:
					nouvelleListe[index] = neuf[index]
		# remplacer les mots qui n'ont pas été touchés :
		for index,mot in enumerate(nouvelleListe):
			if mot == "" :
				nouvelleListe[index]=liste[index]
	
		return nouvelleListe
        
        
	
	def candidatsVerbaux(self,liste2cles,liste2mots):
		""" rend une liste d'indices de verbes qui suivent certaines clés,
		par exemple 'je' ou 'j'.
		par exemple, pour la input
		"hier, je ne lui en ai rien donné, et j'en suis fier"
		(nettoyée et splittée)
		il faut rendre [6,12]
		"""
	
		# drapeau pour nous indiquer quand on est en train de passer au dessus
		# des clitiques :
		alerte = False
		liste = [] # contiendra les indices des verbes à  regarder
	
		for index,mot in enumerate(liste2mots):
			if alerte and (mot not in self.listeClitiques) :
				# si je suis en train de passer sur les clitiques
				# et soudainement, ce n'est plus un clitique, alors
				# je suppose que j'ai trouvé le verbe à traiter
				liste.append(index)
				alerte = False
			if mot in liste2cles:
				alerte = True
		return liste
	
	def decontracte(self,chaine):
		for clitique in self.listeElis:
			# pour chaque clitique qui pourrait êre élisé
			# crée une cdc avec la forme élisée suivi d'une lettre quelconque
			# par exemple " qu'(\w)"
			e = clitique[:-1]
			regsSourceString = " "+e+"'([éêèùûîô\w])"
			# en faire une expression régulière
			regSourceExp = re.compile(regsSourceString)
			# crée une cdc de remplacement
			# par exemple " que \1"
			#regsCibleString = r"\1"
			regsCibleString = " "+clitique+" "+ r"\1"
			#regsCibleString
			# ici se fait le vrai travail : ,re.UNICODE
			chaine = (regSourceExp.sub(regsCibleString," "+chaine))[1:]
	
		return chaine
        
        


	def beautifier(self,chaine,sex):
		"""
		fonction pour printer des lignes qui ont été travaillées
		et où il est donc possible qu'il manque certaines élisions
		"""
		
		#print "___"+chaine
		# posttraitement :
		# pour l'instant seulement des élisions
		for clitique in self.listeElis:
			# pour chaque clitique à  éliser
			# crée une cdc avec ce clitique plus une voyelle
			regsSourceString = "[ ']"+clitique+" ([aeiouyéêèùûîô])"

			# en faire une expression régulière
			regSourceExp = re.compile(regsSourceString)
			# crée une cdc de remplacement
			# (guillemet simple suivi de ce qu'on a trouvé en premier :  donc la voyelle)
			regsCibleString = r"'\1"
			# ajouter le clitique sans son dernier caractère devant
			# cela part de l'idée qu'on n'a toujours qu'un caractère
			# à  enléver
			regsCibleString = " "+clitique[:-1]+regsCibleString

			# ici se fait le vrai travail :
			# à  l'aide de l'expression régulière source,
			# nous remplaçons cette expression par le cible dans
			# la chaîne à traiter content.decode(encoding)).encode(encoding)
			chaine = (regSourceExp.sub(regsCibleString," "+chaine))[1:]
	
		chaine = re.sub(" +"," ",chaine)
		if sex != "unknown" : # choisit le bon coté d'une parenthèse (x/se) en fonction du sexe du patient
			cc = chaine[:]
			mot = ""
			try:
				while "(" in cc:
					ccl=cc.split("(")
					ccgauche=ccl[0]
					cccl=ccl[1].split(")")
					ccdroite = cccl[1]
					par = cccl[0].split("/")
					if sex=="M": mot = par[0]
					else : mot = par[1]
					cc =  ccgauche+mot+ccdroite
				chaine = cc
			except: pass
			
		# on recode pour que ça s'affiche bien
	##        chaine = self.recode(chaine)
		return chaine
		
        

        
	def remplaceSousListe(self,sousListeAvant,sousListeApres,liste):
		""" fonction utilise un double underscore '__' et aucun mot des
		listes peut donc contenir ces deux caratères à  la suite
		c'est ainsi qu'on peut avoir recours aux expressions régulières
		pour ne pas refaire le màªme travail pour les listes
		"""
	
		# on crée des chaînes de caractères à  partir des listes de manière
		# que entre les mots (ou expressions) se trouve des caractères uniques
		# et on a choisi "__" mais ça pourrait êre n'importe quoi d'autre tant
		# que ça n'apparaît pas dans les mots à  traiter
		li = "__".join(liste)
		av = "__".join(sousListeAvant)
		ap = "__".join(sousListeApres)
	
		# on utilise les regex pour remplacer
		res = re.sub("__"+av+"__","__"+ap+"__","__"+li+"__")
		# et on divise à  nouveau dans une liste
		resultat = res.split("__")
		# on enlève les vides au début et à  la fin
		# (provenant des caractères "__" au début et à  la fin)
		resultat.pop()
		resultat.pop(0)
		# on rend le résultat.
		return resultat
        
        


	def choisirBonnePhrase(self,liste2phrases):
		""" prend par défaut une phrase où le patient
		parle de lui-màªme, sinon la dernière
		"""
		bonnePhrase = ""
		for clit in ["je","nous","vous"]:
			# pour chaque clitique qu'on sait retourner
			for phrase in liste2phrases: # pour chaque phrase
				if len(phrase) > 1 :  bonnePhrase = phrase
				# si on a trouvé une phrase avec un bon clitique, on s'arrête
				if clit in phrase: break
		if bonnePhrase == "" : bonnePhrase = liste2phrases[0]
		return bonnePhrase


	def nettoyerTexte(self,texte):
		""" 
		nettoie le texte en le mettant en minuscules
		et en enlevant toute ponctuation
		"""
		propre = texte.lower()
		for c in string.punctuation+"`«»":
			propre=propre.replace(c," ")
		return propre
	
	def phraseEnchassee(self,input,sex):
		
		input.replace("M.","M") # pour éviter qu'on coupe après M. quand on divise l'input en phrases
		phrases = input.split(".")
		
		bonnePhrase = self.choisirBonnePhrase(phrases)
		phraseSplit = (self.nettoyerTexte(bonnePhrase)).split()
		
		# enlever des mots bizarre devant :
		while len(phraseSplit)>1 and phraseSplit[0] in self.motsPasApresQue: phraseSplit.pop(0)
		phraseRemaniee = " ".join(self.changePersonne(phraseSplit))
		if self.lefff.contientVerbe(phraseSplit):
			return self.beautifier( " que "+phraseRemaniee+" ?",sex)
		else :
			return self.beautifier( " '"+phraseRemaniee+"' ?",sex)
		
		
	#def demandeLionel(self,phrasePropre):
		#HOST = "lionel-clement.dyndns.org"
		#tn = telnetlib.Telnet(HOST,54321)
		#reponse=""
		#ldm = phrasePropre.split()
		#for mot in ldm:
			#tn.write(mot+"\n")
			#reponse += mot+" : "+tn.read_until("\n")+"<br>"
		#tn.close()
		#return reponse
		
	#def getLemmasVieux(self,wordlist):
		#tn = telnetlib.Telnet("lionel-clement.dyndns.org",54321)
		#lemlist = []
		#for word in wordlist:
			#tn.write(word+"\n")
			#answer = tn.read_until("\n")[:-1]
			#if answer == "" or answer == "<unknown>" or answer == word:continue
			#lemlist += answer.split("|")
		#return lemlist
	
	
	
	
	
	
	####################################################### ramsch:
	
		
	def answer2lemmalist(self,answer):
		pass
	  
	def askLionel(self,input):
		"""
		input in utf 8
		returns answer in utf 8
		although the server uses iso 8859 1
		"""
		return ""
		#try:
			#tn = telnetlib.Telnet(lemmaHost,lemmaPort)
			#input = (input.decode("utf-8",'ignore')+"###\n".decode("utf-8",'ignore')).encode("iso-8859-1",'ignore')
			##input = input+"#\n"
			#tn.write(input)
			#answer = tn.read_until("###",.5).decode("iso-8859-1").encode("utf-8")[:-3]
		#except: answer = ""
		#return answer
		
	def oldgetLemmas(self,input):	
		params={}
		params["s"]="\n".join(input.split())+"\n"
		params=urllib.urlencode(params)
		#print params+"___"
		lemmas = urllib.urlopen("http://gerdes.fr/lemmm/lemmm.cgi", params).read().split("\n")#[:-2]
		
		if re.search("\d",input):lemmas+=["NUMBER"]
		#print "yyy",lemmas
		return lemmas
	
	     
	def code2lemmas(self,code):
		lemmal=[]
		for lecture in code.split("|"):
			if len(lecture)>1 and lecture!='<UNKNOWN>':
				lemma = lecture.split("@")[1].split("[")[0]
				lemmal+=[lemma]
		return lemmal
	    
	
	def lemmasex(self,word):
		"""
		given an adjectif or participle
		function returns M for masculin and F for feminin
		and None if it can't tell
		"""
		#print word
		if word[-1]=="e": # word maybe feminin
			if word[-2]=="s": # special forms heureuse heureux
				wor=word[:-2]+"x"
			else :
				wor=word[:-1]
			answers = self.askLionel(word+" "+wor).split("&")
			wordlem = self.code2lemmas(answers[0])
			worlem = self.code2lemmas(answers[1])
			for lemme in worlem:
				if lemme in wordlem: return "F"

		else : # word maybe masculin
			worde = word+"e"
			answers = self.askLionel(word+" "+worde).split("&")
			#print answers
			if len(answers)>2:
				wordlem = self.code2lemmas(answers[0])
				wordelem = self.code2lemmas(answers[1])
				#if word[-1]=="é":word=word[:-1]+"er" # pour particpes qui  ont les lemmes des verbes
				for lemme in wordlem:
					if lemme in wordelem: return "M"
		return None
	
	

	def recode(self,chaine):
		# nécessaire pour windows,
		# à  enlever quand on est en ligne de commande de linux
		# cela sert à  choisir le bon encodage si possible pour que
		# les lettres accentuées restent toujours lisibles
		try :
			chaine = unicode(chaine,"iso-8859-1").encode('cp437')
		except UnicodeEncodeError:
			chaine = unicode(chaine,"cp437").encode('iso-8859-1')
		return chaine

	

if __name__ == "__main__":
	f = FrenchLinguist()  
	print f.guesssex("je suis très marron")
	print f.beautifier("vous êtes (sûr/sure) de ne pas avoir des choix ?","F")
	#print f.decontracte("j'adore j'évite j'y vais")
