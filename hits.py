import math
from text_index import TextIndex
from web_graph import Graph
from crawl import Crawler


class HITS:
    def __init__(self):
        self.crawler = Crawler()
        self.crawler.crawl()
        self.text_index = TextIndex()
        self.g = Graph()
        self.auth = {}
        self.hub = {}
        print(self.text_index)

    def calc_hit_score(self, term, reps=10000):
        # initialize the hub and auth score for each node
        for i in range(self.g.count):
            self.auth[i] = 1.0
            self.hub[i] = 1.0
        base_set = self._get_base_set(term)
        if len(base_set) == 0:
            print("Search term not found in index")
            return
        adj_matrix = self._get_base_set_adj_matrix(base_set)
        for i in range(reps):
            self._hits_iter(base_set, adj_matrix)
        hub_auth_scores = []
        s1 = 0
        s2 = 0
        for node in base_set:
            hub_auth_scores.append((node, self.auth[node], self.hub[node]))
            s1 += self.auth[node]
            s2 += self.hub[node]
        print(s1, s2)
        return hub_auth_scores

    def _get_root_set(self, term):
        return self.text_index.query_index(term)

    def _get_base_set(self, term):
        root_set = self._get_root_set(term)
        base_set = []
        for node in root_set:
            if node in self.g.adj_out:
                for node_temp in self.g.adj_out[node]:
                    if node_temp not in base_set:
                        base_set.append(node_temp)
            if node in self.g.adj_in:
                for node_temp in self.g.adj_in[node]:
                    if node_temp not in base_set:
                        base_set.append(node_temp)
        base_set.extend(root_set)
        return base_set

    def _get_base_set_adj_matrix(self, base_set):
        adj_matrix = {'in': {}, 'out': {}}
        for edge in self.g.edges:
            if edge[0] in base_set and edge[1] in base_set:
                if edge[0] not in adj_matrix['out']:
                    adj_matrix['out'][edge[0]] = []
                if edge[1] not in adj_matrix['in']:
                    adj_matrix['in'][edge[1]] = []
                adj_matrix['out'][edge[0]].append(edge[1])
                adj_matrix['in'][edge[1]].append(edge[0])
        return adj_matrix

    def _hits_iter(self, base_set, adj_matrix):
        for node in base_set:
            self._update_auth(node, adj_matrix)
        for node in base_set:
            self._update_hub(node, adj_matrix)
        self._normalize_auth_hub(base_set)

    def _update_auth(self, node, adj_matrix):
        if node in adj_matrix['in']:
            self.auth[node] = sum(self.hub[i] for i in adj_matrix['in'][node])

    def _update_hub(self, node, adj_matrix):
        if node in adj_matrix['out']:
            self.hub[node] = sum(self.auth[i] for i in adj_matrix['out'][node])

    def _normalize_auth_hub(self, base_set):
        # auth_sum = math.sqrt(sum(self.auth[i]**2 for i in base_set))
        # hub_sum = math.sqrt(sum(self.hub[i]**2 for i in base_set))
        auth_sum = (sum(self.auth[i] for i in base_set))
        hub_sum = (sum(self.hub[i] for i in base_set))
        for node in base_set:
            self.auth[node] /= auth_sum
            self.hub[node] /= hub_sum


h = HITS()
print(h.calc_hit_score('pension'))
