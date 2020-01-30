# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 10:31:26 2019

@author: evesg
"""
import matplotlib.pyplot as plt 
import numpy

#Note: titles make graphs way slower
class AsciiGraph:
    def __init__(self, file = None, l = None, time  = None): 
        self.filename = file
        #arranged so graphs can be made off counts lists or text files
        if file is not None:
            counts,time=self.extractFromFile(file)
        else:
            counts,time=l,time  
        self.counts = counts
        self.time = time
        self.conversion = 1 # E = conversion * bin# - linear relationship less accurate than quadratic
        self.noise = []
        #self.reciprocal = 
    
    @staticmethod
    def extractFromFile(file):
        with open(file, 'r') as f:
            counts=f.read().split('\n')
        time = counts[9]
        spaceIndex = time.find(" ") 
        time = int(time[:spaceIndex]) #it is live time now
        del counts[0:12]
        del counts[2048:]
        for x in range(len(counts)):
            counts[x] = int(counts[x])
        return counts,time
    
    def calibrate(self, x, y, degree  = 2, show=False): 
    #x = bin numbers , y = energys (keV)     
        fitCurve = numpy.polyfit(x,y,degree)
        self.fCal = numpy.poly1d(fitCurve) #takes in a bin, gives an energy
        self.fCalInverse = numpy.poly1d(numpy.polyfit(y,x,degree)) #takes in an eregy and gives a bin
        self.linear = numpy.polyfit(x,y,1)
        self.step = self.linear[0]
        if show:
            fig, a1 = plt.subplots()
            x2 = numpy.linspace(-20+min(x), max(x)+20, num=100)
            y2= []
            for i in x2:
                y2.append(self.fCal(i))  
            a1.plot(x, y, 'mp', x2, y2)      
        return fitCurve
        
    def setConversion(self, number): #linear calibration
        self.conversion = number
        
    def setBackgroundNoise(self, calibrationFactor, file="sheilding_bg_all.txt"):
        self.bgfilename = file
        fig2, ax1 = plt.subplots()
        with open(file, 'r') as f:
            bgCounts=f.read().split('\n')
        time = bgCounts[9]
        spaceIndex = time.find(" ")     
        #liveTime = int(time[0:spaceIndex])
        realTime = float(time[spaceIndex+1 :])
        #switch to live time once we get working bg data
        del bgCounts[0:12]
        del bgCounts[2048:]
        for i in bgCounts:
            self.noise.append(float(i)/realTime)   
            #self.noise.append(float(i)/float(calibrationFactor)/realTime)
        ax1.bar(range(2048), self.noise, width = 1,  align = "edge", color = "pink")
        ax1.title.set_text("Background Noise")
        
    def setBGFunc(self, func):
        self.bgFunc= numpy.poly1d(func)
        
    def setNumberOfPeaks(self, num):
        self.numOPeaks = num
        
    def showGraph(self):
        fig, a4 = plt.subplots() 
        a4.bar(range(2048), self.counts, width = 1,  align = "edge", color = "orange")
        a4.set_xlabel("bins")
        if self.filename is not None:
            title = "Graph of " + self.filename
            a4.title.set_text(title)
        plt.show()
    
    def showGraphEnergy(self, func = True): #true to use the quadratic, false for linear
        fig, a2 = plt.subplots()   
        x = []
        for i in range(2048):
            if func == False:                       
                x.append(i*self.conversion)    
            else:           
                x.append(self.fCal(i))        
        a2.bar(x, self.counts, width = 1,  align = "edge", color = "pink")
        a2.set_xlabel("Energies (keV)")
        
    #takes inputs and gives output as bin numbers
    def showSectionGraph(self, start, stop, log =False): 
        fig, a6 = plt.subplots() 
        if start < 0 or stop>2048:
            print( "Error, index out of bounds" )
        else:
            a6.bar(range(start,stop), self.counts[start:stop],align = "edge", width = 1, color= "green", log =log)
            a6.set_xlabel("bins")
            plt.show()
            
    #takes inputs and gives output as Energy levels (keV)      
    def showSectionGraphEnergy(self, start, stop, log = False):
        fig, a5 = plt.subplots() 
        frequencies = []
        x=[]
        i=start
        while i < stop: # i is in keV
             x.append(i)
             frequencies.append(self.counts[int(self.fCalInverse(i))]) 
             i = i+self.step
        graph = a5.bar(x, frequencies ,align = "edge", width = 1, color= "blue", log = log)
        a5.set_xlabel("Energies (keV)")
            ### new attempt
#        x = numpy.arange(start,stop+self.step,self.step)
#        print(x)
#        print(len(numpy.arange(start,stop+self.step,self.step)))
#        print(len(self.counts[int(self.fCalInverse(start)):int(self.fCalInverse(stop))]))
#        graph = a5.bar(numpy.arange(start,stop,self.step), self.counts[int(self.fCalInverse(start)):int(self.fCalInverse(stop))],align = "edge", width = 1, color= "orange")
#        
        return graph
        
    def getBGFunc(self):
        return self.bgFunc
    
    def getCounts(self):
        return self.counts
    
    def getTime(self):
        return self.time
    
    def getDic(self):
        key = list(range(2048))
        vals = self.getCounts()
        return dict(zip(key,vals))
    
    def getFunctions(self):
        return (self.fCal, self.fCalInverse)
    
    def getNumOfPeaks(self):
        return self.numOPeaks
    
    def getRates(self): #counts/sec/keV
        return [float(i)/self.time/self.step for i in self.counts]
    
    def getStep(self):
        return self.step
    
    def graphWithoutNoise(self): #in rates
        fig, a3 = plt.subplots()  
        if len(self.counts) != len(self.noise):
            print("Error - index of rates and counts not the same")
        else:
            self.rates = [float(i)/self.time for i in self.counts]
            #rates = [float(i)/self.conversion/self.time for i in self.counts]
#            plt.bar(range(2048), rates, width = 1,  align = "edge", color = "red")
#            plt.bar(range(2048), self.noise, width = 1,  align = "edge", color = "pink")
            woNoise = []
            for j in range(2048):
                woNoise.append(self.rates[j]-self.noise[j])
            a3.bar(range(2048), woNoise, width = 1,  align = "edge", color = "green") 
            a3.set_ylabel("Rates(counts/second/bin)")
            title = self.filename + " graphed without noise: " + self.bgfilename
            a3.title.set_text(title)
            plt.show()
            return woNoise
        
    def showSectionGraphRates(self, start, end):
        fig, a6 = plt.subplots() 
        x = []
        frequencies = []
        i=start
        while i < end: # i is in keV
            x.append(i)
            frequencies.append(self.counts[int(self.fCalInverse(i))]) 
            i = i+self.step        
        a6.set_xlabel("Energies (keV)")
        rates = [float(i)/self.time/self.step for i in frequencies]
        a6.bar(x, rates, width = 1,  align = "edge", color = "pink") 
        print(len(rates))
        print(len(x))
        a6.set_ylabel("Rates (counts/second/keV)")
        
            
        

        
        
        
        