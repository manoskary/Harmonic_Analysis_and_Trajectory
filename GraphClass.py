from networkx import nx
from numpy import mean


class GraphClass:

    def __init__(self, trajectory):
        self.trajectory = trajectory
        self.vertices = []
        self.edges = []
        self.graph = nx.Graph()
        # self.name = None
        self.style = None
        self.composer = None
        self.harmony = None

    def addVertex(self, index, point):
        self.vertices.append(point)
        self.graph.add_node(index)

    def addEdge(self, edge, weight):
        self.edges.append(edge)
        self.graph.add_edge(edge[0], edge[1])

    def addCentralities(self) : 
        self.kalz_coef = max(list(nx.katz_centrality(self.graph).values()))
        self.glob_clust_coef = mean(list(nx.clustering(self.graph).values()))
        self.square_clustering_coef = mean(
            list(nx.square_clustering(self.graph).values()))
        self.harmonic_coef = max(list(nx.harmonic_centrality(self.graph).values()))
        self.betweenness_coef = max(
            list(nx.betweenness_centrality(self.graph).values()))
        self.closeness_coef = max(list(nx.closeness_centrality(self.graph).values()))

    def addName(self, name):
        self.name = name

    def addStyle(self, style_label):
        self.style = style_label

    def addHarmonyStyle(self, harmony_label):
        self.harmony = harmony_label

    def addComposer(self, composer):
        self.composer = composer

