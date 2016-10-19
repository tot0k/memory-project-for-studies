''' Projet Memory
	CRAVIC Thomas

	Module de gestion de fichiers afin de lire et d'enregistrer les meilleurs scores.
	Pour lancer le jeu, exécutez memory.py

'''
global path
path = "scores.txt"

# Récupère les meilleurs scores par mode de jeu et difficulté dans un tableau à 3 dimensions (mode,difficulté,scores)
def readFile():
	try :
		file = open(path,'r')

		bestScores = [ [[],[],[]], [[],[],[]] ]
		scoreType = 0
		difficulty = 0

		# On parcourt le fichier
		for line in file:

			# Si la ligne n'est pas vide
			if line[0]!="\n":
				# On enlève le retour à la ligne de la fin
				line = line[:len(line)-1]

				# Le dieze démarque les modes de jeu
				if line[0]=="#":
					scoreType += 1

				# Le tirets démarquent la difficulté
				elif line[0]=="-":
					if difficulty!=3:
						difficulty += 1
					else:
						difficulty=1
				else:
					bestScores[scoreType-1][difficulty-1] += [line.split(';')]

		file.close()
		return bestScores

	except FileNotFoundError as e:
		print("Erreur : Le fichier {} n'existe pas. Veuillez télécharger le fichier de scores originel ici : https://goo.gl/zSbbgo".format(path))
		return None


# Formate et écrit un tableau de scores
def writeFile(values):
	try :
		file = open(path,'w')
		for mode in values:
			file.write("#\n")
			for difficulty in mode:
				file.write("-\n")
				for score in difficulty:
					file.write("{};{}\n".format(score[0],score[1]))


	except FileNotFoundError as e:
		print("Erreur : Le fichier {} n'existe pas. Veuillez télécharger le fichier de scores originel ici : https://goo.gl/zSbbgo".format(path))


# Met à jour le tableau de scores
def majBest(mode,difficulty,value):
	mode += -1
	if difficulty == 4:
		difficulty=0
	elif difficulty == 6:
		difficulty = 1
	else:
		difficulty = 2

	scoresTab = readFile()
	scores = scoresTab[mode][difficulty]

	for i in range(len(scores)):
		if float(scores[i][1]) > float(value[1]):
			scores = scores[:i]+[[str(value[0])]+[str(value[1])]]+scores[i:len(scores)]
			if len(scores) > 10:
				scores = scores[:9]
			break;

	if len(scores)<10 and float(value[1]) >= float( scores[len(scores)-1][1]):
		scores += [[str(value[0])]+[str(value[1])]]

	scoresTab[mode][difficulty] = scores
	writeFile(scoresTab)


# Vérifie si quelqu'un vient de faire un meilleur score
def isNewBest(mode,difficulty,value):
	mode += -1
	if difficulty == 4:
		difficulty=0
	elif difficulty == 6:
		difficulty = 1
	else:
		difficulty = 2

	scoresTab = readFile()
	scores = scoresTab[mode][difficulty]

	if len(scores)<10:
		return True
	else :
		for best in scores:
			if float(value) < float(best[1]):
				return True
	return False
