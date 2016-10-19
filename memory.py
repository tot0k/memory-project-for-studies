''' Projet Memory
	CRAVIC Thomas
'''

from tkinter import *
from random import randint
from time import time, sleep


'''---------------- MOTEUR LOGIQUE ----------------'''
# Variables globales aux valeurs initiales
selectedItem = [] 	# Emplacement de la case sélectionnée
imgGrid = []		# Grille des nombres affichés
successCount = 0	# Nombre de couples découverts
gridSize = 0		# Taille du côté de la grille
score = 0			# Nombre d'essais du joueur
startTimeStamp = 0	# timeStamp d'appui sur le bouton Play
gameMode = 0		# Mode de jeu (1=Classique, 2=Temps)
endText = None
tailleFen = 200


# Affiche la grille dans la console (debug)
def showGrid(grid):
	'''Affiche la grille dans la console sous la forme d'une matrice (DEBUG)'''
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if grid[i][j]==0:
				print("{:4}".format("----"), end=" ")
			else:
				print("{:4}".format(grid[i][j]), end=" ")
		print("\n")
	print("\n")


# Place un nombre aléatoirement dans une case vide aléatoire de la grille
def addImg(grid, imgNumber):
	positions = []
	for i in range(gridSize):
		for j in range(gridSize):
			if grid[i][j]==0:
				positions+=[[i,j]]

	if len(positions)!=0:
		selectedPos = randint(0,len(positions)-1)
		grid[ positions[selectedPos][0]] [positions[selectedPos][1] ] = imgNumber	# On place l'image n°imgNumber dans cette case vide
	return grid


# Place autant de couples de nombres que possible dans la grille
def randomizeImg():
	global gridSize
	nbImg = gridSize**2 // 2 # Nombre de cases divisé par 2

	grid = [[0 for i in range(gridSize)] for j in range(gridSize)]

	for i in range(nbImg):
		addImg(grid, i+1) # On ajoute 2 fois chaque image
		addImg(grid, i+1)
	#showGrid(grid)
	return grid


# Détecte si on a choisi le bon couple et agit en conséquence
def tryWin(pos1, pos2):
	global successCount, selectedItem, score, startTimeStamp
	score += 1
	if imgGrid[pos1[0]][pos1[1]] == imgGrid[pos2[0]][pos2[1]]:	# Le couple est le bon.
		successCount += 1
		if successCount == gridSize**2 // 2:					# La partie est finie
			if gameMode == 2:
				score = round(time() - startTimeStamp,2)
			victory()

	else:	# Le couple n'est pas le bon
		sleep(0.5)
		hide(pos1[0],pos1[1])
		hide(pos2[0],pos2[1])

	selectedItem = []


# Vérifie qu'on a le droit de sélectionner la case et agit en conséquence
def clickAction(x,y):
	global selectedItem
	# Si on clique sur une case pas sélectionnée ni déjà validée (donc pas encore affichée)
	if 	main.itemcget(numbersGrid[x][y],"state") == "hidden":	# Si la case n'est pas déjà affichée
		show(x,y)
		main.update()	# On force la mise à jour de la fenêtre

		if len(selectedItem) == 0:	# Si c'est la première case qu'on sélectionne
			selectedItem = [x,y]
		else:
			tryWin(selectedItem, [x,y])


# On calcule la case cliquée en fonction de la position du curseur
def leftClick(event):
	cellWidth = 0.9*tailleFen/gridSize 	# Taille des cellules en pixels
	border = 0.05*tailleFen 	# Taille des bordures en pixel

	# On détecte si on est bien dans la grille
	if not ((event.x < border) or (event.y < border) or (event.x > tailleFen-border) or (event.y > tailleFen-border)):
		posY = int((event.x-border) / cellWidth)
		posX = int((event.y-border) / cellWidth)
		clickAction(posX,posY)


# Réinitialise le jeu
def play(mode,difficulty,taille):
	global imgGrid, gridSize, startTimeStamp, score, successCount, selectedItem, gameMode, tailleFen

	tailleFen = int(taille[0:len(taille)-2]) # On enlève le "px" à la fin
	gridSize = difficulty
	gameMode = mode
	imgGrid = randomizeImg()

	# Remise à l'état initial des variables globales
	selectedItem = []
	successCount = 0
	startTimeStamp = time()
	score = 0

	# Lancement du jeu
	initGame()

	# On cache le texte de victoire
	main.itemconfigure(endText,text="")


'''---------------- MOTEUR GRAPHIQUE ----------------'''
# Affiche le nombre dans la case (x,y)
def show(x,y):
	main.itemconfigure(numbersGrid[x][y],state = "normal")


# Cache le nombre dans la case (x,y)
def hide(x,y):
	main.itemconfigure(numbersGrid[x][y],state = "hidden")


# Vérifie les meilleurs scores et agit en conséquence
def victory():
	texte = "Victory !\nScore : {}".format(score)

	if isNewBest(gameMode,gridSize,score):
		texte += "\nBest Score !"
		main.itemconfigure(endText,text=texte)
		main.update()
		sleep(2)
		enterName()
	else:
		main.itemconfigure(endText,text=texte)
		main.update()
		sleep(2)
		initToolbar()


# Crée la grille de nombres, cachés par défaut
def generateNumbersGrid(size,lenght):
	cellWidth = 0.9*(size/lenght)	# On laisse un espace de 5% sur chaque côté
	k = (size-lenght*cellWidth)/2
	grid = [[0 for j in range(lenght)] for i in range(lenght) ]	# Initialisation de la grille à afficher

	for i in range(lenght):
		for j in range(lenght):
			grid[j][i] = main.create_text(i*cellWidth+cellWidth/2+k,j*cellWidth+cellWidth/2+k,text=str(imgGrid[j][i]),font = ("BAUHS93",int(size/lenght/2),"bold"),state = "hidden")
	return grid


# Renvoie une liste avec autant de couleurs aléatoires qu'il y a de cases, et aucune case adjacente n'a la même couleur
def color(lenght):
	selectedColors = []
	colorList = ['snow','bisque','lemon chiffon','lavender','lavender blush','navy','cornflower blue','slate blue','blue','deep sky blue','light sky blue','dark turquoise','sea green','spring green','chartreuse','green yellow','lime green','khaki','gold','indian red','peru','wheat','chocolate','firebrick','dark salmon','orange','coral','hot pink','pink','violet','medium purple','snow3','tomato','PeachPuff3']
	colorBuff = [colorList[i] for i in range(len(colorList))]

	for i in range(lenght**2):
		index = randint(0,len(colorBuff)-1)
		selectedColors += [colorBuff[index]]
		del(colorBuff[index])

		if len(colorBuff)==0:
			colorBuff = [colorList[i] for i in range(len(colorList))]

	return selectedColors


# Affiche Le quadrillage coloré
def drawGrid(size, lenght):
	global main
	cellWidth = 0.9*size/lenght # On laisse un espace de 5% sur chaque côté
	k = (size-lenght*cellWidth)/2
	colors = color(lenght)
	colorNumber = 0

	for i in range(lenght):
		for j in range(lenght):
			main.create_rectangle(i*cellWidth+k,j*cellWidth+k,(i+1)*cellWidth+k,(j+1)*cellWidth+k, fill = colors[colorNumber])
			colorNumber += 1


# Valide la mise à jour des meilleurs scores
def validateName(pseudo):
	newBest = [pseudo, score]
	majBest(gameMode, gridSize, newBest)
	initToolbar()


# Fenêtre d'acquisition du nom du joueur ayant fait un meilleur score
def enterName():
	global newScoreCan
	fen.geometry("300x200")
	font1 = ("BAUHS93",14)
	font2 = ("BAUHS93",16,'bold')
	bg = "light sky blue"
	activeBg = "DodgerBlue2"
	lineColor = "DodgerBlue2"

	main.destroy()

	newScoresCan = Canvas(fen, width = 300, height = 200, bg = "light sky blue")
	newScoresCan.place(x=0,y=0)

	validateButton = Button(newScoresCan, text = "Valider", command = lambda: validateName(pseudo.get()), bg = activeBg, activebackground=bg,font=font2)

	newScoresCan.create_text(150,20,text="Entrez votre pseudo !",font=("BAUHS93",18,'bold'), fill = "red")
	newScoresCan.create_line(0,50,300,50,fill = lineColor, width = 2)

	pseudo = StringVar()
	pseudo.set("Player")
	saisiePseudo = Entry(newScoresCan, textvariable=pseudo, width=25, font=font1)
	saisiePseudo.place(x=10,y=80)
	validateButton.place(x=100,y=120)
	fen.mainloop()


# Crée la fenêtre
def initInterface():
	global fen, toolbar, scoresCan, newScoresCan, main
	# Création de la fenêtre
	fen = Tk()
	fen.title("Memory - Thomas Cravic")
	fen.resizable(0,0)

	toolbar = Canvas(fen, width = 300, height = 450, bg = "light sky blue")
	main = Canvas(fen, width=tailleFen, height=tailleFen, bg="light grey")
	scoresCan = Canvas(fen, width = 300, height = 400, bg = "light sky blue")
	newScoresCan = Canvas(fen, width = 300, height = 200, bg = "light sky blue")

	initToolbar()


# Crée le menu de base
def initToolbar():
	global toolbar, scoresCan, main

	scoresCan.destroy()
	newScoresCan.destroy()
	main.destroy()

	fen.geometry("300x450")
	toolbar = Canvas(fen, width = 300, height = 450, bg = "light sky blue")
	toolbar.pack()

	font1 = ("BAUHS93",14)
	font2 = ("BAUHS93",16,'bold')
	bg = "light sky blue"
	activeBg = "DodgerBlue2"
	lineColor = "DodgerBlue2"

	# Variables de sélection
	choixMode = IntVar()
	choixDifficulty = IntVar()
	choixTaille = StringVar()

	# Boutons
	playButton = Button(toolbar, text = "Jouer", command = lambda : play(choixMode.get(),choixDifficulty.get(),choixTaille.get()), bg = activeBg, activebackground=bg,font=font2)
	scoresButton = Button(toolbar, text = "Scores", command = initScores, bg = activeBg, activebackground=bg,font=font2)

	# Liste déroulante "taille de la fenêtre"
	tailleSelect = OptionMenu(toolbar,choixTaille,"400px","600px","800px","1000px")
	# Liste à puces "mode de jeu"
	radio_mode1 = Radiobutton(toolbar, text="Classique", variable=choixMode, value=1, bg=bg,activebackground=activeBg, font=font1)
	radio_mode2 = Radiobutton(toolbar, text="Contre la montre", variable=choixMode, value=2, bg=bg,activebackground=activeBg,font=font1)
	# Liste à puces "difficulté"
	radio_difficulty1 =  Radiobutton(toolbar, text="Facile", variable=choixDifficulty, value=4, bg=bg,activebackground=activeBg, font=font1)
	radio_difficulty2 =  Radiobutton(toolbar, text="Normal", variable=choixDifficulty, value=6, bg=bg,activebackground=activeBg, font=font1)
	radio_difficulty3 =  Radiobutton(toolbar, text="Difficile", variable=choixDifficulty, value=8, bg=bg,activebackground=activeBg, font=font1)

	# Affichage Graphique
	toolbar.create_text(150,20,text="Memory - Thomas Cravic",font=("BAUHS93",18,'bold'), fill = "red")
	toolbar.create_line(0,50,300,50,fill = lineColor, width = 2)

	toolbar.create_text(110,75,text="Taille de la fenêtre : ",font=font2, fill="DodgerBlue4")
	tailleSelect.place(x=200,y=60)
	toolbar.create_line(0,100,300,100,fill = lineColor, width = 2)

	toolbar.create_text(150, 130, text="Mode de jeu",font=font2, fill="DodgerBlue4")
	radio_mode1.place(x=50, y=150)
	radio_mode2.place(x=50, y=180)
	toolbar.create_line(0,220,300,220,fill = lineColor, width = 2)

	toolbar.create_text(150, 240, text="Difficulté",font=font2, fill="DodgerBlue4")
	radio_difficulty1.place(x=50, y=260)
	radio_difficulty2.place(x=50, y=290)
	radio_difficulty3.place(x=50, y=320)

	playButton.place(x=30,y=370, width = 100, height=60)
	scoresButton.place(x=170, y=370, width = 100, height=60)

	# Mode par défaut : Classique, Facile, fenêtre de 400px
	choixMode.set(1)
	choixDifficulty.set(4)
	choixTaille.set("600px")


# Crée la fenêtre de sélection des meilleurs scores
def initScores():
	global scoresCan
	fen.geometry("300x450")
	font1 = ("BAUHS93",14)
	font2 = ("BAUHS93",16,'bold')
	bg = "light sky blue"
	activeBg = "DodgerBlue2"
	lineColor = "DodgerBlue2"

	toolbar.destroy()
	main.destroy()
	scoresCan = Canvas(fen, width = 300, height = 450, bg = "light sky blue")
	scoresCan.pack()

	# Variables de sélection
	choixMode = IntVar()
	choixDifficulty = IntVar()

	# Boutons
	validateButton = Button(scoresCan, text = "Valider", command = lambda : showScores(choixMode.get(),choixDifficulty.get()), bg = activeBg, activebackground=bg,font=font2)
	backButton = Button(scoresCan, text = "Retour", command = initToolbar, bg = activeBg, activebackground=bg,font=font2)

	# Liste à puces "mode de jeu"
	radio_mode1 = Radiobutton(scoresCan, text="Classique", variable=choixMode, value=0, bg=bg,activebackground=activeBg, font=font1)
	radio_mode2 = Radiobutton(scoresCan, text="Contre la montre", variable=choixMode, value=1, bg=bg,activebackground=activeBg,font=font1)

	# Liste à puces "difficulté"
	radio_difficulty1 =  Radiobutton(scoresCan, text="Facile", variable=choixDifficulty, value=0, bg=bg,activebackground=activeBg, font=font1)
	radio_difficulty2 =  Radiobutton(scoresCan, text="Normal", variable=choixDifficulty, value=1, bg=bg,activebackground=activeBg, font=font1)
	radio_difficulty3 =  Radiobutton(scoresCan, text="Difficile", variable=choixDifficulty, value=2, bg=bg,activebackground=activeBg, font=font1)


	# Affichage interface
	scoresCan.create_text(150,20,text="Meilleurs Scores",font=("BAUHS93",18,'bold'), fill = "red")
	scoresCan.create_line(0,50,300,50,fill = lineColor, width = 2)

	scoresCan.create_text(140,75,text="Mode de jeu : ",font=font2, fill="DodgerBlue4")
	radio_mode1.place(x=60,y=100)
	radio_mode2.place(x=60,y=130)

	scoresCan.create_text(140,185,text="Difficulté : ",font=font2, fill="DodgerBlue4")
	radio_difficulty1.place(x=60,y=200)
	radio_difficulty2.place(x=60,y=225)
	radio_difficulty3.place(x=60,y=250)

	validateButton.place(x=30,y=370, width = 100, height=60)
	backButton.place(x=160,y=370, width = 100, height=60)

# Crée la fenêtre d'affichage des scores dans un mode et une difficulté particulières
def showScores(mode,difficulty):
	global scoresCan

	fen.geometry("300x450")
	font1 = ("BAUHS93",14,"bold")
	font2 = ("BAUHS93",16,'bold')
	bg = "light sky blue"
	activeBg = "DodgerBlue2"
	lineColor = "DodgerBlue2"

	if mode == 0:
		title = "Classique - "
	else:
		title = "Contre La Montre - "

	if difficulty == 0:
		title += "facile"
	elif difficulty == 1:
		title += "normal"
	else:
		title += "difficile"


	scoresCan.destroy()
	scoresCan = Canvas(fen, width = 300, height = 450, bg = "light sky blue")
	scoresCan.place(x=0,y=0)

	scoreList = readFile()[mode][difficulty]
	backButton = Button(scoresCan, text = "Retour", command = initScores, bg = activeBg, activebackground=bg,font=font2)
	scoresCan.create_text(150,20,text=title,font=("BAUHS93",17,'bold'), fill = "red")


	for i in range(10):
		if len(scoreList) <= i:
			line = ""
		else:
			line = "{} : {}".format(scoreList[i][0],scoreList[i][1])

		scoresCan.create_text(30,60+i*25,text="{:4} | ".format(i+1),font=font1, fill="DodgerBlue4")
		scoresCan.create_text(160,60+i*25,text=line,font=font1, fill="DodgerBlue4")

	backButton.place(x=150,y=370, width = 100, height=60)


# Initialise l'interface de jeu
def initGame():
	global main, numbersGrid, endText
	fen.geometry("{}x{}".format(tailleFen,tailleFen))

	toolbar.destroy()

	main = Canvas(fen, width=tailleFen, height=tailleFen, bg="light grey")
	main.pack()

	# Affichage grille
	drawGrid(tailleFen,gridSize)
	numbersGrid = generateNumbersGrid(tailleFen,gridSize)
	main.bind("<Button-1>", leftClick)

	endText = main.create_text(tailleFen/2, tailleFen/2, text="", font = ("Impact",tailleFen//15,"bold"), fill = "red")


# Méthode principale
if __name__ == '__main__':
	try :
		from fileHandler import *	# Si le fichier fileHandler.py n'existe pas
		initInterface() # Création de l'interface graphique
		fen.mainloop()

	except ImportError as e:
		print("Erreur : Veuillez placer le fichier fileHandler.py à la racine du dossier dans lequel se trouve memory.py")
