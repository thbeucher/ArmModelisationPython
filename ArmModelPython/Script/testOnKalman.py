'''
==============================================
Using the Unscented Kalman Filter and Smoother
==============================================
This simple example shows how one may apply the Unscented Kalman Filter and
Unscented Kalman Smoother to some randomly generated data.
The Unscented Kalman Filter (UKF) and Rauch-Rung-Striebel type Unscented Kalman
Smoother (UKS) are a generalization of the traditional Kalman Filter and
Smoother to models with non-linear equations describing state transitions and
observation emissions. Unlike the Extended Kalman Filter (EKF), which attempts
to perform the same task by using the numerical derivative of the appropriate
equations, the UKF selects a handful of "sigma points", passes them through the
appropriate function, then finally re-estimates a normal distribution around
those propagated points. Experiments have shown that the UKF and UKS are
superior to the EKF and EKS in nearly all scenarios.
The figure drawn shows the true, hidden state; the state estimates given by the
UKF; and finally the same given by the UKS.
'''
import numpy as np
import pylab as pl
from pykalman import UnscentedKalmanFilter
from Main.GenerateTrajectory import GenerateTrajectory
from Utils.InitUtil import initFRRS
from Utils.FileSaving import fileSavingStr, fileSavingBin
import matplotlib.pyplot as plt
from Script.testAll import initAllUsefullObj

# initialize parameters
def transition_function(state, noise):
    a = np.sin(state[0]) + state[1] * noise[0]
    b = state[1] + noise[1]
    return np.array([a, b])

def observation_function(state, noise):
    C = np.array([[-1, 0.5], [0.2, 0.1]])
    return np.dot(C, state) + noise

def showUK():
    transition_covariance = np.eye(2)
    random_state = np.random.RandomState(0)
    observation_covariance = np.eye(2) + random_state.randn(2, 2) * 0.1
    initial_state_mean = [0, 0]
    initial_state_covariance = [[1, 0.1], [-0.1, 1]]
    
    # sample from model
    kf = UnscentedKalmanFilter(
        transition_function, observation_function,
        transition_covariance, observation_covariance,
        initial_state_mean, initial_state_covariance,
        random_state=random_state
    )
    states, observations = kf.sample(50, initial_state_mean)
    
    # estimate state with filtering and smoothing
    filtered_state_estimates = kf.filter(observations)[0]
    smoothed_state_estimates = kf.smooth(observations)[0]
    
    # draw estimates
    pl.figure()
    lines_true = pl.plot(states, color='b')
    lines_filt = pl.plot(filtered_state_estimates, color='r', ls='-')
    lines_smooth = pl.plot(smoothed_state_estimates, color='g', ls='-.')
    pl.legend((lines_true[0], lines_filt[0], lines_smooth[0]),
              ('true', 'filt', 'smooth'),
              loc='lower left'
    )
    pl.show()
    
    
#showUK()

def plotResultTestKalman(coord, coordKalman):
    #fr, rs = initFRRS()
    #coord = fr.getobjread("TEST/coordHATestBIN")
    #coordKalman = fr.getobjread("TEST/saveAllCoordTestBIN")
    difDist = []
    for key, val in coord.items():
        cR = val
        cK = coordKalman[key]
    for el1, el2 in zip(cR, cK):
        a = np.sqrt((el1[0] - el2[0])**2 + (el1[1] - el2[1])**2)
        difDist.append(a)
    t = []
    for i in range(len(difDist)):
        t.append(i)
    
    plt.figure()
    for key, val in coord.items():
        plt.plot([x[0] for x in val], [y[1] for y in val], c = 'b')
    for key, val in coordKalman.items():
        plt.plot([x[0] for x in val], [y[1] for y in val], c = 'r')
        
    plt.figure()
    plt.plot(t, difDist)
    plt.show(block = True)
    return (t, difDist)
    
#plotResultTestKalman()

def plotCov(gt):
    plt.figure()
    tt = []
    for key in gt.KM.saveCovariance.keys():
        keyy = key
        break
    plotCov = [x[0,0] for x in gt.KM.saveCovariance[keyy]]
    for i in range(len(plotCov)):
        tt.append(i)
    plt.figure()
    plt.plot(tt, plotCov)
    plt.show(block = True)
       
def testTrajKalman():
    fr, rs = initFRRS()
    gt = GenerateTrajectory()
    name = "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7BIN"
    theta = fr.getobjread(name)
    gt.setTheta(theta)
    xI, yI = 0.1, 0.35
    '''ii = 1
    difD = {}
    for i in range(6):
        np.savetxt("/home/beucher/workspace/Data/TEST/delay", [ii])
        ii += 5
        cost = gt.generateTrajectories(xI, yI)
        difD[i] = plotResultTestKalman(gt.coordEndEffector, gt.KM.saveAllCoord)
    
    plt.figure()
    for key, val in difD.items():
        plt.plot(val[0], val[1], label = key)
    plt.legend(loc = 0)
    plt.show(block = True)'''
    
    posIni = fr.getobjread(rs.experimentFilePosIni)
    np.savetxt("/home/beucher/workspace/Data/TEST/delay", [25])
    for el in posIni:
        try:
            cost = gt.generateTrajectories(el[0], el[0])
            plotResultTestKalman(gt.coordEndEffector, gt.KM.saveAllCoord)
            print("Success", el[0], el[1])
        except:
            print("fail", el[0], el[1])
            pass
        gt.initParamTraj()
    
    '''x = np.linspace(0.1, 0.5, 10)
    y = np.linspace(0.2, 0.5, 10)
    for i in range(len(x)):
        for j in range(len(y)):
            try:
                cost = gt.generateTrajectories(x[i], y[j])
                #fileSavingStr("TEST/coordHATest", gt.save.coordHaSave)
                #fileSavingStr("TEST/saveAllCoordTest", gt.KM.saveAllCoord)
                #fileSavingBin("TEST/coordHATestBIN", gt.save.coordHaSave)
                #fileSavingBin("TEST/saveAllCoordTestBIN", gt.KM.saveAllCoord)
                #fileSavingStr("TEST/coordEndEffectorTest", gt.coordEndEffector)
                #fileSavingBin("TEST/coordEndEffectorTestBIN", gt.coordEndEffector)
                plotResultTestKalman(gt.coordEndEffector, gt.KM.saveAllCoord)
            except:
                pass
            gt.initParamTraj()'''
    print("cout:", cost)
    
#testTrajKalman()

#Test New Kalman
def testNewKalman():
    fr, rs = initFRRS()
    tgs = initAllUsefullObj(rs.sizeOfTarget[3], fr, rs)
    x, y = 0.1, 0.35
    thetaLocalisation = rs.pathFolderData + "RBFN2/" + str(rs.numfeats) + "feats/ThetaX7NP"
    theta = np.loadtxt(thetaLocalisation)
    tgs.mac.setThetaMAC(theta)
    cost = tgs.tg.runTrajectory(x, y)
    print(tgs.tg.SaveCoordWK, "\n", tgs.tg.SaveCoordUKF)
    for key, val in tgs.tg.SaveCoordWK.items():
        WK = [el for el in val]
        UKF = [el for el in tgs.tg.SaveCoordUKF[key]]
    print(WK)
    difTab = []
    for el1, el2 in zip(WK, UKF):
        a = np.sqrt((el1[0] - el2[0])**2 + (el1[1] - el2[1])**2)
        difTab.append(a)
    t = [i for i in range(len(difTab))]
    plt.figure()
    plt.plot([x[0] for x in WK], [y[1] for y in WK], c = 'b')
    plt.plot([x[0] for x in UKF], [y[1] for y in UKF], c = 'r')
    plt.figure()
    plt.plot(t, difTab)
    plt.show(block = True)
        
        
testNewKalman()


    
    
    
