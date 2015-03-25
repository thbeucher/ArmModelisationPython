import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from FileProcessing.FileReading import FileReading


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


def plotActivationMuscular():
    
    #BrentBVPSolver activations muscular
    fr = FileReading()
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
    
    
plotActivationMuscular()
