import itertools as itt
import ConvexHullMaxPairOfPoints as convHull


INVALID_POS = (104,104)


def isValidPos(pos):
    return pos != INVALID_POS


def intervalToPoint(num, axes, T_axes):
    axe1 = T_axes[0]
    axe2 = T_axes[1]
    axe3 = T_axes[2]
    point = (0, 0)
    if num == 0:
        point = (axes[0], axes[1])
    elif num == axe1:
        point = (axes[0], axes[1]+1)
    elif num == axe2:
        point = (axes[0] + 1, axes[1])
    elif num == axe3 :
        point = (axes[0]-1, axes[1]-1)
    elif num == (12 - axe3):
        point = (axes[0]+1, axes[1]+1)
    elif num == (12 - axe2):
        point = (axes[0] - 1, axes[1])
    elif num == (12 - axe1):
        point = (axes[0], axes[1] - 1)
    else :
        point = INVALID_POS
    return point


def ChordConfiguration(chord, axes, Tonnetz):
    chordEdges = []
    if not isValidPos(axes):
        print(chord,axes)
        raise ValueError("Bad reference point")
    coordDict = {chord[0]: axes}
    n = 0
    while(len(chord) > len(coordDict)):
        for noteA, noteB in itt.product(chord,chord):
            if(noteA in coordDict and noteB not in coordDict):
                newPoint = intervalToPoint((noteB-noteA)%12, coordDict[noteA], Tonnetz)
                if isValidPos(newPoint):
                    coordDict[noteB]=newPoint
            if(n>len(chord)):
                print(chord,coordDict.items(),axes,n,len(chord),len(coordDict))
                raise RuntimeError("Infinite Loop")
        n += 1
    if(any(note not in coordDict for note in chord)):
         print(chord,coordDict.items(),axes)
         raise BaseException("Lost chord")
    return coordDict

def distanceOne(T_axes):
    listofDist = [T_axes[0], T_axes[1], T_axes[2], (12 - T_axes[0]), (12 - T_axes[1]), (12 - T_axes[2])]
    return(listofDist)

def distanceInt(interval, T_axes):
    listofDist = distanceOne(T_axes)
    if interval == 0:
        value = 0
    elif interval in listofDist:
        value = 1
    else :
        value = 2
    return value

def distNoteFromChord(chord, note, Tonnetz):
    distanceValueList = [ 
            distanceInt((i- note)%12, Tonnetz) for i in chord
        ]
    return distanceValueList

def IndexOfCloserNote(chord, note, Tonnetz): 
    valueList = distNoteFromChord(chord, note, Tonnetz)
    minimumIndex = valueList.index(min(valueList))
    return minimumIndex

def positionFromMin(chord, note, coordDict, Tonnetz):
    keyIndex = IndexOfCloserNote(chord, note, Tonnetz)
    noteA = chord[keyIndex]
    number = (note - noteA)%12
    position = coordDict[noteA]
    newPoint = intervalToPoint(number, position, Tonnetz)
    return newPoint

def chordMatrix(Chord1, Chord2, Tonnetz):
    m2 = [
            ([ (distanceInt((i-j)%12, Tonnetz)) for i in Chord1 ]) for j in Chord2
         ]
    return m2

def distance_matrix(chord1, chord2, Tonnetz):
    matrix = chordMatrix(chord1, chord2, Tonnetz)
    l1=[sum([row[i] for row in matrix]) for i in range(len(chord1))]
    l2=list(map(sum, matrix))
    return l1, l2

def IndexesOfMinimum(chord1, chord2, Tonnetz):
    l1, l2 = distance_matrix(chord1, chord2, Tonnetz)
    min1 = min(l1)
    min2 = min(l2)
    minimumIndex1 = l1.index(min1)
    minimumIndex2 = l2.index(min2)
    distValue = distanceInt((chord1[minimumIndex1] - chord2[minimumIndex2])%12, Tonnetz)
    if distValue >= 1 : 
        listOfMinIndices1 = [i for i, n in enumerate(l1) if n > min1-2]
        listOfMinIndices2 = [i for i, n in enumerate(l2) if n > min2-2]
        minCheck = 2
        for i in listOfMinIndices1:
            for j in listOfMinIndices2:
                distVal = distanceInt((chord1[i] - chord2[j])%12, Tonnetz)
                if  distVal < minCheck:
                    minimumIndex1 = i
                    minimumIndex2 = j  
                    minCheck = distVal
    return minimumIndex1, minimumIndex2



def positionOfTheMinNote(chord1, chord2, coordDict1, Tonnetz):
    index1, index2 = IndexesOfMinimum(chord1, chord2, Tonnetz)
    noteA = chord1[index1]
    noteB = chord2[index2]
    chord2[0],chord2[index2] = chord2[index2],chord2[0]
    interval = (noteB - noteA)%12
    position = coordDict1[noteA]
    newPoint = intervalToPoint(interval, position, Tonnetz)
    return newPoint, position


def Trajectory(listofChords, Tonnetz, axes=(0,0)) :
    ListOfDict = []
    for index, chord in enumerate(listofChords):
        if index == 0 :
            ListOfDict.append(ChordConfiguration(chord, axes, Tonnetz))
        elif index == 1:
            newPos = positionOfTheMinNote(listofChords[index-1], chord, ListOfDict[index-1], Tonnetz)[0]
            axes = newPos
            if not isValidPos(axes):
                axes = positionOfTheMinNote(listofChords[index-1], listofChords[index+1], ListOfDict[index-1], Tonnetz)[0]
                nextChordCoordDict = ChordConfiguration(listofChords[index+1], axes, Tonnetz)
                newPos = positionOfTheMinNote(listofChords[index+1], chord, nextChordCoordDict, Tonnetz)[0]
                ListOfDict.append(ChordConfiguration(listofChords[index], newPos, Tonnetz))
            else:
                ListOfDict.append(ChordConfiguration(chord, axes, Tonnetz))
        else :
            newPos = positionOfTheMinNote(listofChords[index-1], chord, ListOfDict[index-1], Tonnetz)[0]
            axes = newPos
            if not isValidPos(axes) :
                axes = positionOfTheMinNote(listofChords[index-2], chord, ListOfDict[index-2], Tonnetz)[0]
                if not isValidPos(axes) :
                    print(chord1, chord2, coordDict1,noteA, noteB)
                    raise RuntimeError("Couldn't match closest points")
            ListOfDict.append(ChordConfiguration(chord, axes, Tonnetz))
    return ListOfDict

def centroid(listOfPoints):
    x, y = zip(*listOfPoints)
    centroid = (sum(x) / len(listOfPoints), sum(y) / len(listOfPoints))
    return centroid

def concat3DictValues(Dict1, Dict2, Dict3) :
    l1 = list(Dict1.values())
    l2 = list(Dict2.values())
    l3 = list(Dict3.values())
    lconcat = l1 + l2 + l3
    return lconcat

def maximumDistanceOfConvexHull(graph1):
    point1, point2 = convHull.diameter(graph1)
    sumofsquares = (point1[0]-point2[0])^2 + (point1[1]-point2[1])^2
    maxdistance = format(sumofsquares**(0.5), '.2f')
    return maxdistance

def TrajectoryCheckPosition(pos1, lastPos1, listofChords, listOfDict, index, ThisChord, Tonnetz):
    if not isValidPos(pos1) : 
        pos1, lastPos1 = positionOfTheMinNote(listofChords[index-2] , ThisChord, listOfDict[index-2] , Tonnetz)
        if not isValidPos(pos1):
            posNext = positionOfTheMinNote(listofChords[index-1], listofChords[index+1], listOfDict[index-1], Tonnetz)[0]
            if not isValidPos(posNext) :        
                raise KeyError('No possible Points')
            else :
                nextChordPoints = ChordConfiguration(listofChords[index+1], posNext, Tonnetz)
                pos1, lastPos1 = positionOfTheMinNote(listofChords[index+1], ThisChord, nextChordPoints, Tonnetz)   
                if not isValidPos(pos1) :
                    raise KeyError('No possible Values')
                else :
                    ThisChordPoints = ChordConfiguration(ThisChord, pos1, Tonnetz)
                    edge = [(pos1, lastPos1)]
                    return ThisChordPoints, edge
        else :
            return TrajectoryLookConnected(pos1, lastPos1, listofChords, ThisChord, index, listOfDict, Tonnetz)
    else :
        return TrajectoryLookConnected(pos1, lastPos1, listofChords, ThisChord, index, listOfDict, Tonnetz)


def TrajectoryLookConnected(pos1, lastPos1, listofChords, ThisChord, index, listOfDict, Tonnetz):
    if pos1 not in listOfDict[index-1] or not isValidPos(pos1):
        newpos1, newlastpos1 = positionOfTheMinNote(listofChords[index-2] , ThisChord, listOfDict[index-2] , Tonnetz)
        if newpos1 in listOfDict[index-2] and isValidPos(newpos1):
            pos1 = newpos1
            lastPos1 = newlastpos1
            return TrajectoryCheckSecond(pos1, lastPos1, listofChords, ThisChord, index, listOfDict, Tonnetz)
        else :
            return TrajectoryCheckSecond(pos1, lastPos1, listofChords, ThisChord, index, listOfDict, Tonnetz)
    else :
        return TrajectoryCheckSecond(pos1, lastPos1, listofChords, ThisChord, index, listOfDict, Tonnetz)

def TrajectoryCheckSecond(pos1, lastPos1, listofChords, ThisChord, index, listOfDict, Tonnetz):
    if not isValidPos(pos1) :
        posNext = positionOfTheMinNote(listofChords[index-1], listofChords[index+1], listOfDict[index-1], Tonnetz)[0]
        if isValidPos(posNext) :
            nextChordPoints = ChordConfiguration(listofChords[index+1], posNext, Tonnetz)
            pos2, lastPos2 = positionOfTheMinNote(listofChords[index+1], ThisChord, nextChordPoints, Tonnetz)
            if isValidPos(pos2) :
                ThisChordPoints2 = ChordConfiguration(ThisChord, pos2, Tonnetz)
                edge = [(pos2, lastPos2)]
                return ThisChordPoints2, edge
            else :
                raise KeyError('No possible Values')
        else :
            raise KeyError('No possible Values')
    else :
        ThisChordPoints1 = ChordConfiguration(ThisChord, pos1, Tonnetz) # Do I need to consider taking index-2 here too? (propably not)
        posNext = positionOfTheMinNote(listofChords[index-1], listofChords[index+1], listOfDict[index-1], Tonnetz)[0]
        if isValidPos(posNext) :
            nextChordPoints = ChordConfiguration(listofChords[index+1], posNext, Tonnetz)
            pos2, lastPos2 = positionOfTheMinNote(listofChords[index+1], ThisChord, nextChordPoints, Tonnetz)
            if isValidPos(pos2) :
                return TrajectoryConvexHullComparison(ThisChord, pos1, lastPos1, pos2, lastPos2, ThisChordPoints1, listOfDict, index, Tonnetz) 
            else :
                edge = [(pos1, lastPos1)]
                return ThisChordPoints1, edge    
        else :
            edge = [(pos1, lastPos1)]
            return ThisChordPoints1, edge


def TrajectoryFirstAndLastChords(listofChords, listOfDict, index, Tonnetz) :
    ThisChord = listofChords[index]
    pos1, lastPos1 = positionOfTheMinNote(listofChords[index-1], ThisChord, listOfDict[index-1], Tonnetz)
    if not isValidPos(pos1):
        raise KeyError('Wrong First Note position')
    ThisChordPoints1 = ChordConfiguration(ThisChord, pos1, Tonnetz)
    edge = [(pos1, lastPos1)]
    return ThisChordPoints1, edge


def TrajectoryConvexHullComparison(ThisChord, pos1, lastPos1, pos2, lastPos2, ThisChordPoints1, listOfDict, index, Tonnetz):
    ThisChordPoints2 = ChordConfiguration(ThisChord, pos2, Tonnetz)
    concatPoints1 = concat3DictValues(ThisChordPoints1, listOfDict[index-1] , listOfDict[index-2] )
    concatPoints2 = concat3DictValues(ThisChordPoints2, listOfDict[index-1] , listOfDict[index-2] )
    graph1 = list(set(concatPoints1))
    graph2 = list(set(concatPoints2))
    distance1 = maximumDistanceOfConvexHull(graph1)
    distance2 = maximumDistanceOfConvexHull(graph2)
    if distance1 > distance2 :
        edge = [(pos2, lastPos2)]
        return ThisChordPoints2, edge
    else :
        edge = [(pos1, lastPos1)]
        return ThisChordPoints1, edge 



def TrajectoryWithFuture(listofChords, listOfBeetweenEdges, listOfDict, Tonnetz, index):
    if index > 1 and index < len(listofChords)-1 :
        ThisChord = listofChords[index]
        pos1, lastPos1 = positionOfTheMinNote(listofChords[index-1], ThisChord, listOfDict[index-1], Tonnetz)
        return TrajectoryCheckPosition(pos1, lastPos1, listofChords, listOfDict, index, ThisChord, Tonnetz)
    else :
        return TrajectoryFirstAndLastChords(listofChords=listofChords, listOfDict=listOfDict, index=index, Tonnetz=Tonnetz)


def TrajectoryLookBeforeLookAhead(listofChords, listOfBeetweenEdges, listOfDict, Tonnetz, index):
    if index > 1 and index < len(listofChords)-1 :
        ThisChord = listofChords[index]
        pos1, lastPos1 = positionOfTheMinNote(listofChords[index-1], ThisChord, listOfDict[index-1], Tonnetz)
        ThisChordPoints1 = ChordConfiguration(ThisChord, pos1, Tonnetz) 
        posNext = positionOfTheMinNote(listofChords[index-1], listofChords[index+1], listOfDict[index-1], Tonnetz)[0]
        nextChordPoints = ChordConfiguration(listofChords[index+1], posNext, Tonnetz)
        pos2, lastPos2 = positionOfTheMinNote(listofChords[index+1], ThisChord, nextChordPoints, Tonnetz)
        ThisChordPoints2 = ChordConfiguration(ThisChord, pos2, Tonnetz)
        concatPoints1 = concat3DictValues(ThisChordPoints1, listOfDict[index-1] , listOfDict[index-2] )
        concatPoints2 = concat3DictValues(ThisChordPoints2, listOfDict[index-1] , listOfDict[index-2] )
        graph1 = list(set(concatPoints1))
        graph2 = list(set(concatPoints2))
        distance1 = maximumDistanceOfConvexHull(graph1)
        distance2 = maximumDistanceOfConvexHull(graph2)
        if pos1 == (104, 104) and pos2 == (104, 104) :
            raise ReferenceError("Couldn't match closest points")
        if distance1 > distance2 :
            listOfDict.append(ThisChordPoints2)
            listOfBeetweenEdges.append([(pos2, lastPos2)])
        else :
            listOfDict.append(ThisChordPoints1)
            listOfBeetweenEdges.append([(pos1, lastPos1)])
    else :
        ThisChord = listofChords[index]
        pos1, lastPos1 = positionOfTheMinNote(listofChords[index-1], ThisChord, listOfDict[index-1], Tonnetz)
        if pos1 == (104, 104) :
            raise ReferenceError("Couldn't match closest points")
        ThisChordPoints1 = ChordConfiguration(ThisChord, pos1, Tonnetz) 
        listOfDict.append(ThisChordPoints1)
        listOfBeetweenEdges.append([(pos1, lastPos1)])

def NewTrajectory(listofChords, Tonnetz, origin=(0,0)) :
    listOfDict = []
    listOfBeetweenEdges = []
    for index, chord in enumerate(listofChords):
        if index == 0 :
            listOfDict.append(ChordConfiguration(chord, origin, Tonnetz))
        elif index == 1:
            newPos, lastPos = positionOfTheMinNote(listofChords[index-1], chord, listOfDict[index-1], Tonnetz)
            origin = newPos
            if not isValidPos(origin) :
                origin = positionOfTheMinNote(listofChords[index-1], listofChords[index+1], listOfDict[index-1], Tonnetz)[0]
                nextChordCoordDict = ChordConfiguration(listofChords[index+1], origin, Tonnetz)
                newPos, lastPos = positionOfTheMinNote(listofChords[index+1], chord, nextChordCoordDict, Tonnetz)
                if not isValidPos(newPos) :
                    raise ReferenceError("Couldn't match closest points")
                listOfDict.append(ChordConfiguration(listofChords[index], newPos, Tonnetz))
                listOfBeetweenEdges.append([(newPos, lastPos)])
            else:
                listOfDict.append(ChordConfiguration(chord, origin, Tonnetz))
                listOfBeetweenEdges.append([(newPos, lastPos)])
        else :
            chordCoord, edge = TrajectoryWithFuture(listofChords, listOfBeetweenEdges, listOfDict, Tonnetz, index)
            listOfDict.append(chordCoord)
            listOfBeetweenEdges.append(edge) 
    return listOfDict, listOfBeetweenEdges
        

def NewTrajectoryLookBefore(listofChords, Tonnetz, origin=(0,0)) :
    listOfDict = []
    listOfBeetweenEdges = []
    for index, chord in enumerate(listofChords):
        if index == 0 :
            listOfDict.append(ChordConfiguration(chord, origin, Tonnetz))
        else :
            TrajectoryLookBeforeLookAhead(listofChords, listOfBeetweenEdges, listOfDict, Tonnetz, index)
    return listOfDict, listOfBeetweenEdges 
        

def TrajectoryNoteEdges(TrajectoryPoints):
    TotalEdges = []
    dist = [-1, 0, 1]
    for dicts in TrajectoryPoints:
        chordEdges = []
        l = list(itt.product(dicts.values(), dicts.values()))
        for couple in l:
            (x1, y1), (x2, y2) = couple
            if (x1 - x2) in dist  and (y1 - y2) in dist:
                if not (((x1 - x2) == 1 and (y1 - y2) == -1) or ((x1 - x2) == -1 and (y1 - y2) == 1)) :
                    chordEdges.append(couple)
        TotalEdges.append(chordEdges)
    return TotalEdges

def SetOfPoints(TrajectoryPoints):
    AllPoints = []
    for dicts in TrajectoryPoints:
        AllPoints = AllPoints + list(dicts.values())
    PointSet = list(set(AllPoints))
    return PointSet, AllPoints

def weightsOfTrajPoints(setOfPoints, multiSetOfPoints):
    dictOfPointWeight = dict()
    for point in setOfPoints :
        dictOfPointWeight[point] = multiSetOfPoints.count(point)
    Maximum = max(list(dictOfPointWeight.values()))
    Minimum = min(list(dictOfPointWeight.values()))
    return dictOfPointWeight