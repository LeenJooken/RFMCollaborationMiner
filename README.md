# **RFM Collaboration Miner**
This code repository is supplementary to the following journal publication: 
> L. Jooken, B. Depaire, M. Jans. “Mining Recency-–Frequency-–Monetary
enriched insights into resources’ collaboration behavior from event data”. In: Engineering Applications of Artificial Intelligence 126 A (2023), p. 106765 
> [doi: 10.1016/j.engappai.2023.106765](https://doi.org/10.1016/j.engappai.2023.106765) 

RFM Collaboration Miner is a project that extracts and constructs a network of collaborating resources (i.e., members) from an event log consisting of events detailing the exact timestamp when a resource worked on a specific object. The project also calculates Recency-Frequency-Monetary values for both the resources and collaboration relationships.

The RFM dimensions represent the following: 
- **Recency**: how recently a resource worked or a resource pair collaborated 
- **Frequency**: how frequently a resource worked or a resource pair collaborated 
- **Monetary**: the monetary value of a resource or collaboration relationship based on the importance of the work performed


The approach makes use of a threshold-based sessionization method that groups events together into work and collaboration sessions. To this end, it utilizes two parameters: 

- A maximal inter-event time which represents a maximum limit on the time between two consecutive events for them to still belong to the same session. If this limit is exceeded, both events belong to separate sessions.
- The maximum duration of a session.
 

The development of this project is part of the PhD. disseration of L. Jooken, supported by the BOF funding of Hasselt University. 



## Input data


As input data, information on the exact timestamp of when a resource worked on a specific object is needed.
To this end, a list of events is needed that each specify the *resource*, the *object*, and the *timestamp*. 

Currently, the program is tailored to extract this event log from Git logs. If an event log is already available, the code can be adjusted to bypass this parser. 

To utilize a Git log, extract the log using this commando in the git bash:
```python
git log --name-status --abbrev-commit --pretty=format:'%h,%an,%ad,%(trailers:key=Co-Authored-by,separator=%x2C,valueonly=TRUE)' --date=iso-local --diff-merges=c --no-renames > log.git
`````
 


## Usage 
In order to run the program, call upon *"MainRFM.py"* and add the following data as arguments: 

- **-s** git log source file to be read; must have extension .git
- **-nf** file name of the output CSV file that will contain the nodes of the network *[optional]*
- **-ef** file name of the output CSV file that will contain the edges of the network *[optional]*
- **-wsD** pass the maximal duration of a work session in minutes (if not included the default is set to 240 min)
- **-wsIet** pass the maximal inter-event time for the work sessions in minutes (if not included the default is set to 1440 min).
When exceeded, it indicates that the two consecutive events certainly belong to separate sessions.
- **-csD** pass the maximal duration of a collaboration session in minutes (if not included the default is set to 10080 min)
- **-csIet** pass the maximal inter-event time for the collaboration sessions in minutes (if not included the default is set to 20160 min). When exceeded, it indicates that the two consecutive events certainly belong to separate sessions.
- **-print** including this argument will print the work and collaboration sessions to CSV files, as well as the objects and resources. These output files can be used as input to the Membership ChangeMiner project. 



 
By illustration: 

The most basic scenario in which the default values are used for most arguments:
```python
MainRFM.py -s log.git 
```
A scenario in which all arguments are user-specified:
```python
MainRFM.py -s log.git -nf nodes.csv -ef edges.csv -wsD 300 -wsIet 1500 -csD 10000 -csIet 20000 -print
```



## Customization options
Some flexibility is built into the code. Included here is a list of the options that can be changed. 

### Anonymization of the output
The names of the resources can be anonymized in the output by uncommenting the required code line in *"Output.py"*. This code should then look like this: 

```python
    def writeNodesRFMCSV(self,nodes,filename):
        ...
        for node in nodes:
            label = node.getLabel()
            #for anonymization, uncomment the next line
            label = self.anonymizeResource()
            writer.writerow([node.getID(),label,node.getWeight(),node.getRecencyValue(),node.getFrequencyValue(),node.getMonetaryValue()])


```


### Recency window size 
To calculate the recency value of a resource and a collaboration relationship, the event log is divided into time bins of a predefined width.
The relevant sessions are then classified into the appropriate bins that each have their contribution to the recency value. The final recency value is the average bin
weight of each session related to a specific resource or resource pair. 
A custom window size (in minutes) can be passed to the Graph constructor in *"MainRFM.py"* as follows. 

```python 
    #construct the graph
    print("Calculating the RFM values:")
    socialgraph = Graph.Graph(recencyWindowSizeEdge = 1440, recencyWindowSizeNode = 1440)

```





## Output
### Collaboration network
The program constructs a collaboration network, which can be written to CSV files: 1 file for the collaboration relationships (edges), 1 file for the resources (nodes).

The node file consists of the following columns: node ID, node label, recency value, frequency value, monetary value

| Id        | Label | Recency  | Frequency  | Monetary  |
|-----------|-------|-------------------|-----------------|----------------|
| numerical | text  | numerical | numerical | numerical|


The edge file consists of the following columns: source node ID, target node ID, recency value, frequency value, monetary value

| Source | Target | Recency  | Frequency  | Monetary  |
|----------------|-------------------|---------------|-----------------|----------------|
| numerical | numerical | numerical | numerical | numerical|

### Work and collaboration sessions 
Using the *"-print"* argument in the command line, the program provides additional output on the work and collaboration sessions that were identified using the internal sessionization approach.
Additionally, both the resources and objects are also printed to CSV. These data files can be used as input to the Membership Changes Miner project. 

**Resources** 

List of all resources (i.e., members) of the organizational network. 

| ResourceID | Label |
|-------------|---------------|
| numerical | text | 

**Objects**

List of all objects that resources work and collaborate on.

| ObjectID  | Label |
|-----------|----------------|
| numerical | text |

**Work sessions**

List of all time windows in which a member worked.

| ResourceID | ResourceLabel | FirstTimestamp | LastTimestamp | MedianTimestamp |
|-------------|---------------| --------- | ----------- | ----------- |
| numerical   | text          | d/m/YYYY H:M:S | d/m/YYYY H:M:S | d/m/YYYY H:M:S |

With
- FirstTimestamp being the timestamp of the first event in the window
- LastTimestamp being the timestamp of the last event in the window 
- MedianTimestamp being the timestamp of the median event in the window

**Collaboration sessions**

List of all time windows in which two members collaborated on a specific object. 

| ResourceID1 | ResourceLabel1 | ResourceID2 | ResourceLabel2 | Object    | ObjectName | FirstTimestamp | LastTimestamp | MedianTimestamp |
|-------------|----------------|-------------|----------------|-----------|------------| ----------- | ----------- | ----------- |
| numerical   | text           | numerical   | text           | numerical | text       | d/m/YYYY H:M:S | d/m/YYYY H:M:S | d/m/YYYY H:M:S |

With
- FirstTimestamp being the timestamp of the first event in the window
- LastTimestamp being the timestamp of the last event in the window 
- MedianTimestamp being the timestamp of the median event in the window


## **Contact**
If you have any questions, please contact the Business Informatics research team at Hasselt University.