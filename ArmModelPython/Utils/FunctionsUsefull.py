from Utils.InitUtil import initFRRS
from Utils.NiemRoot import tronquerNB
import numpy as np
from Utils.FileSaving import fileSavingBin, fileSavingStr
from Utils.FileReading import FileReading
import os
from shutil import copyfile
from posix import remove
import matplotlib.pyplot as plt
from ArmModel.GeometricModel import mgi, mgd
from scipy.spatial import ConvexHull
import math
from Utils.ThetaNormalization import normalization, matrixToVector,\
    vectorToMatrix, unNorm
from Optimisation.LaunchTrajectories import LaunchTrajectories
from matplotlib.mlab import griddata
from matplotlib import cm
from Script.RunTrajectories import saveAllDataTrajectories
import timeit
import matplotlib.patches as patches
from Utils.ReadSetupFile import ReadSetupFile



def returnX0Y0Z(name):
    fr, rs = initFRRS()
    zdico = fr.getobjread(name + "costTrajRBFNBIN")
    xAbn, yAbn, zWithoutAbn, xyAbn, valcost = [], [], [], [], []
    for key,el in zdico.items():
        if not el < 200:
            xAbn.append(tronquerNB(float(key.split("//")[0]), 3))
            yAbn.append(tronquerNB(float(key.split("//")[1]), 3))
            xyAbn.append((tronquerNB(float(key.split("//")[0]), 3), tronquerNB(float(key.split("//")[1]), 3)))
            valcost.append(el-rs.rhoCF)
        else:
            zWithoutAbn.append(el)
    x0, y0 = [], []
    for el in xyAbn:
        x0.append(el[0])
        y0.append(el[1])
    z = valcost
    if not z:
        x0 = []
        y0 = []
        posi = fr.getobjread(rs.experimentFilePosIni)
        for el in posi:
            x0.append(el[0])
            y0.append(el[1])
        z = fr.getobjread(name + "costBIN")
    return x0, y0, z


def returnDifCostBrentRBFN():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/"
    RBFN = fr.getobjread(name + "costTrajBIN")
    Brent = fr.getobjread("trajectoires_cout/trajectoire_coutCoordXBIN")
    dataRBFN, dataBrent, xyRBFN, xyBrent = [], [], [], []
    for el in Brent:
        dataBrent.append((el[2], el[3], el[1]))
        xyBrent.append((el[2], el[3]))
    for key, el in RBFN.items():
        dataRBFN.append((tronquerNB(float(key.split("//")[0]), 3), tronquerNB(float(key.split("//")[1]), 3), el))
        xyRBFN.append((tronquerNB(float(key.split("//")[0]), 3), tronquerNB(float(key.split("//")[1]), 3)))
    difAllPts = []
    for el in xyBrent:
        if el in xyRBFN:
            a = np.abs(dataBrent[xyBrent.index(el)][2] - dataRBFN[xyRBFN.index(el)][2])
            difAllPts.append((el[0], el[1], a))
    fileSavingStr(name + "difCostBrentRBFN", difAllPts)
    fileSavingBin(name + "difCostBrentRBFNBIN", difAllPts)
    return difAllPts

def checkForDoublonInTraj(localisation):
    '''
    
    Input:    -localisation: String, path given the folder where the trajectories are
    '''
    fr = FileReading()
    data, junk = fr.recup_pos_ini(localisation)
    tabEl, doublon = [], []
    for key, el in data.items():
        if el in tabEl:
            doublon.append(key)
            #copyfile(localisation + key, localisation + "doublon/" + key)
            #remove(localisation + key)
        else:
            tabEl.append(el)
    print("ici", len(doublon), doublon)
    c = input("cc")
    print("la", len(tabEl), tabEl)


#checkForDoublonInTraj("/home/beucher/workspace/Data/ThetaAllTraj/")

def playWithTraj():
    fr, rs = initFRRS()
    data, junk = fr.recup_pos_ini(rs.pathFolderTrajectories)
    x, y, x1, y1 = [], [], [], []
    todel = []
    for key, el in data.items():
        if el[0] > -0.25 and el[0] < 0.2499 and el[1] > 0.271: 
            x.append(el[0])
            y.append(el[1])
        else:
            x1.append(el[0])
            y1.append(el[1])
            todel.append(key)
            #remove(rs.pathFolderTrajectories + key)
    print(len(todel), todel)
    print(np.max(x), np.min(x), np.min(y))
    #print(np.max(x1), np.min(x1), np.min(y1))
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(x1, y1, c = 'r')
    plt.show(block = True)


#playWithTraj()    

def posCircle(r, t):
    '''
    give coordinate (x,y) from couple (radius, angle)
    
    Input:      -r: scalar, radius of the circle
                -t: scalar, angle
    
    Output:    -x: scalar, ordinate
                -y: scalar, absciss
    '''
    fr, rs = initFRRS()
    x0 = 0
    y0 = rs.targetOrdinate
    x = x0 + r * math.cos(t)
    y = y0 + r * math.sin(t)
    return x, y

def invPosCircle(x, y):
    '''
    give couple (radius, angle) from coordinate (x, y), here the center of the circle is (0, yt) (yt = 0.6175)
    
    Input:      -x: scalar, ordinate
                -y: scalar, absciss
    
    Output:     -r: scalar, radius of the circle
                -t: scalar, angle
    '''
    fr, rs = initFRRS()
    r = math.sqrt((x**2) + (y - rs.targetOrdinate)**2)
    t = math.atan2(y - rs.targetOrdinate, x)
    return r, t

        
def learningFieldRBFN():
    fr, rs = initFRRS()
    posIni = fr.getobjread(rs.experimentFilePosIni)
    x, y = [], []
    for el in posIni:
        x.append(el[0])
        y.append(el[1])
        
    r, ang = [], []
    for el in posIni:
        a, b = invPosCircle(el[0], el[1])
        a, b = round(a, 2), round(b, 3)
        r.append(a)
        ang.append(b)
    
    #print(r)
    #print(ang)
    xy, junk = fr.recup_pos_ini(rs.pathFolderTrajectories)
    sx, sy = [], []
    for key, val in xy.items():
        rr, tt = invPosCircle(val[0], val[1])
        rr, tt = round(rr, 2), round(tt, 3)
        if rr <= (np.max(r) + (abs(r[1] - r[0]))) and rr >= (np.min(r) - (r[1] - r[0])) and tt >= (np.min(ang) - abs(ang[1] - ang[0])) and tt <= (np.max(ang) + abs(ang[1] - ang[0])):
            sx.append(val[0])
            sy.append(val[1])
        else:
            pass
            #copyfile(rs.pathFolderTrajectories + key, rs.pathFolderData + "/trajNotUsedTmp/" + key)
            #remove(rs.pathFolderTrajectories + key)
    
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(sx, sy, c = 'r')
    plt.show(block = True)
    
#learningFieldRBFN()    

def learningFieldRBFNSquare():
    fr, rs = initFRRS()
    posIni = fr.getobjread(rs.experimentFilePosIni)
    x, y = [], []
    for el in posIni:
        x.append(el[0])
        y.append(el[1])
    xy, junk = fr.recup_pos_ini(rs.pathFolderTrajectories)
    sx, sy = [], []
    for key, val in xy.items():
        if val[0] <= (np.max(x) + 0.02) and val[0] >= (np.min(x) - 0.02) and val[1] >= (np.min(y) - 0.01) and val[1] <= (np.max(y) + 0.02):
            sx.append(val[0])
            sy.append(val[1])
        else:
            pass
            #copyfile(rs.pathFolderTrajectories + key, rs.pathFolderData + "/trajNotUsedTmp/" + key)
            #remove(rs.pathFolderTrajectories + key)
    
    plt.figure()
    plt.scatter(x, y, c = 'b')
    plt.scatter(sx, sy, c = 'r')
    plt.show(block = True)
    
#learningFieldRBFNSquare()

def remakeTrajFolder():
    fr, rs = initFRRS()
    for el in os.listdir(rs.pathFolderData + "/trajNotUsedTmp/"):
        copyfile(rs.pathFolderData + "/trajNotUsedTmp/" + el, rs.pathFolderTrajectories + el)
        remove(rs.pathFolderData + "/trajNotUsedTmp/" + el)
    
#remakeTrajFolder()
    
def testOnWeight():
    fr, rs = initFRRS()
    cf = LaunchTrajectories()
    name = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread(name + "ThetaXBIN")
    thetaN = normalization(theta)
    for i in range(thetaN.shape[0]):
        for j in range(thetaN.shape[1]):
            thetaN[i,j] = thetaN[i,j] - np.random.normal(0,0.000001)
    
    thetaN = matrixToVector(thetaN)
    theta2 = vectorToMatrix(thetaN)
    
    theta2 = unNorm(theta2)
    sti, meanJu = cf.LaunchTrajectoriesRBFN(theta2)
    fileSavingBin(name + "costTrajChangedBIN", sti.costSave)
    
    costBefore = fr.getobjread(name + "costTrajBIN")
    costAfter = fr.getobjread(name + "costTrajChangedBIN")
    
    xb, yb, zb, xa, ya, za, xy = [],[], [], [], [], [], []
    for key, val in costBefore.items():
        xb.append(float(key.split("//")[0]))
        yb.append(float(key.split("//")[1]))
        zb.append(val)
    for key, val in costAfter.items():
        xa.append(float(key.split("//")[0]))
        ya.append(float(key.split("//")[1]))
        za.append(val)
        xy.append((float(key.split("//")[0]), float(key.split("//")[1])))
    difBA = []
    for i in range(len(zb)):
        difBA.append(tronquerNB(abs(zb[i] - za[i]), 4))
    print(difBA)
    
    xi = np.linspace(-0.18, 0.18, 100)
    yi = np.linspace(0.38, 0.5, 100)
    arrXY = np.array(xy)
    hull = ConvexHull(arrXY)
    zh = griddata(xb, yb, difBA, xi, yi)
    
    fig = plt.figure()
    plt.scatter(xa, ya, c = 'b')
    plt.plot(arrXY[hull.vertices, 0], arrXY[hull.vertices, 1], color = 'r')
    cs = plt.contourf(xi, yi, zh, 15, cmap=cm.get_cmap('RdYlBu'))
    fig.colorbar(cs, shrink=0.5, aspect=5)
    plt.show(block = True)
    
#testOnWeight()

def cmaesCostProgression():
    fr, rs = initFRRS()
    costCma = {}
    for i in range(len(rs.sizeOfTarget)):
        name = "OptimisationResults/costEvalAll/costEval" + str(rs.sizeOfTarget[i]) + str(6000)
        costCma[str(str(i) + "_" + str(rs.sizeOfTarget[i]))] = fr.getobjread(name)
    costEvo = {}
    for key, val in costCma.items():
        #val.reverse()
        costArray = np.asarray(val).reshape(rs.maxIterCmaes, rs.popsizeCmaes)
        costEvo[key] = np.mean(costArray, axis = 1)
    y = []
    for i in range(rs.maxIterCmaes):
        y.append(i)
    f, ax = plt.subplots(len(rs.sizeOfTarget), sharex = True)
    for key, x in costEvo.items():
        ax[int(key.split("_")[0])].plot(y, x)
        ax[int(key.split("_")[0])].set_title(str("Target " + key.split("_")[1]))
    plt.show(block = True)
        
#cmaesCostProgression()

def evaluateTheta():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/"
    a = 0
    for el in os.listdir(rs.pathFolderData + name):
        if "ThetaX" in el:
            a += 1
    a = int(a / 2) - 1
    for i in range(a):
        nameTmp = name + "ThetaX" + str(i) + "BIN"
        theta = fr.getobjread(nameTmp)
        nameT = name + "EvaluationOFTheta/Sol" + str(i) + str("/")
        if os.path.isdir(rs.pathFolderData + nameT) == False:
            os.mkdir(rs.pathFolderData + nameT)
        cf = LaunchTrajectories()
        sti, meanJu = cf.LaunchTrajectoriesRBFN(theta)
        saveAllDataTrajectories(nameT, sti, meanJu)
        
#evaluateTheta()

def plotCostColorMapForAllTheta():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/EvaluationOFTheta/"
    xi = np.linspace(-0.25,0.25,100)
    yi = np.linspace(0.35,0.5,100)
    for el in os.listdir(rs.pathFolderData + name):
        nameTmp = name + el + "/"
        x0, y0, z = returnX0Y0Z(nameTmp)
        zi = griddata(x0, y0, z, xi, yi)
        fig = plt.figure()
        t1 = plt.scatter(x0, y0, c=z, marker=u'o', s=50, cmap=cm.get_cmap('RdYlBu'))
        plt.scatter(0, rs.targetOrdinate, c ='g', marker='v', s=200)
        plt.contourf(xi, yi, zi, 15, cmap=cm.get_cmap('RdYlBu'))
        fig.colorbar(t1, shrink=0.5, aspect=5)
        plt.show(block = True)
        
        
#plotCostColorMapForAllTheta()

def plotTrajWhenTargetNotReach():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/costTrajRBFNBIN"
    data = fr.getobjread(name)
    xr, xnr, yr, ynr = [], [], [], []
    for key, val in data.items():
        if val <= 280:
            xnr.append(float(key.split("//")[0]))
            ynr.append(float(key.split("//")[1]))
        else:
            xr.append(float(key.split("//")[0]))
            yr.append(float(key.split("//")[1]))
    plt.figure()
    plt.scatter(xr, yr, c = 'b')
    plt.scatter(xnr, ynr, c = 'r')
    plt.show(block = True)
    
#plotTrajWhenTargetNotReach()

def getTimeDistance(sizeTarget):
    fr, rs = initFRRS()
    name = "OptimisationResults/ResCma" + str(sizeTarget) + "/ResCfb/nbIteCmaBIN"
    #name = "RBFN2/" + str(rs.numfeats) + "feats/nbIteRBFN" + str(sizeTarget) + "BIN"
    nbIteTraj = fr.getobjread(name)
    distTimeDico = {}
    for key, val in nbIteTraj.items():
        nbIteTraj[key] = int(np.mean(nbIteTraj[key]))
        r, t = invPosCircle(float(key.split("//")[0]), float(key.split("//")[1]))
        r = round(r, 2)
        if not r in distTimeDico.keys():
            distTimeDico[r] = []
        distTimeDico[r].append(nbIteTraj[key])
    distTime = []
    for key, val in distTimeDico.items():
        distTimeDico[key] = int(np.mean(distTimeDico[key]))
        distTime.append((key, distTimeDico[key]))
    return distTime

#getTimeDistance(0.02)

def getTimeVariationForEachDistance(sizeTarget):
    fr, rs = initFRRS()
    name = "OptimisationResults/ResCma" + str(sizeTarget) + "/nbItecp5CmaBIN"
    nbIteTraj = fr.getobjread(name)
    distTimeDico = {}
    for key, val in nbIteTraj.items():
        nbIteTraj[key] = int(np.mean(nbIteTraj[key]))
        r, t = invPosCircle(float(key.split("//")[0]), float(key.split("//")[1]))
        r, t = round(r, 2), round(t, 3)
        if not r in distTimeDico.keys():
            distTimeDico[r] = []
        distTimeDico[r].append((nbIteTraj[key], t))
    print(distTimeDico)
    
    plt.figure()
    for key, val in distTimeDico.items():
        for el in val:
            plt.scatter(el[1], el[0])
        break
    plt.show(block = True)
    
#getTimeVariationForEachDistance(0.1)

def evalCostVariation(sizeT):
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/costArrayAll/costArrayBIN" + str(sizeT)
    costArr = fr.getobjread(name)
    print(costArr.shape)
    lineCost = {}
    for i in range(costArr.shape[0]):
        lineCost[i] = costArr.T[i]
    t = []
    for i in range(costArr.shape[0]):
        t.append(i)
    plt.figure()
    for i in range(costArr.shape[0]):
        plt.plot(t, lineCost[i])
        plt.show(block = True)
    
#evalCostVariation(0.02)

def plotExperimentSetup():
    fr, rs = initFRRS()
    q1 = np.linspace(-0.6, 2.6, 100, True)
    q2 = np.linspace(-0.2, 3, 100, True)
    posIni = fr.getobjread(rs.experimentFilePosIni)
    xi, yi = [], []
    xb, yb = [0], [0]
    t = 0
    for el in posIni:
        if el[1] == np.min(posIni, axis = 0)[1] and t == 0:
            t += 1
            a, b = mgi(el[0], el[1], 0.3, 0.35)
            a1, b1 = mgd(np.array([[a], [b]]), 0.3, 0.35)
            xb.append(a1[0])
            xb.append(b1[0])
            yb.append(a1[1])
            yb.append(b1[1])
        xi.append(el[0])
        yi.append(el[1])
    pos = []
    for i in range(len(q1)):
        for j in range(len(q2)):
            coordEl, coordHa = mgd(np.array([[q1[i]], [q2[j]]]), 0.3, 0.35)
            pos.append(coordHa)
    x, y = [], []
    for el in pos:
        x.append(el[0])
        y.append(el[1])
    plt.figure()
    plt.scatter(x, y)
    plt.scatter(xi, yi, c = 'r')
    plt.scatter(0, 0.6175, c = "r", marker=u'*', s = 200)
    plt.plot(xb, yb, c = 'r')
    plt.plot([-0.3,0.3], [0.6175, 0.6175], c = 'g')
    plt.show(block = True)
    
#plotExperimentSetup()


def testNPDOT():
    try:
        import numpy.core._dotblas
        print ('FAST BLAS')
    except ImportError:
        print ('slow blas')
     
    print ("version:", numpy.__version__)
    #print ("maxint:", sys.maxint)
    #print
     
    x = numpy.random.random((1000,1000))
     
    setup = "import numpy; x = numpy.random.random((1000,1000))"
    count = 5
     
    t = timeit.Timer("numpy.dot(x, x.T)", setup=setup)
    print ("dot:", t.timeit(count)/count, "sec")

#testNPDOT()
        
def getDataScattergram(sizeT):
    fr, rs = initFRRS()
    name = "OptimisationResults/ResCma" + str(sizeT) + "/ResCfb/hitDispersion0.1_0.4175BIN"
    coordHit = fr.getobjread(name)
    for key, val in coordHit.items():
        xByPosIni = [x[0] for x in val]
    return xByPosIni
    
    
def plotScattergram():
    rs = ReadSetupFile()
    s = 0
    for i in range(len(rs.sizeOfTarget)):
        dataTmp = getDataScattergram(rs.sizeOfTarget[i])
        if s == 0:
            s += 1
            data = np.asarray(dataTmp)
        else:
            data = np.hstack((data, np.asarray(dataTmp)))
    plt.figure()
    plt.hist(data, 20)
    plt.show(block = True)

#plotScattergram()

def getDistPerfSize(sizeT):
    fr, rs = initFRRS()
    name = "OptimisationResults/ResCma" + str(sizeT) + "/ResCfb/actiMuscuCmaBIN"
    data = fr.getobjread(name)
    DistPerf = {}
    for key, val in data.items():
        r, t = invPosCircle(float(key.split("//")[0]), float(key.split("//")[1]))
        r = round(r, 2)
        if not r in DistPerf.keys():
            DistPerf[r] = []
        DistPerf[r].append(np.mean(val))
    for key, val in DistPerf.items():
        DistPerf[key] = np.mean(val)
    sizeDistPerf = []
    for key, val in DistPerf.items():
        sizeDistPerf.append((sizeT, key, val))
    return sizeDistPerf
    
#getDistPerfSize(0.02)


def plotScattergram2():
    fr, rs = initFRRS()
    data = {}
    for i in range(len(rs.sizeOfTarget)):
        data[rs.sizeOfTarget[i]] = getDataScattergram(rs.sizeOfTarget[i])
    print(data)
            
    plt.figure(1, figsize=(16,9))
    #fig, (ax1, ax2, ax3, ax4) = plt.subplots(len(rs.sizeOfTarget), sharex = True, sharey = True)
    ax1 = plt.subplot2grid((2,2), (0,0))
    ax1.hist(data[rs.sizeOfTarget[0]], 20)
    ax1.plot([-rs.sizeOfTarget[0], -rs.sizeOfTarget[0]], [0, 20], c = 'r', linewidth = 3)
    ax1.plot([rs.sizeOfTarget[0], rs.sizeOfTarget[0]], [0, 20], c = 'r', linewidth = 3)
    ax1.set_title(str("HitDispersion for Target " + str(rs.sizeOfTarget[0])))
    
    ax2 = plt.subplot2grid((2,2), (0,1))
    ax2.hist(data[rs.sizeOfTarget[1]], 20)
    ax2.plot([-rs.sizeOfTarget[1], -rs.sizeOfTarget[1]], [0, 20], c = 'r', linewidth = 3)
    ax2.plot([rs.sizeOfTarget[1], rs.sizeOfTarget[1]], [0, 20], c = 'r', linewidth = 3)
    ax2.set_title(str("HitDispersion for Target " + str(rs.sizeOfTarget[1])))
    
    ax3 = plt.subplot2grid((2,2), (1,0))
    ax3.hist(data[rs.sizeOfTarget[2]], 20)
    ax3.plot([-rs.sizeOfTarget[2], -rs.sizeOfTarget[2]], [0, 20], c = 'r', linewidth = 3)
    ax3.plot([rs.sizeOfTarget[2], rs.sizeOfTarget[2]], [0, 20], c = 'r', linewidth = 3)
    ax3.set_title(str("HitDispersion for Target " + str(rs.sizeOfTarget[2])))
    
    ax4 = plt.subplot2grid((2,2), (1,1))
    ax4.hist(data[rs.sizeOfTarget[3]], 20)
    ax4.plot([-rs.sizeOfTarget[3], -rs.sizeOfTarget[3]], [0, 20], c = 'r', linewidth = 3)
    ax4.plot([rs.sizeOfTarget[3], rs.sizeOfTarget[3]], [0, 20], c = 'r', linewidth = 3)
    ax4.set_title(str("HitDispersion for Target " + str(rs.sizeOfTarget[3])))
    
    plt.show(block = True)
    
#plotScattergram2()
        
        

