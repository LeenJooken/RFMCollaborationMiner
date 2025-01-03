import NetworkXCalculation
import RecencyFunctions
import datetime
from datetime import timedelta
import pandas as pd
import numpy as np

#This class is designed to calculate the weights of the nodes
#You have to initialize the class with the nodelist and edgesList
#To actually calculate the node weights, call calculateNodeWeights()
class NodeWeightCalculator:
    #@param nodes : list of Node objects
    #@param edges : list of Edge objects
    #@param eventList : list of all the Event objects
    def __init__(self,nodes,edges, eventList, recencyWindowSize):
        self.nodes = nodes
        self.edges = edges
        self.eventList = eventList

        #Window size for the recency calculation
        self.recencyWindowSize = recencyWindowSize

        #Decide weight distribution for the summarized node weight
        self.weightR = 1/3
        self.weightF = 1/3
        self.weightM = 1/3


    #Calculate the node weights
    def calculateNodeWeights(self):
        #recency
        self.calculateRecencyValue()

        #frequency
        self.calculateFrequencyValue()

        #monetary
        self.calculateMonetaryValue()

        self.determineFinalWeight()


    #Calculates the recency value dimension of the RFM weight
    #The more recent a resource has worked, the bigger this value
    #Algorithm: divide timeline into n windows of x minutes and assign each one a weight equal to the window number / n
    #Assign each work session of the node to one window (based on the median timestamp of the worksession)
    #The value of the window is the relative frequency =  number of work sessions within the window / total number of work sessions
    #The recency value is the weighted sum of each of these window relative frequencies
    def calculateRecencyValue(self):
        #Determine first and last timestamp of log
        firstAndLastTimeStamp = RecencyFunctions.determineLogEndpoints(self.eventList)

        #Determine bins
        bins = RecencyFunctions.determineBins(firstAndLastTimeStamp,self.recencyWindowSize)

        #Get the bin weights
        binWeights = RecencyFunctions.getBinWeights(bins)


        for node in self.nodes:
            value = self.determineRecencyValueForNode(node,bins,binWeights)
            node.setRecencyValue(value)



    #Function that determines the recency value for this node
    #@param node: the node for which we are going to calculate the recency value
    #@param bins: array of bin cut points
    #@param binWeights : array of the binWeights (ordered)
    #@returns recency value for this node
    def determineRecencyValueForNode(self,node, bins,binWeights):

        #Get df with first column a list of medians for each worksession : these will be binned and counted
        datapoints = self.getDFWorksessionMedians(node)
        value = RecencyFunctions.determineRecencyValue(datapoints,bins,binWeights)
        return value


    #@param node : Node object for which we want to retrieve the median of the work sessions
    #@returns dataframe with column 'Medians' the median times of each worksession
    def getDFWorksessionMedians(self,node):
        worksessions = node.getListOfWorksessions()
        medians = []
        #determine the median for each worksession
        for ws in worksessions:
            medians.append(ws.getMedianTimestamp())

        df = pd.DataFrame({'Medians':medians})

        return df







    #Calculates the frequency value dimension of the RFM weight
    #Algorithm: count the number of worksessions this resource was involved in
    def calculateFrequencyValue(self):
        #how many work sessions does this resource have
        for n in self.nodes :
            number = n.getNumberOfWorksessions()
            n.setFrequencyValue(number)

    #Calculates the monetary value dimension of the RFM weight
    def calculateMonetaryValue(self):
        #object importance
        self.objectImportance()

        #When choosing between the following alternatives: please set the summarized edge weight distribution in the EdgeWeightCalculator!
        #betweenness centrality
        #self.betweennessCentrality()
        #eigenvector centrality
        #self.eigenvectorCentrality()
        return

    #The importance of the collection of objects the resource worked on
    #Algorithm:
    #sum over all the objects: the number of times they worked on the object times the importance of the object
    def objectImportance(self):
        #in how many work sessions is the object included x the importance value of the object
        for n in self.nodes:
            worksessions = n.getListOfWorksessions()
            sum = 0
            for ws in worksessions:
                objects = ws.getObjects()
                for o in objects:
                    sum += o.getImportance()
            n.setMonetaryValue(sum)


    #function that calculates the betweenness centrality:
    #Graph theory centrality measure
    #= number of shortest paths that pass through the vertex
    #high value if node is important gatekeeper of info between disparate parts of the graph
    #So in our case: shows people that form a connection between many separate collab teams
    #A higher value is more likely to be a cross functional team member / spans team boundaries
    def betweennessCentrality(self):
        networkXCalculation = NetworkXCalculation.NetworkXCalculation(self.nodes,self.edges)
        networkXCalculation.calculateBetweennessCentrality()

        for node in self.nodes :
            betweenCentr =  self.networkXCalculation.getBetweennessCentrality(node)
            node.setWeight(betweenCentr)

    #Measures the influence a node has on a network:
    #A node will have a high eigenvector centrality if many important nodes link to it
    #A node with a high value is a central team player
    def eigenvectorCentrality(self):
        networkXCalculation = NetworkXCalculation.NetworkXCalculation(self.nodes,self.edges)
        networkXCalculation.calculateEigenvectorCentrality()
        for node in self.nodes:
            eigenvCentr = self.networkXCalculation.getEigenvectorCentrality(node)
            node.setWeight(eigenvCentr)

    #Function that determines the final (summarized) weight of the node
    def determineFinalWeight(self):
        for n in self.nodes:
            n.calculateFinalWeight(self.weightR,self.weightF,self.weightM)
