'''
Author: Thomas Beucher

Module: testOnKalman

Description: 
'''

import matplotlib.pyplot as plt

def testLastKalman():
    fr, rs = initFRRS()
    tgs = initAllUsefullObj(rs.sizeOfTarget[3], fr, rs)
    x, y = 0.1, 0.35
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    tgs.mac.setThetaMAC(theta)
    cost = tgs.tg.runTrajectory(x, y)
    for val in tgs.tg.SaveCoordWK.values():
        coordXY = val
    plt.figure()
    plt.plot([x[0] for x in coordXY], [y[1] for y in coordXY])
    plt.show(block = True)

#testLastKalman()
    
def testNewKalman():
    fr, rs = initFRRS()
    tgs = initAllUsefullObj(rs.sizeOfTarget[3], fr, rs)
    x, y = 0.1, 0.35
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    tgs.mac.setThetaMAC(theta)
    
    ii, saveD = 5, {}
    for i in range(5):
        tgs.tg.Ukf.setDelayUKF(ii)
        cost = tgs.tg.runTrajectory(x, y)
        for key, val in tgs.tg.SaveCoordVerif.items():
            WK = [el for el in val]
            UKF = [el for el in tgs.tg.SaveCoordUKF[key]]
        difTab = []
        for el1, el2 in zip(WK, UKF):
            a = np.sqrt((el1[0] - el2[0])**2 + (el1[1] - el2[1])**2)
            difTab.append(a)
        t = [i for i in range(len(difTab))]
        WKx, WKy, UKFx, UKFy = [x[0] for x in WK], [y[1] for y in WK], [x[0] for x in UKF], [y[1] for y in UKF]
        saveD[ii] = (WKx, WKy, UKFx, UKFy, difTab, t)
        ii += 5
    
    for key, val in saveD.items():
        print("key: ", key, " last yWK: ", val[1][len(val[1])-1], " last yUKF: ", val[3][len(val[3])-1])
    for key, val in saveD.items():
        plt.figure()
        plt.plot(val[0], val[1], c = 'b')
        plt.plot(val[2], val[3], c = 'r')
    plt.figure()
    for key, val in saveD.items():
        plt.plot(val[5], val[4])
    plt.show(block = True)
        
        
#testNewKalman()
