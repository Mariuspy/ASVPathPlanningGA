# -*- coding: utf-8 -*-
"""
@author: Iratxe
"""
# Imports
from collections import Counter
import itertools
import numpy as np
import random
import parameters_opt_ga as param
import fs_intersec_finding_func as intersec
numBeacons = param.N_BEACON
usedBeacons = param.N_USED_BEACON
invalidRoutes = param.arr_allowed_routes

#%% Create a matrix with as many 1s as beacons --> The connection matrix
def getConnectionMatrix():
    connectionMatrix = np.zeros(numBeacons**2, dtype=int)
    connectionMatrix[:usedBeacons] = 1
    np.random.shuffle(connectionMatrix)
    connectionMatrix = connectionMatrix.reshape(numBeacons, numBeacons)

    return connectionMatrix

#%% Check whether the matrix contains invalid routes, and correct
def removeInvalidRoutes(connectionMatrix):
    # The multiplication will give us 1s for invalid routes we are using
    mult = np.multiply(invalidRoutes, connectionMatrix)

    """ While we still have 1s we find them and set to 0, and move the 1s to the
    left in the same row, until we find a non-invalid route we can use and we set to 1 """
    while np.count_nonzero(mult) != 0:
        for x in range(numBeacons):
            for y in range(numBeacons): #3 = numBeacons
                if mult[x][y] == 1:
                    connectionMatrix[x][y] = 0
                    
                    indChange = y-1
                    if indChange < 0: 
                        indChange = numBeacons-1
                        
                    # If the next in the left is a 1 (invalid), we keep looking
                    while connectionMatrix[x][indChange] == 1:
                        indChange -= 1
                        if indChange < 0:
                            indChange = numBeacons-1 
                            
                    # Until we finally find a route we can use
                    connectionMatrix[x][indChange] = 1

        # Now the multiplication should give 0 1s
        mult = np.multiply(invalidRoutes, connectionMatrix)

    return connectionMatrix

#%% Check whether the matrix contains invalid routes HAU ZEEEEEE
def containsInvalidRoute(connectionMatrix):
    mult = np.multiply(param.arr_allowed_routes, connectionMatrix)
    
    if np.count_nonzero(mult) == 0:
        return False
    else:
        print np.count_nonzero(mult)
        return True

#%% List of connections
def getConnectionList(connectionMatrix):
    connections = []
    for col in range(0, numBeacons):
        for row in range(0, numBeacons):
            if connectionMatrix[row][col] == 1:
                # Two cases to get always the lowest value in the first position,
                # so we can check for duplicated tuples more easily
                if row > col:
                    connections.append(tuple([col, row]))   
                else:
                    connections.append(tuple([row, col]))
                
    return connections

#%% Doubly connected graph condition
def isBiconnected(connectionList):
    beaconList = list(itertools.chain(*connectionList))
    beaconOccurrence = Counter(beaconList)
    isBic = all(x%2 == 0 for x in beaconOccurrence.values())
    if isBic:
        return True
    else:
        return False
    
#%% Find beacons with odd occurrences
def oddOccurrences(connectionList):
    beaconList = list(itertools.chain(*connectionList))
    
    # Initialize counter so it also contains the unused beacons (with value 0), then fill others with values
    beaconNumbers = dict()
    for i in range(1, numBeacons+1):
        beaconNumbers[i] = 0
    beaconOccurrence = Counter(beaconNumbers) 
    beaconOccurrence.update(Counter(beaconList))
    oddBeacons = []
    
    # Find beacons with odd occurrences
    for i, occur in enumerate(beaconOccurrence.values()):
        if occur % 2 != 0:
            oddBeacons.append(i)
            
    return oddBeacons
    
#%% Force Eulerian circuit condition, i.e., no vertices (beacons) with odd occurrences 
def toEulerian(connectionList):
    oddBeacons = oddOccurrences(connectionList)
    numIter = 1
    duplicated = 0
    maxDuplicated = 100
    maxIter = 500
    
    while oddBeacons != [] and duplicated < maxDuplicated and numIter < maxIter:            
        tup = connectionList[0]
        containsOdd = [odd in tup for odd in oddBeacons]
        
        # If the tuple does not contain beacons with an odd occurrence number, we keep it
        if not True in containsOdd:
            connectionList.append(tup)
            connectionList.remove(tup)
        # If not, we modify the tuple by changing the current "odd" beacon with another "odd" beacon
        else:
            if tup[0] in oddBeacons:           
                modifiedTup = (oddBeacons[random.randint(0, len(oddBeacons)-1)], tup[1])
            else:
                modifiedTup = (tup[0], oddBeacons[random.randint(0, len(oddBeacons)-1)])
            modifiedTup = (min(modifiedTup), max(modifiedTup))

            """ We can have the case where it is impossible not to repeat a tuple, 
            to have a self-connected one (according to our modification system) or
            to have an invalid one (according to invalidRoutes). 
            After some iterations we will just discard that tuple that will change
            the size of the connectionList so it will be discarded later in the code (2)"""
            isDuplicated = modifiedTup in connectionList
            isSelfConnected = modifiedTup[0] == modifiedTup[1]              ##ERREPIKATUA!!!
            isInvalid = invalidRoutes[modifiedTup[0]][modifiedTup[1]] == 1
            
            if isDuplicated or isSelfConnected or isInvalid:
                duplicated +=1
                if duplicated == maxDuplicated: 
                    connectionList.remove(tup)
            else:
                duplicated = 0
                connectionList.append(modifiedTup)
                connectionList.remove(tup)
          
        oddBeacons = oddOccurrences(connectionList)
        numIter += 1
                
    return connectionList

#%% Create path from connections
def createPath(validConnections):
    path = []
    path.append(validConnections[0])
    tup = validConnections[0]
    validConnections.remove(tup)
    
    while validConnections != []:
        beginLen = len(path)
        for connect in validConnections:
            if connect[0] == tup[1]:
                path.append(connect)
                tup = connect
                validConnections.remove(connect)
            elif connect[1] == tup[1]:
                path.append((connect[1],connect[0]))
                tup = (connect[1],connect[0])
                validConnections.remove(connect)       
        # In case the circuit is closed before adding all the conections
        # --> All the nodes are not connected
        if len(path) == beginLen:
            break
     
    return path

#%% Create connections from path
def createConnections(path):
    connections = []
    
    for i in range(len(path)-1):
        connections.append(tuple([path[i],path[i+1]]))
    
    return connections 

#%% Create Eulerian circuit path
def getEulerianCircuit():
    cMatrixAttempts = 1
    eulerianAttempts = 1
    maxAttempts = 100
    
    while True:
        
        # GET A MATRIX WITHOUT SELF-CONNECTIONS OR DUPLICATED ROUTES
        connectionMatrix = getConnectionMatrix()
        connectionMatrix = removeInvalidRoutes(connectionMatrix) # --> Solution1
        
        # GET A MATRIX WITHOUT INVALID ROUTES
        connectionList = getConnectionList(connectionMatrix)
        
        while True: # Try different matrices until we get a valid one
            notSelfConnected = all(x == 0 for x in connectionMatrix.diagonal()) ###ERREPIKATUA!!
            notDuplicated = len(list(set(connectionList))) == usedBeacons
            if notSelfConnected and notDuplicated: # This is a valid matrix
                break
            elif cMatrixAttempts == maxAttempts:
                break
            else:
                cMatrixAttempts += 1
                connectionMatrix = getConnectionMatrix()
                connectionMatrix = removeInvalidRoutes(connectionMatrix) # --> Solution1
                connectionList = getConnectionList(connectionMatrix)
        
        # GET AN EULERIAN CIRCUIT, i.e., all nodes are connected together with an odd number of connections each
        validConnections = toEulerian(connectionList)     
        sortedConnections = createPath(validConnections)
        
        allNodesConnected = len(sortedConnections) == usedBeacons #(2)
        if allNodesConnected: # This is an Eulerian circuit        
            path = list(zip(*sortedConnections)[0])           
            break
        elif eulerianAttempts == maxAttempts:
            break

        eulerianAttempts += 1
        
    return path, sortedConnections, cMatrixAttempts, eulerianAttempts


#%% MAIN PROGRAM
def main():
    
    path, sortedConnections, cMatrixAttempts, eulerianAttempts  = getEulerianCircuit()
    
    # Statistics and info 
    print "Attempts to get a valid connection matrix: ", cMatrixAttempts
    print "Attempts to get a valid and Eulerian connection matrix: ", eulerianAttempts
    #print "Sorted connections: \n", sortedConnections
    print "Valid Eulerian circuit: \n", path
    print "Number of invalid routes: ", intersec.invalid_route_count(path,invalidRoutes,range(60))   
    
if __name__ == "__main__":
    
    main()


"""
(1): Nahi izatekotan ibilbide errepikatuk ere gorde

- Sortzen ahal da zerbait barkua depende non dagon handik hasteko ibilbidia, o sea, 
2. balizan baldin badago ta ibilbidia [1,2,3] bada aldatzeko [2,3,1]-era.

- Normalin hasiera puntua da bajua, tuplak (min,max) ordenatuk daudelako
"""