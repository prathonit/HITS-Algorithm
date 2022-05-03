import numpy as np

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