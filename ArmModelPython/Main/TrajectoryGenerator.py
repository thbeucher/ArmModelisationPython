from ArmModel.ParametresRobot import ParametresRobot
from ArmModel.ParametresHogan import ParametresHogan
from ArmModel.ParametresArmModel import ParametresArmModel
from ArmModel.SavingData import SavingData
from Regression.ControlerUtil import ControlerUtil
import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt
from FileProcessing.FileReading import FileReading
import time
from Optimisation.costFunction import costFunction
from FileProcessing.FileSaving import fileSavingStr


#Recuperation des donnees necessaires a la simulation du bras
robot = ParametresRobot()
hogan = ParametresHogan()
arm = ParametresArmModel(hogan.GammaMax)
'''nbf = input("Nombre de features correspondant au controleur voulu: ")
nbf = int(nbf)
nbd = input("Nombre de dimension correspondant au controleur voulu: ")
nbd = int(nbd)
nbt = input("Veuillez choisir le numero d'une trajectoire de travail: ")
nbt = int(nbt)'''
nbf = 3
nbd = 4
nbt = 0
cu = ControlerUtil(nbf,nbd)

#Choix d'une trajectoire de travail
fr = FileReading()
q1, q2 = fr.convertToAngle(0.2, 0.39, robot)

#Initialisation ParametresArmModel
q = np.mat([[q1],[q2]])
dotq = arm.dotq0
save = SavingData()
coordEL, coordHA = save.calculCoord(q, robot)
save.SaveTrajectory(coordEL, coordHA)

cf = costFunction()

#Boucle de traitement
print("Debut du calcul de la trajectoire!")
t0 = time.time()
i = 0;
while coordHA[1] < 0.6175:
    if i < 900:
        #Recuperation du vecteur coordonnees
        inputq = np.array([dotq[0,0], dotq[1,0], q[0,0], q[1,0]])
            
        #Recuperation des activations musculaires
        cu.getCommand(inputq, nbt)
            
        # Calcul du couple Gamma pour une raideur non nulle
        Gamma_AM = (arm.At*arm.fmax-(arm.Kraid*np.diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])))*cu.U
            
        ddotq = arm.MDD( Gamma_AM,q,dotq,robot)
        dotq += ddotq*arm.dt
        q += dotq*arm.dt
            
        #Sauvegarde position pour visualition trajectoire
        coordEL, coordHA = save.calculCoord(q, robot)
        save.SaveTrajectory(coordEL, coordHA)
        #Sauvegarde des differents parametres
        save.saveParameters(q, dotq, ddotq, Gamma_AM, arm)
        
        #Calcul du cout
        if coordHA[1] < 0.6175:
            cf.costFunctionJ(cu.U, 1, arm.t)
        else:
            cf.costFunctionJ(cu.U, 2, arm.t)
    else:
        break
    i += 1
    arm.t += arm.dt
t1 = time.time()
print("Fin du traitement! (Temps de traitement: ", (t1-t0), "s)")
print("Nombre d'iteration pour arriver a la cible: ", len(save.coordHaSave))
print("Valeur de la fonction cout: ", cf.Ju)
#Sauvegarde du coup pour la trajectoire choisie
name = "ControlerResult/trajectoireInit(" + str(save.coordHaSave[0]) + ")Fin(" + str(save.coordHaSave[len(save.coordHaSave)-1]) + ")"
fileSavingStr(name, cf.Ju)

##########################################################################################
##Plot                                                                                  ##
##########################################################################################
save.createCoord()

fig = plt.figure()
upperArm, = plt.plot([],[]) 
foreArm, = plt.plot([],[])
plt.xlim(-0.7, 0.7)
plt.ylim(-0.7,0.7)

def init():
    upperArm.set_data([0],[0])
    foreArm.set_data([save.xEl[0]],[save.yEl[0]])
    return upperArm,foreArm,

def animate(i): 
    xe = (0, save.xEl[i])
    ye = (0, save.yEl[i])
    xh = (save.xEl[i], save.xHa[i])
    yh = (save.yEl[i], save.yHa[i])
    upperArm.set_data(xe, ye)
    foreArm.set_data(xh, yh)
    return upperArm,foreArm
 
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(save.coordHaSave), blit=True, interval=20, repeat=True)

plt.show(block=True)





