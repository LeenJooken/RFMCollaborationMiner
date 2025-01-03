#class that represents a parsed log
#parses the log into a list of events

import Event
import Resource
import Object
import time
import re
from time import mktime
from datetime import datetime
import textdistance
import sys

class Log:
    def __init__(self,logFile):
        self.filename = logFile
        self.listOfResources = []
        self.resourceIterator = 1
        self.objectIterator = 1
        self.listOfObjects = []
        self.listOfEvents = []

        #if input is event log: NOT SUPPORTED YET !
        if(self.filename.lower().endswith('.xes')):
            #self.parseXESLog()
            sys.exit("Error: File format is currently not supported!")
        #if input is svn log: NOT SUPPORTED YET !
        elif(self.filename.lower().endswith('.txt')):
            #self.parseSVNLog()
            sys.exit("Error: File format is currently not supported!")
        #if input is git log:
        elif(self.filename.lower().endswith('.git')):
            self.parseGITlog()
            self.calculateObjectImportance()
        else:
            sys.exit("Error: File format is not supported!")






    def getEventList(self):
        return self.listOfEvents

    def getResourceList(self):
        return self.listOfResources

    def getObjectList(self):
        return self.listOfObjects

    #parses the git log extracted by the commando in the git bash:
    #git log --name-status --abbrev-commit --pretty=format:'%h,%an,%ad,%(trailers:key=Co-Authored-by,separator=%x2C,valueonly=TRUE)' --date=iso-local --diff-merges=c --no-renames > log.git
    def parseGITlog(self):
        commitlines = []
        with open(self.filename,'r',encoding="utf8") as f:
            for line in f:

                line = line.strip()
                lineparts = line.split(",")
                #ending conditions:
                #if \n or line contains > 2 parts: all the relevant commit lines have been collected
                #if \n: skipp this line
                if line:

                #if a new commit starts
                    if (len(lineparts) > 2):
                        #first parse the commit if there was already one in the list
                        if commitlines:
                            #and it was not an empty commit
                            if len(commitlines) > 1:

                                self.parseGITcommit(commitlines)
                                commitlines.clear()
                            else:
                                #throw away empty commit

                                commitlines.clear()
                        #then start the new commit
                        commitlines.append(line)

                    #else append line to the list
                    else:
                        commitlines.append(line)

        #parse the last commit, if the list is not empty
        if commitlines:
            if len(commitlines) > 1:

                self.parseGITcommit(commitlines)

        f.close()


    #function that parses a commit and extracts the events into the interal data structure
    #@param commitlines : list of the different commit lines in the log
    #first line contains commit ID, author, date, and possible coauthors
    #then the files proceeded by their modifier status
    def parseGITcommit(self,commitlines):

        #if list contains only 1 item, it's an empty commit
        if len(commitlines) > 1:
            #parse this commit
            basicinfo = commitlines[0].split(",")
            rev_number = basicinfo[0].strip()

            author = basicinfo[1].lower().strip()
            #try to make a date, it is possible that some resources have a comma formatted name "lastname, firstname"
            try:
                date = time.strptime(basicinfo[2],"%Y-%m-%d %H:%M:%S %z")
            except ValueError:

                author += " " + basicinfo[2].lower().strip()
                date = time.strptime(basicinfo[3],"%Y-%m-%d %H:%M:%S %z")
                #also change the basicinfo array
                basicinfo[1] = author
                basicinfo[2] = date
                basicinfo = basicinfo[:2]+basicinfo[3:]



            date = datetime.fromtimestamp(mktime(date))
            #programmers
            programmers = self.getProgrammersGIT(author,basicinfo)

            filesInfo = self.getFilesGIT(commitlines[1:])
            filelist = filesInfo[0]
            fileStatus = filesInfo[1]
            #now we have all the information, identify the events and add it to the event list
            #identify the events: each programmer worked on each file = event
            #for each programmer
            for p in programmers:
                for fKey, fInfo in fileStatus.items():
                    file = fInfo['File']
                    modifier = fInfo['Status']
                    #make the event
                    event = Event.Event(p, date,file,modifier)
                    #add it to the list
                    self.listOfEvents.append(event)
                    #add this event also to the list of events of the programmer
                    p.addEvent(event)

                    #add this event also to the file object
                    file.addEvent(event,modifier)




    #Function that parses the programmers from this list and returns an array of programmer objects
    #@param author: first author of this commit
    #@param basicinfo: list with commitID, author, date and then possible co-authors
    #@return list of programmer objects that worked on the commit
    def getProgrammersGIT(self,author, basicinfo):
        programmers = []

        #search author
        prog = self.getProgrammerObject(author)
        programmers.append(prog)

        #co-authors
        for i in range(3,len(basicinfo)):
            progName = basicinfo[i]
            #check if not empty
            if progName:
                progNameParts = progName.split("<")
                progName = progNameParts[0].lower().strip()
                prog = self.getProgrammerObject(progName)
                if(prog not in programmers):
                    programmers.append(prog)


        return programmers


    #search in the list of programmers if this programmer already exists as an object
    #@param progName : name of the programmer
    def getProgrammerObject(self,progName):
        prog = self.searchProgrammer(progName)

        #no existing programmer found with this name, create one
        if(not isinstance(prog,Resource.Resource)):

            prog = Resource.Resource(progName,self.resourceIterator)
            #this iterator will also be the node number
            self.resourceIterator = self.resourceIterator +1
            #add it to the general overview list
            self.listOfResources.append(prog)

        return prog



    #search if the programmer with this name already exists in the list
    #@param name = name of the programmer
    #@returns that programmer object
    def searchProgrammer(self,name):

        for elem in self.listOfResources:
            #get list of element's names
            programmerAliases = elem.getNames()
            for programmerAlias in programmerAliases:

                #comparison is case insensitive
                if(programmerAlias.lower() == name.lower()):

                    return elem

                #Take typing errors into account using string comparison

                #Toggle this to include typo check
                isTypo = self.checkIfTypo(programmerAlias.lower(), name.lower())
                #name is basically the same, only with a typo
                if(isTypo):

                    #add this name as an alias for this programmer
                    elem.addAlias(name.lower())

                    return elem
        return ""


    #Check if the two names are the same but contain a typo
    #Do this by calculating the jaro-winkler distance

    #@param name1 = first name of the comparison
    #@param name2 = second name of the comparison
    #@returns True if both string have a high probability of being the same
    def checkIfTypo(self,name1, name2):

        jaroWinkler = textdistance.jaro_winkler(name1,name2)

        if (jaroWinkler > 0.92):

            return True
        else:
            return False


    #Function that returns a list of file objects that belong to the commit
    #@param filelist : list with modifier \t filepath
    #@return [list of file objects, dict with file and its respective modifier]
    def getFilesGIT(self,filelist):
        files = []
        fileStatus = {}
        fileStatIterator = 1

        for i in range(0,len(filelist)):
            #get modifier
            parts = filelist[i].split("\t",1)

            modifier = parts[0]
            modifier = self.translateModifierGIT(modifier)
            #get path
            path = parts[1].strip()

            #check if file already exists
            file = self.searchFile(path)
            #file does not exist
            if(not isinstance(file,Object.Object)):
                file = self.makeFile(path, self.objectIterator)



            #add to dictionary to add to the right list of commits later on
            fileStatus[fileStatIterator] = {'File':file,'Status': modifier}
            fileStatIterator += 1

            files.append(file)

        return [files,fileStatus]

    #Function that classifies the GIT modifier status into the categories: {Added, Modified, Deleted}
    def translateModifierGIT(self, modifier):
        if "M" in modifier:
            return "Modified"
        elif "A" in modifier:
            return "Added"
        elif "D" in modifier:
            return "Deleted"
        else :

            return "Modified"



    #search if file with this path already exists
    #@param filePath = file path
    #@returns that file object
    def searchFile(self,filePath):
        for elem in self.listOfObjects:
            if(elem.getName() == filePath):
                return elem
        return ""

    #Function that makes a file object for this file path
    #@param path  : string of file path
    #@param fileID  :  numeric ID of the file
    def makeFile(self,path,fileID):
        file = Object.Object(fileID,path)
        self.objectIterator = self.objectIterator + 1
        #add it to the general overview list
        self.listOfObjects.append(file)
        return file


    #function that calculates an importance value for each object
    def calculateObjectImportance(self):
        firstAndLastTimeStamp = self.getFirstAndLastCommitDate()

        for object in self.listOfObjects:
            object.calculateImportanceRatio(firstAndLastTimeStamp)


    #@return tuple of time stamp of the first and last event date
    def getFirstAndLastCommitDate(self):
        listOfTimestamps = []
        for event in self.listOfEvents:
            listOfTimestamps.append(event.getTimestamp())

        listOfTimestamps.sort()
        lastTimeStamp = listOfTimestamps[-1]
        firstTimeStamp = listOfTimestamps[0]

        return (firstTimeStamp,lastTimeStamp)
