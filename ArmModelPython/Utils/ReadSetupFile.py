'''
Author: Thomas beucher

Module: ReadConfFile

Description: On retrouve dans ce fichier une fonction permettant de lire le fichier de configuration 
'''

class ReadSetupFile:
    
    def __init__(self):
        self.name = "setup"
        self.readingSetupFile()
    
    def readingSetupFile(self):
        '''
        Cette fonction permet de lire le fichier de configuration 
        '''
        #Recuperation des donnees du fichier de configuration
        with open("/home/beucher/workspace/ArmModelPython/ExperimentSetup/setupFile", "r") as file:
            alls = file.read()
        #Split pour recuperer ligne par ligne
        allsByLign = alls.split("\n")
        #lecture ligne 1, nombre de features
        self.numfeats = int((allsByLign[0].split(":"))[1])
        #lecture ligne 2, choix d'une simulation avec ou sans bruit moteur
        self.noise = (allsByLign[1].split(":"))[1]
        #lecture ligne 3, choix de la valeur de k pour le bruit sur U
        self.knoiseU = float((allsByLign[2].split(":"))[1])
        #lecture ligne 4, choix du Parametre gamma cost function
        self.gammaCF = float((allsByLign[3].split(":"))[1])
        #lecture ligne 5, choix du Parametre rho cost function
        self.rhoCF = int((allsByLign[4].split(":"))[1])
        #lecture ligne 6, choix du Parametre upsilon cost function
        self.upsCF = int((allsByLign[5].split(":"))[1])
        #lecture ligne 7, Pour CMAES, sigma
        self.sigmaCmaes = float((allsByLign[6].split(":"))[1])
        #lecture ligne 8, Pour CMAES, maxIteration
        self.maxIterCmaes = int((allsByLign[7].split(":"))[1])
        #lecture ligne 9, POUR CMAES, popsize
        self.popsizeCmaes = int((allsByLign[8].split(":"))[1])
        #lecture ligne 10, chemin du dossier du projet
        self.pathFolderProject = (allsByLign[9].split(":"))[1]
        #lecture ligne 11, chemin du dossier data
        self.pathFolderData = (allsByLign[10].split(":"))[1]
        #lecture ligne 12, Chemin du dossier contenant les trajectoires
        self.pathFolderTrajectories = (allsByLign[11].split(":"))[1]
        #lecture ligne 13, Taille de la cible pour l'experimentation
        self.sizeOfTarget = float((allsByLign[12].split(":"))[1])
        #lecture ligne 14, ordonnee de la cible
        self.targetOrdinate = float((allsByLign[13].split(":"))[1])
        #lecture ligne 15, Pas de temps utilise pour l'experimentation
        self.dt = float((allsByLign[14].split(":"))[1])
        #reading line 16, initiales positions
        self.experimentFilePosIni = (allsByLign[15].split(":"))[1]
        #reading line 17, number of iteration to stop unresolved trajectory
        self.numMaxIter = int((allsByLign[16].split(":"))[1])
        #reading line 18, final position error
        self.errorPosEnd = float((allsByLign[17].split(":"))[1])


