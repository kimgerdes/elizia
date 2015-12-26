#include <iostream>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>

#include "buildlexicon.h"

#define PACKAGE "lexicon"
#define VERSION "1.0.0"
//#define DIFF

char *LexedBuffer;
unsigned long int nbreItem;
unsigned long int nbreItemMax;
int swap;

struct Fsa *fsa;         // table fsa
InfoBuff *info;   //table des info
TYPEPTR LexedInitial;
Arbre *LexiqueInit;
Arbre *Lexique;

static struct stat *statbuf;
FILE *Table;

////////////////////////////////////////////////////////////
//
////////////////////////////////////////////////////////////
void Usage() {
  fprintf(stderr,
    "Usage: lexicon [global-option] <build|consult> <filename>\n"
    "Global options:\n"
    "-h|--help                              print this\n"
    "-v|--version                           print version\n"
    "-p <name>                              prefix name\n"
    "-d <directory>                         directory\n"
  );
}

////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////
void PrintResults (TYPEPTR Index,
		   bool Sep,
		   FILE *Table)
{
  char Etiquette[LEXEDMAXSTRING]; 
  if (Sep)
    fputs(SEP_PREF, stdout);
  if (Index == (TYPEPTR)(~(0UL))){
    fputs(SEP_UW, stdout);
    if (Sep) fputs(SEP_SUFF, stdout);
    return;
  }
  while (Index != (TYPEPTR)(~(0UL))){
    // an other element will be describe
    strcpy (Etiquette, LexedBuffer+(info[Index].offset));
    fputs(Etiquette, stdout);
    if (info[Index].suivant!=(TYPEPTR)(~(0UL)))
      fputs(SEP_OR, stdout);
    if ((info[Index].suivant)!=(TYPEPTR)(~(0UL)))
      Index=info[Index].suivant;
    else
      Index=(TYPEPTR)(~(0UL));
  }
  if (Sep) fputs(SEP_SUFF, stdout);
}

////////////////////////////////////////////////////////////
// input: string
// output: info
////////////////////////////////////////////////////////////
TYPEPTR SearchStatic(TYPEPTR Index,
		     char *Str)
{
  char *car=Str;
  Index=fsa[Index].fils;
  // for each letter of the suffix
  while (*car){
    // parse the brothers while founding the actual char
    while (*car != fsa[Index].car){
      if (fsa[Index].frere != (TYPEPTR)(~(0UL)))
	Index=fsa[Index].frere;
      else
	return (TYPEPTR)(~(0UL));
    }
    if (*car != fsa[Index].car)
      return ((TYPEPTR)(~(0UL)));
    if (*(car+1)){
      if (fsa[Index].fils != (TYPEPTR)(~(0UL)))
	Index=fsa[Index].fils;
      else
	return (TYPEPTR)(~(0UL));
    } else
      if (fsa[Index].info != (TYPEPTR)(~(0UL)))
	return fsa[Index].info;
    car++;
  } 
  return (TYPEPTR)(~(0UL));
}

////////////////////////////////////////////////////////////
// 
////////////////////////////////////////////////////////////
void List(TYPEPTR Index,
	  char *Chaine,
	  int Rang,
	  FILE *Table)
{
  Chaine[Rang] = fsa[Index].car;
  if (fsa[Index].fils != (TYPEPTR)(~(0UL)))
    List(fsa[Index].fils, Chaine, Rang+1, Table);
  if (fsa[Index].frere != (TYPEPTR)(~(0UL)))
    List(fsa[Index].frere, Chaine, Rang, Table);
  if (fsa[Index].info != (TYPEPTR)(~(0UL))){
    Chaine[Rang] = fsa[Index].car;
    Chaine[Rang+1]=0;
    fputs (Chaine, stdout);
    putchar('\t');
    PrintResults(fsa[Index].info, 0, Table);
    putchar('\n');
  }
}

////////////////////////////////////////////////////////////
//
////////////////////////////////////////////////////////////
int
SaveFSA(FILE *Fichier)
{
  TYPEPTR Taille;
  int NbrBytes;
  // encodage des offsets (16 ou 32 bits)
  NbrBytes=sizeof(TYPEPTR);
  fwrite(&NbrBytes, sizeof(NbrBytes), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "%d bytes\n", NbrBytes);
#endif //DIFF
  Taille=(TYPEPTR)~0UL;
  fwrite(&Taille, sizeof(Taille), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "Test %lX\n", Taille);
#endif //DIFF
  // nombre d'offsets du fsa
  nbreItem=0;
  Taille=0;
  LexiqueInit->SetIndexStaticFSA(Taille);
  fwrite(&Taille, sizeof(Taille), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "Size FSA %lX\n", Taille);
#endif //DIFF
  if(Taille == (TYPEPTR)~0UL){
    fputs ("*** Error: Lexicon too large\n", stderr);
    fclose(Fichier);
    return 0;
  }
  Taille=0;
  LexiqueInit->SetIndexStaticInfo(Taille);
  fwrite(&Taille, sizeof(Taille), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "Size Info %lX\n", Taille);
#endif //DIFF
  if(Taille == (TYPEPTR)~0UL){
    fputs("*** Error: Data too large\n", stderr);
    fclose(Fichier);
    return 0;
  }
#ifdef DIFF
  fprintf(stdout, "---FSA---\n");
#endif //DIFF
  LexiqueInit->PrintStaticFSA(Fichier);
#ifdef DIFF
  fprintf(stdout, "---Info---\n");
#endif //DIFF
  LexiqueInit->PrintStaticInfo(Fichier);
  fputs("*** Writing Data\n", stderr);
  fflush(Fichier);
  // table
  fflush(Fichier);
  fwrite(&LexedInitial, sizeof(LexedInitial), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "Initial: %lX\n", LexedInitial);
#endif //DIFF
  return 1;
}

////////////////////////////////////////////////////////////
//
////////////////////////////////////////////////////////////
int
LoadFSA(FILE *Fichier){
  TYPEPTR TailleFsa;
  TYPEPTR TailleInfo;
  int NbrBytes;
  fputs("*** Loading Finite State Automata\n", stderr);
  fread(&NbrBytes, sizeof(NbrBytes), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "%d bytes\n", NbrBytes);
#endif //DIFF
  fread(&TailleFsa, sizeof(TailleFsa), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "Test %lX\n", TailleFsa);
#endif //DIFF
  if(NbrBytes!=(sizeof(TYPEPTR)) || (TailleFsa!=(TYPEPTR)~0UL)){
    fputs("*** fatal error:\n*** lexicon not compiled with the good version of Lexed or on an incompatible system\n", stderr);
    fclose (Fichier);
    return 0;
  }
  fread(&TailleFsa, sizeof(TailleFsa), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "Size FSA %lX\n", TailleFsa);
#endif //DIFF
  fread(&TailleInfo, sizeof(TailleInfo), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "Size Info %lX\n", TailleInfo);
#endif //DIFF
#ifdef DIFF
  fprintf(stdout, "---FSA---\n");
#endif //DIFF
  fsa = new Fsa[TailleFsa+1];
  fread(fsa, sizeof(Fsa), TailleFsa, Fichier);
#ifdef DIFF
  for(unsigned long int TailleSy=0;TailleSy<TailleFsa;TailleSy++){
    fprintf(stdout, " so:%lX", fsa[TailleSy].fils);
    fprintf(stdout, " br:%lX", fsa[TailleSy].frere);
    fprintf(stdout, " in:%lX", fsa[TailleSy].info);
    fprintf(stdout, " <%c>\n", fsa[TailleSy].car);
  }
#endif //DIFF
#ifdef DIFF
  fprintf(stdout, "---Info---\n");
#endif //DIFF
  info = new InfoBuff [TailleInfo+1];
  fread(info, sizeof(InfoBuff), TailleInfo, Fichier);
#ifdef DIFF
  for(unsigned long int TailleSy=0;TailleSy<TailleInfo;TailleSy++){
    fprintf(stdout, " su:%lX of:%lX\n", info[TailleSy].suivant, info[TailleSy].offset);
  }
#endif //DIFF
  fread(&LexedInitial, sizeof(LexedInitial), 1, Fichier);
#ifdef DIFF
  fprintf(stdout, "Initial: %lX\n", LexedInitial);
#endif //DIFF
  return 1;
}

////////////////////////////////////////////////////////////
// Calcule les offsets du tableau FSA
////////////////////////////////////////////////////////////
void Arbre::SetIndexStaticFSA(TYPEPTR &Index)
{
  Arbre *LexiqueSy;
  for (LexiqueSy=this;LexiqueSy!=NULL;LexiqueSy=LexiqueSy->frere){
    LexiqueSy->adress = Index++;
    if (LexiqueSy->fils)
      LexiqueSy->fils->SetIndexStaticFSA(Index);
  }
}

////////////////////////////////////////////////////////////
// écrit les enregistrements du FSA
// les offsets sont calculés sur 32 (vs 16) bits si long==1
////////////////////////////////////////////////////////////
void Arbre::PrintStaticFSA(FILE *Out)
{
  Fsa Elt;
  Arbre *LexiqueSy;
  if (this==LexiqueInit){
    LexedInitial=this->adress;
  }
  for (LexiqueSy=this;LexiqueSy;LexiqueSy=LexiqueSy->frere){
    Elt.fils=(LexiqueSy->fils==NULL)?(TYPEPTR)~0UL:LexiqueSy->fils->adress;
    Elt.frere=(LexiqueSy->frere==NULL)?(TYPEPTR)~0UL:LexiqueSy->frere->adress;
    Elt.info=(LexiqueSy->info==NULL)?(TYPEPTR)~0UL:LexiqueSy->info->adress;
    Elt.car=LexiqueSy->car;
    fwrite(&Elt, sizeof(Elt), 1, Out);
#ifdef DIFF
    fprintf(stdout, " so:%lX br:%lX in:%lX <%c>\n", Elt.fils, Elt.frere, Elt.info, Elt.car);
#endif //DIFF
    LexiqueSy->fils->PrintStaticFSA(Out);
  }
}

////////////////////////////////////////////////////////////
// Calcule les offsets du tableau info
////////////////////////////////////////////////////////////
void Arbre::SetIndexStaticInfo(TYPEPTR &Index)
{
  Info *InfoSy;
  Arbre *LexiqueSy;
  for (LexiqueSy=this;LexiqueSy!=NULL;LexiqueSy=LexiqueSy->frere)
    LexiqueSy->fils->SetIndexStaticInfo(Index);
  for (LexiqueSy=this;LexiqueSy!=NULL;LexiqueSy=LexiqueSy->frere){
    for (InfoSy=LexiqueSy->info;InfoSy!=NULL;InfoSy=InfoSy->GetSuivant()){
      InfoSy->adress = Index++;
    }
  }
}

////////////////////////////////////////////////////////////
// écrit les enregistrement du tableau d'infos
// les offsets sont calculés sur 32 (vs 16) bits si long==1
////////////////////////////////////////////////////////////
void Arbre::PrintStaticInfo(FILE *Out){
  Info *InfoSy;
  Arbre *LexiqueSy;
  InfoBuff Elt;
  for (LexiqueSy=this;LexiqueSy!=NULL;LexiqueSy=LexiqueSy->frere)
    LexiqueSy->fils->PrintStaticInfo(Out);
  for (LexiqueSy=this;LexiqueSy!=NULL;LexiqueSy=LexiqueSy->frere){
    for (InfoSy=LexiqueSy->info;InfoSy!=NULL;InfoSy=InfoSy->GetSuivant()){
      Elt.suivant=(InfoSy->suivant!=NULL)?InfoSy->suivant->adress:(TYPEPTR)(~(0UL));
      Elt.offset=InfoSy->offset;
      fwrite(&Elt, sizeof(Elt), 1, Out);
#ifdef DIFF
      fprintf(stdout, " su:%lX of:%lX\n", Elt.suivant, Elt.offset);
#endif //DIFF
    }
  }
}

////////////////////////////////////////////////////////////
// ajoute un mot dans l'arbre à lettres
////////////////////////////////////////////////////////////
void Arbre::Add(char *Chaine,
		TYPEPTR Offset){
  //Info *InfoSy;
  if (!this->car){
    this->car = Chaine[0];
    if (!Chaine[1]){
      if(this->info){
	this->info = new Info(this->info, Offset);
      }
      else
	this->info = new Info(NULL, Offset);
    }
    else{
      if (!this->fils)
	this->fils = new Arbre(NULL, NULL, NULL, Chaine[1]);
      this->fils->Add((char *)Chaine+1, Offset);
    }
  }
  else if (this->car == Chaine[0]){
    if (!Chaine[1]){
      if(this->info){
	this->info = new Info(this->info, Offset);
      }
      else
	this->info = new Info(NULL, Offset);
    }
    else{
      if (!this->fils)
	this->fils = new Arbre(NULL, NULL, NULL, Chaine[1]);
      this->fils->Add((char *)Chaine+1, Offset);
    }
  }
  else if (this->frere)
    this->frere->Add(Chaine, Offset);
  else{
    this->frere = new Arbre(NULL, NULL, NULL, Chaine[0]);
    this->frere->Add(Chaine, Offset);
  }
}

////////////////////////////////////////////////////////////
//
////////////////////////////////////////////////////////////
int Build(int argn, char **argv, int pos, char* Directory, char* Prefix) {

  FILE *Input;
  FILE *FSA;
  char InputFile[LEXEDMAXSTRING];
  char TableFile[LEXEDMAXSTRING];
  char FSAFile[LEXEDMAXSTRING];
  char chaine [LEXEDMAXSTRING];
  char graphie [LEXEDMAXSTRING];
  char oldChaine [LEXEDMAXSTRING];
  unsigned int i;
  unsigned int rang;
  TYPEPTR offset;
  
  *InputFile=0;
  offset = 0;
  rang = 0;

  // mode specific options
  for (i = pos; argv[i]; i++) {
    if (argv[i][0] == '-') {
    } else {
      strcpy (InputFile, argv[i]);
    }
  }

  sprintf (TableFile, "%s/%s.tbl", Directory, Prefix);
  Table = fopen (TableFile, "w");
  if (!Table) {
    fprintf (stderr, "Unable to open file %s for writing\n", TableFile);
    exit (0);
  }
  
  if (*InputFile) {
    fprintf(stderr, "*** Loading lexicon %s\n", InputFile);
    Input = fopen (InputFile, "r");
    if (!Input) {
      fprintf (stderr, "Unable to open file %s for reading\n", InputFile);
      exit (0);
    }
  } else {
    fprintf(stderr, "*** Loading lexicon from stdin\n");
    Input = stdin;
  }

  statbuf=(struct stat *)malloc(sizeof(struct stat));
  stat(InputFile, statbuf);
  nbreItemMax=statbuf->st_size;
  free(statbuf);

  if (Lexique == NULL) {
    Lexique=new Arbre(NULL, NULL, NULL, '\0');
    Lexique->fils=new Arbre(NULL, NULL, NULL, '\0');
    LexiqueInit=Lexique;
    Lexique=Lexique->fils;
  }

  while (fgets(chaine, LEXEDMAXSTRING, Input)) {
    if (!*chaine) {
      continue;
    }

    for (i = 0; i <= strlen(chaine) && (!strchr ("\t", chaine[i])); i++)
      /* empty */;

    chaine[strlen(chaine)-1] = 0;
    strcpy (graphie, chaine);
    if (i < strlen (chaine)) {
      graphie[i]=0;
      if (!strcmp(chaine+i+1, oldChaine)) {
	Lexique->Add(graphie, offset);
      } else {
	// Adds one entry
	offset = ftell(Table);
	Lexique->Add(graphie, offset);
	fprintf(Table, "%s%c", chaine+i+1, 0);
      }
      strcpy (oldChaine, chaine+i+1); 
    } else {
      // the entry of one word without any information is the same as the previous:
      // aaa info_of_aaa
      // bbb
      //
      // bbb -> info_of_aaa
      Lexique->Add(graphie, offset);
    }

    nbreItem+=strlen(chaine)+1;
    if (!(rang++ % 1357)) {
      fprintf (stderr, " %.0f%%\r", (100*(float)nbreItem)/(float)nbreItemMax);
    }
  }

  if (*InputFile) {
    fclose (Input);
  }

  fclose (Table);
  
  sprintf (FSAFile, "%s/%s.fsa", Directory, Prefix);
  //cerr << "*** type: " << sizeof(TYPEPTR)*8 << "\n";
  fputs("*** Writing Finite State Automata\n", stderr);
  FSA = fopen (FSAFile, "w");
  if (FSA) {
    SaveFSA(FSA);
    fclose (FSA);
  } else {
    fprintf (stderr, "Unable to open file %s for writing\n", FSAFile);
    exit (0);
  }
  return 0;
}

////////////////////////////////////////////////////////////
//
////////////////////////////////////////////////////////////
int Consult(int argn, char **argv, int pos, char* Directory, char* Prefix)
{
  FILE *Input;
  FILE *Table;
  FILE *FSA;
  char InputFile[LEXEDMAXSTRING];
  char TableFile[LEXEDMAXSTRING];
  char FSAFile[LEXEDMAXSTRING];
  char chaine [LEXEDMAXSTRING];
  int i;
  bool Lists=false;
  //char *buf;
  int ok;
  unsigned long int Taille;
  TYPEPTR info;
  *InputFile=0;

  // mode specific options
  for (i = pos; argv[i]; i++) {
    fprintf(stderr, "###%s\n", argv[i]);
    if (argv[i][0] == '-') {
      if (!strcmp(argv[i]+1, "l")) {
	Lists=true;
      }
    } else {
      strcpy (InputFile, argv[i]);
    }
  }
  
  sprintf (FSAFile, "%s/%s.fsa", Directory, Prefix);
  FSA = fopen(FSAFile, "r");
  if (!FSA) {
    fprintf(stderr, "File %s not found\n", FSAFile);
    exit (0);
  } else {
    if (!LoadFSA(FSA)) {
      return 1;
    } 
    fclose (FSA);
  }

  sprintf (TableFile, "%s/%s.tbl", Directory, Prefix);
  Table = fopen (TableFile, "r");
  if (!Table) {
    fprintf(stderr, "File %s not found\n", TableFile);
    exit (0);
  } else {
    fputs("*** Load buffer in memory\n", stderr);
    statbuf = (struct stat *)malloc(sizeof(struct stat));
    stat(TableFile, statbuf);
    Taille = statbuf->st_size;
    free(statbuf);
    
    LexedBuffer = new char [Taille];
    LexedBuffer[0] = 0;
    
    ok = fread (LexedBuffer, 1, Taille, Table);
    fclose (Table);
  }
  
  if (Lists) {
    char *Chaine = (char *)malloc (5*1024*1024);
    //strcpy(Chaine, "                     ");
    strcpy(Chaine, "");
    List(fsa[LexedInitial].fils, Chaine, 0, Table);
    strcpy(Chaine, "");
    free(Chaine);
    return 0;
  }

  if ((*InputFile)) {
    fprintf(stderr, "*** Seaching %s\n", InputFile);
    Input = fopen (InputFile, "r");
    if (!Input) {
      fprintf (stderr, "Unable to open file %s for reading\n", InputFile);
      exit (0);
    }
  } else {
    fprintf(stderr, "*** Searching from stdin\n");
    Input = stdin;
  }
  while (fgets (chaine, LEXEDMAXSTRING, Input)) {
    //
    chaine[strlen(chaine)-1]=0;
    info = SearchStatic(LexedInitial, chaine);
    PrintResults(info, 1, Table);
    fflush(stdout);
  }
  
  if (*InputFile) {
    fclose (Input);
  }
  
  return 0;
}

////////////////////////////////////////////////////////////
// 
////////////////////////////////////////////////////////////
int main(int argn,
	 char **argv)
{
  char Prefix[LEXEDMAXSTRING];
  char Directory[LEXEDMAXSTRING];
  if (argn > 1) {
    // generic options
    for (int i = 1; argv[i]; i++) {
      if (argv[i][0] == '-') {
	if (!strcmp(argv[i]+1, "p")) {
	  if ((i+1 >= argn) || argv[i+1][0] == '-') {
	    Usage();
	  } else {
	    strcpy (Prefix, argv[++i]);
	  }
	} else if (!strcmp(argv[i]+1, "d")) {
	  if ((i+1 >= argn) || argv[i+1][0] == '-') {
	    Usage();
	  } else {
	    strcpy (Directory, argv[++i]);
	  }
	} else if (!strcmp(argv[i]+1, "v") || !strcmp(argv[i]+1, "-version")) {
	  fprintf(stderr, "%s version %s\n", PACKAGE, VERSION);
	  exit(0);
	} else if (!strcmp(argv[i]+1, "h") || !strcmp(argv[i]+1, "-help")) {
	  Usage();
	} else {
	  Usage();
	}
      } else {
	if (!strcmp(argv[i], "build")) {
	  return Build(argn, argv, i+1, Directory, Prefix);
	} else if (!strcmp(argv[i], "consult")) {
	  return Consult(argn, argv, i+1, Directory, Prefix);
	} else {
	  Usage();
	}
      }
    }
  } else {
    Usage();
  }
  return 0;
}
