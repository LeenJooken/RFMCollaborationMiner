#This class is designed to calculate the weights of the edges
import RecencyFunctions
from datetime import timedelta
import pandas as pd
import numpy as np

class EdgeWeightCalculator:

    def __init__(self,edges, eventList, recencyWindowSize):
        self.edges = edges
        self.eventList = eventList

        #Window size for the recency calculation
        #TO DO: makes this a parameter
        self.recencyWindowSize = recencyWindowSize

        #TODO weights as parameters
        self.weightR = 1/3
        self.weightF = 1/3
        self.weightM = 1/3

    #Calculate the edge weights based on the RFM principle
    def calculateEdgeWeights(self):
        #recency
        self.calculateRecencyValue()

        #frequency
        self.calculateFrequencyValue()

        #monetary
        self.calculateMonetaryValue()

        self.determineFinalWeight()

    #Calculates the recency value dimension of the RFM weight
    #The more recent a pair of resources has collaborated, the bigger this value
    #Algorithm: divide timeline of the entire log into n windows of x minutes and assign each one a weight equal to the window number / n
    #Assign each collaboration of the edge to one window (based on the median timestamp of the collaboration)
    #The value of the window is the relative frequency =  number of collaborations within the window / total number of collaborations
    #The recency value is the weighted sum of each of these window relative frequencies
    def calculateRecencyValue(self):
        #Determine the first and last timestamp of the log
        firstAndLastTimeStamp = RecencyFunctions.determineLogEndpoints(self.eventList)


        #Determine bins
        bins = RecencyFunctions.determineBins(firstAndLastTimeStamp, self.recencyWindowSize)
        #Get the bin weights
        binWeights = RecencyFunctions.getBinWeights(bins)

        for edge in self.edges:
            value = self.determineRecencyValueForEdge(edge,bins,binWeights)
            edge.setRecencyValue(value)


    #Function that determines the recency value for this edge
    #@param edge: the edge for which we are going to calculate the recency value
    #@param bins: array of bin cut points
    #@param binWeights : array of the binWeights (ordered)
    #@returns recency value for this edge
    def determineRecencyValueForEdge(self,edge, bins,binWeights):
        #Get DF with the first column a list of medians for each collaboration session: these will be the datapoints that will be binned and counted
        datapoints = self.getDFCollaborationMedians(edge)
        value = RecencyFunctions.determineRecencyValue(datapoints,bins,binWeights)
        return value

    #@param edge : Edge object for which we want to retrieve the median of the collaboration sessions
    #@returns dataframe with column 'Medians' the median times of each collaboration session
    def getDFCollaborationMedians(self,edge):
        collaborations = edge.getListOfCollaborations()
        medians = []
        #determine the median for each collaboration
        for collab in collaborations:
            medians.append(collab.getMedianTimestamp())

        df = pd.DataFrame({'Medians':medians})

        return df

    #Calculates the frequency value dimension of the RFM weight
    #The more frequent two resources collaborate the bigger this value
    #Algorithm: count the number of collaborations between the 2 resource
    def calculateFrequencyValue(self):
        for e in self.edges :
            number = e.getNumberOfCollaborations()
            e.setFrequencyValue(number)

    #Calculates the monetary value dimension of the RFM weight
    #The importance of the collection of objects both resources collaborated on
    #Algorithm:
    #sum over all the objects: the number of times they collaborated on the object times the importance of the object
    def calculateMonetaryValue(self):
        for e in self.edges:
            collaborations = e.getListOfCollaborations()
            sum = 0
            for c in collaborations:
                sum += c.getObject().getImportance()
            e.setMonetaryValue(sum)

    #Function that determines the final (summarized) weight of the edge
    #Necessary if for the calculation of the node weight one choses to use the betweenness or eigenvector centrality
    def determineFinalWeight(self):
        for e in self.edges:
            e.calculateFinalWeight(self.weightR,self.weightF,self.weightM)
