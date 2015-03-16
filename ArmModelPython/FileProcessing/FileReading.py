import pickle
import ArmModel.ParametresRobot as pr
import numpy as np
import math as ma
#import cma as cma
import os.path as op

class FileReading():
    
    def __init__(self):
        #Recuperation des commandes
        self.u1 = []
        self.u2 = []
        self.u3 = []
        self.u4 = []
        self.u5 = []
        self.u6 = []
        self.uCommand = {}
        self.data_store = {}   
        self.name_store = []
    #target(4) estimated_state(4) actual_state(4) noised_command(6) command(6) estimated_next_state(4) 
    #actual_next_state(4) next_acceleration(2)
    #Recuperation des donnees du fichier dans une matrice
    def recup_data(self):
        chemin = "/home/beucher/workspace/ArmModelPython/FileProcessing/trajectoires/"
        nameFichier = input("Veuillez entrer le nom courant des fichiers à traiter: ")
        nbFichier = input("Veuillez entrer le nombre de fichier à traiter: ")
        nbFichier = int(nbFichier)
        j = 0
        nbf = 0
        while j < nbFichier:
            if op.isfile(chemin + nameFichier + str(j+1+nbf) + ".log") == False:
                nbf += 1
            mat = np.loadtxt(chemin + nameFichier + str(j+1+nbf) + ".log")
            i = 0
            k = 0
            state = []
            command = []
            while i < mat.size/34:
                state.append((mat[i][k+8], mat[i][k+9], mat[i][k+10], mat[i][k+11]))
                command.append((mat[i][k+18], mat[i][k+19], mat[i][k+20], mat[i][k+21], mat[i][k+22], mat[i][k+23]))
                i += 1
            self.data_store[str(nameFichier + str(j+1+nbf) + "_state")] = state
            self.data_store[str(nameFichier + str(j+1+nbf) + "_command")] = command
            self.name_store.append(str(nameFichier + str(j+1+nbf)))
            j += 1
    
    #################################################################################################################
    ## Fonction pour mettre dans tes tableaux separes les differentes activations musculaires                      ##
    #################################################################################################################
    def tabActivationMuscu(self, nameFileTemp):
        #Recuperation dans des tableaux des activations musculaires
        j = 0
        while j < len(self.data_store[str(nameFileTemp + "_command")]):
            self.u1.append(((self.data_store[str(nameFileTemp + "_command")])[j])[0])
            self.u2.append(((self.data_store[str(nameFileTemp + "_command")])[j])[1])
            self.u3.append(((self.data_store[str(nameFileTemp + "_command")])[j])[2])
            self.u4.append(((self.data_store[str(nameFileTemp + "_command")])[j])[3])
            self.u5.append(((self.data_store[str(nameFileTemp + "_command")])[j])[4])
            self.u6.append(((self.data_store[str(nameFileTemp + "_command")])[j])[5])
            j += 1
        #Rangement dans un dictionnaire des differents tableaux d'activations musculaires
        self.uCommand["u1"] = self.u1
        self.uCommand["u2"] = self.u2
        self.uCommand["u3"] = self.u3
        self.uCommand["u4"] = self.u4
        self.uCommand["u5"] = self.u5
        self.uCommand["u6"] = self.u6
    '''data_store = {}   
    data_store, nameFichier, nbFichier = recup_data()
    print(len(data_store))
    print(len(data_store[str(nameFichier + "1_state")]))
    print(len(data_store[str(nameFichier + "1_command")]))'''
    
    
    ###########################################################################################
    #La suite de ce code permet de récupérer q1 et q2 à partir du x et du y de la main
    ###########################################################################################
    '''def convertToAngle(xh, yh, robot):
        if (xh**2+yh**2-robot.l1**2-robot.l2**2)/(2*robot.l1*robot.l2) < -1:
            q2 = np.arccos(1)
        else:
            q2 = np.arccos((xh**2+yh**2-robot.l1**2-robot.l2**2)/(2*robot.l1*robot.l2))
        q1 = ma.atan2(yh, xh)-ma.atan2(robot.l2*np.sin(q2), robot.l1 + robot.l2*np.cos(q2))
        return q1, q2
    
    coord = [(-0.2,0.39)]
    coord.append((-0.1,0.39))
    coord.append((0.,0.39))
    coord.append((0.1,0.39))
    coord.append((0.2,0.39))
    coord.append((-0.3,0.0325))
    coord.append((-0.2,0.0325))
    coord.append((-0.1,0.0325))
    coord.append((0.,0.0325))
    coord.append((0.1,0.0325))
    coord.append((0.2,0.0325))
    coord.append((0.3,0.0325))
    coord.append((0.,0.6175))
    
    f = lambda col: col[0]
    g = lambda col: col[1]
    print(f(coord[0]))
    
    angle = []
    robot = pr.ParametresRobot()
    for el in coord:
        q1, q2 = convertToAngle(el[0], el[1], robot)
        angle.append((q1,q2))
    print(angle)
    
    monfichier = open("q1q2pourChaqueXhYh","w")
    i = 0
    for el1 in coord:
        monfichier.write(str(i+1) + "-Coordonnees: (xh=" + str(el1[0]) + ",yh=" + str(el1[1]) + ") et angle du bras associés: (p1=" + str(f(angle[i])) + ",p2=" + str(g(angle[i])) + ")\n")
        i += 1
    monfichier.close()
    
    monFichierAjout = open("q1q2pourChaqueXhYh","a")
    for el in angle:
        monFichierAjout.write("{" + str(el[0]) + "," + str(el[1]) + "},")
    monFichierAjout.close()
    
    print(ma.atan2(2, 1))'''






