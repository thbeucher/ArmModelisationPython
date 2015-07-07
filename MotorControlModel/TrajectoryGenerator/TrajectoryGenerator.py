'''
Author: Thomas Beucher

Module: TrajectoryGenerator

Description: Class to generate a trajectory
'''
from Utils.StateVectorUtil import getDotQAndQFromStateVectorS, createStateVector
from ArmModel.GeometricModel import mgd, mgi
from Utils.CreateVectorUtil import createVector


class TrajectoryGenerator:
    
    def __init__(self):
        self.name = "TrajectoryGenerator"
        
    def initParametersTG(self, armP, rs, nsc, cc, sizeOfTarget, Ukf, armD, mac):
	'''
	Initializes the parameters used to run the functions below

	Inputs:		-armP, armParameters, class object
			-rs, readSetup, class object
			-nsc, nextStateComputation, class object
			-cc, costComputation, class object
			-sizeOfTarget, size of the target, float
			-Ukf, unscented kalaman filter, class object
			-armD, armDynamics, class object
			-mac, muscularActivationCommand, class object
	'''
        self.armP = armP
        self.rs = rs
        self.nsc = nsc
        self.cc = cc
        self.sizeOfTarget = sizeOfTarget
        self.Ukf = Ukf
        self.armD = armD
        self.mac = mac
    
    def runTrajectory(self, x, y):
	'''
	Generates trajectory from the initiale position (x, y)

	Inputs:		-x: absciss of the initiale position, float
			-y: ordinate of the initiale position, float

	Output:		-cost: the cost of the trajectory, float
	'''
	#computation of the articular position q1, q2 from the initiale coordinates (x, y)
        q1, q2 = mgi(x, y, self.armP.l1, self.armP.l2)
	#create the position vector [q1, q2]
        q = createVector(q1, q2)
	#create the speed vector [dotq1, dotq2]
        dotq = createVector(0., 0.)
	#create the state vector [dotq1, dotq2, q1, q2]
        state = createStateVector(dotq, q)
	#compute the coordinates of the hand and the elbow from the position vector
        coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
	#initializes parameters for the trajectory
        i, t, cost = 0, 0, 0
        self.Ukf.initObsStore(state)
        self.armD.initStateAD(state)
        #loop to generate next position until the target is reached 
        while coordHand[1] < self.rs.targetOrdinate:
	    #stop condition to avoid infinite loop
            if i < self.rs.numMaxIter:
		#computation of the next muscular activation vector
                Ucontrol = self.mac.getCommandMAC(state)
		#computation of the arm state
                realState = self.armD.mddAD(Ucontrol)
		#computation of the approximated state
                state = self.Ukf.runUKF(Ucontrol, realState)
		#computation of the cost
                cost = self.cc.computeStateTransitionCost(cost, Ucontrol, t)
		#get dotq and q from the state vector
                dotq, q = getDotQAndQFromStateVectorS(state)
		#computation of the coordinates to check if the target is reach or not
                coordElbow, coordHand = mgd(q, self.armP.l1, self.armP.l2)
            else:
                break
            i += 1
            t = self.rs.dt
	#check if the target is reach and give the reward if yes
        if coordHand[0] >= -self.sizeOfTarget/2 and coordHand[0] <= self.sizeOfTarget/2 and coordHand[1] >= self.rs.targetOrdinate:
            cost = self.cc.computeFinalCostReward(cost, t)
	#return the cost of the trajectory
        return cost
    
    
    
    
    
