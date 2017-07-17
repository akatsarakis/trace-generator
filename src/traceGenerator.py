#!/usr/bin/python

import sys, getopt, random
import numpy as np

class TraceGenerator:
    def __init__(self, expA, keyNo, cacheSize, serverNo, writeRate, requestNo ,poissonInterval):
        self.expA = expA
        self.requestNo = requestNo 
        self.keyNo = keyNo
        self.cacheSize = cacheSize
        self.serverNo = serverNo
        self.writeRate = writeRate
        self.poissonInterval = poissonInterval
        self.serverHPopularity = [0] * self.serverNo
        self.serverNPopularity = [0] * self.serverNo
        self.key = 0
        self.hotKeys2server = [0] * self.cacheSize
        self.hotKeyPopularity = [0] * self.cacheSize
        self.calcHotRateNServerPopularities()
        #print self.hotKeyPopularity
        
    def produceTrace(self):
        poison = np.random.poisson(self.poissonInterval, self.requestNo)
        timestamp = 0
        for i in range(0, self.requestNo):                  # input from standard input
            timestamp += poison[i]
            self.calcReqTypeKeyAndHomeServer()
            print self.reqType, random.randint(0, self.serverNo -1), self.homeServer, self.key, timestamp 
    
    def calcReqTypeKeyAndHomeServer(self):
        if random.uniform(0.0, 1.0) <= self.hotRate:
            self.reqType = "H"
            self.key =  np.random.choice(self.cacheSize, 1, p = self.hotKeyPopularity)[0]
            self.homeServer = self.hotKeys2server[self.key-1]
        else:
            self.reqType = "N"
            self.key = self.getARandomNormalKey()
            self.homeServer = np.random.choice(self.serverNo, 1, p = self.serverNPopularity)[0]
        if random.uniform(0.0, 1.0) <= self.writeRate:
            self.reqType += "W"
        else:
            self.reqType += "R"
            
    def calcHotRateNServerPopularities(self):
        cacheHit = 0.0
        sum = 0
        for i in range(1, self.keyNo + 1):
            #Start section <changed recently>
            if self.expA == 0:
                keyPopularity = 1 / self.keyNo
            else:
                keyPopularity = 1 / pow(i, self.expA)
            #End section <changed recently>
            sum = sum + keyPopularity
            if i == self.cacheSize:
                cacheHit = sum
            if i <= self.cacheSize:
                randomServer = random.randint(0, self.serverNo-1)
                self.hotKeys2server[i-1] = randomServer
                #self.hotKeys2server[i-1] = (i) % self.serverNo LOAD BALANCE
                self.hotKeyPopularity[i-1] = keyPopularity     
                self.serverHPopularity[randomServer] += keyPopularity
            else:
                self.serverNPopularity[random.randint(0, self.serverNo-1)] += keyPopularity
        for i in range(0, self.cacheSize):
            self.hotKeyPopularity[i] = self.hotKeyPopularity[i] / cacheHit
        for i in range(0, self.serverNo):
            self.serverHPopularity[i] = self.serverHPopularity[i] / cacheHit
            self.serverNPopularity[i] = self.serverNPopularity[i] / (sum - cacheHit)
        self.hotRate = cacheHit/sum
     
    def getARandomNormalKey(self):
        return random.randint(self.cacheSize+1, self.keyNo)
