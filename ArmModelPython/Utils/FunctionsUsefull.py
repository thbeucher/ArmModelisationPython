from Utils.InitUtil import initFRRS
from Utils.NiemRoot import tronquerNB
import numpy as np
from Utils.FileSaving import fileSavingBin, fileSavingStr
from Utils.FileReading import FileReading
import os
from shutil import copyfile
from posix import remove
import matplotlib.pyplot as plt
from ArmModel.GeometricModel import mgi
from scipy.spatial import ConvexHull
import math
from Utils.ThetaNormalization import normalization, matrixToVector,\
    vectorToMatrix, unNorm
from Optimisation.costFunction import costFunctionRBFN
from matplotlib.mlab import griddata
from matplotlib import cm



def returnX0Y0Z():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/"
    zdico = fr.getobjread(name + "costTrajBIN")
    xAbn, yAbn, zWithoutAbn, xyAbn, valcost = [], [], [], [], []
    for key,el in zdico.items():
        if not el < 280:
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
    give couple (radius, angle) from coordinate (x, y)
    
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
    posIni = fr.getobjread("PosIniExperimentCircular")
    x, y = [], []
    for el in posIni:
        x.append(el[0])
        y.append(el[1])
        
    r, ang = [], []
    for el in posIni:
        a, b = invPosCircle(el[0], el[1])
        if not tronquerNB(a, 3) in r and not (tronquerNB(a, 3) + 0.001) in r and not (tronquerNB(a, 3) - 0.001) in r:
            r.append(tronquerNB(a, 3))
        if not tronquerNB(b, 3) in ang:
            ang.append(tronquerNB(b, 3))
    
    #print(r)
    #print(ang)
    xy, junk = fr.recup_pos_ini(rs.pathFolderTrajectories)
    sx, sy = [], []
    for key, val in xy.items():
        rr, tt = invPosCircle(val[0], val[1])
        if rr <= (np.max(r) + (abs(r[1] - r[0]))) and rr >= (np.min(r) - (r[1] - r[0])) and tt >= (np.min(ang) - abs(ang[1] - ang[0])) and tt <= (np.max(ang) + abs(ang[1] - ang[0])):
            sx.append(val[0])
            sy.append(val[1])
        else:
            copyfile(rs.pathFolderTrajectories + key, rs.pathFolderData + "/trajNotUsedTmp/" + key)
            remove(rs.pathFolderTrajectories + key)
    
    #plt.figure()
    #plt.scatter(x, y, c = 'b')
    #plt.scatter(sx, sy, c = 'r')
    #plt.show(block = True)
    
#learningFieldRBFN()    

def remakeTrajFolder():
    fr, rs = initFRRS()
    for el in os.listdir(rs.pathFolderData + "trajUseForRBFNTmp/"):
        remove(rs.pathFolderData + "trajUseForRBFNTmp/" + el)
    
    for el in os.listdir(rs.pathFolderTrajectories):
        copyfile(rs.pathFolderTrajectories + el, rs.pathFolderData + "trajUseForRBFNTmp/" + el)
    
    for el in os.listdir(rs.pathFolderData + "/trajNotUsedTmp/"):
        copyfile(rs.pathFolderData + "/trajNotUsedTmp/" + el, rs.pathFolderTrajectories + el)
        remove(rs.pathFolderData + "/trajNotUsedTmp/" + el)
    
    
def testOnWeight():
    fr, rs = initFRRS()
    name = "RBFN2/" + str(rs.numfeats) + "feats/"
    theta = fr.getobjread(name + "ThetaXBIN")
    thetaN = normalization(theta)
    for i in range(thetaN.shape[0]):
        for j in range(thetaN.shape[1]):
            thetaN[i,j] = thetaN[i,j] - np.random.normal(0,0.000001)
    
    thetaN = matrixToVector(thetaN)
    theta2 = vectorToMatrix(thetaN)
    
    theta2 = unNorm(theta2)
    sti, meanJu = costFunctionRBFN(theta2)
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
        name = "OptimisationResults/costEval" + str(rs.sizeOfTarget[i])
        costCma[str(rs.sizeOfTarget[i])] = fr.getobjread(name)
    print(len(costCma))
    
cmaesCostProgression()
        




        