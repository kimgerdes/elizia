//<head>//////////////////////////////////////////////////////////////
//
//	
//	Conception & programmation :
//	Lionel Clément
//	e-mail : lionel.clement@labri.fr
//
//	samedi 10 mai 2008
//
//
////////////////////////////////////////////////////////////////</head>////

#ifndef LEXICON_H
#define LEXICON_H

#define LEXEDMAXSTRING 255
//#define SEP_PREF "<w><a ref=\""
#define SEP_PREF ""

// #define SEP_UW "UNKNOWN"
// kim changed to empty:
#define SEP_UW ""
//#define SEP_SUFF "\"/></w>\n"
#define SEP_SUFF "\n"

// kim changed to space:
//#define SEP_OR "\"/><a ref=\""
#define SEP_OR " "

typedef unsigned long int TYPEPTR;

struct Fsa {
  public:
  TYPEPTR fils;
  TYPEPTR frere;
  TYPEPTR info;
  int car;
} ;

struct InfoBuff {
  public:
  TYPEPTR suivant;
  TYPEPTR offset;
};

class Arbre
{
public:
  class Arbre *fils;
  class Arbre *frere;
  class Info *info;
  int car;
  TYPEPTR adress;
  
  Arbre(Arbre *Fils,
	Arbre *Frere,
	Info *Info,
	unsigned int Car)
    {
      adress=0;
      fils = Fils;
      frere = Frere;
      info = Info;
      car = Car;
    };
  
  ~Arbre() {};

  void Add(char *, 
	   TYPEPTR);
  void SetIndexStaticFSA(unsigned long int &);
  void PrintStaticFSA(FILE *);
  void SetIndexStaticInfo(unsigned long int &);
  void PrintStaticInfo(FILE *);
};

class Info
{

 public:
  class Info *suivant;
  TYPEPTR offset;
  TYPEPTR adress;
  
  Info(Info *Suivant = NULL, TYPEPTR Offset = 0)
    {
      adress=0;
      suivant=Suivant;
      offset=Offset;
    };
  
  ~Info(){};
  
  Info *GetSuivant()
  {
    return suivant;
  }
  
  TYPEPTR GetOffset()
  {
    return offset;
  }
  
  void PrintStatic(FILE *);
};

#endif // LEXICON_H
