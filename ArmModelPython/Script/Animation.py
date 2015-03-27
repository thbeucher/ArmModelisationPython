#######################################################################################
########## Author: Thomas Beucher // Module: Animation ################################
#######################################################################################
from ArmModel.SavingData import SavingData
import matplotlib.pyplot as plt
from matplotlib import animation
from FileProcessing.FileReading import FileReading

################################################################################################
######################## trajectories Animation ################################################
################################################################################################
def animatAct(nbfeat):
    ###Mots cles: "All" pour lancer toutes les trajectoires ou alors choississez le numero de la trajectoire souhaitees

    choix = input("Veuillez choisir la trajectoire a visualiser: ")
    fr = FileReading()
    save = SavingData()
    
    fig = plt.figure()
    upperArm, = plt.plot([],[]) 
    foreArm, = plt.plot([],[])
    plt.xlim(-0.7, 0.7)
    plt.ylim(-0.7,0.7)
    plt.plot([-0.7,0.7], [0.6175, 0.6175])
    plt.scatter(0, 0.6175, c ='g', marker='o', s=50)
    
    #Fonction d'initialisation pour l'animation
    def init():
        upperArm.set_data([0],[0])
        foreArm.set_data([save.xEl[0]],[save.yEl[0]])
        return upperArm,foreArm,
    
    #Fonction utiliser pour generer les differentes position du bras pour l'animation     
    def animate(i): 
        xe = (0, save.xEl[i])
        ye = (0, save.yEl[i])
        xh = (save.xEl[i], save.xHa[i])
        yh = (save.yEl[i], save.yHa[i])
        upperArm.set_data(xe, ye)
        foreArm.set_data(xh, yh)
        return upperArm,foreArm
    
    if choix == "All":
        nameCoordEL = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireEL" + choix
        nameCoordHA = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireHA" + choix
        coordEL = fr.getobjread(nameCoordEL)
        coordHA = fr.getobjread(nameCoordHA)
        save.createCoord(2, coordHA, coordEL)
        ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(coordEL), blit=True, interval=20, repeat=True)
        plt.show()
    else: 
        nameCoordEL = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireEL" + choix
        nameCoordHA = "RBFN2/" + str(nbfeat) + "feats/CoordTraj/CoordTrajectoireHA" + choix
        coordEL = fr.getobjread(nameCoordEL)
        coordHA = fr.getobjread(nameCoordHA)
        save.createCoord(2, coordHA, coordEL)
        ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(coordEL), blit=True, interval=20, repeat=True)
        plt.show()