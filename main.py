from time import time
from utils import get_input
from pagerank import PageRank
import numpy as np

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
    print("PageRank scores: {}".format(iter_scores))
    # print("PageRank scores: {}".format(iter_scores))

if __name__ == '__main__':
    main()