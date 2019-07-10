import networkx as nx



class GraphTrajectoryClass:
    def __init__(self, graph):
        self.trajectory = graph.trajectory
        self.graph = graph.graph



class GraphClass:
    def __init__(self, graph):
        self.graph = graph
        self.kaltz_coef = max(list(nx.katz_centrality(self.graph).values()))
        self.glob_clust_coef = mean(list(nx.clustering(self.graph).values()))
        self.square_clustering_coef = mean(
            list(nx.square_clustering(self.graph).values()))
        self.harmonic_coef = max(list(nx.harmonic_centrality(self.graph).values()))
        self.betweenness_coef = max(
            list(nx.betweenness_centrality(self.graph).values()))
        self.closeness_coef = max(list(nx.closeness_centrality(self.graph).values()))