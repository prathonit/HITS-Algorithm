import numpy as np
from time import time
from utils import get_input

class PageRank:
    def __init__(self, graph, n_nodes, n_edges=None):
        """
        Given a graph with number of nodes and edges, perform the PageRank algorithm and return the scores.

        Args:
            graph: Adjacency matrix of the graph.
            n_nodes: Number of nodes in the graph.
            n_edges: Number of edges in the graph.

        Returns:--ht
            pageRankScores: PageRank scores of all the nodes in the graph.
        """
        self.graph = graph
        self.n_nodes = n_nodes
        self.n_edges = n_edges
        self.input_nodes = list(range(self.n_nodes))

    def get_scores_iterative(self, alpha=0.1, epsilon=0.0000001):
        """
        Calculate the PageRank scores of all the nodes in the graph iteratively.

        Args:
            alpha: Teleportation probabiility.
            epsilon: Error threshold.

        Returns:
            PageRank scores of all the nodes in the graph.
        """

        # Intialize  matrix
        M = self.graph / np.sum(self.graph, axis=0)

        teleportation_matrix = np.zeros(self.n_nodes)
        pageRankScores = np.zeros(self.n_nodes)

        # Update Teleportation and Page Rank Score Matrices with 1/n_nodes for the input nodes.
        for node_id in self.input_nodes:
            teleportation_matrix[int(node_id)] = 1 / self.n_nodes
            pageRankScores[int(node_id)] = 1 / self.n_nodes

        print('Calculating PageRank Scores with alpha = ' + str(alpha) + '...')

        # Calculating Page Rank Scores
        while True:
            oldPageRankScores = pageRankScores
            pageRankScores = (alpha * np.dot(M, pageRankScores)) + ((1 - alpha) * teleportation_matrix)
            if np.linalg.norm(pageRankScores - oldPageRankScores) < epsilon:
                break

        # Normalizing Page Rank Scores
        pageRankScores = pageRankScores / np.sum(pageRankScores)

        return pageRankScores

    def getLeftEigenVector(self, P):
        """
        Calculate the left eigenvector of the matrix P.

        Args:
            P: Matrix of the graph.

        Returns:
            Left eigenvector of the matrix P.
        """
        values, Vector = np.linalg.eig(np.array(P).T)
        left_vec = Vector[:, 0].T
        left_vec_norm = (left_vec/left_vec.sum()).real
        return left_vec_norm

    def get_scores_eigen(self, alpha = 0.1):
        """
        Calculate the PageRank scores of all the nodes in the graph using the eigenvalue decomposition of the matrix.

        Returns:
            PageRank scores of all the nodes in the graph.
        """
        # Calculating Page Rank Scores
        # P = self.graph / np.sum(self.graph, axis=0)

        M = self.graph / np.sum(self.graph, axis=0)

        M = M * (1 - alpha)
        M = M + (alpha/self.n_nodes)

        left_vec = self.getLeftEigenVector(M)
        pageRankScores = left_vec / sum(left_vec)

        return pageRankScores


