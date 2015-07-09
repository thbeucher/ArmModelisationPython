'''
Author: Thomas Beucher

Module: InitUtil

Description: We find here function which give acces to some class
'''
'''import sys
from GlobalVariables import pathWorkingDirectory
sys.path.append(pathWorkingDirectory + "/Utils")'''

from Utils.FileReading import FileReading
from Utils.ReadSetupFile import ReadSetupFile


def initFRRS():
    '''
	Initializes class object FileReading and ReadSetup
	'''
    fr = FileReading()
    rs = ReadSetupFile()
    return fr, rs