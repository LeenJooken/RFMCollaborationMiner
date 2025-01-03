#This file does not contain a class, but help functions to calculate the recency value of a node and an edge
import datetime
from datetime import timedelta
import pandas as pd
import numpy as np

#@param eventList : an array of Event objects
#@returns a tuple with the start and end timestamp of the log
def determineLogEndpoints(eventList):
    timestamps = []
    for e in eventList :
        timestamps.append(e.getTimestamp())

    timestamps.sort()
    endpoints = (timestamps[0],timestamps[-1])
    return endpoints

#Determine the bins for the calculation of the Recency value
#@param endpoints : tuple with 2 datetime objects: the start and end point
#@param windowSize : width of a bin in minutes
#@returns array with cut points for the bins
def determineBins(endpoints, windowSize):

    cutpoint = endpoints[1]
    bins = [cutpoint]
    beginstamp = endpoints[0]
    while cutpoint >= beginstamp:
        cutpoint = cutpoint - timedelta(minutes = windowSize)
        bins.insert(0,cutpoint)

    return bins

#@param bins: array with the cutpoints for the bins, as created by the function determineBins
#@returns array with the weight of each bin from the start of the log to the end
def getBinWeights(bins):
    #prepare the binweights  = binnumber / total number of bins
    numberOfBins = len(bins) - 1
    binWeights = np.arange(1/numberOfBins,1+ (1/numberOfBins),1/numberOfBins)
    return binWeights



#Function that determines the recency value for this node
#@param datapoints: dataframe with a column 'Medians' that contains the datapoints to place in the bins (datetime objects)
#@param bins: array of bin cut points
#@param binWeights : array of the binWeights (ordered)
#@returns recency value
def determineRecencyValue(datapoints,bins,binWeights):

    df = datapoints

    #Total number of datapoints
    totalNumberOfDP = len(df['Medians'])

    #add bins
    df['Bins'] = pd.cut(df['Medians'],bins)

    #Count the number of values for each bin
    binValueCounts = df['Bins'].value_counts(sort=False)

    #This value should be relative: % of all the datapoints: save this in array
    relFreq = []
    for val, cnt in binValueCounts.items(): #iteritems():
        relFreq.append(cnt/totalNumberOfDP)

    #Sum of the binweight x relfreq for all the bins = the recency value
    recencyValue = 0
    for i in range(0,len(relFreq)):
        recencyValue += relFreq[i] * binWeights[i]

    return recencyValue
