from networkx import algorithms
from numpy import mean

class GraphTrajectoryClass :
	def __init__(self, graph, trajectory) :
		self.graph = graph
		self.trajectory = trajectory
		self.kaltz_coef = max(list(kaltz_centrality(graph).values()))
		self.glob_clust_coef = np.mean(list(clustering(graph).values()))
		self.square_clustering = np.mean(list(square_clustering(graph).values()))
		self.harmonic_coef = max(list(harmonic_centrality(graph).values()))
		self.betweenness_coef = max(list(betweenness_centrality(graph).values()))
		self.closeness_coef = max(list(closeness_centrality(graph).values()))