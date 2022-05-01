import numpy as np
from time import time

class PageRank:
    def __init__(self, graph, n_nodes, n_edges):
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

    def get_scores_iterative(self, alpha=0.85, epsilon=0.0000001):
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
    Main function. Calls the get_input() and get_scores_iterative() functions and prints the PageRank scores and time taken.
    """
    graph, n_nodes, n_edges = get_input()
    start = time()
    pr = PageRank(graph, n_nodes, n_edges)
    scores = pr.get_scores_iterative()
    end = time()
    print("PageRank scores: {} \nTime taken: {:.4f}s".format(scores, end - start))

if __name__ == '__main__':
    main()