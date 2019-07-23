import itertools as itt
import ConvexHullMaxPairOfPoints as convHull
from TrajectoryClass import TrajectoryClass
from FirstNotePosition import TonnetzToString
from Data_and_Dicts import dictOfTonnetz

INVALID_POS = (104, 104)


class PlacementError(RuntimeError):
    def __init__(self, message="Could not place Chord with this strategy"):
        self.message = message


def isValidPos(pos):
    return pos != INVALID_POS

# Successively tries to apply different strategies,
# stopping at the first successful one.
# Strategies are functions which take no argument (typically lambdas
# wrapping a function with its arguments)


def applyFirstSuccessful(strategies):
    result = False
    for strategy in strategies:
        try:
            result = strategy()
        # Consume exceptions silently
        except PlacementError:
            pass
        if result:
            return result
    raise PlacementError()


def intervalToPoint(num, axes, T_axes):
    axe1 = T_axes[0]
    axe2 = T_axes[1]
    axe3 = T_axes[2]
    point = (0, 0)
    if num == 0:
        point = (axes[0], axes[1])
    elif num == axe1:
        point = (axes[0], axes[1] + 1)
    elif num == axe2:
        point = (axes[0] + 1, axes[1])
    elif num == axe3:
        point = (axes[0] - 1, axes[1] - 1)
    elif num == (12 - axe3):
        point = (axes[0] + 1, axes[1] + 1)
    elif num == (12 - axe2):
        point = (axes[0] - 1, axes[1])
    elif num == (12 - axe1):
        point = (axes[0], axes[1] - 1)
    else:
        point = INVALID_POS
    return point


def ChordConfiguration(chord, axes, Tonnetz):
    if not isValidPos(axes):
        print(chord, axes)
        raise ValueError("Bad reference point")
    coordDict = {chord[0]: axes}
    n = 0
    while(len(chord) > len(coordDict)):
        for noteA, noteB in itt.product(chord, chord):
            if(noteA in coordDict and noteB not in coordDict):
                newPoint = intervalToPoint(
                    (noteB - noteA) %
                    12, coordDict[noteA], Tonnetz)
                if isValidPos(newPoint):
                    coordDict[noteB] = newPoint
            if(n > len(chord)):
                print(
                    chord,
                    coordDict.items(),
                    axes,
                    n,
                    len(chord),
                    len(coordDict))
                raise RuntimeError("Infinite Loop")
        n += 1
    if(any(note not in coordDict for note in chord)):
        print(chord, coordDict.items(), axes)
        raise BaseException("Lost chord")
    return coordDict


def distanceOne(T_axes):
    listofDist = [
        T_axes[0],
        T_axes[1],
        T_axes[2],
        (12 - T_axes[0]),
        (12 - T_axes[1]),
        (12 - T_axes[2])]
    return(listofDist)


def distanceInt(interval, T_axes):
    listofDist = distanceOne(T_axes)
    if interval == 0:
        value = 0
    elif interval in listofDist:
        value = 1
    else:
        value = 2
    return value


def distNoteFromChord(chord, note, Tonnetz):
    distanceValueList = [
        distanceInt((i - note) % 12, Tonnetz) for i in chord
    ]
    return distanceValueList


def IndexOfCloserNote(chord, note, Tonnetz):
    valueList = distNoteFromChord(chord, note, Tonnetz)
    minimumIndex = valueList.index(min(valueList))
    return minimumIndex


def positionFromMin(chord, note, coordDict, Tonnetz):
    keyIndex = IndexOfCloserNote(chord, note, Tonnetz)
    noteA = chord[keyIndex]
    number = (note - noteA) % 12
    position = coordDict[noteA]
    newPoint = intervalToPoint(number, position, Tonnetz)
    return newPoint


def chordMatrix(Chord1, Chord2, Tonnetz):
    m2 = [([(distanceInt((i - j) % 12, Tonnetz)) for i in Chord1])
          for j in Chord2]
    return m2


def distance_matrix(chord1, chord2, Tonnetz):
    matrix = chordMatrix(chord1, chord2, Tonnetz)
    l1 = [sum([row[i] for row in matrix]) for i in range(len(chord1))]
    l2 = list(map(sum, matrix))
    return l1, l2


def IndexesOfMinimum(chord1, chord2, Tonnetz):
    l1, l2 = distance_matrix(chord1, chord2, Tonnetz)
    min1 = min(l1)
    min2 = min(l2)
    minimumIndex1 = l1.index(min1)
    minimumIndex2 = l2.index(min2)
    distValue = distanceInt(
        (chord1[minimumIndex1] - chord2[minimumIndex2]) %
        12, Tonnetz)
    if distValue >= 1:
        listOfMinIndices1 = [i for i, n in enumerate(l1) if n > min1 - 2]
        listOfMinIndices2 = [i for i, n in enumerate(l2) if n > min2 - 2]
        minCheck = 2
        for i in listOfMinIndices1:
            for j in listOfMinIndices2:
                distVal = distanceInt((chord1[i] - chord2[j]) % 12, Tonnetz)
                if distVal < minCheck:
                    minimumIndex1 = i
                    minimumIndex2 = j
                    minCheck = distVal
    return minimumIndex1, minimumIndex2


def positionOfTheMinNote(chord1, chord2, coordDict1, Tonnetz):
    index1, index2 = IndexesOfMinimum(chord1, chord2, Tonnetz)
    noteA = chord1[index1]
    noteB = chord2[index2]
    chord2[0], chord2[index2] = chord2[index2], chord2[0]
    interval = (noteB - noteA) % 12
    position = coordDict1[noteA]
    newPoint = intervalToPoint(interval, position, Tonnetz)
    return newPoint, position


def centroid(listOfPoints):
    x, y = zip(*listOfPoints)
    centroid = (sum(x) / len(listOfPoints), sum(y) / len(listOfPoints))
    return centroid


def concat3DictValues(Dict1, Dict2, Dict3):
    l1 = list(Dict1.values())
    l2 = list(Dict2.values())
    l3 = list(Dict3.values())
    lconcat = l1 + l2 + l3
    return lconcat


def maximumDistanceOfConvexHull(graph1):
    point1, point2 = convHull.diameter(graph1)
    sumofsquares = (point1[0] - point2[0]) ^ 2 + (point1[1] - point2[1]) ^ 2
    maxdistance = format(sumofsquares**(0.5), '.2f')
    return maxdistance


def computeChordCoord(thisChord, someChordCoord, Tonnetz):
    origin, otherRefOrigin = positionOfTheMinNote(
        list(someChordCoord.keys()), thisChord, someChordCoord, Tonnetz)
    if not isValidPos(origin):
        raise PlacementError()
    thisChordCoord = ChordConfiguration(thisChord, origin, Tonnetz)
    edge = [(origin, otherRefOrigin)]
    return thisChordCoord, edge


def TrajectoryConvexHullComparison(
        placement1,
        placement2,
        lastChordCoord,
        secondLastChordCoord):
    concatPoints1 = concat3DictValues(
        placement1[0],
        lastChordCoord,
        secondLastChordCoord)
    concatPoints2 = concat3DictValues(
        placement2[0],
        lastChordCoord,
        secondLastChordCoord)
    graph1 = list(set(concatPoints1))
    graph2 = list(set(concatPoints2))
    distance1 = maximumDistanceOfConvexHull(graph1)
    distance2 = maximumDistanceOfConvexHull(graph2)
    if distance1 > distance2:
        return placement2
    else:
        return placement1


def TrajectoryCheckSecond(placement1, trajectory):
    try:
        secondLastChordCoord = trajectory.getLastPosition(2)
        lastChordCoord = trajectory.getLastPosition()
        nextChord = trajectory.getNextChord()
        placement2 = placeChordWithVirtualRef(
            trajectory.getThisChord(),
            lastChordCoord,
            nextChord,
            trajectory.Tonnetz)
        return TrajectoryConvexHullComparison(
            placement1, placement2, lastChordCoord, secondLastChordCoord)
    except PlacementError:
        return placement1


def TrajectoryLookConnected(trajectory):
    thisChord = trajectory.getThisChord()
    thisChordPoints1, edge1 = computeChordCoord(
        thisChord, trajectory.getLastPosition(), trajectory.Tonnetz)
    if edge1[0][1] != edge1[0][0]:
        try:
            thisChordPoints2, edge2 = computeChordCoord(
                thisChord, trajectory.getLastPosition(2), trajectory.Tonnetz)
            if edge2[0][1] == edge2[0][0]:
                return TrajectoryCheckSecond(
                    (thisChordPoints2, edge2), trajectory)
        except PlacementError:
            pass
    return TrajectoryCheckSecond((thisChordPoints1, edge1), trajectory)


def TrajectoryCheckPosition(trajectory):
    return applyFirstSuccessful([
        lambda: TrajectoryLookConnected(trajectory),
        lambda: computeChordCoord(
                trajectory.getThisChord(),
                trajectory.getLastPosition(2),
                trajectory.Tonnetz),
        *(
            lambda: placeChordWithVirtualRef(
                    trajectory.getThisChord(),
                    trajectory.getLastPosition(),
                    trajectory.getNextChord(lookahead),
                    trajectory.Tonnetz)
            for lookahead in range(1, min(5, trajectory.chordsRemaining()))
        )
    ])


def TrajectoryWithFuture(trajectory):
    if trajectory.index > 1 and trajectory.chordsRemaining() > 1:
        return TrajectoryCheckPosition(trajectory)
    elif trajectory.index == 0:
        raise PlacementError("Strategy not valid for this position")
    else:
        return computeChordCoord(
            trajectory.getThisChord(),
            trajectory.getLastPosition(),
            trajectory.Tonnetz)


def placeChordWithVirtualRef(thisPCS, placedChordCoord, tempPCS, Tonnetz):
    virtualChordCoord, _ = computeChordCoord(
        tempPCS, placedChordCoord, Tonnetz)
    return computeChordCoord(thisPCS, virtualChordCoord, Tonnetz)


def NewTrajectory(listOfChords, Tonnetz, origin=(0, 0)):
    trajectory = TrajectoryClass(
        ChordConfiguration(
            listOfChords[0],
            origin,
            Tonnetz),
        listOfChords,
        Tonnetz)
    for index, chord in enumerate(listOfChords):
        if index == 0:
            continue
        elif index == 1:
            thisChordCoord, connectingEdge = applyFirstSuccessful([
                lambda: computeChordCoord(
                    trajectory.getThisChord(),
                    trajectory.getLastPosition(),
                    trajectory.Tonnetz),
                lambda: placeChordWithVirtualRef(
                    trajectory.getThisChord(),
                    trajectory.getLastPosition(),
                    trajectory.getNextChord(),
                    trajectory.Tonnetz)
            ])
        else:
            thisChordCoord, connectingEdge = TrajectoryWithFuture(trajectory)
        trajectory.addChord(thisChordCoord, connectingEdge)
    return trajectory

# ----------------------------------------------OTHER TRAJECTORY----------


def trajectoryRecursive(trajectory):
    alpha = 1
    while trajectory.index - alpha >= 0:
        try:
            return computeChordCoord(
                trajectory.getThisChord(),
                trajectory.getLastPosition(alpha),
                trajectory.Tonnetz)
        except PlacementError:
            pass
        alpha += 1
    raise PlacementError()


def TrajectoryLookBefore(listOfChords, Tonnetz, origin=(0, 0)):
    trajectory = TrajectoryClass(
        ChordConfiguration(
            listOfChords[0],
            origin,
            Tonnetz),
        listOfChords,
        Tonnetz)
    for index, chord in enumerate(listOfChords):
        if index == 0:
            continue
        elif index == 1:
            thisChordCoord, connectingEdge = applyFirstSuccessful([
                lambda: computeChordCoord(trajectory.getThisChord(),
                                          trajectory.getLastPosition(),
                                          trajectory.Tonnetz),
                lambda: placeChordWithVirtualRef(trajectory.getThisChord(),
                                                 trajectory.getLastPosition(),
                                                 trajectory.getNextChord(),
                                                 trajectory.Tonnetz)
            ])
        else:
            thisChordCoord, connectingEdge = trajectoryRecursive(trajectory)
        trajectory.addChord(thisChordCoord, connectingEdge)
    return trajectory


# ------------------------TRAJECTORY NO FUTURE------------------------------
def getDictFromTonnetz(Tonnetz):
    notePoints = dictOfTonnetz[TonnetzToString(Tonnetz)]
    return notePoints


def lastResort(trajectory):
    baseNoteDict = getDictFromTonnetz(trajectory.Tonnetz)
    thisChordRandomNote = trajectory.getThisChord()[0]
    lastChordRandomNote = trajectory.listOfChords[trajectory.index - 1][0]
    lastChordCoord = trajectory.getLastPosition()
    x1, y1 = baseNoteDict[lastChordRandomNote]
    x2, y2 = baseNoteDict[thisChordRandomNote]
    relation = (x1 - x2, y1 - y2)
    thisChordNoteCoord = (lastChordCoord[lastChordRandomNote][0] + relation[0],
        lastChordCoord[lastChordRandomNote][1] + relation[1])
    coordinates = ChordConfiguration(
        trajectory.getThisChord(), thisChordNoteCoord, trajectory.Tonnetz)
    return coordinates, []


def TrajectoryNoFuture(listOfChords, Tonnetz, origin=(0, 0)):
    trajectory = TrajectoryClass(
        ChordConfiguration(
            listOfChords[0],
            origin,
            Tonnetz),
        listOfChords,
        Tonnetz)
    for index, chord in enumerate(listOfChords):
        if index == 0:
            continue
        else:
            thisChordCoord, connectingEdge = applyFirstSuccessful([
                lambda: trajectoryRecursive(trajectory),
                lambda: lastResort(trajectory)
            ])
        trajectory.addChord(thisChordCoord, connectingEdge)
    return trajectory


# ------------------------TRAJECTORY EDGES----------------------------------


def TrajectoryNoteEdges(trajectory):
    TotalEdges = []
    dist = [-1, 0, 1]
    for dicts in trajectory.chordPositions:
        chordEdges = []
        cartl = list(itt.product(dicts.values(), dicts.values()))
        for couple in cartl:
            (x1, y1), (x2, y2) = couple
            if (x1 - x2) in dist and (y1 - y2) in dist:
                if not (((x1 - x2) == 1 and (y1 - y2) == -1)
                        or ((x1 - x2) == -1 and (y1 - y2) == 1)):
                    chordEdges.append(couple)
        TotalEdges.append(chordEdges)
    return TotalEdges


def SetOfPoints(trajectory):
    AllPoints = []
    for dicts in trajectory.chordPositions:
        AllPoints = AllPoints + list(dicts.values())
    PointSet = list(set(AllPoints))
    return PointSet, AllPoints


def weightsOfTrajPoints(setOfPoints, multiSetOfPoints):
    dictOfPointWeight = dict()
    for point in setOfPoints:
        dictOfPointWeight[point] = multiSetOfPoints.count(point)
    # Ideas about Using Normalized weights :
    # Maximum = max(list(dictOfPointWeight.values()))
    # Minimum = min(list(dictOfPointWeight.values()))
    return dictOfPointWeight
