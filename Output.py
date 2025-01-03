#Class that writes the graph to CSV

import operator
import argparse
import csv
import io

class Output:
    def __init__(self):
        self.anonymizationCounter = 1


    def anonymizeResource(self):
        name = "R" + str(self.anonymizationCounter)
        self.anonymizationCounter += 1
        return name

    

    #Write RFM values of resources and their relations to 2 separate CSVs: nodes and edges
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
        writer.writerow(["Id","Label","Recency","Frequency","Monetary"])
        #write all the nodes to the file
        for node in nodes:
            label = node.getLabel()
            #for anonymization, uncomment the next line
            #label = self.anonymizeResource()
            writer.writerow([node.getID(),label,node.getRecencyValue(),node.getFrequencyValue(),node.getMonetaryValue()])


    #write Source, Target, Weight, RFM values of the edges to csv
    #@param edges : list of Edge objects
    #@param filename: csv file
    #@returns
    def writeEdgesRFMCSV(self,edges,filename):
        #check first if the filename isn't empty
        if not filename:
            filename = "relationsRFM.csv"

        writer = csv.writer(io.open(filename,'w+',newline='',encoding="utf-8"),delimiter=";")
        #write the header: Source, Target, Weight, type
        writer.writerow(["Source","Target","Recency","Frequency","Monetary"])
        #write all the edges to the file
        for edge in edges:
            writer.writerow([edge.getSourceNodeID(),edge.getTargetNodeID(),edge.getRecencyValue(),edge.getFrequencyValue(),edge.getMonetaryValue()])





    #Write the list of work sessions to CSV using the resources and object IDS
    #Write the info down as resource ID, resource label, and the first, last and median timestamps of the work session
    #It does not include info on the events or the specific objects
    #@param list: list of Worksession objects
    def writeWorkSessionListToCSV(self, list):
        filename = "workSessions.csv"

        writer = csv.writer(io.open(filename,'w+',newline='',encoding="utf-8"),delimiter=";")
        #write header
        writer.writerow(["ResourceID","ResourceLabel","FirstTimestamp", "LastTimeStamp","MedianTimestamp"])

        #write all the work sessions to the file
        for workSession in list:
            firstTimestamp = workSession.getFirstTimestamp()
            firstTimestamp = firstTimestamp.strftime("%d/%m/%Y, %H:%M:%S")
            lastTimestamp = workSession.getLastTimestamp()
            lastTimestamp = lastTimestamp.strftime("%d/%m/%Y, %H:%M:%S")
            medianTimestamp = workSession.getMedianTimestamp()
            medianTimestamp = medianTimestamp.strftime("%d/%m/%Y, %H:%M:%S")


            writer.writerow([workSession.getResource().getID(), workSession.getResource().getLabel(),
            firstTimestamp,lastTimestamp, medianTimestamp ])


    #Write the list of collaboration sessions to CSV using the resources and object IDs
    #@param list: list of all collaboration sessions (Collaboration objects) that have been identified over all resource pairs and objects
    def writeCollabListToCSV(self,list):
        filename = "collaborationSessions.csv"

        writer = csv.writer(io.open(filename,'w+',newline='',encoding="utf-8"),delimiter=";")
        #write header
        writer.writerow(["ResourceID1","ResourceLabel1","ResourceID2","ResourceLabel2","ObjectID","ObjectName","FirstTimestamp", "LastTimeStamp","MedianTimestamp"])

        #write all the collaboration sessions to the file
        for collaborationSession in list:
            firstTimestamp = collaborationSession.getFirstTimestamp()
            firstTimestamp = firstTimestamp.strftime("%d/%m/%Y, %H:%M:%S")
            lastTimestamp = collaborationSession.getLastTimestamp()
            lastTimestamp = lastTimestamp.strftime("%d/%m/%Y, %H:%M:%S")
            medianTimestamp = collaborationSession.getMedianTimestamp()
            medianTimestamp = medianTimestamp.strftime("%d/%m/%Y, %H:%M:%S")


            writer.writerow([collaborationSession.getSource().getID(), collaborationSession.getSource().getLabel(),
            collaborationSession.getTarget().getID(),collaborationSession.getTarget().getLabel(), collaborationSession.getObject().getID(), collaborationSession.getObject().getName(),firstTimestamp,lastTimestamp, medianTimestamp ])

    #Write the resources ID and label to CSV
    #@param resources:  list of Resource objects
    def writeResourcesToCSV(self,resources):
        filename = "resources.csv"

        writer = csv.writer(io.open(filename,'w+',newline='',encoding="utf-8"),delimiter=";")
        #write header
        writer.writerow(["ResourceID","Label"])
        for resource in resources:
            writer.writerow([resource.getID(), resource.getLabel()])


    #Write the object ID and label to CSV
    #@param objects:  list of Resource objects
    def writeObjectsToCSV(self,objects):
        filename = "objects.csv"

        writer = csv.writer(io.open(filename,'w+',newline='',encoding="utf-8"),delimiter=";")
        #write header
        writer.writerow(["ObjectID","Label"])
        for object in objects:
            writer.writerow([object.getID(), object.getName()])