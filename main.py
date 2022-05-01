import networkx as nx

web_graph = nx.read_gpickle("data/web_graph.gpickle")
n = web_graph.nodes[0]

G = web_graph.to_undirected()

# for i in range(100):
#     print(nx.node_connected_component(G, i))
print((web_graph.edges()))
