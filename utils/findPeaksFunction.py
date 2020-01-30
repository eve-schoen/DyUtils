# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 10:34:55 2019

@author: evesg
"""
#To Do:
#may consider wanting to eliminate the biggest peaks first by doing some sort of decreasing value times sqrt(f(i))

import numpy
import math
import matplotlib.pyplot as plt
from scipy.stats import norm
from GaussClass import fitGauss, gaussian_fit, newFitGauss
from AsciiGraph import AsciiGraph
from scipy.optimize import curve_fit

peakBins = []

def findPeaksExt(cntsDic, numOfSigmas = 20, onePeak = [], show =  False, gr= None):
    x = list(cntsDic.keys())[100:] #100 because that is where I start collecting (might be 70 for o)
    y = list(cntsDic.values())[100:] 
    fitCurve = numpy.polyfit(x,y, 10) #can lower 40 and graph looks the same but gives less peaks
    f = numpy.poly1d(fitCurve)
    if show:
        fig, ax = plt.subplots()
        ax.plot(x, y, 'm', x, f(x)) 
    for i in x:
        if f(i) > 0:
            if i in cntsDic: # line i changed from list()
                if cntsDic.get(i) > float(numOfSigmas) * math.sqrt(f(i)) + f(i): # > 2 * sqrt of noise ?--> depends on data            
                    if not onePeak or onePeak[-1] == i-1:   
                        onePeak.append(i)
                    else:
                        peakBins.append(onePeak[:]) 
                        for j in onePeak: # remove? (or potentially could add based on function but....)
                            cntsDic.pop(j)
                        onePeak = []
                        return findPeaksExt(cntsDic, numOfSigmas, onePeak, show, gr)    
    #sorting the peaks so that bins next to each other are counted as one peak
    peakBins.sort()
    h = 0
    while h < len(peakBins)-1:
        if peakBins[h][-1] + 1 >= peakBins[h+1][0]: #changed from == to >= for partialconsolidate... sus
            peakBins[h].extend(peakBins[h+1])
            peakBins[h].sort()
            peakBins[h] = list(dict.fromkeys(peakBins[h])) #removes duplicates https://www.w3schools.com/python/python_howto_remove_duplicates.asp
            del peakBins[h+1]
        else:
            h= h+1
    #print("Number of peaks: from find peaks ext", len(peakBins))
    if isinstance(gr, AsciiGraph):
        gr.setBGFunc(f)
        #~~~~~~~~~~~~~ graphs back ground function and graph ~~~~~~~~~~~~~~~~~~~~~~
#        x=numpy.linspace(0,2048,1000)
#        F =f(x)
#        plt.bar(range(2048), gr.counts, width = 1,  align = "edge", color = "orange", log=False)
#        plt.plot(x,F)
#        plt.show()
    return peakBins

def getPeakPeaks(graph, lpeak):
    if lpeak == None:
        lpeak = findPeaksExt(graph.getDic())
    peakBins = []
    for i in lpeak:
        peak = max([graph.getCounts()[x] for x in i])
        for j in i:
            if graph.getCounts()[j] == peak:
                peakBins.append(j)
    return peakBins
            
def getPeakMeans(graph, lpeak = None,  showGraphs = False):
    findPeaksExt(graph.getDic(), 20, [], False, graph)
    if lpeak == None:
        lpeak = findPeaksExt(graph.getDic())
    peakMeans = []
    for x in lpeak:
        if len(x) > 1 and min(x) >10 : #optional just trying to get rid of edge issues                 
            peakMeans.append(fitGauss(graph, min(x)-5, max(x)+5, False)[0])
            if showGraphs:
                fig, a1 = plt.subplots()
                a1.bar(range((min(x)-15), (max(x)+15)),graph.getCounts()[min(x)-15:max(x)+15], width = 1)
    graph.setNumberOfPeaks(len(peakMeans))
    return peakMeans
#redoing it
def getPeakMeansNew(graph, lpeak = None,  showGraphs = False):
    peakMeans = []
    for x in lpeak:
        if len(x) > 1 and min(x) >10 : #optional just trying to get rid of edge issues
            data = []
            for i in range(min(x)-5, max(x)+5):
                    for j in range(graph.getCounts()[i])-graph.getBGFunc()(i):
                        data.append(i) 
            mu, sig = norm.fit(data)
            start = mu-3*sig
            stop = mu+3*sig
            if lpeak.index(x) is not 0 and lpeak.index(x) is not len(lpeak)-1:
                if mu - 3 * sig < lpeak[lpeak.index(x) - 1][len(lpeak[lpeak.index(x) - 1])-1]:
                    start = lpeak[lpeak.index(x) - 1][len(lpeak[lpeak.index(x) - 1])-1]+ sig
            if lpeak.index(x) is not len(lpeak)-1:
                if mu + 3 * sig > lpeak[lpeak.index(x) + 1][0]:
                    stop = lpeak[lpeak.index(x) + 1][0] - sig
            stop = int(round(stop))
            start = int(start)
            if stop -start > 2:
                peakMeans.append(fitGauss(graph, start, stop, False)[0])
            if showGraphs:
                fig, a1 = plt.subplots()
                a1.bar(range(start, stop),graph.getCounts()[start:stop], width = 1)
    graph.setNumberOfPeaks(len(peakMeans))
    return peakMeans

def getPeaks(graph, lpeak): #just takes bin of the highest number, does not do mean
    peaks =[]
    for x in lpeak:
        for j in x:
            if graph.getCounts()[j] == max([graph.getCounts()[i] for i in x]):
                peaks.append(int(j))
    return peaks

def convertToEnergy(graph, l): #converts list of lists, list or number from bin to energy
    lbins = l
    if isinstance(lbins, int):
        lbins = graph.getFunctions()[0](l)
    elif isinstance(lbins[0], list):
        for a in lbins:
            for b in range(len(a)):
                a[b] = graph.getFunctions()[0](a[b])
    elif isinstance(lbins, list):
        for i in range(len(lbins)):
            lbins[i] = graph.getFunctions()[0](lbins[i])
    else:
        print("error in convert to energy")
    return lbins

def newPeakFinder(graph): #can only be run after get peak means bc need numberofpeaks
    data = []
    for i in range(2048):
        for j in range(graph.getCounts()[i]):
            data.append(i)
    popt, pcov = curve_fit(data)
    x = numpy.linspace(0, 2048, num = 2048)
    f = numpy.poly1d(popt)
    y= []
    for x in range(2048):
        y.append(f(x))
    plt.bar(range(2048), graph.getCounts(), width = 1,  align = "edge", color = "orange")
    plt.plot(x,y, 'mp')
    plt.show()
    
    
    
        