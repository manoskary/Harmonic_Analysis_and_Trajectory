import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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

def select_k(spectrum, minimum_energy = 0.7):
    running_total = 0.0
    total = sum(spectrum)
    if total == 0.0:
        return len(spectrum)
    # Find the eigen values that describe the minimum enery % of the piece
    for i in range(len(spectrum)):
        running_total += spectrum[i]
        if running_total / total >= minimum_energy:
            return i + 1
    return len(spectrum)

def CompareGraphsSpectrum(graph1, graph2) :
    laplacian1 = nx.spectrum.laplacian_spectrum(graph1)
    laplacian2 = nx.spectrum.laplacian_spectrum(graph2)
    k1 = select_k(laplacian1)
    k2 = select_k(laplacian2)
    #take the fewer dimensions to describe the result
    k = min(k1, k2)
    #the similarity is the sum of the eukleidian distance of the most important nodes
    similarity = sum((laplacian1[:k] - laplacian2[:k])**2)
    return similarity


def CreateGraph(Points, Edges):
    G = nx.Graph()
    newG, Nodes = CreateVertices(Points, G)
    Graph = CreateEdges(Nodes, Edges, newG)
    return Graph

def GlobalClusteringCoefficient(graph):
    coef = np.mean(list(nx.clustering(graph).values()))
    return coef


def PlotCentralities(graph):

    c_degree = nx.degree_centrality(graph)
    c_degree = list(c_degree.values())

    c_eigenvector = nx.katz_centrality(graph)
    c_eigenvector = list(c_eigenvector.values())

    c_harmonic = nx.harmonic_centrality(graph)
    c_harmonic = list(c_harmonic.values())

    c_betweenness = nx.betweenness_centrality(graph)
    c_betweenness = list(c_betweenness.values())

    plt.figure(figsize=(18, 12))
    f, axarr = plt.subplots(2, 2, num=1)
    plt.sca(axarr[0,0])
    nx.draw(graph, cmap = plt.get_cmap('inferno'), node_color = c_degree, node_size=300, with_labels=True)
    axarr[0,0].set_title('Degree Centrality', size=16)

    plt.sca(axarr[0,1])
    nx.draw(graph, cmap = plt.get_cmap('inferno'), node_color = c_eigenvector, node_size=300, with_labels=True)
    axarr[0,1].set_title('Eigenvalue Centrality (Katz)', size=16)

    plt.sca(axarr[1,0])
    nx.draw(graph, cmap = plt.get_cmap('inferno'), node_color = c_harmonic, node_size=300, with_labels=True)
    axarr[1,0].set_title('harmonic_centrality Centrality', size=16)

    plt.sca(axarr[1,1])
    nx.draw(graph, cmap = plt.get_cmap('inferno'), node_color = c_betweenness, node_size=300, with_labels=True)
    axarr[1,1].set_title('Betweenness Centrality', size=16)

def CentralityPoint4D(graph):
    c_degree = nx.degree_centrality(graph)
    c_degree = max(list(c_degree.values()))

    c_eigenvector = nx.katz_centrality(graph)
    c_eigenvector = max(list(c_eigenvector.values()))

    c_harmonic = nx.harmonic_centrality(graph)
    c_harmonic = max(list(c_harmonic.values()))

    c_betweenness = nx.betweenness_centrality(graph)
    c_betweenness = max(list(c_betweenness.values()))

    point = (c_degree, c_eigenvector, c_harmonic, c_betweenness)
    return point


import heapq


def CentralityPoint2D(graph, numberOfPoints, typePlot):

    points = dict()    

    c_eigenvector = nx.katz_centrality(graph)
    c_eigenvector = heapq.nlargest(numberOfPoints, list(c_eigenvector.values()))
    max_eigenvector = max(c_eigenvector)
    points['Eigenvalues'] = c_eigenvector

    c_betweenness = nx.betweenness_centrality(graph)
    c_betweenness = heapq.nlargest(numberOfPoints, list(c_betweenness.values()))
    max_betweenness = max(c_betweenness)
    points['Betweenness'] = c_betweenness

    c_closeness = nx.closeness_centrality(graph)
    c_closeness = heapq.nlargest(numberOfPoints, list(c_closeness.values()))
    max_closeness = max(c_closeness)
    points['Closeness'] = c_closeness

    c_harmonic = nx.harmonic_centrality(graph)
    c_harmonic = heapq.nlargest(numberOfPoints, list(c_harmonic.values()))
    max_harmonic = max(c_harmonic)
    points['Harmonic'] = c_harmonic

    c_degree = nx.degree_centrality(graph)
    c_degree = heapq.nlargest(numberOfPoints, list(c_degree.values()))
    max_degree = max(c_degree)
    points['Degree'] = c_degree

    glCoe = GlobalClusteringCoefficient(graph)

    points['Mix'] = (max_eigenvector, max_harmonic, max_betweenness)
    points['Mix2'] = (max_eigenvector, glCoe, max_betweenness)
    points['Mix3'] = (max_eigenvector, glCoe, max_harmonic)
    points['Mix4'] = (glCoe, max_betweenness, max_harmonic)

    return points[typePlot]

def kaltzCentrality(graph, numberOfPoints):
    c_eigenvector = nx.katz_centrality(graph)
    c_eigenvector = heapq.nlargest(numberOfPoints, list(c_eigenvector.values()))
    return c_eigenvector

def betweennessCentrality(graph, numberOfPoints) :   
    c_betweenness = nx.betweenness_centrality(graph)
    c_betweenness = heapq.nlargest(numberOfPoints, list(c_betweenness.values()))
    return c_betweenness

def closenessCentrality(graph, numberOfPoints) :
    c_closeness = nx.closeness_centrality(graph)
    c_closeness = heapq.nlargest(numberOfPoints, list(c_closeness.values()))
    return  c_closeness

def harmonicCentrality(graph, numberOfPoints) :
    c_harmonic = nx.harmonic_centrality(graph)
    c_harmonic = heapq.nlargest(numberOfPoints, list(c_harmonic.values()))
    return c_harmonic

def degreeCentrality(graph, numberOfPoints) :
    c_degree = nx.degree_centrality(graph)
    c_degree = heapq.nlargest(numberOfPoints, list(c_degree.values()))
    return c_degree

def chooseCentrality(graph, numberOfPoints, typePlot) :
    if typePlot == 'kaltz' :
        return kaltzCentrality(graph, numberOfPoints)
    elif typePlot == 'betweenness' :
        return betweennessCentrality(graph, numberOfPoints)
    elif typePlot == 'closeness' :
        return closenessCentrality(graph, numberOfPoints)
    elif typePlot == 'harmonic' :
        return harmonicCentrality(graph, numberOfPoints)
    elif typePlot == 'degree' :
        return degreeCentrality(graph, numberOfPoints) 
    else :
        raise KeyError()
