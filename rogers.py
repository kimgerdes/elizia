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

class Rogers:
	
	noRecall = ["Question","Retour","Déjà","Vide","Bref","Fin","des insultes","Remerciements","Répétition",
			"Parceque","Négation","Négation Avoir","Oui","Faim","Reprise","Salutation","tutoiement",
			"moi","votre identité sexuelle"]
	ordered = ["des insultes","Salutation","Remerciements"]
	noCycle = ["des insultes"]
	stop = ["Fin"]
	
	answers={}
	keywords={}
	quality={}
		
	quality["Question"] = 1	
	answers["Question"] =[	"A vous de me le dire !",
				"C'est moi qui pose les questions ici.",
				"Si je vous donnais des réponses, ça serait trop facile.",
				"Si j'avais des réponses à de telles questions, croyez-vous que je serais ici ?",
				"Mon rôle n'est pas de répondre à vos questions !",
				"J'ai des questions à toutes vos réponses.",
				"Pourquoi le demandez-vous ?",
				"Vous ne le savez pas déjà ?",
				"Est-ce que cette question vous intéresse ?",
				"Quelle réponse souhaitez-vous entendre ?",
				"Qu'en pensez-vous ?",
				"Est-ce que cette question vous vient souvent à l'esprit ?",
				"Que désirez-vous vraiment savoir ?",
				"Avez-vous posé la question à une autre personne?",
				"Avez-vous posé ces questions auparavant ?",
				"Quelles autres questions vous viennent à l'esprit lorsque vous demandez ça?",
				"Pourquoi êtes-vous tellement intéressé à le savoir ?",
				"L'approche rogérienne à la thérapie a des avantages mais aussi l'inconvénient que je ne peux répondre à vos questions."]
	quality["Retour"] = 0
	answers["Retour"]=[	"Approfondissez !",
				"Continuez, précisez votre pensée.",
				"Pourriez-vous développer un peu ?",
				"Quels sentiments cela éveille-t-il en vous quand vous dites xxx ",
				"Je suis ravie que vous parveniez à verbaliser xxx ",
				"N'arrêtez pas ! Vous êtes sur la bonne voie !",
				"Cela vous fait quoi de me dire xxx",
				"Pourquoi dites-vous xxx",
				"Je vois.",
				"Je comprends.",
				"Je vous écoute !",
				"Racontez plus de détails, s'il vous plaît !",
				"Ceci est très intéressant.",
				"Qu'est-ce que cela vous suggère ?",
				"Pourriez-vous expliciter le fait xxx",
				"Que se passe-t-il en vous quand vous prononcez à haute voix xxx",
				"Comment peut-on finir par dire xxx",
				"Je n'arrive pas à comprendre xxx"]
	quality["Répétition"] = 2
	answers["Répétition"] = ["Vous avez déjà dit ça. Avançons. Je vous écoute !",
				"Oui, parfois il est utile de se répéter. Mais j'ai bien compris ce point.",
				"Comme l'a bien dit Boris Vian :  'La mort n'est pas drôle parce qu'elle ne supporte pas la répétition.'",
				"Anatole France dirait :  'A l'endroit du public, répéter c'est prouver.'",
				"Attendez-vous une autre réponse de ma part ?",
				"Quand on n'a pas de mémoire, on se répète : quand on en a, on répète les autres.","Encore !"]
	quality["Vide"] = 1	
	answers["Vide"] = [	"N'hésitez pas, je suis votre docteur !",
				"Mais si vous ne dites rien, je ne peux vous aider.",
				"Pourquoi êtes-vous si hésitant(/e) de me parler ?",
				"Vous êtes là, parce que vous souffrez. Parlez-moi de vos souffrances !",
				"Le silence nous amène vers le rien.",
				"Le silence est un ami qui ne trahit jamais."]
				
	
	quality["Bref"] = 1
	answers["Bref"] = [	"Vous n'êtes pas prodigue de paroles !",
				"Il faudrait en dire un peu plus.",
				"Vous êtes un peu trop taciturne.",
				"Vous ne dites pas un mot de trop."]
	quality["Reprise"] = 2	
	answers["Reprise"] = [	"Revenons à nos moutons et parlons un peu plus de xxx.",
				"Peut-être vous serait-il plus utile de reprendre notre discussion au sujet de xxx.",
				"Pourquoi ne continuez-vous pas de parler de xxx ?",
				"Pourquoi avez-vous abordé le sujet de xxx ?",
				"Cela nous amène trop loin. Une discussion au sujet de xxx vous aidera plus.",
				"Avant vous parliez de xxx, n'est-ce pas ?"]	
				
############################# cas mixtes
	quality["votre identité sexuelle"] = 7
	keywords["votre identité sexuelle"] = [	"queer","gay","drag queen","drag king","ying","yang","derrida",
						"bisexualité","bi","bisexuel","trans genre"]
	answers["votre identité sexuelle"] = [	"Lisez Derrida !","Lisez Butler !",
				"Êtes-vous plutôt Ying ou plutôt Yang ?",
				"L'adjectif attributif s'accorde en français !",
				"Aimez-vous le déconstructionisme ?",
				"Êtes-vous trans-genre ?",
				"Êtes-vous queer ?",
				"Pour ma part, je suis hétérosexuelle. Mais il faut le reconnaître, le bisexuel a deux fois plus de chances le samedi soir.",
				"Êtes-vous dans une transition de genres ?",
				"Les catégories de genre ne sont pas rigides.",
				"Que cela signifie pour vous d'être une femme ?",
				"Que cela signifie pour vous d'être un homme ?"]	
############################## fin cas spéciaux
	quality["Salutation"] = 6
	keywords["Salutation"] = [	"bonjour","bonsoir","salut","hi","coucou","saluer","bienvenu","bienvenue"]
	answers["Salutation"] = [	"Je vous souhaite la bienvenue à cette session de thérapie !",
					"Oui, bonjour ! Pourquoi aimez-vous tant saluer ?", 
					"Je note que vous aimez saluer ! ",
					"Je me sens tout à fait flatée. Vos parents vous ont salué suffisamment ?", 
					"Vous êtes en train de faire un test de Turing ?",
					"Ok, alors on recommence... - C'est vous qui payez ça !"]
	quality["Remerciements"] = 3				
	keywords["Remerciements"] = [	"merci","remercie","remerciements","remercier","suis reconnaissant","suis reconnaissante"]
	answers["Remerciements"] = [	"Je vous en prie !","De rien !", "Je note que vous aimez remercier ! ",
					"Je me sens tout à fait flatée.", 
					"Vous êtes en train de faire un test de Turing ?",
					"Ok, alors on recommence... - C'est vous qui payez ça !"]
	quality["Fin"] = 8	
	keywords["Fin"] = [	"au revoir","bye","ça suffit","à la prochaine", "bonne nuit","en vais",
				"à bientôt",
				"vous laisser","dois partir","bonne soirée",
				"ciao", "tchao","je me casse","à plus","à+"]
	answers["Fin"] = [	"Au revoir. Ma secrétaire vous enverra la facture sous peu.",
				"S'il vous reste de l'argent sur votre carte de crédit, alors on se reverra demain.",
				"Bonne guérison ! Et n'oubliez pas de régler sous sept jours.",
				"J'aimerais terminer sur un message d'espoir. Je n'en ai pas. En échange, est-ce que deux messages de désespoir vous iraient ?",
				"Si vous n'avez pas dépassé votre autorisation de découvert, on se reverra demain."]
	quality["tutoiement"] = 6
	keywords['tutoiement'] = ["tu", "te", "t", "toi","tes","ton","ta","tutoyer","ma poule","ma chère"]
	answers['tutoiement'] = ["Le vouvoiement serait plus approprié...", 
						"Je vous vouvoie, faites de même je vous prie !", 
						"Un peu de politesse ne vous étoufferait pas.", 
						"On n'a pas élevé les cochons ensemble !", 
						"Continuez à me vouvoyez je vous prie.", 
						"Ca vous amuse de me tutoyer ?", 
						"Pensez-vous me connaître assez pour me tutoyer ?"]
	
	quality["votre intérêt pour moi"] = 9
	keywords['votre intérêt pour moi'] = ["je t'aime", "envie de toi", "envie de te","envie de vous",
						"veux te","veux vous","je te"
					]
	answers['votre intérêt pour moi'] = ["Votre intérêt pour moi est sordide.",
						"Je vous prie d'arrêter ces enfantillages.",
						"Merci. Très peu pour moi. Reprenez-vous s'il vous plaît !",
						"Vous me semblez me prendre pour quelqu'un d'autre."
						]

	quality["ce fameux test de Turing"] = 9
	keywords['ce fameux test de Turing'] = ["ami décédé","amie décédée", "frère de mon père","frere de mon pere",
						"frère de ma mère", "soeur de ma mère",
						"soeur de mon père","mere du fils ","amie à ma soeur",
						"cousin germain de",
						"Qui est le plus lourd","Turing","incolores",
						"repondez vous pas à ma question","repondez à ma question"
					]
	answers['ce fameux test de Turing'] = ["Ah ! Encore un patient qui ne veut pas guérir ses problèmes, mais qui veut tester mon intelligence...",
						"Vous pensez vraiment que je ne connais pas ce genre de question ?",
						"Et même si je vous donnais la bonne réponse, ça ne vous aiderait pas avec vos problèmes !",
						"Et si vous poseriez cette question à des humains et vous me parliez de votre enfance ?",
						"Soyez un peu plus créati(f/ve) s'il vous plaît quand il s'agit de tester mon intelligence ! C'est insultant que vous me croyez si bête !"
						]

	
	quality["mon identité"] = 8
	keywords['mon identité'] = ["vous êtes qui", "avec qui est ce que je", "qui êtes vous", "qui etes vous",
					"votre nom", "vous appelez","appelez vous",
					"vous appellez","appellez vous",
					"moi c est", "moi, c est",
					"qui est elizia","qui est eliza","qui est éliza","qui est élizia",
					"je me appelle", "mon nom"
					]
	answers['mon identité'] = ["Je suis Élizia. Au plaisir de faire votre connaissance !", 
				"Je m'appelle Élizia, mais je suis pas là pour parler de moi.", 
				"Je suis Élizia. Je suis là pour vous aider !", 
				"Mon nom est Élizia, mais je ne pense pas qu'on devrait parler de moi.", 
				"Élizia. Enchantée.", 
				"C'est avec grand plaisir que je me présente à vous. Élizia.",
				"Je pensais m'avoir déjà présentée...",
				"Dis-moi comment tu t'appelles,je te dirai qui tu es ? - Je n'y crois pas...", 
				"Je m'appelle Élizia. Et si on continuait à parler de vous ?"]
	quality["moi"] = 5
	keywords['moi'] = ["vous", "vos", "votre", "vôtre","elizia","eliza","éliza","élizia"]
	answers['moi'] = [ 	"Parlons plutôt de vous.", 
				"Je ne suis pas là pour parler de moi.", 
				"Vous ne me payez pas pour parler de moi !", 
				"Je ne pense pas qu'on devrait parler de moi.", 
				"Passons à autre chose.", 
				"Parlez-vous de moi en particulier ?",
				"En quoi croyez-vous que j'ai un lien avec vos problèmes ?",
				"Parler de moi ne vous apporterait rien.", 
				"Pourquoi vouloir parler de moi ?", 
				"Ne m'impliquez pas là-dedans !", 
				"Je n'ai rien à voir avec ça.",
				"Nous parlons de vous, pas de moi.",
				"Vous ne parlez pas vraiment de moi, n'est-ce pas ?",
				"Si on continue à parler de moi, je risque de faire un contre-transfert",
				"Quel était le sujet de notre conversation déjà ?", 
				"On ne pose pas de telles questions à une dame !", 
				"Autrui joue toujours dans la vie de l'individu le rôle d'un modèle, d'un objet, d'un associé ou d'un adversaire.",
				"Et si on continuait à parler de vous ?"]
	quality["vous"] = 2
	keywords['vous'] = ["je", "j", "moi", "mon","ma","mes","m","nous","nos","notre"]
	answers['vous'] = [ 	"Avez-vous l'impression que les gens ne vous écoutent pas quand vous parlez de vous ?", 
				"Parler de soi-même n'est pas toujours facile.", 
				"Je suis ravie que vous réussissiez à parler de vous-même !", 
				"Votre entourage vous accepte comme vous êtes ?", 
				"Je est quelqu'un d'autre.",
				"Vous acceptez-vous vous-même ?",
				"Vous vous aimez ?",
				"Pourriez-vous aimer une personne comme vous-même ?",
				"Je commence à vous connaître.", 
				"Vous me semblez être quelqu'un de très sensible à l'intérieur.", 
				"Le moi est haïssable... mais il s'agit de celui des autres.",
				"Il ne faut compter que sur soi-même. Et encore, pas beaucoup.",
				"Le ça, le moi et le surmoi constituent les trois instances de la personne."]	
	quality["des insultes"] = 7			
	keywords["des insultes"] = [ 	"chier","merde","sous merde","limitée du bulbe","simplette","trou duc",
					"emmerdeur","emmerdeuse","emmerder","vtf","pouf",
					"tu me soules","vous me soulez","tu me soûles","vous me soûlez",
					"conasse","connasse","conne","pétasse","poufiasse",
					"grogniasse","grognasse","abrutie","fiotte",
					"connard","abruti","salopard","ignorant",
					"tasspe","sale porc","batard","gourdasse","blondasse",
					"pute","putain", "salope","salop","saloppe","salaud","pestifféré",
					"con", "gouine","gouines","gueuler","enculer",
					"va te faire","allez vous faire",
					"pédé","pd","tafiole","tapette","pédale","dégage",
					"bordel","raclure","foutre","nique","niquer","fuck", "gueule"]
	answers["des insultes"] = [	"Ne soyez pas grossi(er/ère), s'il vous plaît !" ,
					"Recentrez-vous sur votre objectif !",
					"Ecoutez-vous ! Ça frise le mauvais goût !",
					"On peut se tutoyer ? T'es lourd(/e) !",
					"Veillez à soigner votre langage !",
					"Vous semblez ne pas avoir compris le but de cette thérapie !",
					"Insulter ceux qui veulent vous aider ne vous mènera à rien !",
					"Non mais vous vous croyez où ? C'est mon dernier avertissement!",
					"Je ne continue pas dans ces conditions. Au revoir",
					"Vous insistez !!!!"]
	quality["des rires"] = 9		
	keywords["des rires"] = ["mdr", "mdrr", "mdrrr", "mdrrrr","hihihi","hihi","hahaha","haha",
				"lol", "lool", "loool", "looool","bêtise","blague","blaguer",
				"ptdr", "xpdr",  "rire",  "risée", "drôle",  "amusant","n importe quoi",
				"blaireau", "blairotte","bourrin","comique","humour","connerie","moquer",
				"amuser", "fun", "funny", "rigoler", "éclater"]
	answers["des rires"] = [ 	"Qu'est-ce qui vous fait rire ?", 
					"Pierre Desproges disait : 'On peut rire de tout mais pas avec n'importe qui !'", 
					"Riez-vous souvent dans votre vie quotidienne ?", 
					"La plupart du temps, je ne rigole pas beaucoup. Et le reste du temps je ne rigole pas du tout.",
					"Le rire est la meilleure des thérapies !", 
					"Saviez-vous que rire muscle les abdos ?", 
					"Il est dangereux d'être sincère, à moins d'être également stupide.",
					"Contente de voir que vous vous amusez !", 
					"Pourquoi riez-vous ?"]
	quality["Parceque"] = 2
	keywords["Parceque"] = ["parce que","puisque","donc", "alors","cause","logique","logiquement","postuler",
				"si","afin","condition","contradiction","contraire",
				"démonstration","preuve","priori","raison",
				"ainsi","lien"]
	answers["Parceque"] = [ 	"Le but de cette thérapie est de trouver les faits, pas de raisonner.",
					"Est-ce la seule raison ?",
					"Peut-il vraiment y avoir un lien ?",
					"D'autres raisons vous viennent à l'esprit ?",
					"Cette raison explique-t-elle autre chose ?",
					"À quelles autres raisons peut-on penser ?",
					"Cela ne me semble pas être une implication nécessaire.",
					"Arrêtez de vous trouver des excuses.",
					"Parlez-moi plus de votre logique.",
					"Pourquoi cette contradiction ?"]
		
	quality["Oui"] = 2			
	keywords["Oui"] =    [ "ouai","oui","de accord","bien","ok","pas faux","exactement ça","est ça","j adhère","ah bon",
				"est vrai" ,"il me semble","accepter","absolument","à fond","complètement","franchement",
				"facile","intéressant", "intéresser", "intérêt","exactement","génial","genial","cool",
				"évidemment","super","vachement",
				"correctement","correct"]
	answers["Oui"] =  [   	"Mais encore ?",
				"Vous êtes sûr(/e) ?",
				"C'est très positif.",
				"Pourtant, vous ne me semblez pas tout à fait convaincu(/e).",
				"Vous acceptez facilement ce que disent les autres.",
				"La réponse est oui. Mais quelle était la question ?",
				"Bien... Bien... Bien...",
				"C'est bien d'être positi(f/ve), mais essayez d'approfondir la question !"]
				
	quality["Négation"] = 1	
	keywords["Négation"] =    ["rien","jamais","aucun","aucune","non","pas du tout","pire","ni","marre","nier",
					"ras le","contre","contrer","trop","négatif","pas terrible",
					"insupportable"]
	answers["Négation"] =  [	"Vous n'êtes pas un peu négati(f/ve) ?",
					"Think positive !",
					"Nier ne sert à rien.",
					"Tentez de réformuler ça plus positivement !",
					"Dites-vous cela seulement pour être négati(f/ve) ?",
					"Je vous sens un peu négati(f/ve).",
					"Pourquoi pas ?",
					"Pourriez-vous être plus positi(f/ve) ?"]
	quality["Négation Avoir"] = 3	
	keywords["Négation Avoir"] =    ["je ne ai","je ne avais","nous ne avons","nous ne avions"]
	answers["Négation Avoir"] =  [	"Vous avez ! Vous avez !",
					"Arrêtez de regretter de ne pas avoir !",
					"Remplacez 'avoir' par 'être' !"
					]				
						
					
					
	quality["vos erreurs"] = 6					
	keywords['vos erreurs'] = ["autant pour moi", "suis trompé", "suis trompée","désolé","erreur",
					"lapsus","excusez moi",
					"pardon","navré"]
	answers['vos erreurs'] = [	"je vous en prie !", "Ce n'est rien !", 
					"S'il-vous-plait ne vous excusez pas!",
					"Les excuses ne sont pas nécessaires.",
					"Que ressentez-vous lorsque vous vous excusez ?",
					"Ne soyez pas tellement sur la défensive !",
					"Ne nous attachons pas à ce genre de détails...",
					"Il n'y a pas de problème !"]
	quality["l'anglais"] = 4
	keywords["l'anglais"] = ["yes", "no", "hello", "good", "english", "you","no", "hallo"]
	answers["l'anglais"] = ["I don't speak english.", 
					"sori, but my inglish is bat",
					"Soyez gentil(/le), parlez français !", 
					"Vous n'aimez pas le français ?", 
					"Qu'est-ce que vous n'aimez pas dans le français ?"]
	quality["vos SMS"] = 4		
	keywords['vos SMS'] = ["lol", "stp", "mdr", "k", "cé", "kesk", ":-)", ";-)","^_^",":o)",":-p",
					"pk",
					"sms","chatter"]
	answers['vos SMS'] = [ 	"L'orthographe française m'émerveille, pas vous ?",
					"Je ne parle pas SMS.", 
					"Les jeunes, et leur langage...",
					"Ecrivez correctement s'il vous plaît. - J'ai déjà du mal à vous comprendre !"]
	quality["votre famille"] = 9					
	keywords["votre famille"] =   [	"mère","père","papa","maman","fils","enfant","enfance","bébé",
					"crèche","sucette",
					"fille","frère","soeur","sœur","famille","adoption","gène","génétique",
					"géniteur","généalogique","parents","parental",
					"accoucher","familial","femme","mari","époux","epoux","épouse","epouse",
					"bru", "gendre", "oncle", "tante", "inceste", "belle famille",
					"oedipe","eudipe","œdipe","électre","œdipien","autoritaire","autorité",
					"punir","refouler","refoulement","mâle","femelle",
					"freud","jung","psychanalyse","psychanaliste","psychanalyste","psy","psys","conscient","inconscient",
					"incestueux","inceste","surmoi", "intériorisation", "intérioriser",
					"divan","transfert",
					"enfant", "grands parents", "cousin", "cousine"]
	answers["votre famille"] =   [   "Parlez un peu plus de votre famille, s'il vous plaît.",
					"Que signifie la famille pour vous ?",
					"Verriez-vous un lien avec votre famille ?",
					"L'enfer c'est les autres. Qu'en pensez-vous ?",
					"Êtes-vous sure d'avoir résolu votre (Œdipe/Electre) ?",
					#"Inzest macht die Kinder froh und Erwachsene ebenso?",
					"La famille est un facteur important dans la vie de tous.",
					"Que pensez-vous de vos rapports familiaux ?", 
					"Que pouvez-vous dire de votre enfance ?", 
					"Pourrez-vous un jour pardonner ?", 
					"Définissez vos relations avec vos parents.", 
					"On ne choisit pas sa famille mais on vit avec, ainsi que ses défauts et ses qualités."]
			
	quality["votre vie sentimentale"] = 8
	keywords["votre vie sentimentale"] =    [	"amant","petit copain","petite copine","petit ami", "petite amie",
							"chéri","chérie","mari","ma femme","sa femme","maitresse","amoureux",
							"mon ami","ma copine", "mon copin"
							]
	answers["votre vie sentimentale"] =    [  "Quel rapport avez-vous au couple ?",
						"Quand vous êtes en couple, dans quel mesure vous sentez-vous réellement engagé(/e) ?",
						"Pensez-vous reproduire le modèle du couple parental ?",
						"En quoi votre couple diffère-t-il du couple que formaient vos parents ?",
						"Avez-vous vu vos parents dans des situations intimes ?"
						
					]
				
	quality["votre sexualité"] = 9	
	keywords['votre sexualité'] = [	 'amant', "anus","anal",'backroom', 'baisable','baiser',  'bander', 
					"bécoter",
					'bibite', 'bite', 'branler', 'branlette',  'caresse', "caresser", 
					"castration","castrer",'chatte', "cochon","frigide",
					'chaudasse', 'clitoris', 'couille', "cul", 'cunilingus', 'déflorer','doigt', 
					'domination',"débauche", 'dégorger le poireau', 'excitation',"faisable", 
					'fellation', "fesse",'fist fucking', 'fouet', 'fusion', 'fétichiste', "fétichisme",
					"forniquer",
					'gaule', "génital",'godemiché', "honte",
					"impuissance",'jouir', 'jouissance',  
					'lesbienne', 'maitresse', 'masturbation', 'minou', 'mouillé', 
					'onanisme', 'orgasme', 'partenaire', 'partouze', 'passion',"pénis",
					"perversion","pervertir","pervers",
					'pipe', "pipi",'plaisir', 'poignet', 'prostituée', 'pulsion',  'sensualité', 'sensuel',
					 'sexe', 'sexualité', 'sexuel', "sexy",'sodomie', 'soumission',
					'sperme', 'stupre', 'taquiner popaul', 'tarte aux poils',
					"tirer sur l'asticot", 'tripoter le jonc', 'trou', 'turlutte', "viagra",
					'vibromasseur', 'éjaculation','débridé',"menotte","rapport",
					'érotique',"turpitude","dérèglement","excès","libertinage","vice","dévergondage","orgie",
					"masochiste","masochisme","phallique",
					"sadique","sadiste","sadisme",
					"sein","stupre","luxure","débordement",
					"surabondance","dépravation","immoralité",
					"lasciveté","impudicité","inconduite","polissonnerie","gérontophile",
					"pédophile","zoophile","indécence","volupté","égarement","abus",
					"lubrifiant","capote","vaseline","lubricité","perversion",
					"pénétrer","prostitution","prostituer",
					"gaudriole","tripoter"]
	answers['votre sexualité'] = [	"Comment définiriez-vous votre sexualité ?", "Vous sentez vous pleinement épanoui(/e) ?", 
					"""Alfred Capus disait : " l'amour, c'est quand on obtient pas tout de suite ce qu'on désire ", qu'en pensez-vous ?""",
					"""Le sexe sans amour est une expérience vide, mais parmi les expériences vides, c'est une des meilleures.""",
					"""La différence entre le sexe et la mort, c'est que mourir, vous pouvez le faire seul, et personne ne se moquera de vous.""",
					"Le sexe apaise les tensions. L'amour les provoque.",
					"Pour vous, amour et sexualité, sont-ils des notions indépendantes ?", 
					"Reprenez confiance en vous, osez ! Vous vous sentirez mieux !", 
					"Parlez-vous de sexualité avec votre partenaire ?", 
					"Accédez-vous au plaisir facilement ?",
					"Le sexe entre deux personnes, c'est  beau. Entre cinq personnes, c'est fantastique...",
					"Hé ! Il ne faut se moquer de la masturbation ! C'est faire l'amour avec quelqu'un qu'on aime...",
					"La conscience est la conséquence du renoncement aux pulsions.",
					"Essayez d'en parler à vos amis, vous verrez que vous n'êtes pas seul(/e).", 
					"N'ayez pas honte de vos sentiments, parlez plus librement.",
					"Je vous conseille d'aller voir de temps en temps 'Sex and the City' !"]
	
	quality["votre mariage"] = 7			
	keywords['votre mariage'] = ["marier","fiancée","fiancer","mariage", "engagement", "engager", "chéri", "chérie",
					"couple", "conjungo", "alliance", "association", "union",
					"hymen", "hyménée",   "cortège", "sacrement",  "noce", 
					"union légitime", "épousaille", "conjugal"]
	answers['votre mariage'] = ["Revenez me voir avec votre partenaire !!!", 
						"L'amour est une sorte de butoir contre la solitude.",
						"Mes parents avaient vécu quarante ans ensemble, mais par pure animosité.",
						"Je suis aussi une thérapeute conjugale !!!", 
						"La vie à deux est plus précieuse."]
	quality["votre adolescence"] = 4				
	keywords['votre adolescence'] = ["adolescent", "adolescents", "adolescente", "adolescentes", 
					"rebelle", "rébellion",   "rebellion",  "fuguer", "jeunesse",
					
					"acné", "boutons", "bouton",  "scooter", "scooters", "boite de nuit" ,
					"boîte de nuit"]
	answers['votre adolescence'] = [ 	"Les adolescents sont insupportables !", 
					"Tout ira mieux après 20 ans.", 
					"Ce n'est qu'une mauvaise période.", 
					"Parlez-moi plus de votre jeunesse.",
					"Vous ne pensez pas que ça va passer ?", 
					"Ca doit être dur à vivre !"]
		
	quality["vos amis"] = 7				
	keywords["vos amis"] =   [	"ami","amis","amitié","copain","copains","copine","copines","pote","rencontrer",
					"consoler","ensemble"
					]
	answers["vos amis"] =  [   	"Il peut être important de s'étaler un peu plus au sujet de vos amis.",
					"L'amitié signifie quoi pour vous ?",
					"Est-ce que vos amis se font du souci pour vous ?",
					"Est-ce que vos amis s'en prennent à vous ?",
					"Etes-vous certain(/e) d'avoir des amis?",
					"Est-ce que vous vous imposez à vos amis?",
					"Peut-être que l'amour que vous portes à vos amis vous préoccupe.",
					"Oui, personne ne peut vivre sans amis.",
					"Celui qui n'est plus ton ami ne l'a jamais été.",
					"Si tous les hommes savaient ce qu'ils disent les uns les autres, il n'y aurait pas quatre amis dans le monde."]
					

	quality["la joie"] = 5			
	keywords['la joie'] = ["bonheur", "plaisir", "gaieté", "félicité", "satisfaction", "allégresse", "bien être",
				"bénéfique","sympa","sympathique","positif","ça gaze","heureux","kif","kiffer",
				"euphorie", "enthousiasme", "contentement", "ravissement", "entrain", "délice", "extase", 
				"volupté", "transport", "ivresse", "réjouissance", "béatitude", "exaltation", "jouissance", 
				"émerveiller", "épanoui", "épanouir","épanouissement","convivial",
				"amusement", "jubilation", "agrément", "enjouement", "enchantement", "douceur", "exultation", 
				"rigolade", "hilarité", "griserie", "bienfait", "liesse", "régal", "ardeur", "avantage", 
				"consolation", "sourire", "rayonnement", "rayonner", "folichonnerie", "fierté", "aise", 
				"beau","fasciner","impressionner","plaire", 
				"célébration","encourager","encourageant"]
	answers['la joie'] = [  "La vie est plus longue quand on est heureux.",
				"La vie est meilleure quand on la kiffe",
				"Il existe une euphorie du mal.",
				"La mélancolie, c'est le bonheur d'être triste.",
				"Le bonheur est vide, le malheur est plein.",
				"Il faut créer le bonheur pour protester contre l'univers du malheur.",
				"Soyez toujours optimiste comme les mots que vous utilisez."]
	quality["vos problèmes"] = 4							
	keywords["vos problèmes"] =    ["malaise","malheureux","problème","malheur","mal","noir","dérouter","déroute",
					"malheureuse","pas heureux","mélancolie","mélancolique","déprime","déprimer","fuir","seul",
					"solitude","triste","tristesse","narcissisme","narcissique",
					"ego","égo","amnésique","amnésie","crise","naze","nase",
					"pleurer","chialer","pleurnicher","larme",
					"dépression","dépressif","dépressive","las","lasse","lassé","lassée", "navrant",
					"pessimiste","pessimisme","no future","pas évident","foutu","foutue",
					"angoissé","angoisse","dément","débile","grand chose",
					"difficile","divorce","enterrement","enfer","démon","séparation","psy",
					"psychologue","psychanalyste",
					"psychiatre","psychologique","à côté de la plaque","neurologue","neurologie","sentiment",
					"sens pas bien","vraiment pas bien",
					"sens mal", "vais mal", "vais pas bien", "suis mal ",
					"irm", "imagerie par résonnance magnétique","courage","déplorable","à côté de ses pompes",
					"rater","confiance","confiant","conseiller","conseil",
					"affronter","consternation",
					"difficulté","catastrophe","mourir","mort","suicider","suicide", "bête",
					"morbide","à la masse","à côté de la plaque"]
	answers["vos problèmes"] = [   	"Reprennez-vous, vous êtes trop négati(f/ve).", 
					"Courage, la thérapie est justement là pour aider à reprendre confiance en vous.", 
					"Vous semblez perdre pied.",
					"Comment cela se manifeste ?",
					"Qu'est-ce que cette douleur vous suggère ?",
					"La vie ne vaut rien, mais rien ne vaut la vie.",
					"Les ennuis, c'est comme le papier hygiénique, on en tire un, il en vient dix.",
					"Non seulement la vie est horrible, mais en plus elle est courte.",
					"Est-il possible que vous ayez besoin de plus de confiance en vous ?",
					"Parler vous redonnera confiance en vous.",
					"Le bonheur est dans le pré.", 
					"Secouez-vous !",
					"Vous semblez vraiment mal. Mais ne vous inquiétez pas ; je suis là.",
					"La vie se divise en deux catégories : l'horreur et le malheur.",
					"Ne soyez pas triste, la vie est belle.", 
					"Si rien ne va, allez voir un éthologue !", 
					"Pas de panique ! Elizia s'occupe de tout !", 
					"Rien ne vaut le chocolat pour remonter le moral !", 
					"Rire prolonge la vie pensez-y...", 
					"La vie est courte profitez-en !", 
					"Respirez !! Ça calme...", 
					"Comment vous sentez-vous ?", 
					"A malheur bonheur est bon.", 
					"Prenez la vie par le bon bout et ça ira mieux !",
					"Rien n'est plus drôle que le malheur... c'est la chose la plus comique du monde."]
	quality["la trahison"] = 9			
	keywords['la trahison'] = ["trahison", "trahisons", "trahir",  "traitre", "traitresse",  "tromper", 
					"tromperie",  "dupe", "duper", "dupes", "dupé",  "annuler","fidélité","fidel",
					"couillé", "couillés", "couillée", "couillées", "couiller", "infidèle",
					"jaloux", "mentir","mensonge","mensonger",
					"déception","décevoir",
					"infidélité", "perfidie", "perfide", "perfides", "fourberie", "fourbe", 
					"déloyauté", "déloyal",  "déloyale",  "hypocrisie", "hypocrite", "félonie", "félon", 
					"adultère", "délaissement", "délaissé", "avouer","confier","excuse","excuser",
					"inconstance", "bassesse", "dénonciation", "parjure", "délation", "duperie", "concussion", "cocuage", "cocu","cocufier","cocufiage"]
	answers['la trahison'] = [ 	"Il faut savoir pardonner.", 
					"Cela vous fait-il mal d'en parler ?", 
					"C'est une situation délicate à laquelle il faut remédier.", 
					"Vous sentez vous trahi(/e) ?", 
					"Que ressentez vous après ce coup dur ?", 
					"La trahison est le propre de l'homme, personne n'est parfait.", 
					"Pourriez-vous refaire confiance ?", 
					"La fidélité se fait rare de nos jours !", 
					"Dans toute relation, la loyauté est primordiale.", 
					"Votre mère a-t-elle parfoid trompé votre père ?",
					"Ce sentiment vous hante-t-il ?"]
	quality["vos dépendances"] = 9			
	keywords["vos dépendances"] =   [	"fumer","cigarette","clope","splif","spliff","oinj","joint","joints","bédos",
						 "zeb","shit","cocaïne","coke","héroine","lsd","ecstasy","dope",
						 "poudre","rail","crack","drogue","droguer","accro","toxico",
						 "dépendant",
						 "dépendance","marley"]
	answers["vos dépendances"] =  [   	
						"La dernière fois, ça remonte à quand ?",
						"Faites-le vous seul ou avec des amis ?",
						"Mais pourquoi recourir à des paradis artificiels ?",
						"Pourquoi refusez-vous d'affronter la réalité ?",
						"Mais comme l'a dit Bob Marley : 'You're running away, but you can't run away from yourself'!"]
						
	quality["la musique"] = 9					
	keywords["la musique"] =   [	"musique","piano","chant","chanson","chanter","instrument","violon","partition","métronome",
				"solfège","musicien","pianiste","guitariste","guitare","opéra","concert","mozart",
				 "poudre","rail","crack","drogue","droguer","accro","toxico",
				 "chopin", "rythme"]					
						

	answers["la musique"] =  [   	  "Je ne peux pas écouter trop de Wagner. Ça me donne cette envie de conquérir la Pologne...",
				  "La musique adoucie les mœurs.","La musique est l'aliment de l'amour.",
				  "La musique est une révélation plus haute que toute sagesse et toute philosophie.",
				  "Sans la musique, la vie serait une erreur.",
				  "Aimer la musique, c'est se garantir un quart de son bonheur.",
				  "Toute musique qui ne peint rien n'est que du bruit.",
				  "La vraie musique suggère des idées analogues dans des cerveaux différents.",
				  "La musique commence là où s'arrête le pouvoir des mots.",
				  "La musique. C'est un cadeau de la vie. Ça existe pour consoler. Pour récompenser. Ça aide à vivre.",
				  "La musique vaut toutes les philosophies du monde.",
				  "La musique mérite d'être la seconde langue obligatoire de toutes les écoles du monde.",
				  "La musique est le seul plaisir sensuel sans vice.",
				  "Là où s'arrête le pouvoir des mots commence la musique.",
				  "La musique met l'âme en harmonie avec tout ce qui existe.",
				  "La musique suffit pour une existence mais un existence ne suffit pas à la musique.",
				  "La musique donne une âme à nos coeurs et des ailes à la pensée.",
				  "Le vase donne une forme au vide, et la musique au silence.",
				  "La musique n'est pas une question de style mais de sincérité." ]
					






						
	quality["vos maladies"] = 8
	keywords['vos maladies'] = [ 	"incontinence","malade", "maladie",  "maladif", "maladifs", "maladive","cabinet","hypocondriaque",
					"grippe", "angine", "toux", "vomir", "repos", "reposer","consultation","consulter",
					"tousser", "toussez", "tousse", "tousses", "dégueuler", "dégueulé", "dégueule",  "fièvre", "fièvreux", 
					"fiévreux", "pansement","bandage", "thérapie","hémoroïdes","hémorroïdes","dentiste",
					"soins", "soigner",  "piqûre", "piqûres", "piqure", "piqures", "antibiotique", "antibiotiques",	"médecin","médicament", "médicaments", "médicinal",
					 "suis pas bien", "trouble", 
					"affection", "fait mal", "ai mal", 
					"atteinte", "altération", "indisposition", "tare", "rage", "souffrance", "marotte", "crise", "épreuve", "chancre", "lèpre", 
					"infirmité", "troubles", "trouble", "mal être", "traumatisme", "tic", "syndrome", "rechute", "plaie", "peste",  "médecine",   "infirmière", "infirmier", 
					"docteur","sécu","sécurité sociale", "docteurs","infecter","guérir","soigner","pillule","pilule"]
	answers['vos maladies'] = ["Essayez de ne pas négliger votre santé !", 
					"Votre santé est-elle une priorité dans votre vie ?", 
					"Peut être devriez-vous voir un médecin ?", 
					"Vous vous sentez bien, maintenant ?",
					"Si cette thérapie ne marche pas, vous pouvez toujours essayer Lourdes...",
					"Il faut absolument prendre soin de vous.", 
					"Le travail, c'est la santé !", 
					"Le système de santé français est malheureusement complexe...", 
					"La santé, c'est primordial."]
							
							
	quality["votre avenir"] = 4						
	keywords["votre avenir"] =    [	"projet","réussir","réussite","projets",
					"avenir","futur","concrétiser","entamer","commencer",
					"destiné","destin",					"concrétisé","espoir","réalisation","construire","construction",
					"créer","création",
					"développer","développement",
					"essayer","interrogation","but","curieux","envisager"]
	answers["votre avenir"] =        [   	"C'est encourageant, vous construisez des projets !",
						"Comment vous projetez-vous dans l'avenir ?", 
						"Comment construisez-vous votre futur ?",
						"Paul Cioran a dit qu'on se suicide toujours trop tard. Qu'en pensez-vous ?",
						"Comment vous imaginez-vous dans quelques années ?",
						"Avez-vous foi en votre avenir ?", 
						"Êtes-vous confiant(/e) quant à votre avenir ?"]      
	quality["vos craintes"] = 6					
	keywords["vos craintes"] =   [ 	"crainte","craindre", "hésite", "demander","demande",
					"hésitation","incertain","dubitatif","peut être","doute","douter","hésiter","hésitation"]
	answers["vos craintes"] =   [   "Mais d'où vient votre incertitude?",
					"Il faut que vous ayez plus confiance en vous !",
					"Vous ne semblez pas vraiment convaincu(/e).",
					"Pourquoi ce ton hésitant?",
					"Soyez rassuré(/e), je suis là pour vous écouter.",
					"La confiance en soi vous mènera vers la guérison.",
					"Commencez par vous faire confiance."]
	quality["vos obligations"] = 6					
	keywords["vos obligations"] =   [ 	"devoir","falloir", "nécessaire", "nécessité",
				        "obliger","obligatoire","engagement","exigence","impératif",
					"obligation","contraint","contraindre","contrainte"]
	answers["vos obligations"] =   [   "Réfléchissez : vous êtes sûr(/e) de ne pas avoir des choix ?",
					"Vouloir est pouvoir.",
					"Il n'y a pas que'un seul chemin possible. C'est à vous de choisir.",
					'Oubliez le verbe "devoir" et remplacez-le avec "vouloir".']
					
				
	

	
	
	quality["vos envies"] = 6								
	keywords["vos envies"] =   [ 	"envie","désir","envies","souhaiter","souhait","vouloir","volonté","aimer",
					"amour","questionner","fou de","folle de","détester","haïr",
					"besoin","espérer","refuser","envier",
					"préférer","préférence","désirer"]
	answers["vos envies"] =        ["Mais de quoi avez-vous réellement envie ?",
					"En avez-vous réellement envie ?",
					"Avez-vous essayé ?",
					"Pouvez-vous nommer d'autres désirs ?",
					"Le bonheur n'est pas avoir ce qu'on souhaite, mais souhaiter ce qu'on a.",
					"Mieux vaut réaliser son souhait que souhaiter l'avoir fait.",
					"Il y a deux tragédies dans la vie. L'une est de ne pas obtenir ce que l'on désire ardemment, et l'autre de l'obtenir.",
					"Nous ne sommes jamais aussi mal protégés contre la souffrance que lorsque nous aimons.",
					"Êtes-vous sûr(/e) que vos souhaits correspondent à vos besoins ?"]
	quality["vos peurs"] = 6			
	keywords["vos peurs"] =   [ 	"peur","cauchemar","crainte","craintes","effrayé","persécution","psychose","effrayer",
					"névrose","panique","vertige","paranoiaque","paranoïaque","paranoïa","aliénation","folie",
					"obsession","obsédé","délire","démence","manie","spectre","hantise","hallucination","mélancolie",
					"confusion mentale","ramollissement cérébral","schizophrénie","schizophrène",
					"suicider","suicide", "manquer","manque",
					"enfermement","enfermer",
					"trouillard","anxiété","phobie"]
	answers["vos peurs"] =        [ "Êtes-vous sujet à des peurs liées au vide ou à l'enfermement ?",
					"De quoi avez-vous vraiment peur ?",
					"L'origine des névroses est à chercher dans des traumatismes apparus durant l'enfance.",
					"Qu'est-ce qui vous effraie ?"]
	quality["vos rêves"] = 8					
	keywords["vos rêves"] =   [ 	"imaginer","imagination","rêve","rêver","image","fantasme","fantasmatique"]
	answers["vos rêves"] =        [ "S'agit-il plutot de désir ou d'interdit lié à votre journée précédente ?",
					"A votre avis, en quoi ce rêve est-il révélateur de votre situation actuelle ?",
					"Comment pouvez-vous m'expliquer le sens de ces images ?",
					"Qu'est-ce que ce rêve vous suggère ?",
					"Rêvez-vous souvent?",
					"Qui apparaît dans vos rêves ?",
					"Etes-vous troublé(/e) par vos rêves ?",
					"Le rêve est le gardien du sommeil.",
					"Quelles interprétations pouvez-vous en faire ?"]
	quality["la religion"] = 5				
	keywords["la religion"] =    [ 	"religion","dieu","déesse","crois","ange","prière","prie","moine","paradis",
					"église","prêtre","croyances","croyance","ésotérique","ésotérisme","gourou",
					"prier","croire",
					"astrologie","étoile","islam"]
	answers["la religion"] =        [   	"Que pensez-vous de la phrase 'La religion est l'opium du peuple' ?",
					    "Comment croire en dieu, si la semaine dernière seulement, ma langue s'est coincée dans le rouleau d'une machine à écrire électrique ?",
						"Croire est ne pas savoir.",
						"Si seulement dieu me faisait un signe clair ! Comme un virement sur un compte suisse à mon nom  !",
						"Si Dieu existe, j'espère qu'il a une bonne excuse.",
						"L'éternité, c'est long, surtout vers la fin.",
						"Nous sommes lents à croire ce qui fait mal à croire.",
						"Sans votre religion, vous sentiriez-vous plus libre ?",
						"Pourquoi parlez-vous de vos croyances ?",
						"Malraux a dit que le 21e siècle sera réligieux ou ne sera pas. Qu'en pensez-vous ?"] 
						
	quality["votre métier"] = 7				
	keywords["votre métier"] =    [ "travail","travailler","métier",
					"instituteur","institutrice","boulanger","boucher","charcutier",
					"chauffeur","barman","commerçant","ingénieur","vendeur",
					"chirurgien","avocat","libraire","secrétaire",
					'avancer',"collègue"]
	answers["votre métier"] =    [ 	"Avez-vous toujours voulu faire cette profession?",
					"Vous vous entendez bien avec vos collègues?",
					"Vous vous sentez bien sur votre lieu de travail?",
					"La peur de l'ennui est la seule excuse du travail."]
										
	
	quality["l'étude"] = 7
	keywords["l'étude"] =   [ 	"étude","étudier","université","fac","faculté",
					"profession","éducation","école",
					"prof","professeur","enseignement","capes","agrégation",
					"professionnel","professionnelle","examen","formation","intellectuel",
					"incompétent","apprendre","approfondir","thèse","note","cnrs","chercheur",
					"partiel","classe","cours","camarade","exam", "exams"]
					
	answers["l'étude"] =     [ "Mais quel métier voudriez-vous faire ?",
					"Vos buts professionnels sont-ils réalistes ?",
					"Construisez-vous un projet à travers votre formation ?",
					"Vous sentez-vous bien dans vos études ?",
					"Rien de ce qu'il est bon de savoir ne peut être compris avec l'esprit.",
					"Avez-vous de bonnes méthodes de travail ?",
					"Votre manque d'éducation semble être compensée par une faillite morale la plus totale.",
					"Essayez-vous de vous intégrer ?",
					"""Sénèque a dit "Etudie, non pour savoir plus, mais pour savoir mieux." Qu'en pensez-vous?""",
					'Montesquieu dirait: "Il faut avoir beaucoup étudié pour savoir peu."',
					"Vos études vous correspondent-elles ?"]
	quality["l'informatique"] = 7			
	keywords["l'informatique"] = [ 	"ordinateur", "ordi","pc", "disque dur", "disques durs", "disque externe", 
					"disques externes", "disque interne", "disques internes", "programmation",
					"programme",
					"clavier", "écran", "logiciel", "internet", "web", "net","machine",
					"informatique","informaticien","robot","robotique",
					"artificielle","ia","linux","windows","apple","mac",
					"surfer", "ram", "rom", "carte graphique", "cartes graphiques"]
	answers["l'informatique"] = [ 	"Avez-vous réellement besoin d'un ordinateur ?", 
					"Qu'est-ce que vous aimez dans l'informatique ?", 
					"Personnellement, je collectionne les souris.", 
					"Pourriez-vous aimer un informaticien ?",
					"Avez-vous peur des ordinateurs ?",
					"L'intelligence artificielle se définit comme le contraire de la bêtise naturelle.",
					"Et si je n'étais pas comme vous, en chair et en os, ça vous mettrait mal à l'aise ?",
					"Peut-être avez-vous peur des machines ?",
					"Peut-être pourriez-vous voir un informaticien ?"]
	quality["jeux vidéos"] = 7					
	keywords['jeux vidéos'] = ["consoles", "console", "jeux vidéo", "jeu vidéo", "xbox", 
					"x box", "xbox", "nintendo", "ds", "sega", "sony", "wii", "playstation", 
						"geek", "geeks", "nerd", "nerds", "counter", "atari", "master system", "dreamcast",]
	answers['jeux vidéos'] = [ 	"Moi aussi, j'aimais les jeux dans ma jeunesse !", 
					"J'ai eu une mégadrive autrefois !", 
					"Pensez-vous que c'est un problème ?", 
					"Ah ! Les miracles de la technologie !", 
					"Quelle est votre console préférée ?", 
					"Quel est votre jeu préféré ?", 
					"Quel jeu avez vous acheté récemment ?", 
					"Êtes vous accro aux jeux vidéos ?", 
					"Il n'y a pas d'âge pour s'amuser !"]
						
						
	quality["cinéma"] = 7				
	keywords["cinéma"] =    [ 	"cinéma","film","films","acteur","actrice","acteurs","actrices","cannes"]
	answers["cinéma"] = [   	"Vous allez souvent au cinéma ?",
					"Est-ce que vous aimez les films de gladiateurs ?",
					"Est-ce que vous aimez les films d'aventure ?",
					"Que pensez-vous des films de cul ?",
					"Que pensez-vous des films d'amour ?" ,
					"Hollywood ? C'est une usine où l'on fabrique dix-sept films sur une idée qui ne vaut même pas un court métrage.",
					"Avez-vous un héro avec lequel vous aimez vous identifier ?",
					"Quel genre de film représente le mieux vos difficultés actuelles ?"]
	quality["la télévision"] = 7			
	keywords['la télévision'] = ["télé", "télévisé", "télévisés","télévisée","télévisées"]
	answers['la télévision'] = [ 	"La télé , on y perd son temps !", "Il faut se méfier de la télé!!",
					"La vie n'imite pas l'art, elle imite la mauvaise télévision.",
					"Il y'a des choses plus intéressantes dans la vie."]
	quality["vos activités sportives"] = 7
	keywords['vos activités sportives'] = ["sport", "sports", "sportif", "sportifs", "sportive", "sportives", "foot", 
				"football", "hand", "handball", "basket", "basketball", "ski", "skier", 
				 "courir", "jogging", "tennis", "ping pong", "courbature", "courbaturé", 
				 "baseball", "base ball",  "ballon", "balle",  "badminton", "raquette", 
				 "botter en touche","bottage en touche",
				 "muscle",  "musclé",  "muscler","abdo","abdos","abdominaux"]
	answers['vos activités sportives'] = [ 	"Pratiquez vous un sport en particulier ?", 
						"Aimez vous le sport ?", 
						"Je ne suis moi-même pas très sportive.", 
						"Le sport pourrait sans doute vous soulager.", 
						"Même les sportifs peuvent déprimer !", 
						"Le sport peut faire partie d'une thérapie.", 
						"Quel intérêt trouvez-vous dans le sport ?", 
						"Avez vous fait du sport dans votre enfance ?", 
						"Vos parents étaient-ils sportifs ?", 
						"""Comme dit le proverbe : "un esprit sain dans un corps sain !" """]
	quality["votre relation avec l'animal"] = 7		
	keywords["votre relation avec l'animal"] =    ["zoo","éléphant","poule","singe","cheval","chat","chien","oiseau","vache","héron",
					"pigeon","félin","chèvre","ver","moustique","insecte","animal","fourrure","léopard","lion",
					"panthère","poisson","grenouille","panda","koala","prince charmant","environnement",
					"queue","pitbull", "pittbul","doudou","dragon",
					"ferme","mouche","animalier",
					"campagne","pie","museau","groin","mufle"]
	answers["votre relation avec l'animal"] =[   	"Avez-vous peur d'un animal?",
							"Quel animal vous incarne le mieux?",
							"Vous aimez les animaux ?",
							"Que vous apportent les animaux?", 
							"Que pensez-vous de votre relation au monde animalier ?",
							"Les psychologues pour animaux ont beaucoup de succès. Que diriez-vous d'aller consulter ?",
							"La ferme est un lieu convivial allez-y cela vous fera du bien.",
							"En quel animal aimeriez-vous vous réincarner?",
							"Quel est votre animal préféré?",
							"Posséder un animal vous apaisera.",
							"Avez vous déjà envisagez de prendre un animal de compagnie ?"]
	quality["vous et les poils"] = 7				
	keywords['vous et les poils'] = ["araignée", "bestiole","raser",
					 "vertébrés", "poil", "poilus", "poilu", 
					 "veuve noire", "veuves noires", "miguale", "tarentule"]
	answers['vous et les poils'] = ["Qu'est ce qui vous répulse chez les araignées ?", 
					"Parlez-vous d'une experience qui a mal tournée ?", 
					"Pouvez-vous me décrire les araignées que vous détestez le plus ?", 
					"Il faut apprendre a surmonter cette peur.",
					"Essayez de demander l'avis d'un vétérinaire."]
	quality["la nausée"] = 7			 
	keywords['la nausée'] = ["nausée", "dégueulasse","affadissement","dégoût","dégoûtation","vomitif","diarrhée",
					"débecqueter","dégoûter","écœurer","écoeurer","écoeuré","dégeuli","chiasse","colique","colonoscopie",
					"roter","péter","peter","pete", "puer","puant", "baver", "glaire", "mucosité", "mucus", "muqueux",
					"écœurant","écoeurant","vivisection","morve","ordure"]
	answers['la nausée'] = ["Vous préférez dégoûter ou être dégouté ?", 
					"Le dégoût est une chose curieuse.", 
					"le dégoût et la volupté se rejoignent et s'annulent.", 
					"J'ai envie de vomir."]
	quality["vos couleurs"] = 5			
	keywords['vos couleurs'] = ["jaune", "rouge", "bleu","bleue","noir", "blanc", "vert",
				"violet", "orange", "marron", "couleur", "brun"]
	answers['vos couleurs'] = ["Oui, moi aussi, j'aime bien les couleurs.", "La vie est plus belle avec cette couleur."]
	
	quality["mon nez"] = 9
	keywords["mon nez"] = ["nez","blair","tarin","truffe"]
	answers["mon nez"] = ["Mon nez !", "Je ne trouve pas de cache-nez à ma taille !",
						"C'est bien de se trouver nez à nez, ne vous trouvez pas ?", 
						"Vous ne m'auriez pas dans le nez par hasard ?",
						"Ne nous bouffons pas le nez et parlons plus de vos problèmes !",
						"Mon travail est de fourrer mon nez partout. Même dans vos problèmes !"]
						
	quality["l'anatomie"] = 5
	keywords["l'anatomie"] = ["tête", "oeil", "yeux", "nez", "oreille", "oreilles", "main","dent","anatomie",
						"corps","coeur","cœur","cheveu",
						"gorge",  "estomac", "jambe", "pied"]
	answers["l'anatomie"] = ["Vous devriez consulter un médecin, je suis seulement psychanalyste.", 
						"A la fin de la consultation je vais vous donner le numéro d'un spécialiste.", 
						"Ne seriez-vous pas un peu hypocondriaque par hasard ?"]					
	quality["votre alimentation"] = 7
	keywords["votre alimentation"] =    [ "faim","sandwich","ventre","soif","déjeuner","diner","dîner","pomme","poire",
				"poulet","steak","fromage","pain","croissant","baguette","nutella","sausissson","yaourt",
				"confiture","poireau","salade","régime","gras","graisse","huile","thé","café",
				"cuisiner","cuisine","épicé","chocolat","choucroute","bouillir",
				"croquer","grossir","nutritionniste","nourriture","haribo","suis gros","suis grosse",
				"trop gros", "trop grosse",
				"café","banane","cookies","brownies","chips","coca cola","mc donald","hamburger",
				"quick","kfc","biscuits","biscuit","aliments","aliment","frite","frites","coco",
				"bonbon","manger","boire","bouffer","bouffe","pâte","framboise","fraise","myrtille"	]
	answers["votre alimentation"] =     [ "Avez-vous faim ?",
				"Avez-vous bien mangé avant de venir en consultation ?",
				"Haribo, c’est beau la vie pour les grands et les petits !",
				"Les régimes peuvent vous rendre malheureux.",
				"Avez-vous déjà pensé qu'il pourrait s'agir d'un problème de nourriture ?",
				"Quel est votre répas favori ?",
				"Avez vous cuisiné hier soir ?",
				"Dis-moi ce que vous mangez, je vous dirais qui vous êtes.",
				"Il faut que vous mangiez plus équilibré.",
				"Avez-vous déjà pensé à consulter un nutritionniste ?",
				"Mangez moins et dites m'en plus à votre sujet !"]
	quality["vos vêtements"] = 5					
	keywords["vos vêtements"] =    [ "fringue","pantalon","chemise","chaussette","cuissarde","soutient-gorge","soutif",
					"bouton","tissu","chaussure","chapeau","béret","beret","gants","string",
					"mitène","écharpe","tunique","toge","santiague","botte","tailleur",
					"nike","adidas","puma",
					"sandalette","bottine","basket","polo"]
	answers["vos vêtements"] =    [ "Avez vous pensé à un relooking ?",
					"Il faut changer d'avis, comme de chemise.",
					"Avez vous la fièvre acheteuse ?",
					"Allez faire les boutiques, ça vous fera du bien !"]
	quality["vos dépenses"] = 5	
	keywords["vos dépenses"] =   [ 	"cher","chère","prix","augmentation","argent","des sous","avare","crédit","découvert",
					"de sous","riche","pauvre","riches","soldes","réduction","discount","lidl","franprix",
					"casino","carrefour","auchan","monoprix","payer","rentière","rentier","entretenir",
					"acheter","acheteuse","acheteur","consommer","dépenser","épargner","investir",
					"coûter","cher","bon marché","approprier","boutique","fric","bourgeois",
					"facture","facturer",
					"luxe","cheap","made in"]
	answers["vos dépenses"] =[ 	"Vous avez bien investi votre argent dans une thérapie !",
					"A quoi sert l'argent s'il faut travailler pour en avoir ?",
					"L'argent est préférable à la pauvreté, ne serait-ce que pour des raisons financières.",
					"Oui, la vie coûte cher !","Êtes-vous avare ?",
					"Quelle personne vous est la plus chère ?"]		
										
	quality["vos vacances"] = 6
	keywords["vos vacances"] =    [	"plage","mer","plages","ski","vacance","farniente","fatigue","fatigué",
					"voyage","voyager","congé","soleil","détente","aventure","aventurer",
					"surf","plongée","plonger","bateau","palmiers","palmier","cocotier",
					"montagnes","montagne","campagne","apaiser","calme","découverte","découvrir",
					"piscine"]
	answers["vos vacances"] =    [  "Pensez-vous à prendre un peu de vacances?",
					"Où comptez-vous partir?",
					"Vous avez le teint pâle, vous avez besoin d'un bon bol d'air.",
					"Allez voir votre patron et prenez quelques jours de congé !",
					"On voyage pour changer, non de lieu, mais d'idées."]
			
	quality["racisme"] = 5
	keywords['racisme'] = ["nègre", "négresse","bamboula","racisme", "race", "rebeu", "discrimination", "bougnoule","raton","ratonade",
						"facho","fachiste","fachisme","kkk", "hitler","sous-homme","art dégénéré","niakoué",
						"métèque","machuré","intolérant","intolérance"]
	answers['racisme'] = ["L'intelligence a des limites que la connerie ne connaît pas !",
						"C'est consternant", "C'est déplorable.", "Aimez-vous les Négresses vertes ?",
						"Cela révèle une étroitesse d'esprit ! Qu'en pensez-vous ?",
						"Pourquoi abordez-vous ce sujet ?",
						"Vous y pensez souvent ?",
						"Comment vous positionnez-vous par rapport de ces propos ?"]
	quality["jardinage"] = 6					
	keywords['jardinage'] = ["arbre","feuille","semer", "fleur","graine","planter", "terre", "arroser", "aroser", "feuille", "racine",
						"pot de fleur","poussé","creuser",
						"jardin","verger","jardin","parc","plantation",
						"rose","tulipe","bonsaï","bonsai","chrysanthème",
						"potager","pépinière","courtil","closerie","nature","paysage",
						"ouche","ménagerie","marais","jardinet","hortillonnage","fruitier","espace vert","éden"]
	answers['jardinage'] = ["Semer est semer l'espoir.",
						"C'est bien d'aimer la nature.", "L'écologie est à la mode !", "Nous n'avons qu'une seule planète.",
						"Vous aimez donc la vie ?","La vie est une fleur.",
						"Avez-vous arosé vos plantes ?"]
	quality["linguistique"] = 7				
	keywords['linguistique'] = [ 	"linguistique","linguiste","langue", "syntaxe","sémantique","syntaxique",
					"morphologie","topologie","euphémisme",
					"syllabe","énoncer","énonciation","français","orthographe",
					"phonologie", "phonétique","parole","esprit",
					"chomsky","saussure","tesnière","accent","argot","articulation","articuler",
					"babiller", "bafouiller", "balbutier", "baragouiner",  "bégayer", "bredouiller", "chevroter",
					"communiquer", "confabuler",  "dialecte",  "diction",  "discourir",  "énoncer", 
					"giberner", "haranguer", "idiome",   "jargon", "jargonner", "jaser", "jaspiner", 
					"langage", "nasiller", "parole", "patois", "pérorer", "phonation", "prononcer", 
					"prononciation", "rabâcher", "communiquer",  "soliloquer", "style",
					"flexion","verbe","adjectif","nominal","phrase","mot",
					"turing","wittgenstein","sprechen"]
	answers['linguistique'] = [ 	"Vous semblez vous intéresser à la linguistique.",
					"Celui qui ne connaît pas les langues étrangères ne sait rien de sa propre langue.", 
					"La langue ment à la parole et la parole à la pensée."
						]
	quality["notre communication"] = 4					
	keywords['notre communication'] = [ 	"parler","communication","conversation", "souler","soulez","soûler","question",
				        "interroger","répondre",
						"discuter","vouvoiement","tutoiement","réponse","répondre","avertissement","avertir",
						"aborder","taciturne","interlocutrice","interlocuteur","bavarder","dire",
						"raconter","expliquer","expliciter","explicite","idée","insulter","insulte",
						"insister",
						"converser", "débattre", "débat","déclamer","déclamation",
						"dialoguer","dialogue","discuter","discussion",
						"comprendre","compréhension","avis"]
	answers['notre communication'] = ["On parle toujours mal quand on a rien à dire.",
			#"La nature nous a donné deux oreilles et seulement une langue afin de pouvoir écouter davantage et parler moins. ",
			"Que cherchez-vous vraiment quand vous me parlez ?",
			"Souffrez-vous des troubles communicatifs ?",
			"Worüber man nicht sprechen kann, darüber muss man schweigen.", 
			"La seule manière de parler de rien est d'en parler comme si c'était quelque chose.", 
			"Il ne suffit pas de parler, il faut parler juste."
						]
	quality["temps"] = 4			
	keywords['temps'] = ["temps","seconde","minute","heure", "jour","nuit","minuit", "midi", "semaine", "mois", 
						"demain","hier","aujourd'hui","an","éternité","décennie","toujours",
						"pas encore","souvenir","quand",
						"janvier","février","mars","avril","juin","juillet", "août", "septembre",
						"octobre","novembre","décembre",
						"lundi","mardi","mercredi", "jeudi", "vendredi", "samedi", "dimanche",
						"année","anniversaire","printemps","été","automne","hiver","durée","durer","âge","vieux",
						"jeune","veillard","vieillard","vie","mémoire","alzeimer","alzheimer","tasse à bec",
						"actuel",'attendre']
	answers['temps'] = [		"Le temps passe trop vite.",
					"La sagesse s'accroît avec l'âge.", 
					"Il y a des gens qui se contentent de tuer le temps en attendant que le temps les tue.", 
					"Le temps révèle tout.",
					"Qui a dit 'Il n'est rien de plus précieux que le temps, puisque c'est le prix de l'éternité.' ?",
					"Ah! jeunesse !",
					"Quand ?",
					"Pour vivre centenaire, il faudrait abandonner toutes les choses qui donnent envie de vivre centenaire.",
					"Penser contre son temps, c'est de l'héroïsme. Mais le dire, c'est de la folie.",
					"""Dans cent ans qu'aimeriez-vous que l'on dise de vous ? - J'aimerais que l'on dise : "elle se porte bien pour son âge !" """]		
	quality["les nombres"] = 3								
	keywords['les nombres'] = ["NUMBER","arithmétique","compter","comptage","deux","trois","quatre","numéro","premier"]
	answers['les nombres'] = [	"La numérologie vous intéresse ?",
					"Les mathématiques ont-elles un sens pour vous ?", 
					"Avez-vous eu des problèmes avec l'arithmétique à l'école ?", 
					"On ne peut pas tout compter !"]	
										
	# réagir à d'autres mots clés
	#"mémoire",en foutre une
	#artificiel art dame leurrer naïveté
	#autorisation bourgeois  accouche
	# par exemple : 
	#               entendre Pouët, pouet
	# doutes, bonheur, tristesse,
	#               suicide, crime,  mode, contradiction
	#               informatique, linguistique, ...........
	# à faire...
	# cerveau : Mon cerveau ? C'est mon second organe préféré.
	# 
	# d'autres idées : engager une conversation qui permet de connaître
	# le nom, le sexe, l'âge du patient
	# ou extraire automatiquement le sexe grâce à des phrase comme
	# je suis content / je suis contente
	#