1. lefff --> lemmafile
	lefff2lemmm.py
	produces lemmm.txt
	
2. build c++ file:
	decide on SEP_PREF "<w><a ref=\" in buildlexicon.h
	g++ -o buildlexicon buildlexicon.cc
	produces executable buildlexicon
	
3. build tree:
	./buildlexicon -d . -p lemmdico build < lemmm.txt
	produces lemmdico.tbl lemmdico.fsa
	
4. test result:
	./buildlexicon -d . -p lemmdico consult
	

