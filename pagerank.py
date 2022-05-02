import numpy as np
from time import time

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

        # InitializeTeleportation matrix and Page Rank Scores with Zeros for all graph nodes
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
        pageRankScores = pageRankScores / sum(pageRankScores)

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

def get_input():
    """
    Reads the input from input file and returns the graph, number of nodes and number of edges.

    Returns:
        graph: Adjacency matrix of the graph.
        n_nodes: Number of nodes in the graph.
        n_edges: Number of edges in the graph.
    """
    with open("graph.txt") as f:
        for lno, line in enumerate(f):
            # print(lno, line)
            if lno == 0:
                n_nodes = int(line)
                graph = [[0 for _ in range(n_nodes)] for _ in range(n_nodes)]
            elif lno == 1:
                n_edges = int(line)
            else:
                u, v = line.split(',')
                u, v = int(u) - 1, int(v) - 1
                graph[u][v] = 1
    
    return np.array(graph), n_nodes, n_edges

def main():
    """
    Main function. Calls the get_input() and get_scores_iterative() functions and prints the PageRank scores.
    """
    graph, n_nodes, n_edges = get_input()
    start = time()
    pr = PageRank(graph, n_nodes, n_edges)
    iter_scores = pr.get_scores_iterative()
    eigen_scores = pr.get_scores_eigen()
    end = time()
    print("Iterative PageRank scores: {}".format(iter_scores))
    print("Eigen Value PageRank scores: {}".format(eigen_scores))

if __name__ == '__main__':
    main()