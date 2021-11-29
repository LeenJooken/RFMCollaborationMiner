#Class that writes the graph to CSV

import operator
import argparse
import csv
import io

class Output:
    def __init__(self):
        self.anonymizationCounter = 1


    def anonymizeProgrammer(self):
        name = "P" + str(self.anonymizationCounter)
        self.anonymizationCounter += 1
        return name

    

    #Write RFM values of resources and their relations to 2 seperate CSVs: nodes and edges
    #@param nodes: list of Node objects
    #@param edges: list of Edge objects
    #@param nodes_filename: filename of nodes file
    #@param edges_filename: filename of edges file
    def writeRFMToCSV(self,nodes,edges,nodes_filename,edges_filename):
        self.writeNodesRFMCSV(nodes,nodes_filename)
        self.writeEdgesRFMCSV(edges,edges_filename)



    #write Id, Label, weight, RFM values of the nodes to csv
    #@param nodes : list of nodes
    #@param filename: csv file
    #@returns
    def writeNodesRFMCSV(self,nodes,filename):
        #check first if the filename isnt empty
        if not filename:
            filename = "resourcesRFM.csv"

        writer = csv.writer(io.open(filename,'w+',newline='',encoding ="utf-8"),delimiter=";")
        #write the header: Id, Label and weight
        writer.writerow(["Id","Label","Summarized Weight","Recency","Frequency","Monetary"])
        #write all the nodes to the file
        for node in nodes:
            label = node.getLabel()
            #for anonymization, uncomment the next line
            #label = self.anonymizeProgrammer()
            writer.writerow([node.getID(),label,node.getWeight(),node.getRecencyValue(),node.getFrequencyValue(),node.getMonetaryValue()])


    #write Source, Target, Weight, RFM values of the edges to csv
    #@param edges : list of Edge objects
    #@param filename: csv file
    #@returns
    def writeEdgesRFMCSV(self,edges,filename):
        #check first if the filename isnt empty
        if not filename:
            filename = "relationsRFM.csv"

        writer = csv.writer(io.open(filename,'w+',newline='',encoding="utf-8"),delimiter=";")
        #write the header: Source, Target, Weight, type
        writer.writerow(["Source","Target","Summarized Weight","Recency","Frequency","Monetary"])
        #write all the edges to the file
        for edge in edges:
            writer.writerow([edge.getSourceNodeID(),edge.getTargetNodeID(),edge.getWeight(),edge.getRecencyValue(),edge.getFrequencyValue(),edge.getMonetaryValue()])
