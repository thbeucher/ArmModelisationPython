'''
Author: Thomas Beucher

Module: GlobalVariables

Description: global variables used in the project
'''

import os

pathWorkingDirectory = os.getcwd()
pathListForm = pathWorkingDirectory.split("/")
pathDataFolder = pathWorkingDirectory.replace(pathListForm[4], '') + "Data/"
pathTrajectoriesFolder = pathDataFolder + "trajectoires/"