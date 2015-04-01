import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from FileProcessing.FileReading import FileReading
from ArmModel.SavingData import SavingData
from matplotlib import animation
from matplotlib.mlab import griddata


def costColorPlot(name, wha):
    xt = 0
    yt = 0.6175
    x0 = [-0.2,-0.1,0,0.1,0.2,-0.3,-0.2,-0.1,0,0.1,0.2,0.3]
    y0 = [0.39,0.39,0.39,0.39,0.39,0.26,0.26,0.26,0.26,0.26,0.26,0.26]
    
    fr = FileReading()
    if wha == "rbfn":
        z = fr.getobjread(name)
        z = np.array(z)
        maxz = np.max(z)
        minz = np.min(z)
    elif wha == "brent":
        z = fr.getobjread("trajectoires_cout/trajectoire_coutXBIN")
        z = np.array(z)
        xy0tmp = fr.recup_pos_ini()
        x0 = []
        y0 = []
        for el in xy0tmp.values():
            x0.append(el[0])
            y0.append(el[1])
        maxz = np.max(z)
        minz = np.min(z)
    zb = (z-minz)/(maxz - minz)
    xi = np.linspace(-0.40,0.40,100)
    yi = np.linspace(0.1,0.5,100)
    zi = griddata(x0, y0, zb, xi, yi)
    
    fig = plt.figure()
    t1 = plt.scatter(x0, y0, c=z, marker=u'o', s=200, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c ='g', marker='v', s=200)
    CS = plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(t1, shrink=0.5, aspect=5)
    
    plt.show(block = True)

####################################################################################
############ Fonction pour afficher les activations musculaires U ##################
####################################################################################
def plotActivationMuscular(what, nbfeat):
    fr = FileReading()
    if what == "brent":
        #BrentBVPSolver activations muscular
        fr.recup_data(1)
        j = 0
        traj = {}
        trajIte = {}
        trajVal = {}
        #Récupération des activations musculaires de chaque trajectoire
        for i in range(len(fr.data_store)):
            if str("trajectoire" + str(i) + "_command") in fr.data_store.keys():
                traj[str("trajectoire" + str(i) + "_command")] = fr.data_store[str("trajectoire" + str(i) + "_command")]
                j += 1
        j = 0
        trajValTmp = {}
        for i in range(6*12):
            trajValTmp[i] = []
        u = 0
        l = 0
        for i in range(len(traj)):
            trajiteTmp = []
            if not str("trajectoire" + str(i+1+l) + "_command") in traj.keys():  
                l += 1
            for k in range(len(traj[str("trajectoire" + str(i+1+l) + "_command")])):
                trajiteTmp.append(k)
                for t in range(6):
                    trajValTmp[t+u].append((traj[str("trajectoire" + str(i+1+l) + "_command")])[k][t])
            u += 6
            trajIte[j] = trajiteTmp
            #trajVal[j] = trajValTmp
            j += 1
        u = 0
        for i in range(len(traj)):
            brent = plt.Figure()
            for j in range(6):
                plt.plot(trajIte[i], trajValTmp[j+u])
            u += 6
            plt.show(block = True)
    elif what == "RBFN":
        ch = input("Voulez vous afficher les activations musculaires avec bruit?(Y or N): ")
        trajIteU = {}
        trajVal = {}
        for i in range(6*12):
            trajVal[i] = []
        u = 0
        for i in range(12):
            trajIteU[i] = []
            if ch == "N":
                nameU = "RBFN2/" + str(nbfeat) + "feats/MuscularActivation/ActiMuscuTrajectoireX" + str(i+1)
            elif ch == "Y":
                nameU = "RBFN2/" + str(nbfeat) + "feats/MuscularActivation/ActiMuscuNoiseTrajectoireX" + str(i+1)
            ut1 = fr.getobjread(nameU)
            for j in range(len(ut1)):
                trajIteU[i].append(j)
                for t in range(6):
                    trajVal[t+u].append(ut1[j][t])
            u += 6
        u = 0
        for i in range(12):
            rbfn = plt.Figure()
            for j in range(6):
                plt.plot(trajIteU[i], trajVal[j+u])
            u += 6
            plt.show(block = True)

    
def plotAnimationTraj(what):
    fr = FileReading()
    if what == "RBFN":
        for i in range(12):
            save = SavingData()
            nameCoordEL = "RBFN2/2feats/CoordTraj/CoordTrajectoireEL" + str(i+1)
            nameCoordHA = "RBFN2/2feats/CoordTraj/CoordTrajectoireHA" + str(i+1)
            coordEL = fr.getobjread(nameCoordEL)
            coordHA = fr.getobjread(nameCoordHA)
            save.createCoord(2, coordHA, coordEL)
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
            
            ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(save.xEl), blit=True, interval=20, repeat=True)
            plt.show(block=True)
    

def plot_pos_ini():
    fr = FileReading()
    xy = fr.recup_pos_ini()
    x = []
    y = []
    for el in xy.values():
        x.append(el[0])
        y.append(el[1])
    plt.figure()
    c = np.linspace(0,1,len(x))
    plt.scatter(x, y, c = c, marker=u'o', s=25, cmap=cm.get_cmap('RdYlBu'))
    plt.show(block = True)


#plotActivationMuscular("brent")    
#plotActivationMuscular("RBFN")
#plotAnimationTraj("RBFN")






