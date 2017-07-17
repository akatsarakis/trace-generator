#!/usr/bin/python

import sys, getopt, random
from traceGenerator import TraceGenerator
import numpy as np

def main(argv):
    
    keyNo = 12500
    serverNo= 10
    cacheSize = 256000
    exponentA = 0.99
    writeRate = 0.05
    requestNo = 100000
    poissonInterval = 100
    try:
        opts, args = getopt.getopt(argv,"hs:w:i:r:c:k:a:")
    except getopt.GetoptError:
        print "-w <requestNo> -k <keyNo> -s <server_No> -c <cache_size> -i <poison_interval_in_nanosecs> -r <write_rate> -a <Zipf_exponent>" 
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "-w <requestNo> -k <keyNo> -s <server_No> -c <cache_size> -i <poison_interval_in_nanosecs> -r <write_rate> -a <Zipf_exponent>" 
            sys.exit()
        elif opt == "-s":
            serverNo = int(arg)
        elif opt == "-r":
            writeRate = float(arg)
        elif opt == "-a":
            exponentA = float(arg)
        elif opt == "-w":
            requestNo = int(arg)
        elif opt == "-i":
            poissonInterval = int(arg)
        elif opt == "-c":
            cacheSize = int(arg)
        elif opt == "-k":
            keyNo = int(arg)
    tg = TraceGenerator(exponentA, keyNo, cacheSize, serverNo, writeRate, requestNo, poissonInterval)
    tg.produceTrace();

if __name__ == "__main__":
    main(sys.argv[1:])
