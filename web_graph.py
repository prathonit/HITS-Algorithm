import networkx as nx
import config


class Graph:
    def __init__(self):
        self.web_graph = nx.read_gpickle(config.GRAPH_DATASET_PATH)
        self.edges = self.web_graph.edges()
        self.adj_in = {}
        self.adj_out = {}
        for edge in self.edges:
            if edge[0] not in self.adj_out:
                self.adj_out[edge[0]] = []
            if edge[1] not in self.adj_in:
                self.adj_in[edge[1]] = []
            self.adj_out[edge[0]].append(edge[1])
            self.adj_in[edge[1]].append(edge[0])

    def get_content(self, node_id):
        return self.web_graph.nodes[node_id]['page_content']