#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: GlobalVariables

Description: global variables used in the project
'''

import os

pathWorkingDirectory = os.getcwd()
'''if not os.path.isdir(pathWorkingDirectory):
    usrName = os.getlogin()
    pathWorkingDirectory = pathWorkingDirectory.replace('//', '')'''
pathListForm = pathWorkingDirectory.split("/")
pathDataFolder = pathWorkingDirectory.replace(pathListForm[len(pathListForm)-1], '') + "Data/"
pathTrajectoriesFolder = pathDataFolder + "trajectoires/"

print(pathDataFolder)