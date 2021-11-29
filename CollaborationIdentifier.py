#Class that identifies collaborations in the list of events that is passed to it
import datetime
from datetime import timedelta
import Collaboration

class CollaborationIdentifier:

    #@param events: list of Event objects
    #@param resources : list of Resource objects
    #@param objects : list of Object objects
    #@param maxDurationSession : timewindow how long a collaboration can be at max in minutes; default = 7 days
    #@param minTimeBetween : if there is this much time between 2 events, it means that the second belongs to a new collaboration session; in minutes
    def __init__(self, events, resources, objects,  maxDurationSession = 10080 , minTimeBetween = 20160 ):
        self.events = events
        self.resources = resources
        self.objects = objects
        self.maxDurationSession = maxDurationSession
        self.minTimeBetween = minTimeBetween
        self.collaborations = []

        self.identifyCollaborations()




    def getCollaborationList(self):
        return self.collaborations

    #Function that identifies the collaborations in the event list
    def identifyCollaborations(self):
        #check for each pair of resources
        for sourceIterator in range(0,len(self.resources)-1):
            source = self.resources[sourceIterator]
            for targetIterator in range(sourceIterator+1,len(self.resources)):
                target = self.resources[targetIterator]


                #identify the collaboration on their mutual files
                self.identifyCollaborationsForPair(source,target)



    #Identify collaboration on their mutual files and make for each one a Collaboration object
    #@param source:  resource 1  of the type Resource object
    #@param target:  resource 2  of the type Resource object
    def identifyCollaborationsForPair(self,source,target):
        filesSource = source.getListOfObjects()
        filesTarget = target.getListOfObjects()

        #get list of files they have in common
        filesInCommon = self.getItemsInCommon(filesSource, filesTarget)


        for file in filesInCommon:
            #determine and make the Collaboration objects
            self.identifyCollaborationsForPairFile(source,target,file)


    #@param list1
    #@param list2
    #@returns list of the items they have in common
    def getItemsInCommon(self,list1, list2):
        list1_set = set(list1)
        list2_set = set(list2)
        itemsInCommon = list1_set & list2_set
        return itemsInCommon

    #Function that identifies the collaboration between the source resource
    #and target resource on the given object
    #@param source : Resource object
    #@param target : Programmer object
    #@param file : Object object they are collaborating on
    #@condition: both resources should have worked on the object at least once (there has to be a timestamp of an event i which this resource worked on this object)
    def identifyCollaborationsForPairFile(self,source,target,file):
        timestampsSource = source.getTimestampsForObject(file)
        timestampsSource.sort()
        timestampsTarget = target.getTimestampsForObject(file)
        timestampsTarget.sort()

        #make these arrays into arrays of tuples that specify the label so we know which resource
        tuplesSource = self.makeTupleArrayTimestampLabel(timestampsSource,"Source")
        tuplesTarget = self.makeTupleArrayTimestampLabel(timestampsTarget,"Target")
        #make it into 1 array and sort it according to timestamp
        timestamps = tuplesSource + tuplesTarget

        #sort based on timestamp
        timestamps = sorted(timestamps,key = lambda x: x[1])

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
                #end of this collaboration session
                self.processCollaboration(source,target,file,session)
                session = []

            session.append(nextItem)
            previousItem = nextItem
            previousStamp = nextStamp

        #process the last session
        self.processCollaboration(source,target,file,session)



    #Function that makes a array of tuples with the label as the first element and the timestamp as the second
    #@param timestamps : array of datetime elements
    #@param label : textstring as label
    #@returns array of tuples with the label as the first element and the timestamp as the second
    def makeTupleArrayTimestampLabel(self,timestamps,label):
        tuples = []
        for ts in timestamps:
            tuples.append((label,ts))

        return tuples


    #Process the collaboration session:
    #if it is longer than the max duration of a session it needs to be split into separate parts
    #@param source : Resource object
    #@param target : Resource object
    #@param file : Object object they are collaborating on
    #@param session : array with tuples: key = "source", or "target" to indicate whose timestamp it is; and value = timestamp ORDERED ON TIMESTAMP
    def processCollaboration(self,source,target,file,session):
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
            self.processCollaboration(source,target,file,firstpart)
            self.processCollaboration(source,target,file,secondpart)


        else:
            #this is 1 session, make a collaboration object
            self.createCollaboration(source,target,file,session)



    #Find between which 2 timestamps is the biggest gap and return these indexes
    #@param session: array with tuples: key = "source", or "target" to indicate whose timestamp it is; and value = timestamp  ORDERED ON TIMESTAMP
    #@returns index after which the biggest gap appears
    def findBiggestTimegap(self, session):
        timestamps = []
        for s in session:
            timestamps.append(s[1])

        #Midpoint of the session
        midpoint = timestamps[0] + ((timestamps[-1] - timestamps[0])/2)
        index = 0
        currentMaxDiff = 0

        previousStamp = session[0][1]

        for i in range(1,len(session)):
            nextStamp = session[i][1]
            diff = nextStamp - previousStamp
            #Difference in minutes
            diff = diff.total_seconds()/60

            if (diff > currentMaxDiff):
                index = i-1
                currentMaxDiff = diff
            elif (diff == currentMaxDiff):
                #determine which gap is more favourable
                index = self.determineMostFavourableCutpoint(index,i-1,session,midpoint,diff)

            previousStamp = nextStamp

        return index

    #Function that determines whether index1 or index2 is the better cutpoint to cut the timestamps array into 2, based on which results in more collaborations
    #@param index1 :  first index of the timestamps array , 1st possible cutpoint
    #@param index2 : second index of the timestamps array , 2nd possible cutpoint
    #@param session : array with tuples: key = "source", or "target" to indicate whose timestamp it is; and value = timestamp  ORDERED ON TIMESTAMP
    #@param midpoint  : timedate that indicates the midpoint of a window
    #@param gapsize: size of gap in minutes
    #@returns index1 or 2 , depending which one is the better cutpoint
    #The best cutpoint cuts the array into 2 of which both parts contain collaboration
    #The 2nd best cutpoint results into 1 collaboration (and lies closest to the midpoint of the window)
    #The least best option is when neither cutpoint leads to collaboration, so the point closest to the midpoint of the window is returned
    def determineMostFavourableCutpoint(self, index1,index2,session,midpoint,gapsize):
        #Determine if there is collaboration in the window parts
        collabTypeIndex1 = self.determineQualitySplitpoint(index1,session)
        collabTypeIndex2 = self.determineQualitySplitpoint(index2,session)

        #compare them
        if (collabTypeIndex1 < collabTypeIndex2):
            #index 1 is better
            index =  index1
        elif (collabTypeIndex2 < collabTypeIndex1):
            #index 2 is better
            index =  index2
        else :
            #they are equal, so choose the point that is closest to the midpoint of the window
            index = self.determineClosesToMidpoint(midpoint, index1, index2,session,gapsize)

        return index


    #Function that determines whether the timestamp on index 1 or 2 is the closest to the given midpoint
    #@param midpoint  : timedate that indicates the midpoint of a window
    #@param index1 :  first index of the timestamps array of which its timestamp needs to be compared to the midpoint
    #@param index2 : second index of the timestamps array of which its timestamp needs to be compared to the midpoint
    #@param session : array with tuples: key = "source", or "target" to indicate whose timestamp it is; and value = timestamp  ORDERED ON TIMESTAMP
    #@param gapsize: size of gap in minutes
    #@returns index1 or 2 , depending on which timestamp[index] + gapsize/2 lies closes to the midpoint
    def determineClosesToMidpoint(self, midpoint, index1, index2, session,gapsize):
        #find time in the middle of the gap
        stamp1 = session[index1][1] + timedelta(minutes = (gapsize/2))
        stamp2 = session[index2][1] + timedelta(minutes = (gapsize/2))

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



    #Function that determines how good the split point is
    #@param index : nindex to split the array on
    #@param session : array with tuples: key = "source", or "target" to indicate whose timestamp it is; and value = timestamp  ORDERED ON TIMESTAMP
    #@return how good the splitpoint is on a scale of 3, 1 being the highest score
    def determineQualitySplitpoint(self,index,session):
        qualityvalue = 2

        #split in 2
        firstpart = session[0:index+1]
        secondpart = session[index+1:]

        #Determine if there is collaboration in the window parts
        collabPart1 = self.isThereCollaborationInWindow(firstpart)
        collabPart2 = self.isThereCollaborationInWindow(secondpart)

        if(collabPart1 and collabPart2):
            qualityvalue = 1
        elif not(collabPart1 or collabPart2):
            qualityvalue = 3
        #else qualityvalue = 2

        return qualityvalue

    #Function that checks if both source and target have timestamps in this session
    #@param session : array with tuples: key = "source", or "target" to indicate whose timestamp it is; and value = timestamp
    #@returns whether there is collaboration between the source and target in this window (both have at least 1 timestamp in this window)
    def isThereCollaborationInWindow(self,session):
        collab = False
        arrays = self.convertTupleArrayToTimestampArray(session)
        sourceTimestamps = arrays[0]
        targetTimestamps = arrays[1]
        #if they both contain timestamps, collaboration took place
        if(sourceTimestamps and targetTimestamps):
            collab = True

        return collab



    #Create a collaboration object ONLY IF collaboration took place in this window
    #@param source : Resource object
    #@param target : Resource object
    #@param file : Object object they are collaborating on
    #@param session : array with tuples: key = "source", or "target" to indicate whose timestamp it is; and value = timestamp
    def createCollaboration(self,source,target,file,session):
        timestampArrays = self.convertTupleArrayToTimestampArray(session)
        sourceStampsInWindow = timestampArrays[0]
        targetStampsInWindow = timestampArrays[1]

        #if they both contain timestamps, collaboration took place
        if(sourceStampsInWindow and targetStampsInWindow):
            #make a collaboration object
            collaboration = Collaboration.Collaboration(source,target,file,sourceStampsInWindow,targetStampsInWindow)
            #add to the collaboration list
            self.collaborations.append(collaboration)


    #Convert the array of tuples of format ("Source",datetime object) or ("Target",datetime object)
    #to 2 separate arrays only containing the source datetime objects or target ones
    #@param session : array of tuples of format ("Source",datetime object) or ("Target",datetime object)
    #@returns tuple(array1,array2) with array1 an array of only the source timestamps, and array2 one of only the target timestamps
    def convertTupleArrayToTimestampArray(self, session):
        sourceStamps = [elem[1] for elem in session if elem[0] == "Source"]
        targetStamps = [elem[1] for elem in session if elem[0] == "Target"]
        sourceStamps.sort()
        targetStamps.sort()

        return(sourceStamps,targetStamps)



    def printCollaborations(self):
        print("The collaborations that were identified:")
        for c in self.collaborations :
            c.print()


    def printTimestamps(self,stamps):
        for t in stamps:
            print(t.strftime("%m/%d/%Y, %H:%M:%S"))
