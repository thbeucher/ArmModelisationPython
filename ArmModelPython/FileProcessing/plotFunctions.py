import numpy as np
import matplotlib.pyplot as plt
from FileProcessing.FileReading import FileReading

def plotActivationMuscular():
    
    #BrentBVPSolver activations muscular
    fr = FileReading()
    fr.recup_data(0)
    j = 0
    i = 1
    traj = {}
    trajIte = {}
    trajVal = {}
    for el in fr.data_store.values():
        if str("trajectoire" + str(i) + "_command") in fr.data_store.keys():
            traj[j] = el
            j += 1
        i += 1
    j = 0
    print(traj)
    for el in traj.values():
        print(el)
        trajiteTmp = []
        trajValTmp = []
        for i in range(len(el)):
            trajiteTmp.append(i)
            trajValTmp.append(el[i])
        trajIte[j] = trajiteTmp
        trajVal[j] = trajValTmp
        j += 1
    for i in range(len(traj)):
        brent = plt.Figure()
        plt.plot(trajIte[i], trajVal[i])
    plt.show()
    
    
plotActivationMuscular()
