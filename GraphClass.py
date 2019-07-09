import networkx as nx

def CreateVertices(TrajectoryPoints, Graph) :
    setOfNodes = NodesSetCreate(TrajectoryPoints)
    nodes = dict()
    for index, point in enumerate(setOfNodes) :
        Graph.add_node(index)
        nodes[point] = index
    return Graph, nodes

def NodesSetCreate(TrajectoryPoints) :
    listOfNodes = []
    for dictChord in TrajectoryPoints :
        for node in dictChord.values() :
            listOfNodes.append(node)
    setOfNodes = list(set(listOfNodes))
    return setOfNodes

def EdgesSetCreate(TrajectoryEdges) :
    listOfEdges = []
    for edgesList in TrajectoryEdges :
        for edge in edgesList:
            listOfEdges.append(edge)
    setOfEdges = list(set(listOfEdges))
    return setOfEdges, listOfEdges

def EdgeWeights(setOfEdges, multiSetOfEdges):
    weights = dict()
    for edge in setOfEdges:
        weights[edge] = multiSetOfEdges.count(edge)
    edgeWeights = map((1 / max(list(weights.values()))), weights.values()) 
    return weights

def CreateEdges(Nodes, Edges, Graph):
    setOfEdges, multiSetOfEdges = EdgesSetCreate(Edges)
    weights = EdgeWeights(setOfEdges, multiSetOfEdges)
    for edge in setOfEdges :
        if (edge[0] in Nodes) and (edge[1] in Nodes): 
            Graph.add_edge(Nodes[edge[0]], Nodes[edge[1]], weight = weights[edge])
    return Graph

class GraphClass :
	def __init__(self, trajectory) :
		self.graph = nx.Graph()
		self.vertices = NodesSetCreate(trajectory.chordPositions)