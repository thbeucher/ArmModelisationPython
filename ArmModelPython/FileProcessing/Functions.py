from FileProcessing.FileReading import FileReading
from FileProcessing.FileSaving import fileSavingStr, fileSavingBin
import numpy as np
from ArmModel.SavingData import SavingData
import matplotlib.pyplot as plt
from matplotlib import animation


def normalizeThetaFunction():
    fr = FileReading()
    fr.getTheta(3, 0)
    vzeros = []
    #Enregistrement des theta en Str
    for i in range(6):
        name = "ThetaAllTraj/Theta_u" + str(i+1)
        fileSavingStr(name, fr.theta_store[str("u" + str(i+1))])
    #Normalisation des theta
    for i in range(6):
        mini = np.min(fr.theta_store[str("u" + str(i+1))])
        maxi = np.max(fr.theta_store[str("u" + str(i+1))])
        vs = fr.theta_store[str("u" + str(i+1))]
        v = (vs - mini)/(maxi - mini)
        vtest = v + 0.1
        name = "ThetaAllTraj/thetaNormalize_u" + str(i+1)
        fileSavingStr(name, v)
        nameb = "ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)
        fileSavingBin(nameb, v)
    #Coefficient de normalisation
    for i in range(6):
        namec = "ThetaAllTraj/CoefNormalization_theta_u" + str(i+1)
        vTmp = fr.getobjread(str("ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)))
        coef =  np.divide(vTmp, fr.theta_store[str("u" + str(i+1))])
        fileSavingBin(namec, coef)
        fileSavingStr(str(namec + "_str"), coef)

    
    
'''normalizeThetaFunction()
f = FileReading()
for i in range(6):
    tn = f.getobjread(str("ThetaAllTraj/Python_thetaNormalize_u" + str(i+1)))
    coef = f.getobjread(str("ThetaAllTraj/CoefNormalization_theta_u" + str(i+1)))
    tl = np.divide(tn, coef)
    fileSavingStr(str("ThetaAllTraj/thetaRetrouve_u" + str(i+1)), tl)'''



################################################################################################
######################## trajectories Animation ################################################
################################################################################################
choix = input("Veuillez choisir la trajectoire à visualiser: ")
fr = FileReading()
save = SavingData()

fig = plt.figure()
upperArm, = plt.plot([],[]) 
foreArm, = plt.plot([],[])
plt.xlim(-0.7, 0.7)
plt.ylim(-0.7,0.7)
plt.plot([-0.7,0.7], [0.6175, 0.6175])
plt.scatter(0, 0.6175, c ='g', marker='o', s=50)

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

if choix == "All":
    nameCoordEL = "RBFN2/2feats/CoordTraj/CoordTrajectoireEL" + choix
    nameCoordHA = "RBFN2/2feats/CoordTraj/CoordTrajectoireHA" + choix
    coordEL = fr.getobjread(nameCoordEL)
    coordHA = fr.getobjread(nameCoordHA)
    save.createCoord(2, coordHA, coordEL)
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(coordEL), blit=True, interval=20, repeat=True)
    plt.show()
else: 
    nameCoordEL = "RBFN2/2feats/CoordTraj/CoordTrajectoireEL" + choix
    nameCoordHA = "RBFN2/2feats/CoordTraj/CoordTrajectoireHA" + choix
    coordEL = fr.getobjread(nameCoordEL)
    coordHA = fr.getobjread(nameCoordHA)
    save.createCoord(2, coordHA, coordEL)
    ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(coordEL), blit=True, interval=20, repeat=True)
    plt.show()










