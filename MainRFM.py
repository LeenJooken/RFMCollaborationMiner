#Calculate the RFM scores for resources and their relationships and export them to csv


import Log
import Output
import CollaborationIdentifier
import WorksessionIdentifier
import Graph
import argparse




#main function of the program
def main(log_file,nodes_file,edges_file):
    #read and parse the log
    log = Log.Log(log_file)
    #identifying the worksessions
    print("Identifying the worksessions")
    sessionIdentifier = WorksessionIdentifier.WorksessionIdentifier(log.getEventList(), log.getResourceList(),log.getObjectList())


    #identifying  the collaborations
    print("Identifying the collaborations")
    collabIdentifier = CollaborationIdentifier.CollaborationIdentifier(log.getEventList(), log.getResourceList(),log.getObjectList())

    #construct the graph
    print("Calculating the RFM values:")
    socialgraph = Graph.Graph()
    socialgraph.constructGraph(log.getEventList(),log.getResourceList(),collabIdentifier.getCollaborationList(),sessionIdentifier.getWorksessions())
    nodes = socialgraph.getNodesList()
    edges = socialgraph.getEdgesList()

    #Write output files
    print("Writing the output files")
    writeOutput = Output.Output()
    writeOutput.writeRFMToCSV(nodes,edges,nodes_file,edges_file)
    print("Done")


########################################
#parse the command line arguments
print("Parsing the arguments")
parser = argparse.ArgumentParser()
parser.add_argument("-s","--source",help="pass the sourcefile to be read")
parser.add_argument("-nf","--nodes_filename",help="pass the resources CSV filename")
parser.add_argument("-ef","--edges_filename",help="pass the relationships CSV filename")

args = parser.parse_args()
log_file = args.source
nodes_file = args.nodes_filename
edges_file = args.edges_filename

#run the program
main(log_file,nodes_file,edges_file)
