#!/usr/bin/env python
# -*- coding: utf-8 -*-
#cython: boundscheck=False, wraparound=False
'''
Author: Thomas Beucher

Module: InitUtil

Description: We find here function which give acces to some class
'''

from FileReading import FileReading
from ReadSetupFile import ReadSetupFile


def initFRRS():
    '''
	Initializes class object FileReading and ReadSetup
	'''
    fr = FileReading()
    rs = ReadSetupFile()
    return fr, rs
