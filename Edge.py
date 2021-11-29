

#class that represents an edge
class Edge:

    #@param source : Node object of source node
    #@param target: Node object of target node
    #@param listOfCollaborations: all collaborations in which these 2 resources are involved
    def __init__(self,source,target, listOfCollaborations):
        self.sourceNode = source
        self.targetNode = target
        #the summarized weight
        self.weight = 1
        #the 3 dimensions of the weight
        self.recency = 1
        self.frequency = 1
        self.monetary = 1

        self.type = "Undirected"
        self.listOfCollaborations = listOfCollaborations

    #@returns how many times the 2 resources collaborated (number of Collaboration objects in the listOfCollaborations)
    def getNumberOfCollaborations(self):
        return len(self.listOfCollaborations)

    def getListOfCollaborations(self):
        return self.listOfCollaborations


    def setType(self,type):
        self.type = type

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

    def getTupleFormat(self):
        return (self.sourceNode,self.targetNode)

    def getTupleFormatIDonly(self):
        return (self.sourceNode.getID(),self.targetNode.getID())

    def getWeight(self):
        return self.weight

    def getSourceNode(self):
        return self.sourceNode

    def getSourceNodeID(self):
        return self.sourceNode.getID()

    def getTargetNode(self):
        return self.targetNode

    def getTargetNodeID(self):
        return self.targetNode.getID()

    def getType(self):
        return self.type

    #@param node: Node object
    #@returns boolean whether the node is part of this edge
    def containsNode(self,node):
        return ((self.sourceNode == node) or (self.targetNode == node))

    #check if the edge connects the 2 specified nodes
    def connects(self,node1,node2):
        return (((self.sourceNode == node1)and(self.targetNode == node2)) or ((self.sourceNode == node2)and(self.targetNode == node1)))

    #Determine 1 summarized final weight based on a weighted sum of the RFM values
    #@param weightR weight for the recency value
    #@param weightF weight for the frequency value
    #@param weightM weight for the monetary value
    def calculateFinalWeight(self,weightR,weightF,weightM):
        self.weight = weightR * self.recency + weightF * self.frequency + weightM * self.monetary


    def print(self):
        print("Edge : ", self.sourceNode.getLabel(), " - ", self.targetNode.getLabel(), "  weight = ", self.weight, "RFM ",self.recency, self.frequency, self.monetary, self.type)
        print("Collaborations : ")
        for c in self.listOfCollaborations:
            c.print()
