#class that represents 1 event
#Represents a resource that worked on an object at a specific moment in time

class Event:

    #@param resource : a programmer object
    #@param timestamp:  a datetime object
    #@param object :   a file object
    #@param modifier:  if the file was "added" , "modified", or "deleted"
    def __init__(self, resource, timestamp, object, modifier):
        self.resource = resource
        self.timestamp = timestamp
        self.object = object

        if modifier in ("Added","Deleted","Modified"):
            self.modifier = modifier
        else:
            print("Modifier unknown: ", modifier)
            self.modifier = "Modified"


    def getTimestamp(self):
        return self.timestamp

    def getObject(self):
        return self.object


    def print(self):
        print( self.resource.getLabel(), " worked on ", self.object.getName(), " on ", self.timestamp.strftime("%m/%d/%Y, %H:%M:%S"))
