#Class that represents a work session of one resource
#contains a number of events
import statistics

class Worksession:

    #@param resource  :  Resource object
    #@param events : list of Event objects
    def __init__(self,resource, events):
        self.resource = resource
        self.events = events

    def getResource(self):
        return self.resource

    #@returns DISTINCT list of objects that appear in the events of this worksession
    def getObjects(self):
        objects = []
        for e in self.events:
            o = e.getObject()
            if o not in objects:
                objects.append(o)
        return objects

    def getFirstTimestamp(self):
        timestamps = []
        for e in self.events :
            ts = e.getTimestamp()

            #only distinct timestamps to get an overview on which points in time events took place, not how many events
            if ts not in timestamps:
                timestamps.append(ts)

        timestamps.sort()

        return timestamps[0]

    def getLastTimestamp(self):
        timestamps = []
        for e in self.events :
            ts = e.getTimestamp()

            #only distinct timestamps to get an overview on which points in time events took place, not how many events
            if ts not in timestamps:
                timestamps.append(ts)

        timestamps.sort()

        return timestamps[-1]

    #@returns the median timestamp of all the events in the worksession
    def getMedianTimestamp(self):
        timestamps = []
        for e in self.events :
            ts = e.getTimestamp()

            #only distinct timestamps to get an overview on which points in time events took place, not how many events
            if ts not in timestamps:
                timestamps.append(ts)

        timestamps.sort()
        numberOfStamps = len(timestamps)

        #if it's even
        if numberOfStamps % 2 == 0:
            #get median in an even array
            stamp1 = timestamps[int((numberOfStamps/2))-1]
            stamp2 = timestamps[int(numberOfStamps/2)]
            #find middle point
            median = stamp1 + (stamp2 - stamp1)/2
        else:
            #Get the median in an odd array
            median = timestamps[int((numberOfStamps-1)/2)]


        return median

    def getTimestamps(self):
        ts = []
        for e in self.events:
            ts.append(e.getTimestamp())
        return ts

    def print(self):
        print("During this work session, resource ", self.resource.getLabel()," worked on:")
        for e in self.events:
            e.print()
