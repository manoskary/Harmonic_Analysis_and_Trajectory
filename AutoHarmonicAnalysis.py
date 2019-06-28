from Tonnetz_Select import *
from TrajectoryCalculationsWithClass import *
from TrajectoryClass import *
from FirstNotePosition import *
from music21 import converter, corpus, instrument, midi, note, chord, pitch
from NetworkX_GraphTranslation import *
from scipy.spatial.distance import directed_hausdorff
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from MelodyExtraction import *
import os


def BachTonnetzSelect(number):
	listOfBachPieces = dict()
	for chorale in corpus.chorales.Iterator(1, number, returnType='filename'):
	    file = corpus.parse(chorale)
	    listOfBachPieces[chorale] = analysisFromCorpus(file)
	return listOfBachPieces

def BachTrajectoryGraphs(number, type = 'NewTrajectory'):
	listOfBachPieces = BachTonnetzSelect(number)
	BachTrajectoryPoints = dict()
	BachTrajectoryPointWeights = dict()
	BachTrajectoryEdges = dict()
	BachGraph = dict()
	# In this definition we keep only the graph but feel free to output anything else as well
	for key in listOfBachPieces :
	    chordList, Tonnetz = listOfBachPieces[key]
	    firstPoint = PlaceFirstNote(chordList, Tonnetz)
	    if type == 'NewTrajectory' :
	    	trajectory = NewTrajectory(chordList, Tonnetz, firstPoint)
	    else : 
	    	trajectory = TrajectoryLookBefore(chordList, Tonnetz, firstPoint)
	    Edges = TrajectoryNoteEdges(trajectory) + trajectory.connectingEdges
	    
	    setOfPoints, multiSetOfPoints = SetOfPoints(trajectory)
	    
	    BachTrajectoryPoints[key] = np.array(setOfPoints)
	    BachTrajectoryPointWeights[key] = weightsOfTrajPoints(setOfPoints, multiSetOfPoints)
	    BachTrajectoryEdges[key] = Edges
	    BachGraph[key] = CreateGraph(trajectory.chordPositions, Edges)

	return BachGraph



def ComparingGraphs(DictOfGraphs):
    GraphComparison = dict()
    for key1, key2 in itt.product(DictOfGraphs.keys(), DictOfGraphs.keys()) :
        if key1 != key2 :
            graph1 = DictOfGraphs[key1]
            graph2 = DictOfGraphs[key2]
            newKey = key1 + " vs " + key2
            GraphComparison[newKey] = CompareGraphsSpectrum(graph1, graph2)
    return GraphComparison


def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1] == valueToFind:
            listOfKeys.append(item[0])
    return  listOfKeys


def open_midi(file_path, remove_drums=True):
	mf = midi.MidiFile()
	mf.open(file_path)
	mf.read()
	mf.close()
	if (remove_drums):
		for i in range(len(mf.tracks)):
			mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]
	return midi.translate.midiFileToStream(mf)


def concat_path(path, child):
	newpath = path + "/" + child
	return newpath

def GraphOfNewPiece(newPiece, directory):  
	TrajectoryPoints = dict()
	TrajectoryPointWeights = dict()
	TrajectoryEdges = dict()
	Graph = dict()
	if directory == 'corpus' :
		file = ms.corpus.parse(newPiece)
		chordList, Tonnetz = analysisFromCorpus(file)
	else :
		if newPiece.endswith(".mid") or newPiece.endswith(".MID"):
			file = open_midi(concat_path(directory, newPiece), directory)
			chordList, Tonnetz = analysisFromCorpus(file)
		elif newPiece.endswith(".mxl") or newPiece.endswith(".xml"):
			chordList, Tonnetz = fromMidiToPCS(newPiece)
	if Tonnetz == [3, 4, 5] :
		firstPoint = PlaceFirstNote(chordList, Tonnetz)
		trajectory = NewTrajectory(chordList, Tonnetz, firstPoint)
		Edges = TrajectoryNoteEdges(trajectory) + trajectory.connectingEdges
		setOfPoints, multiSetOfPoints = SetOfPoints(trajectory)	    
		TrajectoryPoints[newPiece] = np.array(setOfPoints)
		TrajectoryPointWeights[newPiece] = weightsOfTrajPoints(setOfPoints, multiSetOfPoints)
		TrajectoryEdges[newPiece] = Edges
		Graph[newPiece] = CreateGraph(trajectory.chordPositions, Edges)
	return(Graph)

#---------------------------------------- GRAPH COMPARISON TECHNIQUES ADAPTED TO THE FORMAT A DICT OF PIECES-----------------------------

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
	print(getKeysByValue(graphComparison, minimum), minimum)
	print(getKeysByValue(graphComparison, maximum), maximum)
	return graphComparison

def ComparisonOfTrajectories(numberOfChorales, otherPiece) :
	# Create the graphs for chorales and the otherPiece
	BachDict = BachTonnetzSelect(numberOfChorales) #Tonnetz Select
	BachGraph = BachTrajectoryGraphs(BachDict)
	graphOfNewPiece = GraphOfNewPiece(otherPiece)
	# Compare the graphs
	newDictOfGraphs = Merge(BachGraph, graphOfNewPiece)

	spectralGraphCompare = SpectralGraphCompare(newDictOfGraphs)
	globalClusteringCoef = GlobalClustering(newDictOfGraphs)

	# return a dictionary of all trajectory graphs (key = name of piece)
	return newDictOfGraphs, spectralGraphCompare, globalClusteringCoef



def ComparisonOfTrajectoriesLookBefore(numberOfChorales, otherPiece) :
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


#------------------------------- ALL TRAJECTORY AUTOMATIC COMPARISON ---------------------------------------------------


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


def ComparisonOfTrajectoriesLookBeforeUnit(BachDict, otherPiece) :
	# Create the graphs for chorales and the otherPiece
	BachGraph = BachTrajectoryLookBeforeGraphs(BachDict)
	graphOfNewPiece = GraphOfNewPieceLookBefore(otherPiece)
	# Compare the graphs
	newDictOfGraphs = Merge(BachGraph, graphOfNewPiece)

	spectralGraphCompare = SpectralGraphCompare(newDictOfGraphs)
	globalClusteringCoef = GlobalClustering(newDictOfGraphs)

	# return a dictionary of all trajectory graphs (key = name of piece)
	return newDictOfGraphs, spectralGraphCompare, globalClusteringCoef


def AllCompare(numberOfChorales, otherPiece) :
	BachDict = BachTonnetzSelect(numberOfChorales)
	result1 = ComparisonOfTrajectoriesUnit(BachDict, otherPiece)
	result2 = versionComparisonOfTrajectoriesLookBeforeUnit(BachDict, otherPiece)
	return result1, result2


def CentralitiesScatterPlot(dictOfGraphs1, dictOfGraphs2, typePlot='Mix'):
	points1 = []

	fig = plt.figure()
	ax = Axes3D(fig)

	for key, graph in dictOfGraphs1.items():
		point = CentralityPoint2D(graph, 3, typePlot) 
		points1.append(point)

	points2 = []
	for key, graph in dictOfGraphs2.items():
		point = CentralityPoint2D(graph, 3, typePlot)
		points2.append(point)

	x1, y1, z1 = zip(*points1)
	x2, y2, z2 = zip(*points2)

	ax.scatter(x1, y1, z1,  alpha=0.5, c='b', edgecolors='none', s=30)
	ax.scatter(x2, y2, z2, alpha=0.5, c='r', edgecolors='none', s=30)

	if typePlot == 'Mix' :
		ax.set_xlabel('Eigen')
		ax.set_ylabel('Harmonic')
		ax.set_zlabel('Betweenness')
	elif typePlot == 'Mix2' :
		ax.set_xlabel('Eigen')
		ax.set_ylabel('GlobalClustering')
		ax.set_zlabel('Betweenness')
	elif typePlot == 'Mix3' :
		ax.set_xlabel('Eigenvalues')
		ax.set_ylabel('GlobalClustering')
		ax.set_zlabel('Harmonic')
	else : 
		ax.set_xlabel(typePlot)

	plt.show()

def plotCentrality(dictOfGraphs, numberOfPoints=3, typeOfCentrality='kaltz') :
	fig = plt.figure()
	ax = Axes3D(fig)

	points = []

	for graph in dictOfGraphs.values():
		point = chooseCentrality(graph, numberOfPoints, typeOfCentrality)
		points.append(point)

	x, y, z = zip(*points)

	ax.scatter(x, y, z,  alpha=0.5, c='b', edgecolors='none', s=30)

	ax.set_xlabel(typeOfCentrality)


def plotAllCentralities3D(dictOfGraphs):
	centralities = ['kaltz', 'betweenness', 'closeness', 'harmonic', 'degree']
	for centrality in centralities :
		plotCentrality(dictOfGraphs, 3, centrality)


def GetWorksByComposer(composerName):
	listofWorks = ms.corpus.getComposer(composerName)
	dictOfGraphs = dict()
	if len(listofWorks) > 0 :
		for piece in listofWorks:
			try :
				print("Building Trajectory for ", piece)
				graph = GraphOfNewPiece(piece, 'corpus')
				dictOfGraphs = Merge(dictOfGraphs, graph)
			except :
				print("--> Cannot build Trajectory for ", piece)
	return dictOfGraphs


def GetWorksByDirectory(directory): 
	dictOfGraphs = dict()
	for file in os.listdir(directory):
		if file.endswith(".mid") or file.endswith(".MID") or file.endswith(".mxl") or file.endswith(".xml"):
			try :
				print("Building Trajectory for ", file)
				graph = GraphOfNewPiece(file, directory)
				dictOfGraphs = Merge(dictOfGraphs, graph)
			except :
				print("--> Cannot build Trajectory for ", file)
	return dictOfGraphs
				

def BachMelodyTonnetzSelect(number):
	listOfBachPieces = dict()
	for chorale in corpus.chorales.Iterator(1, number, returnType='filename'):
	    file = corpus.parse(chorale)
	    # Add the melody's corresponding Tonnetz
	    listOfBachPieces[chorale] = analysisFromCorpus(file), melodyTonnetzCorpus(file)
	return listOfBachPieces


def BachTrajectoryGraphsWithMelodyTonnetz(number, type = 'NewTrajectory'):
	listOfBachPieces = BachMelodyTonnetzSelect(number)
	BachTrajectoryPoints = dict()
	BachTrajectoryPointWeights = dict()
	BachTrajectoryEdges = dict()
	BachGraph = dict()
	# melodygraphs
	BachGraphT129 = dict()
	BachGraphT138 = dict()

	# In this definition we keep only the graph but feel free to output anything else as well
	for key in listOfBachPieces :
	    (chordList, Tonnetz), melodyTon = listOfBachPieces[key]
	    firstPoint = PlaceFirstNote(chordList, Tonnetz)
	    if type == 'NewTrajectory' :
	    	trajectory = NewTrajectory(chordList, Tonnetz, firstPoint)
	    else : 
	    	trajectory = TrajectoryLookBefore(chordList, Tonnetz, firstPoint)
	    Edges = TrajectoryNoteEdges(trajectory) + trajectory.connectingEdges
	    
	    setOfPoints, multiSetOfPoints = SetOfPoints(trajectory)
	    
	    BachTrajectoryPoints[key] = np.array(setOfPoints)
	    BachTrajectoryPointWeights[key] = weightsOfTrajPoints(setOfPoints, multiSetOfPoints)
	    BachTrajectoryEdges[key] = Edges

	    #Separate the graphs based on their melody Tonnetz
	    if melodyTon == [1, 2, 9] :
	    	BachGraphT129[key] = CreateGraph(trajectory.chordPositions, Edges)
	    else :
	    	BachGraph[key] = CreateGraph(trajectory.chordPositions, Edges)

	return BachGraphT129, BachGraph

