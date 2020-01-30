# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 16:23:08 2020

@author: Eve
"""

import sys
sys.path.append("C:\\Users\\mitadm\\Documents\\Documents\\UROP\\utils")
from AsciiGraph import AsciiGraph
#from findPeaksFunction import findPeaksExt, getPeakPeaks

def backgroundNoiseGr(gr, y):
    x = [81, 276.4, 302.9, 356]
    gr.calibrate(x,y)
    tot = 0
    for x in range(int(gr.fCal(350)), int(gr.fCal(375))):
        tot += gr.getDic().get(x)
        print(tot)
    gr.showSectionGraph(int(gr.fCal(350)),int(gr.fCal(375)))
    #print(tot/25/gr.getTime())
    return tot/25/gr.getTime()