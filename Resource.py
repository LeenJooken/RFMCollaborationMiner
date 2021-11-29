#class that represents a resource

class Resource:
    def __init__(self,name,id):
        self.name = name
        self.ID = id
        self.aliases = [name]

        #list of all the events this resource is involved in
        #reflects when the resource worked on which object
        #list of Event objects
        self.events = []



    def getName(self):
        return self.name

    def setName(self,name):
        self.name = name

    def getID(self):
        return self.ID

    #add an alias for this resource
    def addAlias(self,name):
        if not (name in self.aliases):
            self.aliases.append(name)

    #get list of resource names
    def getNames(self):
        return self.aliases

    #returns a string of all the resource aliases
    def getLabel(self):
        label = ""
        count = 0
        for alias in self.aliases:
            if(count != 0):
                label += "+"
            label += alias
            count += 1
        return label


    def getEvents(self):
        return self.events

    #Append this event to the resource's list of events in which he was involved
    #@param event  : event object
    def addEvent(self,event):
        self.events.append(event)

    #@returns a list of  all the objects this programmer worked on in his Event list
    def getListOfObjects(self):
        files = []
        for e in self.events:
            f = e.getObject()
            if f not in files:
                files.append(f)

        return files

    #@param file : Object object
    #@returns a list of time stamps the programmer worked on this object
    def getTimestampsForObject(self,file):
        timestamps = []
        for e in self.events:
            if e.getObject() == file:
                time = e.getTimestamp()
                if time not in timestamps:
                    timestamps.append(time)

        return timestamps
