# A script that takes a trajectory object and builds a graph object 
# as defined in Graph Class

from itertools import product
from GraphClass import GraphClass


# from trajectory build edges based on cartesian product
def TrajectoryNoteEdges(trajectory):
    TotalEdges = []
    dist = [-1, 0, 1]
    for dicts in trajectory.chordPositions:
        chordEdges = []
        cartl = list(product(dicts.values(), dicts.values()))
        for couple in cartl:
            (x1, y1), (x2, y2) = couple
            if (x1 - x2) in dist and (y1 - y2) in dist:
                if not (((x1 - x2) == 1 and (y1 - y2) == -1)
                        or ((x1 - x2) == -1 and (y1 - y2) == 1)):
                    chordEdges.append(couple)
        TotalEdges.append(chordEdges)
    return TotalEdges


# Add Vertex one by one in object
def CreateVertices(graph):
    setOfNodes = NodesSetCreate(graph)
    nodes = dict()
    for index, point in enumerate(setOfNodes):
        graph.addVertex(index, point)
        nodes[point] = index
    return nodes


# Take the set of all duplicate points in trajectory object
def NodesSetCreate(graph):
    listOfNodes = []
    for dictChord in graph.trajectory.chordPositions:
        for node in dictChord.values():
            listOfNodes.append(node)
    setOfNodes = list(set(listOfNodes))
    return setOfNodes


# Take the set of all duplicate points in trajectory object
def EdgesSetCreate(TrajectoryEdges):
    listOfEdges = []
    for edgesList in TrajectoryEdges:
        for edge in edgesList:
            listOfEdges.append(edge)
    setOfEdges = list(set(listOfEdges))
    return setOfEdges, listOfEdges


# add weights on edges based on multiplicity
def EdgeWeights(setOfEdges, multiSetOfEdges):
    weights = dict()
    for edge in setOfEdges:
        weights[edge] = multiSetOfEdges.count(edge)
    # Use the following to normalize edge weights
    # edgeWeights = map((1 / max(list(weights.values()))), weights.values())
    return weights


# Take the set of all duplicate points in trajectory object
def CreateEdges(graph, Nodes, Edges):
    setOfEdges, multiSetOfEdges = EdgesSetCreate(Edges)
    weights = EdgeWeights(setOfEdges, multiSetOfEdges)
    for edge in setOfEdges:
        if (edge[0] in Nodes) and (edge[1] in Nodes):
            graph.addEdge(edge, weights[edge])


# Create the object by encapsulating all functions
def CreateGraph(trajectory):
    graph = GraphClass(trajectory)
    edges = TrajectoryNoteEdges(trajectory)
    nodes = CreateVertices(graph)
    CreateEdges(graph, nodes, edges)
    graph.addCentralities()
    return graph
