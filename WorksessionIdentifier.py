import Worksession
import Event
import datetime
from datetime import timedelta

class WorksessionIdentifier:

    #@param events: list of Event objects
    #@param resources : list of Resource objects
    #@param objects : list of Object objects
    #@param maxDurationSession : timewindow how long a worksession can be at max in minutes
    #@param minTimeBetween : if there is this much time between 2 events, it means that the second belongs to a new worksession; in minutes
    def __init__(self, events, resources, objects, maxDurationSession = 240 , minTimeBetween = 1440 ):
        self.events = events
        self.resources = resources
        self.objects = objects
        self.maxDurationSession = maxDurationSession
        self.minTimeBetween = minTimeBetween
        self.worksessions = []

        self.identifyWorksessions()



    #@returns array of Worksession elements
    def getWorksessions(self):
        return self.worksessions

    #Function that will identify the work sessions for every resource
    def identifyWorksessions(self):
        #check for each resource
        for resource in self.resources:
            events = resource.getEvents()
            self.identifyWorksessionsForResource(resource,events)


    #Identifies the worksessions for this resource based on the event list and makes the worksession objects
    #@param resource : Resource object
    #@param events : list of Event objects
    def identifyWorksessionsForResource(self, resource, events):
        #get dict with as key the event and value the timestamp
        timestamps = self.getTimestamps(events)
        #sort by timestamp
        timestamps = sorted(timestamps.items(),key = lambda x: x[1])

        session = []
        previousItem = timestamps[0]
        previousStamp = previousItem[1]
        session.append(previousItem)

        for counter in range(1,len(timestamps)):
            nextItem = timestamps[counter]
            nextStamp = nextItem[1]
            #if difference > minTimeBetween : it is the start of a new session
            boundarypoint = previousStamp + timedelta(minutes = self.minTimeBetween)
            if nextStamp > boundarypoint:
                #end of this worksession
                self.processWorksession(resource,session)
                session = []

            session.append(nextItem)
            previousItem = nextItem
            previousStamp = nextStamp

        #process the last session
        self.processWorksession(resource,session)





    #Process the worksession:
    #if it is longer than the max duration of a session it needs to be split into separate parts
    #@param resource : Resource object
    #@param session : array with dict items: key = event and value = timestamp
    def processWorksession(self,resource,session):
        firstTimeStamp = session[0][1]
        lastTimeStamp = session[-1][1]

        endpoint = firstTimeStamp + timedelta(minutes = self.maxDurationSession)
        if lastTimeStamp > endpoint:
            #need to split
            #find the biggest gap
            index = self.findBiggestTimegap(session)

            #split in 2
            firstpart = session[0:index+1]
            secondpart = session[index+1:]
            #process each of the parts
            self.processWorksession(resource,firstpart)
            self.processWorksession(resource,secondpart)


        else:
            #this is 1 session, make a session object
            self.createWorkSession(resource,session)




    #Create a work session object
    #@param resource : Resource object
    #@param session : array with dict items: key = event and value = timestamp
    def createWorkSession(self,resource, session):
        events = []
        for s in session:
            events.append(s[0])

        worksession = Worksession.Worksession(resource,events)
        self.worksessions.append(worksession)


    #Find between which 2 timestamps is the biggest gap and return these indexes
    #@param session: array with dict items: event as key and timestamp as value  ORDERED ON TIMESTAMP
    #@returns index after which the biggest gap appears
    def findBiggestTimegap(self, session):
        timestamps = []
        for s in session:
            timestamps.append(s[1])

        #Midpoint of the session
        midpoint = timestamps[0] + ((timestamps[-1] - timestamps[0])/2)
        index = 0
        currentMaxDiff = 0
        previousStamp = timestamps[0]

        for i in range(1,len(timestamps)):
            nextStamp = timestamps[i]
            diff = nextStamp - previousStamp
            #Difference in minutes
            diff = diff.total_seconds()/60

            if (diff > currentMaxDiff):
                index = i-1
                currentMaxDiff = diff
            elif (diff == currentMaxDiff):
                #look which one is more towards the midpoint of the session's timewindow
                #returns the index that is closes to the midpoint
                index = self.determineClosesToMidpoint(midpoint, index, i-1, timestamps,diff)

            previousStamp = nextStamp

        return index

    #Function that determines whether the timestamp on index 1 or 2 is the closest to the given midpoint
    #@param midpoint  : timedate that indicates the midpoint of a window
    #@param index1 :  first index of the timestamps array of which its timestamp needs to be compared to the midpoint
    #@param index2 : second index of the timestamps array of which its timestamp needs to be compared to the midpoint
    #@param timestamps : array with timestamps, ordered
    #@param gapsize: size of gap in minutes
    #@returns index1 or 2 , depending on which timestamp[index] + gapsize/2 lies closes to the midpoint
    def determineClosesToMidpoint(self, midpoint, index1, index2, timestamps,gapsize):
        #find time in the middle of the gap
        stamp1 = timestamps[index1] + timedelta(minutes = (gapsize/2))
        stamp2 = timestamps[index2] + timedelta(minutes = (gapsize/2))

        if stamp1 < midpoint:
            diff1 = midpoint - stamp1
        else:
            diff1 = stamp1 - midpoint

        if stamp2 < midpoint:
            diff2 = midpoint - stamp2
        else:
            diff2 = stamp2 - midpoint

        #compare diff1 and 2
        if diff2 < diff1:
            return index2
        #else
        return index1



    #@param events : list of Event objects
    #@returns : a dict with the event as key and timestamp as value
    def getTimestamps(self,events):
        dict = {}
        for e in events:
            dict[e] = e.getTimestamp()

        return dict


    def print(self):
        print("The worksessions that were identified:")
        for w in self.worksessions:
            w.print()
