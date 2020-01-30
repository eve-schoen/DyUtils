# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 09:58:44 2019

@author: evesg
"""

import sys
import os
sys.path.append(os.path.join(os.getcwd(),"..\\Background Data"))
from AsciiGraph import AsciiGraph

def consolidate(pth):
    path = pth
    filePth = path +"\\"
    tCounts = [0] * 2048
    tTime = 0
    for file in os.listdir(path):
        if os.path.isdir(file):
            print("here")
            pass #ignore folders
        if file[-3:] == ".py":
            pass #ignore code files
        else:    
            graph = AsciiGraph(filePth + file)
            tCounts = [sum(i) for i in zip(tCounts,graph.getCounts())]
            tTime = tTime + graph.getTime()
    return (tCounts, tTime)

def partialConsolidate(pth, percent): #enter number 0-1 for percent of total directory you want
    filePth = pth +"\\"
    allFiles = sorted(os.listdir(pth), key = fileNumber)
    increment = int(len(allFiles)*percent)
    cntsAndTimes = []
    start = 0  
    while start + increment <= len(os.listdir(pth)): #I could make this one method with default percent = 1
        tCounts = [0] * 2048
        tTime = 0
        for file in allFiles[start: start+increment]: 
            if file[-3:] == ".py":
                pass #ignore code files
            else:  
                graph = AsciiGraph(filePth + file)
                print(filePth + file)
                tCounts = [sum(i) for i in zip(tCounts,graph.getCounts())]
                tTime = tTime + graph.getTime()
        cntsAndTimes.append((tCounts, tTime))
        start = start + increment
    return cntsAndTimes
            
#@staticmethod I'm confused why i don't need this
def fileNumber(fileName):
    numOf_ = fileName.count("_")
    for x in range(numOf_):
        start = fileName.index("_")
        fileName = fileName[start+1:]
    end = fileName.index(".")
    fileNum = fileName[:end]
    if fileNum.isdigit():
        return int(fileName[:end])
    else:
        print("No file number found on one file, -1 returned")
        return 100
