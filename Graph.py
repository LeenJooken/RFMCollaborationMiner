import Node
import Edge
import EdgeWeightCalculator
import NodeWeightCalculator

#class that represents the social graph,
#contains a node and edge list
class Graph:
    #Must call constructgraph after this initialization
    def __init__(self,recencyWindowSizeEdge = 1440,recencyWindowSizeNode = 1440):
        self.nodes = []
        self.edges = []

        #Recency window sizes
        self.recencyWindowSizeEdge = recencyWindowSizeEdge
        self.recencyWindowSizeNode = recencyWindowSizeNode




    #@returns list of Node objects
    def getNodesList(self):
        return self.nodes
    #@returns list of Edge objects
    def getEdgesList(self):
        return self.edges

    def addNodeToList(self,node):
        self.nodes.append(node)

    def addEdgeToList(self,edge):
        self.edges.append(edge)

    #@param resource: Resource object
    #@returns Node object of this resource
    def searchNodeByResource(self,resource):
        node = [target for target in self.nodes if target.getResource()==resource]

        return node[0]



    #constructs the graph: builds node & edges list
    #@param eventList : list of Event objects
    #@param resourceList : list of Resource objects
    #@param collaborationList : list of Collaboration objects
    #@param worksessionsList: list of Worksession objects
    def constructGraph(self,eventList,resourceList,collaborationList,worksessionsList):
        #build the base graph
        print("    Building the nodes list")
        self.buildNodesList(resourceList,worksessionsList)
        print("    Building the edges list")
        self.buildEdgesList(resourceList,collaborationList)

        print("    Calculating the edge weights")
        self.calculateEdgeWeights(eventList)
        print("    Calculating the node weights")
        self.calculateNodeWeights(eventList)



    #build the nodes list
    def buildNodesList(self,resources,worksessionsList):
        #include all resources and set the weight default at 1
        #build the list
        for res in resources:
            sessions = self.collectWorksessionsForResource(worksessionsList,res)
            self.addNodeToList(Node.Node(res,1,sessions))

    #Collect all the worksessions in which this resource was involved
    #@param worksessionsList : list of all worksession Objects
    #@param resource : Resource object
    #@returns array of all Worksession objects the resource is involved in
    def collectWorksessionsForResource(self,worksessionsList,resource):
        sessions = []
        for ws in worksessionsList:
            if (resource == ws.getResource()):
                sessions.append(ws)

        return sessions

    #build the edges list
    def buildEdgesList(self, resources, collaborations):
        #check for every couple of resources whether they have a collaboration object associated
        #check for each pair of resources
        for sourceIterator in range(0,len(resources)-1):
            source = resources[sourceIterator]
            for targetIterator in range(sourceIterator+1,len(resources)):
                target = resources[targetIterator]

                #check if a collaboration edge should be constructed
                self.constructCollaborationEdge(source,target,collaborations)

    #Function that constructs a edge between the source and target if there is a collaboration
    #@param source : Resource object 1
    #@param target : Resource object 2
    #@param collaborations : list of Collaboration objects
    def constructCollaborationEdge(self,source,target,collaborations):
        relevantCollabs = self.collectRelevantCollaborations(source,target,collaborations)

        #if there are collabs
        if relevantCollabs:
            sourceNode = self.searchNodeByResource(source)
            targetNode = self.searchNodeByResource(target)
            edge = Edge.Edge(sourceNode,targetNode,relevantCollabs)
            #add edge to the list
            self.addEdgeToList(edge)

    #Function collects all the Collaboration objects in the list, for which the collab was between resource 1 and 2
    #@param source : Resource object 1
    #@param target : Resource object 2
    #@param collaborations : list of Collaboration objects
    #@returns list of Collaborations between resource 1 and 2; if there exists none then the list will be empty
    def collectRelevantCollaborations(self,source,target,collaborations):
        relevantCollabs = [collab for collab in collaborations if collab.getTupleFormat()==(source,target)]
        return relevantCollabs


    #Calculates the weight for the edges
    #@param eventList = list of all the Event objects
    def calculateEdgeWeights(self,eventList):
        edgeWeightCalculator = EdgeWeightCalculator.EdgeWeightCalculator(self.edges,eventList,self.recencyWindowSizeEdge)
        #calculate and set the edge weights
        edgeWeightCalculator.calculateEdgeWeights()


    #Calculates the weight for the nodes
    #@param eventList = list of all the Event objects
    def calculateNodeWeights(self,eventList):
        nodeWeightCalculator = NodeWeightCalculator.NodeWeightCalculator(self.nodes,self.edges, eventList,self.recencyWindowSizeNode)
        nodeWeightCalculator.calculateNodeWeights()





    #print out the contents of this class
    def print(self):
        print("   Nodes:")
        self.printNodes()
        print("   Edges:")
        self.printEdges()


    def printNodes(self):
        for n in self.nodes:
            n.print()

    def printEdges(self):
        for e in self.edges:
            e.print()
