import numpy as np
import pandas as pd
from pagerank import PageRank
import matplotlib.pyplot as plt
from tqdm import tqdm
from time import time
num_nodes = list(range(5, 705, 5))
times = []

for i in tqdm(num_nodes):
    graph = np.random.randint(2, size=(i, i))
    start = time()
    pr = PageRank(graph, i)
    end = time()
    times.append(end - start)

plt.plot(num_nodes, times)
plt.show()