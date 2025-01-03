#Calculate the RFM scores for resources and their relationships and export them to csv


import Log
import Output
import CollaborationIdentifier
import WorksessionIdentifier
import Graph
import argparse




#main function of the program
def main(log_file,nodes_file,edges_file,writeSessionsToCSV,wsMaxDuration,csMaxDuration,wsMaxIet,csMaxIet):
    #read and parse the log
    log = Log.Log(log_file)
    #identifying the worksessions
    print("Identifying the worksessions")
    sessionIdentifier = WorksessionIdentifier.WorksessionIdentifier(log.getEventList(), log.getResourceList(),log.getObjectList(),wsMaxDuration,wsMaxIet)


    #identifying  the collaborations
    print("Identifying the collaborations")
    collabIdentifier = CollaborationIdentifier.CollaborationIdentifier(log.getEventList(), log.getResourceList(),log.getObjectList(),csMaxDuration,csMaxIet)


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


    if writeSessionsToCSV:
        listOfWorkSessions = sessionIdentifier.getWorksessions()
        listOfCollaborations = collabIdentifier.getCollaborationList()
        print("Writing the collaboration session list to CSV")
        writeOutput.writeCollabListToCSV(listOfCollaborations)
        print("Writing the work session list to CSV")
        writeOutput.writeWorkSessionListToCSV(listOfWorkSessions)
        # write the resources to CSV
        # write the objects to CSV
        objects = log.getObjectList()
        resources = log.getResourceList()
        print("Writing the resource list to CSV")
        writeOutput.writeResourcesToCSV(resources)
        print("Writing the object list to CSV")
        writeOutput.writeObjectsToCSV(objects)

    print("Done")


########################################

#parse the command line arguments
print("Parsing the arguments")
parser = argparse.ArgumentParser()
parser.add_argument("-s","--source",help="pass the sourcefile to be read")
parser.add_argument("-nf","--nodes_filename",help="pass the resources CSV filename")
parser.add_argument("-ef","--edges_filename",help="pass the relationships CSV filename")
parser.add_argument("-wsD","--ws_duration",default=240,help="pass the maximal duration of a work session in minutes")
parser.add_argument("-wsIet","--ws_iet",default=1440, help="pass the maximal inter-event time for the work sessions in minutes")
parser.add_argument("-csD","--cs_duration",default=10080,help="pass the maximal duration of a collaboration session in minutes")
parser.add_argument("-csIet","--cs_iet",default=20160,help="pass the maximal inter-event time for the collaboration sessions in minutes")
parser.add_argument("-print","--print_sessions",action="store_true",help="include this when you want to print the session data to CSV")

args = parser.parse_args()
log_file = args.source
nodes_file = args.nodes_filename
edges_file = args.edges_filename
sessionData = args.print_sessions
wsMaxDuration = int(args.ws_duration)
csMaxDuration = int(args.cs_duration)
wsMaxIet = int(args.ws_iet)
csMaxIet = int(args.cs_iet)

log_file = "book3.git"
#run the program
main(log_file,nodes_file,edges_file,sessionData,wsMaxDuration,csMaxDuration,wsMaxIet,csMaxIet)


