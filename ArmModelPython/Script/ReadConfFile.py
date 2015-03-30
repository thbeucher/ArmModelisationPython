


def readingConfigurationFile():
    #Recuperation des donnees du fichier de configuration
    with open("setupFile", "r") as file:
        alls = file.read()
    #Split pour recuperer ligne par ligne
    allsByLign = alls.split("\n")
    #lecture ligne 1, nombre de features
    nbfeat = int((allsByLign[0].split(":"))[1])
    #lecture ligne 2, choix d'une simulation avec ou sans bruit moteur
    noise = (allsByLign[1].split(":"))[1]