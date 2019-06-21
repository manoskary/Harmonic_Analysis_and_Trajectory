import itertools as itt

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
        point = (104, 104)
    return point


def ChordConfiguration(chord, axes, Tonnetz):
    chordEdges = []
    if axes == (104,104):
        print(chord,axes)
        raise ValueError("Bad reference point")
    coordDict = {chord[0]: axes}
    n = 0
    while(len(chord) > len(coordDict)):
        for noteA, noteB in itt.product(chord,chord):
            if(noteA in coordDict and noteB not in coordDict):
                newPoint = intervalToPoint((noteB-noteA)%12, coordDict[noteA], Tonnetz)
                if(newPoint != (104,104)):
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
#     if newPoint == (104,104):
#         positionOfTheMinNote()
#         print(chord1, chord2, coordDict1,noteA, noteB)
#         raise RuntimeError("Couldn't match closest points")
    return newPoint  


def Trajectory(listofChords, Tonnetz, axes=(0,0)) :
    ListOfDict = []
    ListsOfEdges = []
    for index, chord in enumerate(listofChords):
        if index == 0 :
            ListOfDict.append(ChordConfiguration(chord, axes, Tonnetz))
        elif index == 1:
            newPos = positionOfTheMinNote(listofChords[index-1], chord, ListOfDict[index-1], Tonnetz)
            axes = newPos
            if axes == (104, 104) :
                axes = positionOfTheMinNote(listofChords[index-1], listofChords[index+1], ListOfDict[index-1], Tonnetz)
                nextChordCoordDict = ChordConfiguration(listofChords[index+1], axes, Tonnetz)
                newPos = positionOfTheMinNote(listofChords[index+1], chord, nextChordCoordDict, Tonnetz)
                ListOfDict.append(ChordConfiguration(listofChords[index], newPos, Tonnetz))
            else:
                ListOfDict.append(ChordConfiguration(chord, axes, Tonnetz))
        else :
            newPos = positionOfTheMinNote(listofChords[index-1], chord, ListOfDict[index-1], Tonnetz)
            axes = newPos
            if axes == (104, 104) :
                axes = positionOfTheMinNote(listofChords[index-2], chord, ListOfDict[index-2], Tonnetz)
                if axes == (104,104):
                    print(chord1, chord2, coordDict1,noteA, noteB)
                    raise RuntimeError("Couldn't match closest points")
            ListOfDict.append(ChordConfiguration(chord, axes, Tonnetz))
    return ListOfDict
        

def TrajectoryLookBefore(listofChords, Tonnetz, axes=(0,0)) :
    ListOfDict = []
    for index, chord in enumerate(listofChords):
        if index == 0 :
            ListOfDict.append(ChordConfiguration(chord, axes, Tonnetz))
        else :
            newPos = positionOfTheMinNote(listofChords[index-1], chord, ListOfDict[index-1], Tonnetz)
            if axes == newPos:
                axes = newPos
            elif (abs(axes[0] - newPos[0]) == 1 or abs(axes[1] - newPos[1]) == 1) and index > 1  :
                newPosPrev =  positionOfTheMinNote(listofChords[index-2], chord, ListOfDict[index-2], Tonnetz)
                if newPosPrev == axes :
                    axes = newPosPrev 
                else :
                    axes = newPos
            if axes == (104, 104) :
                axes = positionOfTheMinNote(listofChords[index-2], chord, ListOfDict[index-2], Tonnetz)
                if axes == (104,104):
                    print(chord1, chord2, coordDict1,noteA, noteB)
                    raise RuntimeError("Couldn't match closest points")
            ListOfDict.append(ChordConfiguration(chord, axes, Tonnetz))
    return ListOfDict


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
        