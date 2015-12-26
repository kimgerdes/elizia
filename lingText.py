#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
#,sys,copy
from UserString import UserString
#from string import punctuation

verbose = False
#verbose = True	


class LingText(UserString):
	         
	def __init__(self, seq="") :
		UserString.__init__(self, seq.decode("utf-8"))
		#self.spaces = spaces
		self.length = len(self)
		self.wordSet = []
		#if self.length<2:return
		#self.makeParagText()
		#print  "<br>$$$",self.data
		
		# the text-dictionary giving for a position (0.12309...) the corresponding paragraph:
		self.parFracText=self._getParFracText()
		self.parPos = sorted(self.parFracText.iterkeys())
		#print self.parPos
		
		#for k in self.parPos:
			#print "<br>***",k,": ",self.parFracText[k],"<br>"
		#print ")))))))))))))))))))init LIngtext fini<br><br><br>"
		
		self.makeWordSet()

		
	
	def makeWordSet(self,data=None):
		if data == None : da=self.data
		#da.decode('utf-8')
		#da = unicode(da, "UTF-8")
		expression = re.compile(ur'\W+', re.UNICODE+re.M+re.IGNORECASE)
		wset = set(expression.split(da) )
		wset.discard(u'')
		#wlist = re.split(r"\w+", da, re.UNICODE+re.M+re.IGNORECASE)
		#wlist = [item.encode('utf-8') for item in wlist]
		#wset = set(wlist)
		if data == None : self.wordSet=wset
		return wset
		
	def getText(self,pos):
		"""
		get paragraph text for a position
		"""
		if pos in self.parPos: return self.parFracText[pos].encode( "utf-8" )
		else: return ""
		
	def getWholeText(self):
		return self.data.encode( "utf-8" )
	
	def getParForPos(self,pos): #get paragraph containing position (fraction)
		low = 0.0
		for p in self.parPos:
			if pos<p:return low
			low = p
		return p
	
	
	def replaceWord(self,oldWord,beforeNewWord="",afterNewWord="",text=None,newWord=r"\2"):
		"""
		example:
		replaceWord("le",beforeNewWord="before:",afterNewWord=":after")
		"""
		dat = text.decode("utf-8")
		if text == None : dat=self.data
		strOldWord = r"([\W])("+re.escape(oldWord)+r")(\W)"
		expOldWord = re.compile(strOldWord, re.UNICODE+re.M+re.IGNORECASE)
		expNewWord = r"\1"+beforeNewWord+newWord+afterNewWord+r"\3"
		
		#print expOldWord.pattern
		#print expNewWord
		
		datNew =  (expOldWord.sub(expNewWord," "+dat+" ")[1:-1]).encode( "utf-8" )
		if text == None : self.data=datNew
		return datNew
		
		
	def markWords(self,text,wordlist,beforeMark,afterMark):
		for w in wordlist:
			text = self.replaceWord(w,beforeMark,afterMark,text)
		return text	
			
	def getWordIndeces(self,word):
		strWord = "([\W])("+re.escape(word)+")(\W)"
		expWord = re.compile(strWord, re.UNICODE+re.M+re.IGNORECASE)
		return [match.start() for match in expWord.finditer(" "+self.data+" ")]
	
	def getWordFreq(self,word):
		return len(self.getWordIndeces(word))/float(self.length)
	
	def getWordPositions(self,word):
		return [float(index)/self.length for index in self.getWordIndeces(word)]
		
	def _getParagIndeces(self,newline="\n"):
		expWord = re.compile(newline, re.UNICODE+re.M+re.IGNORECASE)
		return [0]+[match.start()+1 for match in expWord.finditer(self.data[:-1])]
	
	def _getParFracText(self,newline="\n"):
		return dict(zip(self._getParagFractions(),re.split(newline,self.data[:-1])))
	
	def _getParagFractions(self,newline="\n"):
		return [float(i)/self.length for i in self._getParagIndeces(newline)]
	
	
	
        
    
if __name__ == "__main__":
	#verbose = True
	#if verbose: print "test:"
	
	lingText = LingText(seq="""
	le  ..leùù**  lele le$ leé Scepticisme ou occultisme ? 
	Le complot du 11-Septembre n’aura pas lieu 
	L’idée que les attentats du 11-Septembre auraient été manigancés par la Maison Blanche a fait son chemin. Or, réplique Alexander Cockburn, figure marquante de la gauche radicale aux Etats-Unis, une telle croyance témoigne, paradoxalement, d’une forme d’hébétement devant la puissance américaine, alors même que celle-ci échoue dans des entreprises bien moins herculéennes que l’éventuelle réalisation (puis la dissimulation) d’un tel complot.le""".decode("utf-8"))
		
	

	
	print lingText.data
	
	s = lingText.makeWordSet()
	
	for w in s:
		print w
	
	#print lingText.getWordIndeces("\n")
	
	print "\n"
	
	oldWord = uword = r"pr".decode('utf-8')
	beforeNewWord = " before:"
	afterNewWord=":after "
	newWord=r"\2"
	
	dat = """président pr prù pr* pr= président   pr+àà """.decode('utf-8')
	#strOldWord = r"(\W)("+re.escape(oldWord)+r")(\W)"
	dat  = lingText.data
	
	strOldWord = r"\W+"
	
	expOldWord = re.compile(strOldWord, re.UNICODE+re.M+re.IGNORECASE)
	#expNewWord = r"\1"+beforeNewWord+newWord+afterNewWord #+r"\3"
	#expNewWord = beforeNewWord+r"XXX"+afterNewWord #+r"\3"
	expNewWord = r"XXX"#+r"\3"
	#print expOldWord.pattern
	#print expNewWord
	
	datNew =  expOldWord.sub(expNewWord," "+dat+" ")[1:-1]

	
	
