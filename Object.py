#Represents an object

class Object:

    def __init__(self,ID,name):
        self.name = name
        self.ID = ID
        self.importance = 1

        #keep track of the events in which this file was the object
        self.modifiedIn = []
        self.addedIn = []
        self.deletedIn = []



    def getName(self):
        return self.name

    def getID(self):
        return self.ID

    def getImportance(self):
        return self.importance

    #Add an event to the right list according to the modifier
    #@param event : Event object
    #@param modifier : "Added" "Deleted"  or "Modified"
    def addEvent(self, event, modifier):

        if modifier == "Added":
            if(not event in self.addedIn):
                self.addedIn.append(event)
        elif modifier == "Deleted":
            if(not event in self.deletedIn):
                self.deletedIn.append(event)
        else:
            if(not event in self.modifiedIn):
                self.modifiedIn.append(event)


    #Function that calculates the importance of a object based on a ratio:
    #the number of months in which it was changed / the number of months is exists
    #@param firstAndLastTimeStamp  = tuple with the first timestamp of the log and the last
    def calculateImportanceRatio(self,firstAndLastTimeStamp):
        addedTimestamps = []
        for event in self.addedIn:
            addedTimestamps.append(event.getTimestamp())
        addedTimestamps.sort()
        deletedTimestamps = []
        for event in self.deletedIn:
            deletedTimestamps.append(event.getTimestamp())
        deletedTimestamps.sort()
        timestamps = []
        for event in self.modifiedIn:
            timestamps.append(event.getTimestamp())
        for event in self.addedIn:
            timestamps.append(event.getTimestamp())

        numberOfMonthsExistence = 0
        numberOfMonthsChanged = 0
        iteratorAdded = 0
        iteratorDeleted = 0


        if(not addedTimestamps):
            beginstamp = firstAndLastTimeStamp[0]
            #only 2 scenarios possible : 0 or 1 deleted timestamp
            if(not deletedTimestamps):
                endstamp = firstAndLastTimeStamp[1]
            else:
                endstamp = deletedTimestamps[0]
            numberOfMonthsExistence += self.calculateNumberOfMonthsExistence(beginstamp,endstamp)
            numberOfMonthsChanged += self.calculateNumberOfMonthsChanged(beginstamp,endstamp,timestamps)


        while(iteratorAdded < len(addedTimestamps)):
            beginstamp = addedTimestamps[iteratorAdded]
            iteratorAdded += 1

            if(iteratorDeleted == len(deletedTimestamps)):
                #all deleted stamps are done
                endstamp = firstAndLastTimeStamp[1]

            else:
                endstamp = deletedTimestamps[iteratorDeleted]
                iteratorDeleted += 1

            if(endstamp < beginstamp):
                beginstamp = firstAndLastTimeStamp[0]
                iteratorAdded -= 1


            numberOfMonthsExistence += self.calculateNumberOfMonthsExistence(beginstamp,endstamp)
            numberOfMonthsChanged += self.calculateNumberOfMonthsChanged(beginstamp,endstamp,timestamps)



        importance = numberOfMonthsChanged/numberOfMonthsExistence

        #what if importance = 0 ?
        if importance == 0 :
            importance = 0.00001


        self.importance = importance




    #calculate how many months this object exists between these 2 timestamps
    def calculateNumberOfMonthsExistence(self,beginstamp, endstamp):

        numberOfMonths = abs(endstamp.year - beginstamp.year) * 12 + abs(endstamp.month - beginstamp.month)
        numberOfMonths += 1
        return numberOfMonths

    #calculate in how many months between begin and end the object was changed
    #@param timestamps = list of timestamps when the file was committed
    def calculateNumberOfMonthsChanged(self,beginstamp,endstamp,timestamps):
        timestamps.sort()
        numberOfMonths = 0
        currentMonth = -1
        currentYear = -1
        for stamp in timestamps:
            #only consider the timestamps between the timespan
            if((stamp >= beginstamp)and(stamp <= endstamp)):
                if((stamp.month != currentMonth) or (currentYear != stamp.year)):
                    currentMonth = stamp.month
                    currentYear = stamp.year
                    numberOfMonths += 1

        return numberOfMonths
