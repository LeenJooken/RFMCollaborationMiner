#Class that represents a collaboration


class Collaboration:

    #@param resource1  :  Resource object
    #@param resource2  : Resource object
    #@param timestampsRS1  : list of datetime object of when resource 1 worked on the object that are all considered part of the same collaboration
    #@param timestampsRS2  : list of datetime object of when resource 2 worked on the object that are all considered part of the same collaboration
    #@param object :  Object object
    def __init__(self,resource1, resource2, object, timestampsRS1, timestampsRS2):
        self.resource1 = resource1
        self.timestampsResource1 = timestampsRS1
        self.resource2 = resource2
        self.timestampsResource2 = timestampsRS2
        self.object = object

    def getSource(self):
        return self.resource1

    def getTarget(self):
        return self.resource2

    def getTupleFormat(self):
        return (self.resource1,self.resource2)

    def getObject(self):
        return self.object

    def getFirstTimestamp(self):
        timestamps = self.timestampsResource1 + self.timestampsResource2

        timestamps.sort()

        return timestamps[0]

    def getLastTimestamp(self):
        timestamps = self.timestampsResource1 + self.timestampsResource2

        timestamps.sort()

        return timestamps[-1]

    #@returns the median timestamp of all the timestamps in the collaboration
    def getMedianTimestamp(self):
        #remove duplicate timestamps from the lists of resource 1 and 2
        #Not necessary here as duplicates are already removed when making the collaboration session
        #resource1Timestamps = list(dict.fromkeys(self.timestampsResource1))
        #resource2Timestamps = list(dict.fromkeys(self.timestampsResource2))
        #Note that there still could be duplicates if the same stamp is in R1 and R2, but this is okay
        timestamps = self.timestampsResource1 + self.timestampsResource2

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


    #print out the content of this class in the command line
    def print(self):
        print("Collaboration between: ", self.resource1.getLabel(), " and ", self.resource2.getLabel(), " on file ", self.object.getName())
        print("Timestamps source: ")
        for t in self.timestampsResource1:
            print(t.strftime("%m/%d/%Y, %H:%M:%S"))
        print("Timestamps target: ")
        for t in self.timestampsResource2:
            print(t.strftime("%m/%d/%Y, %H:%M:%S"))
