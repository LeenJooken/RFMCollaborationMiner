


#class that represents a node
class Node:

    #@param resource : Resource object that is represented by the node
    #@param weight : the node's weight
    #@param listOfWorksessions : array of Worksession objects in which the resource is involved
    def __init__(self,resource,weight,listOfWorksessions):
        self.resource = resource
        #weight summarized
        self.weight = weight
        #3 dimensions of weight
        self.recency = 0
        self.frequency = 0
        self.monetary = 0

        self.ID = resource.getID()

        self.listOfWorksessions = listOfWorksessions

    def getResource(self):
        return self.resource

    def getLabel(self):
        return (self.resource.getLabel())

    def getID(self):
        return self.ID

    def getWeight(self):
        return self.weight

    def setWeight(self,weight):
        self.weight = weight

    def setRecencyValue(self,value):
        self.recency = value

    def getRecencyValue(self):
        return self.recency

    def setFrequencyValue(self,value):
        self.frequency = value

    def getFrequencyValue(self):
        return self.frequency

    def setMonetaryValue(self,value):
        self.monetary = value

    def getMonetaryValue(self):
        return self.monetary

    #@returns number of worksessions this node has done
    def getNumberOfWorksessions(self):
        return len(self.listOfWorksessions)

    def getListOfWorksessions(self):
        return self.listOfWorksessions

    #Determine 1 summarized final weight based on a weighted sum of the RFM values
    #@param weightR weight for the recency value
    #@param weightF weight for the frequency value
    #@param weightM weight for the monetary value
    def calculateFinalWeight(self,weightR,weightF,weightM):
        self.weight = weightR * self.recency + weightF * self.frequency + weightM * self.monetary

    def print(self):
        print("Node : ", self.resource.getLabel()," with weight = ", self.weight, " R,F,M ",self.recency, self.frequency,self.monetary)
        print("Related work sessions: ")
        for ws in self.listOfWorksessions:
            ws.print()
