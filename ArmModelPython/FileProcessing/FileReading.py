'''
Author: Thomas Beucher
Module: FileReading
'''
import pickle
import numpy as np
import math as ma
#import cma as cma
import os.path as op
import os
from posix import getcwd
from ArmModel.ParametresRobot import ParametresRobot
from FileProcessing.FileSaving import fileSavingStr
from numpy import isnan
from ArmModel.SavingData import SavingData
from Optimisation.NiemRoot import tronquerNB
#from nt import getcwd #Windows

class FileReading():
    
    def __init__(self):
        '''
        Initialisation des parametres de la classe
        '''
        #Recuperation des commandes
        self.uCommand = {}
        self.data_store = {}   
        self.name_store = []
        self.theta_store = {}
    
    ################################################################################################
    ######################## Fonction permettant de récupérer les données d'un fichier #############
    ################################################################################################
    def getobjread(self, name):
        folder = getcwd()
        folder = op.split(folder)
        folder = folder[0] + "/Data/"
        namet = folder + name
        with open(namet, "rb") as file:
                mondepickler = pickle.Unpickler(file)
                data = mondepickler.load()
        return data
    
    #target(4) estimated_state(4) actual_state(4) noised_command(6) command(6) estimated_next_state(4) 
    #actual_next_state(4) next_acceleration(2)
    #Recuperation des donnees du fichier dans une matrice
    def recup_data(self, choix = 1):
        chemin = getcwd()
        chemin = op.split(chemin)
        chemin = chemin[0] + "/Data/trajectoires/"
        if choix == 1:
            print("Nombre de fichier disponible: ", len(os.listdir(chemin))-1)
            nameFichier = input("Veuillez entrer le nom courant des fichiers a traiter: ")
            nbFichier = input("Veuillez entrer le nombre de fichier à traiter: ")
            nbFichier = int(nbFichier)
        else:
            #nom du fichier courant
            nameFichier = "trajectoire"
            #nombre de fichier a traiter
            nbFichier = len(os.listdir(chemin))-1
        j = 0
        l = 0
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
            if l == 0:
                stateAll = np.array(state)
                commandAll = np.array(command)
                l += 1
            else:
                stateAll = np.vstack((stateAll, state))
                commandAll = np.vstack((commandAll, command))
            j += 1
        return stateAll, commandAll
    
    def recup_pos_ini(self):
        '''
        Cette fonction permet de recuperer toutes les positions initiales des trajectoires utilisees pour
        entrainer l'algorithme de regression
        '''
        print("Debut de recuperation des positions initiales!")
        chemin = getcwd()
        chemin = op.split(chemin)
        chemin = chemin[0] + "/Data/trajectoires/"
        save = SavingData()
        robot = ParametresRobot()
        angleIni = {}
        fr = FileReading()
        for el in os.listdir(chemin):
            if "trajectoire" in el:
                #Chargement du fichier
                mati = np.loadtxt(chemin + el)
                #recuperation de q1 et q2 initiales et conversion en coordonnees
                coordElbow, coordHand = save.calculCoord(np.mat([[mati[0,10]], [mati[0,11]]]), robot)
                angleIni[el] = (coordHand[0], coordHand[1])
        print("Fin de recuperation des positions initiales!")
        return angleIni
        
    ###########################################################################################
    #Cette fonction permet de récuperer q1 et q2 à partir du x et du y de la main
    ###########################################################################################
    def convertToAngle(self, xh, yh, robot):
        '''
        Cette fonction permet de récuperer q1 et q2 à partir du x et du y de la main
        '''
        q2 = ma.atan2(np.sqrt(1-(xh**2+yh**2-robot.l1**2-robot.l2**2)/(2*robot.l1*robot.l2)), (xh**2+yh**2-robot.l1**2-robot.l2**2)/(2*robot.l1*robot.l2))
        #if q2 < 0:
            #q2 = q2*(-1)
        q1 = ma.atan2(yh, xh)-ma.atan2(robot.l2*np.sin(q2), robot.l1 + robot.l2*np.cos(q2))
        return q1, q2

fr = FileReading()
robot = ParametresRobot()
save = SavingData()
x = np.arange(-0.45,0.45,0.05)
y = np.arange(0.25,0.55,0.05)
X,Y = np.meshgrid(x,y)
p = fr.convertToAngle(X[5,5], Y[5,5], robot)
print(X[5,5], Y[5,5], "\n", p[0], p[1], "\n", save.calculCoord(np.mat([[p[0]],[p[1]]]), robot))
q = []
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        q.append(fr.convertToAngle(X[i,j], Y[i,j], robot))
cor = []
for el in q:
    if not isnan(el[0]) or not isnan(el[1]):
        corE, corH = save.calculCoord(np.mat([[el[0]],[el[1]]]), robot)
        cor.append(corH)
    elif isnan(el[0]) or isnan(el[1]):
        cor.append(("nan", "nan"))
with open("testUnitaireConvertToAngle", "w+") as file:
    co = 0
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            if not isnan(q[j+co][0]):
                a = tronquerNB(X[i,j], 3)
                b = tronquerNB(Y[i,j], 3)
                c = tronquerNB(q[j+co][0], 3)
                d = tronquerNB(q[j+co][1], 3)
                e = tronquerNB(cor[j+co][0], 3)
                f = tronquerNB(cor[j+co][1], 3)
                g = tronquerNB(e-a, 3)
                h = tronquerNB(f-b, 3)
                file.write(str("xy:("+str(a)+","+str(b)+")    q1,q2:("+str(c)+","+str(d)+")    x'y':("+str(e)+","+str(f)+")    err xy:("+str(g)+","+str(h) +")\n"))
        co += X.shape[1]

'''fr = FileReading()
fr.recup_pos_ini()
robot = ParametresRobot()
q = []
rec = []
save = SavingData()
#Bout de code pour generer les q1, q2 associes aux positions initiales
a = [(-0.2,0.39),(-0.1,0.39),(0.0,0.39),(0.1,0.39),(0.2,0.39),(-0.3,0.26),(-0.2,0.26),(-0.1,0.26),(0.0,0.26),(0.1,0.26),(0.2,0.26),(0.3,0.26)]
for el in a:
    q.append(fr.convertToAngle(el[0], el[1], robot))
fileSavingStr("coucouPOS", q)
for el in q:
    coorE, coorH = save.calculCoord(np.mat([[el[0]], [el[1]]]), robot)
    rec.append(coorH)
fileSavingStr("coucouRECOR", rec)'''

'''x = np.arange(-0.5,0.5,0.025)
y = np.arange(0.1,0.6,0.025)
X, Y = np.meshgrid(x,y)
print(x.shape, y.shape, X.shape, Y.shape)
q = []
fr = FileReading()
robot = ParametresRobot()
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        a,b = fr.convertToAngle(X[i,j], Y[i,j], robot)
        if np.isnan(a) or np.isnan(b):
            pass
        else:
            q.append((a, b))
print(len(q), np.max(q, axis = 0), np.min(q, axis = 0), "\n", q)
with open("q1q2747", "w+") as file:
    for el in q:
        file.write(str("{" + str(el[0]) + "," + str(el[1]) + "},"))'''

'''q = []
fr = FileReading()
robot = ParametresRobot()
for el in a:
    q.append(fr.convertToAngleTest(el[0], el[1], robot))
fileSavingStr("q1q2ForPosIniAlea", q)'''




