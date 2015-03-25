import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from FileProcessing.FileReading import FileReading
from ArmModel.SavingData import SavingData
from matplotlib import animation


def costColorPlot():
    xt = 0
    yt = 0.6175
    xo = [-0.2,-0.1,0,0.1,0.2,-0.3,-0.2,-0.1,0.,0.1,0.2,0.3]
    yo = [0.39,0.39,0.39,0.39,0.39,0.0325,0.0325,0.0325,0.0325,0.0325,0.0325,0.0325]
    zo = [0,-13908,-14449,-12625,-13531,0,-3663,-14358,0,0,-85982,-39388,0]
    #z = np.divide(zju, zju[10])
    #moy = np.dot(zju, np.array([1,1,1,1,1,1,1,1,1,1,1,1,1]).T)/8
    #for i in range(len(zju)):
        #if zju[i] == 0:
            #zju[i] = moy
    x1 = [-0.1,0,0.1,0.2,-0.2,-0.1,0.2,0.3]
    y1 = [0.39,0.39,0.39,0.39,0.0325,0.0325,0.0325,0.0325]
    z1 = [-13908,-14449,-12625,-13531,-3663,-14358,-85982,-39388]
    
    x2 = [-0.2,-0.1,0,0.1,0.2,-0.2,-0.1,0,0.2,0.3]
    y2 = [0.39,0.39,0.39,0.39,0.39,0.0325,0.0325,0.0325,0.0325,0.0325]
    z2 = [-14750,-13046,-15062,-19213,-22248,-22216,-20001,-10883,-23251,-25703]
    
    #rbfn3feats
    x3 = [-0.2,-0.1,0,0.1,-0.3,-0.2,-0.1]
    y3 = [0.39,0.39,0.39,0.39,0.0325,0.0325,0.0325]
    z3 = [-389118.9654470043, -52586.418821205392, -30077.157557982577, -36671.103639770852, -28344.344809749276, -76257.873404483442, -122648.18240195756]
    
    #rbfn2feats
    x4 = [-0.2,-0.1,0,0.1,0.2,-0.3,-0.2,-0.1,0.1,0.2,0.3]
    y4 = [0.39,0.39,0.39,0.39,0.39,0.0325,0.0325,0.0325,0.0325,0.0325,0.0325]
    z4 = [4476.5986069261062, 3548.932094627422, 2550.8052246753091, 2243.5188898035408, 3889.8187394899551, 9092.3997452895528, 9542.7502806432221, 7235.5788222904139, 6555.1901482250778, 6800.8533329513602, 9911.0973462760012]
    
    fig = plt.figure()
    t1 = plt.scatter(x4, y4, c=z4, marker=u'o', s=200, cmap=cm.get_cmap('RdYlBu'))
    plt.scatter(xt, yt, c ='g', marker='v', s=200)
    fig.colorbar(t1, shrink=0.5, aspect=5)
    
    plt.show()


def plotActivationMuscular(what):
    fr = FileReading()
    if what == "brent":
        #BrentBVPSolver activations muscular
        fr.recup_data(0)
        j = 0
        traj = {}
        trajIte = {}
        trajVal = {}
        for i in range(len(fr.data_store)):
            if str("trajectoire" + str(i) + "_command") in fr.data_store.keys():
                traj[str("trajectoire" + str(i) + "_command")] = fr.data_store[str("trajectoire" + str(i) + "_command")]
                j += 1
        j = 0
        trajValTmp = {}
        for i in range(6*10):
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
        trajIteU = {}
        trajVal = {}
        for i in range(6*12):
            trajVal[i] = []
        u = 0
        for i in range(12):
            trajIteU[i] = []
            nameU = "RBFN2/2feats/ActiMuscuTrajectoire" + str(i+1)
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
    
   
#plotActivationMuscular("brent")    
#plotActivationMuscular("RBFN")
plotAnimationTraj("RBFN")






