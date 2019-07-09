from Tonnetz_Select import *
from TrajectoryCalculationsWithClass import *
from TrajectoryClass import *
from FirstNotePosition import *
from music21 import converter, corpus, instrument, midi, note, chord, pitch
from NetworkX_GraphTranslation import *
from structural_functions import getKeyByValue
import numpy as np
from MelodyExtraction import *
import os


def BachTonnetzSelect(number):
    listOfBachPieces = dict()
    for chorale in corpus.chorales.Iterator(1, number, returnType='filename'):
        file = corpus.parse(chorale)
        listOfBachPieces[chorale] = analysisFromCorpus(file)
    return listOfBachPieces


def BachTrajectoryGraphs(number, type='NewTrajectory'):
    listOfBachPieces = BachTonnetzSelect(number)
    BachTrajectoryPoints = dict()
    BachTrajectoryPointWeights = dict()
    BachTrajectoryEdges = dict()
    BachGraph = dict()
    # In this definition we keep only the graph but feel free to output
    # anything else as well
    for key in listOfBachPieces:
        chordList, Tonnetz = listOfBachPieces[key]
        firstPoint = PlaceFirstNote(chordList, Tonnetz)
        if type == 'NewTrajectory':
            trajectory = NewTrajectory(chordList, Tonnetz, firstPoint)
        else:
            trajectory = TrajectoryLookBefore(chordList, Tonnetz, firstPoint)
        Edges = TrajectoryNoteEdges(trajectory) + trajectory.connectingEdges

        setOfPoints, multiSetOfPoints = SetOfPoints(trajectory)

        BachTrajectoryPoints[key] = np.array(setOfPoints)
        BachTrajectoryPointWeights[key] = weightsOfTrajPoints(
            setOfPoints, multiSetOfPoints)
        BachTrajectoryEdges[key] = Edges
        BachGraph[key] = CreateGraph(trajectory.chordPositions, Edges)

    return BachGraph


def ComparingGraphs(DictOfGraphs):
    GraphComparison = dict()
    for key1, key2 in itt.product(DictOfGraphs.keys(), DictOfGraphs.keys()):
        if key1 != key2:
            graph1 = DictOfGraphs[key1]
            graph2 = DictOfGraphs[key2]
            newKey = key1 + " vs " + key2
            GraphComparison[newKey] = CompareGraphsSpectrum(graph1, graph2)
    return GraphComparison


def open_midi(file_path, remove_drums=True):
    mf = midi.MidiFile()
    mf.open(file_path)
    mf.read()
    mf.close()
    if (remove_drums):
        for i in range(len(mf.tracks)):
            mf.tracks[i].events = [
                ev for ev in mf.tracks[i].events if ev.channel != 10]
    return midi.translate.midiFileToStream(mf)


def concat_path(path, child):
    newpath = path + "/" + child
    return newpath


def GraphOfNewPiece(newPiece, directory):
    TrajectoryPoints = dict()
    TrajectoryPointWeights = dict()
    TrajectoryEdges = dict()
    Graph = dict()
    if directory == 'corpus':
        file = ms.corpus.parse(newPiece)
        chordList, Tonnetz = analysisFromCorpus(file)
    else:
        if newPiece.endswith(".mid") or newPiece.endswith(".MID"):
            file = open_midi(concat_path(directory, newPiece), directory)
            chordList, Tonnetz = analysisFromCorpus(file)
        elif newPiece.endswith(".mxl") or newPiece.endswith(".xml"):
            chordList, Tonnetz = fromMidiToPCS(newPiece)
    if Tonnetz == [3, 4, 5]:
        firstPoint = PlaceFirstNote(chordList, Tonnetz)
        trajectory = NewTrajectory(chordList, Tonnetz, firstPoint)
        Edges = TrajectoryNoteEdges(trajectory) + trajectory.connectingEdges
        setOfPoints, multiSetOfPoints = SetOfPoints(trajectory)
        TrajectoryPoints[newPiece] = np.array(setOfPoints)
        TrajectoryPointWeights[newPiece] = weightsOfTrajPoints(
            setOfPoints, multiSetOfPoints)
        TrajectoryEdges[newPiece] = Edges
        Graph[newPiece] = CreateGraph(trajectory.chordPositions, Edges)
    return(Graph)

# ---------------------------------------- GRAPH COMPARISON TECHNIQUES ADA


def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def GlobalClustering(dictOfGraphs):
    globalClusteringCoef = dict()
    for key, graph in dictOfGraphs.items():
        globalClusteringCoef[key] = GlobalClusteringCoefficient(graph)
    return globalClusteringCoef


def SpectralGraphCompare(dictOfGraphs):
    graphComparison = ComparingGraphs(dictOfGraphs)
    minimum = min(list(graphComparison.values()))
    maximum = max(list(graphComparison.values()))
    print(getKeyByValue(graphComparison, minimum), minimum)
    print(getKeyByValue(graphComparison, maximum), maximum)
    return graphComparison


def ComparisonOfTrajectories(numberOfChorales, otherPiece):
    # Create the graphs for chorales and the otherPiece
    BachDict = BachTonnetzSelect(numberOfChorales)  # Tonnetz Select
    BachGraph = BachTrajectoryGraphs(BachDict)
    graphOfNewPiece = GraphOfNewPiece(otherPiece)
    # Compare the graphs
    newDictOfGraphs = Merge(BachGraph, graphOfNewPiece)

    spectralGraphCompare = SpectralGraphCompare(newDictOfGraphs)
    globalClusteringCoef = GlobalClustering(newDictOfGraphs)

    # return a dictionary of all trajectory graphs (key = name of piece)
    return newDictOfGraphs, spectralGraphCompare, globalClusteringCoef


def ComparisonOfTrajectoriesLookBefore(numberOfChorales, otherPiece):
    # Create the graphs for chorales and the otherPiece
    BachDict = BachTonnetzSelect(numberOfChorales)
    BachGraph = BachTrajectoryLookBeforeGraphs(BachDict)
    graphOfNewPiece = GraphOfNewPieceLookBefore(otherPiece)
    # Compare the graphs
    newDictOfGraphs = Merge(BachGraph, graphOfNewPiece)

    spectralGraphCompare = SpectralGraphCompare(newDictOfGraphs)
    globalClusteringCoef = GlobalClustering(newDictOfGraphs)

    # return a dictionary of all trajectory graphs (key = name of piece)
    return newDictOfGraphs, spectralGraphCompare, globalClusteringCoef


# ------------------------------- ALL TRAJECTORY AUTOMATIC COMPARISON ----


def ComparisonOfTrajectoriesUnit(BachDict, otherPiece):
    # Create the graphs for chorales and the otherPiece
    BachGraph = BachTrajectoryGraphs(BachDict)
    graphOfNewPiece = GraphOfNewPiece(otherPiece)
    # Compare the graphs
    newDictOfGraphs = Merge(BachGraph, graphOfNewPiece)

    spectralGraphCompare = SpectralGraphCompare(newDictOfGraphs)
    globalClusteringCoef = GlobalClustering(newDictOfGraphs)

    # return a dictionary of all trajectory graphs (key = name of piece)
    return newDictOfGraphs, spectralGraphCompare, globalClusteringCoef


def ComparisonOfTrajectoriesLookBeforeUnit(BachDict, otherPiece):
    # Create the graphs for chorales and the otherPiece
    BachGraph = BachTrajectoryLookBeforeGraphs(BachDict)
    graphOfNewPiece = GraphOfNewPieceLookBefore(otherPiece)
    # Compare the graphs
    newDictOfGraphs = Merge(BachGraph, graphOfNewPiece)

    spectralGraphCompare = SpectralGraphCompare(newDictOfGraphs)
    globalClusteringCoef = GlobalClustering(newDictOfGraphs)

    # return a dictionary of all trajectory graphs (key = name of piece)
    return newDictOfGraphs, spectralGraphCompare, globalClusteringCoef


def AllCompare(numberOfChorales, otherPiece):
    BachDict = BachTonnetzSelect(numberOfChorales)
    result1 = ComparisonOfTrajectoriesUnit(BachDict, otherPiece)
    result2 = versionComparisonOfTrajectoriesLookBeforeUnit(
        BachDict, otherPiece)
    return result1, result2


def GetWorksByComposer(composerName):
    listofWorks = ms.corpus.getComposer(composerName)
    dictOfGraphs = dict()
    if len(listofWorks) > 0:
        for piece in listofWorks:
            try:
                print("Building Trajectory for ", piece)
                graph = GraphOfNewPiece(piece, 'corpus')
                dictOfGraphs = Merge(dictOfGraphs, graph)
            except BaseException:
                print("--> Cannot build Trajectory for ", piece)
    return dictOfGraphs


def GetWorksByDirectory(directory):
    dictOfGraphs = dict()
    for file in os.listdir(directory):
        if file.endswith(".mid") or file.endswith(
                ".MID") or file.endswith(".mxl") or file.endswith(".xml"):
            try:
                print("Building Trajectory for ", file)
                graph = GraphOfNewPiece(file, directory)
                dictOfGraphs = Merge(dictOfGraphs, graph)
            except BaseException:
                print("--> Cannot build Trajectory for ", file)
    return dictOfGraphs


# def BachMelodyTonnetzSelect(number):
# 	listOfBachPieces = dict()
# 	for chorale in corpus.chorales.Iterator(1, number, returnType='filename'):
# 	    file = corpus.parse(chorale)
# 	    # Add the melody's corresponding Tonnetz
# 	    listOfBachPieces[chorale] = analysisFromCorpus(file), melodyTonnetzCorpus(file)
# 	return listOfBachPieces


# def BachTrajectoryGraphsWithMelodyTonnetz(number, type = 'NewTrajectory'):
# 	listOfBachPieces = BachMelodyTonnetzSelect(number)
# 	BachTrajectoryPoints = dict()
# 	BachTrajectoryPointWeights = dict()
# 	BachTrajectoryEdges = dict()
# 	BachGraph = dict()
# 	# melodygraphs
# 	BachGraphT129 = dict()
# 	BachGraphT138 = dict()

# 	# In this definition we keep only the graph but feel free to output anything else as well
# 	for key in listOfBachPieces :
# 	    (chordList, Tonnetz), melodyTon = listOfBachPieces[key]
# 	    firstPoint = PlaceFirstNote(chordList, Tonnetz)
# 	    if type == 'NewTrajectory' :
# 	    	trajectory = NewTrajectory(chordList, Tonnetz, firstPoint)
# 	    else :
# 	    	trajectory = TrajectoryLookBefore(chordList, Tonnetz, firstPoint)
# 	    Edges = TrajectoryNoteEdges(trajectory) + trajectory.connectingEdges

# 	    setOfPoints, multiSetOfPoints = SetOfPoints(trajectory)

# 	    BachTrajectoryPoints[key] = np.array(setOfPoints)
# 	    BachTrajectoryPointWeights[key] = weightsOfTrajPoints(setOfPoints, multiSetOfPoints)
# 	    BachTrajectoryEdges[key] = Edges

# 	    #Separate the graphs based on their melody Tonnetz
# 	    if melodyTon == [1, 2, 9] :
# 	    	BachGraphT129[key] = CreateGraph(trajectory.chordPositions, Edges)
# 	    else :
# 	    	BachGraph[key] = CreateGraph(trajectory.chordPositions, Edges)

# 	return BachGraphT129, BachGraph


# The point of the following functions is to find the pieces that deviate
# from the centralities distribution


def getCentrCoord(dictOfGraphs):
    coordDict = dict()
    for key, graph in dictOfGraphs.items():
        point = CentralityPoint2D(graph, 3, 'Mix')
        coordDict[key] = point
    return coordDict


def meanPoint(coordDict):
    x, y, z = zip(*list(coordDict.values()))

    mean = (float(format(sum(x) / len(coordDict), '.2f')),
            float(format(sum(y) / len(coordDict), '.2f')))
    return mean


def getOffPoints(coordDict):
    distanceDict = dict()
    mean = meanPoint(coordDict)
    for point in coordDict.values():
        sumofsquares = (point[0] - mean[0])**2 + (point[1] - mean[1])**2
        distance = float(format(sumofsquares**(0.5), '.2f'))
        distanceDict[point] = distance
    maxdistance = max(list(distanceDict.values()))
    offPoint = getKeyByValue(distanceDict, maxdistance)
    offPiece = getKeyByValue(coordDict, offPoint)
    return offPiece


def getInPoint(coordDict):
    distanceDict = dict()
    mean = meanPoint(coordDict)
    for point in coordDict.values():
        sumofsquares = (point[0] - mean[0])**2 + (point[1] - mean[1])**2
        distance = float(format(sumofsquares**(0.5), '.2f'))
        distanceDict[point] = distance
    maxdistance = min(list(distanceDict.values()))
    offPoint = getKeyByValue(distanceDict, maxdistance)
    offPiece = getKeyByValue(coordDict, offPoint)
    return offPiece


def getPiecesOutOfDistribution(dictOfGraphs, edge='max'):
    coordDict = getCentrCoord(dictOfGraphs)
    if edge == 'max':
        piece = getOffPoints(coordDict)
    else:
        piece = getInPoint(coordDict)
    try:
        corpusPiece = piece[0] + '.xml'
        s = ms.corpus.parse(corpusPiece)
        s.show()
    except BaseException:
        print('Cannot show the score')
    return piece


def SortPiecesByDistances(dictOfGraphs):
    coordDict = getCentrCoord(dictOfGraphs)
    distanceDict = dict()
    mean = meanPoint(coordDict)
    for point in coordDict.values():
        sumofsquares = (point[0] - mean[0])**2 + (point[1] - mean[1])**2
        distance = float(format(sumofsquares**(0.5), '.2f'))
        distanceDict[point] = distance
    distance = sorted(distanceDict.values())
    print(distance)
    for dist in distance:
        point = getKeyByValue(distanceDict, dist)
        piece = getKeyByValue(coordDict, point)
        print(piece)


def twoDictsDistCompare(dictOfGraphs1, dictOfGraphs2):
    coordDict1 = getCentrCoord(dictOfGraphs1)
    coordDict2 = getCentrCoord(dictOfGraphs2)
    mean1 = meanPoint(coordDict1)
    mean2 = meanPoint(coordDict2)
    distanceDict1 = dict()
    for point in coordDict1.values():
        sumofsquares = (point[0] - mean2[0])**2 + (point[1] - mean2[1])**2
        distance = float(format(sumofsquares**(0.5), '.2f'))
        distanceDict1[point] = distance
    maxdistance = min(list(distanceDict1.values()))
    offPoint = getKeyByValue(distanceDict1, maxdistance)
    offPiece1 = getKeyByValue(coordDict1, offPoint)

    distanceDict2 = dict()
    for point in coordDict2.values():
        sumofsquares = (point[0] - mean2[0])**2 + (point[1] - mean2[1])**2
        distance = float(format(sumofsquares**(0.5), '.2f'))
        distanceDict2[point] = distance
    maxdistance = min(list(distanceDict2.values()))
    offPoint = getKeyByValue(distanceDict2, maxdistance)
    offPiece2 = getKeyByValue(coordDict2, offPoint)

    return offPiece1, offPiece2
