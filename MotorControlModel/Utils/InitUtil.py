#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Thomas Beucher

Module: InitUtil

Description: We find here function which give acces to some class
'''

from Utils.FileReading import FileReading
from Utils.ReadSetupFile import ReadSetupFile


def initFRRS():
    '''
	Initializes class object FileReading and ReadSetup
	'''
    fr = FileReading()
    rs = ReadSetupFile()
    return fr, rs