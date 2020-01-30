# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 14:22:06 2019

@author: evesg
"""
import matplotlib.pyplot as plt
import numpy
from scipy.stats import norm
import statistics as stats

#could subtract noise --> don't have to assume linearity even using functino
numSig = 3

def gaussian_fit(xdata,ydata):
    mu = numpy.sum(xdata*ydata)/numpy.sum(ydata)
    sigma = numpy.sqrt(numpy.abs(numpy.sum((xdata-mu)**2*ydata)/numpy.sum(ydata)))
    return mu, sigma

def newFitGauss(graph, start, stop, show = False): #start and stop must be bin numbers 
    print("start, stop")
    print(start, stop)    
    data = []
    for i in range(start, stop):
        for j in range(graph.getCounts()[i]):
            data.append(i) 
    mu, sigma = norm.fit(data)
    print("sig1")
    print(sigma)
    sig = stats.stdev(data,mu)
    print("sig2")
    print(sig)
    data = []
    for i in range(int(start-numSig*sig+5), int(stop+numSig*sig-5)):
        for j in range(graph.getCounts()[i]-int(graph.getBGFunc()(i))): #must do findPeaksExt first
            data.append(i) 
    x = numpy.linspace(start, stop, 100)
    y=1/numpy.sqrt(2*sig*sig*numpy.pi)*numpy.exp(-(x-mu)*(x-mu)/(2*sig*sig))
    print("start, stop of final calc")
    print(start, stop) 
    mu, sig = gaussian_fit(x,y)
    print("sig3")
    print(sig)
    
    if show:
        fig, ax = plt.subplots() 
        ax.hist(data, stop-start, density= True) #(can be removed)
        print("mean, sigma :")
        print(mu, sig)
        #x = numpy.linspace(start-numSig*sig, stop+numSig*sig, num = 100)
        #y = norm.pdf(x, mu, sig)
        ax.plot(x,y, 'mp')
        plt.show()
    return (mu, sig)
#reconstruct old fitgauss
def fitGauss(graph, start, stop, show = False): #start and stop must be bin numbers     
    data = []
    for i in range(start, stop):
        for j in range(graph.getCounts()[i]-int(graph.getBGFunc()(i))): #haven't test BGFunc, must run findPeaksExt first
            data.append(i) 
    mean, sigma = norm.fit(data)
    sig = stats.stdev(data,mean)
#    print("norm.fit() vs stats.stdev()")
#    print(str(sigma) + " vs " + str(sig))
    
    if show:
        fig, ax = plt.subplots() 
        ax.hist(data, stop-start, density= True) #(can be removed)
        print("mean, sigma :")
        print(mean, sigma)
        x = numpy.linspace(start-numSig*sig, stop+numSig*sig, num = 100)
        y = norm.pdf(x, mean, sigma)
        ax.plot(x,y, 'mp')
        plt.show()
    return (mean, sigma)

def fitGaussCounts(counts, start, stop, show = False): #start and stop must be bin numbers     
    data = []
    for i in range(start, stop):
        for j in range(counts[i]):
            data.append(i)
    
    mean, sigma = norm.fit(data)
    if show:
        fig, ax = plt.subplots() 
        ax.hist(data, stop-start, density= True) #(can be removed)
        print("mean, sigma :")
        print(mean, sigma)
        x = numpy.linspace(start, stop, num = 100)
        y = norm.pdf(x, mean, sigma)
        ax.plot(x,y, 'mp')
        plt.show()
    return (mean, sigma)


    