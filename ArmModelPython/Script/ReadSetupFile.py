'''Author: Thomas beucher
    Module: ReadConfFile
    On retrouve dans ce fichier une fonction permettant de lire le fichier de configuration '''


class ReadSetupFile:
    
    def __init__(self):
        self.name = "setup"
    
    def readingSetupFile(self):
        '''Cette fonction permet de lire le fichier de configuration '''
        #Recuperation des donnees du fichier de configuration
        with open("setupFile", "r") as file:
            alls = file.read()
        #Split pour recuperer ligne par ligne
        allsByLign = alls.split("\n")
        #lecture ligne 1, nombre de features
        self.numfeats = int((allsByLign[0].split(":"))[1])
        #lecture ligne 2, choix d'une simulation avec ou sans bruit moteur
        self.noise = (allsByLign[1].split(":"))[1]