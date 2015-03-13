#!/usr/local/bin/python
"""
-----Put your information here-----
    
    authors: "???", "???", "???"
    emails: "???", "???", "???"

-----------------------------------
"""

from Regression.functionApproximator import *
from Regression.functionApproximator_PlottingTools import *
from Regression.functionApproximator_LW import *



### Load data set to be approximated (for batch methods)
############################################################################


filename = './noisyDataSet.txt'
data = np.loadtxt(filename)


### Set up FA variables
############################################################################

# Number of features/basis functions used in the FA. (hint: 15 is a good starting point)
numFeats = 5#"""Tune me !""" 

# Indicated as "alpha" in the gradient descent method. Determines the "distance" traveled in the direction of the gradient for each step.
# (Only used in Gradient Descent)
# (Defaults to 0.01)
learningRate = 0.01#"""Tune me !"""

# Minimum change between thetas between two consecutive iterations. This is used as a convergence criterion.
# (Iterative methods only)
# (Defaults to 0.00001)
minDelta = 0.00001#"""Tune me !"""

# Maximum number of iterations used for training the FA 
# (Iterative methods only)
# (Defaults to 20000)
maxIteration = 100#"""Tune me !"""


### Setting up the FA and experimenting with different training methods
############################################################################


# Create the FA object called, "funcApprox", and initialize it with the FA variables set above.
funcApprox = fa(numFeats, learningRate, minDelta, maxIteration)

################################################################
### Train the FA with the 4 methods described in the handout ###
### just uncomment the training method you wish to test.      ###
################################################################

## Gradient Descent
#funcApprox.train_GD() #feat=17/lr=0.2/mD=0.00001/mI=40000

## Least Squares
funcApprox.train_LS(data)

## Recursive Least Squares
#funcApprox.train_RLS()

## Recursive Least Squares Version 2
#funcApprox.train_RLS2()


plotFA(funcApprox, data)
#animPlotFA(funcApprox, data)


# Create the Locally Weighted FA object called, "funcApproxLocal", and initialize it with the FA variables set above.
#funcApproxLocal = fa_lw(numFeats, minDelta, maxIteration)

#funcApproxLocal.train_LWLS(data)
#print("thethathetahtaht: ", funcApproxLocal.theta.shape, funcApproxLocal.theta)

#plotFA(funcApproxLocal, data)


