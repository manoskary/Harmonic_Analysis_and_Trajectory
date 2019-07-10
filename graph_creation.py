from itertools import product
from GraphClass import GraphClass


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


def CreateVertices(graph):
    setOfNodes = NodesSetCreate(graph)
    nodes = dict()
    for index, point in enumerate(setOfNodes):
        graph.addVertex(index, point)
        nodes[point] = index
    return nodes


def NodesSetCreate(graph):
    listOfNodes = []
    for dictChord in graph.trajectory.chordPositions:
        for node in dictChord.values():
            listOfNodes.append(node)
    setOfNodes = list(set(listOfNodes))
    return setOfNodes


def EdgesSetCreate(TrajectoryEdges):
    listOfEdges = []
    for edgesList in TrajectoryEdges:
        for edge in edgesList:
            listOfEdges.append(edge)
    setOfEdges = list(set(listOfEdges))
    return setOfEdges, listOfEdges


def EdgeWeights(setOfEdges, multiSetOfEdges):
    weights = dict()
    for edge in setOfEdges:
        weights[edge] = multiSetOfEdges.count(edge)
    # Use the following to normalize edge weights
    # edgeWeights = map((1 / max(list(weights.values()))), weights.values())
    return weights


def CreateEdges(graph, Nodes, Edges):
    setOfEdges, multiSetOfEdges = EdgesSetCreate(Edges)
    weights = EdgeWeights(setOfEdges, multiSetOfEdges)
    for edge in setOfEdges:
        if (edge[0] in Nodes) and (edge[1] in Nodes):
            graph.addEdge(edge, weights[edge])


def CreateGraph(trajectory):
    graph = GraphClass(trajectory)
    edges = TrajectoryNoteEdges(trajectory)
    nodes = CreateVertices(graph)
    CreateEdges(graph, nodes, edges)
    graph.addCentralities()
    return graph
    