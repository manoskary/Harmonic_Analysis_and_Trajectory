from NetworkX_GraphTranslation import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

def getCentrCoord(dictOfGraphs, typePlot) :
	points = []
	coordDict = dict()
	for key, graph in dictOfGraphs.items():
		point = CentralityPoint2D(graph, 3, typePlot) 
		points.append(point)
		coordDict[key] = point
	return zip(*points)

def CentralitiesScatterPlot(dictOfGraphs1, dictOfGraphs2, dictOfGraphs3, typePlot='Mix'):
	
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax = fig.gca(projection='3d')

	x1, y1, z1 = getCentrCoord(dictOfGraphs1, typePlot)
	x2, y2, z2 = getCentrCoord(dictOfGraphs2, typePlot)
	x3, y3, z3 = getCentrCoord(dictOfGraphs3, typePlot)

	ax.scatter(x1, y1, z1,  alpha=0.5, c='b', edgecolors='none', s=30, label='first input')
	ax.scatter(x2, y2, z2, alpha=0.5, c='r', edgecolors='none', s=30, label='second input')
	ax.scatter(x3, y3, z3, alpha=0.5, c='g', edgecolors='none', s=30, label='third input')

	if typePlot == 'Mix' :
		ax.set_xlabel('Eigen')
		ax.set_ylabel('Harmonic')
		ax.set_zlabel('Betweenness')
	else : 
		ax.set_xlabel(typePlot)

	plt.title('3D plotting')
	plt.legend(loc=2)
	plt.show()		


def Centralities2DPlot(dictOfGraphs1, dictOfGraphs2, dictOfGraphs3):

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)

	x1, y1, z1 = getCentrCoord(dictOfGraphs1, 'Mix')
	x2, y2, z2 = getCentrCoord(dictOfGraphs2, 'Mix')
	x3, y3, z3 = getCentrCoord(dictOfGraphs3, 'Mix')

	ax.scatter(x1, z1, alpha=0.5, c='b', edgecolors='none', s=30, label='first input')
	ax.scatter(x2, z2, alpha=0.5, c='r', edgecolors='none', s=30, label='first input')
	ax.scatter(x3, z3, alpha=0.5, c='g', edgecolors='none', s=30, label='first input')

	ax.set_xlabel('Eigen')
	ax.set_ylabel('Harmonic')

	plt.title('Centralities 2D Plot 3 gengre')
	plt.legend(loc=2)
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


