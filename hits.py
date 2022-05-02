import math
from text_index import TextIndex
from web_graph import Graph
from crawl import Crawler


class HITS:
    """
    HITS Class
    Implements the HITS algorithm
    """
    def __init__(self):
        self.crawler = Crawler()
        self.crawler.crawl()
        self.text_index = TextIndex()
        self.g = Graph()
        self.auth = {}
        self.hub = {}

    def calc_hit_score(self, term, reps=10000):
        """
        Calculates the hub and auth score for the base set of given query term.
        :param term:
        :param reps:
        :return:
        """
        # initialize the hub and auth score for each node
        for i in range(self.g.count):
            self.auth[i] = 1.0
            self.hub[i] = 1.0
        root_set = self._get_root_set(term)
        base_set = self._get_base_set(term)
        if len(base_set) == 0:
            print(root_set)
            print(base_set)
            print("Search term not found in index")
            return
        adj_matrix = self._get_base_set_adj_matrix(base_set)
        for i in range(reps):
            print(i)
            prev_auth = self.auth.copy()
            prev_hub = self.hub.copy()
            self._hits_iter(base_set, adj_matrix)
            diff = 0.00001
            flag = 1
            for j in range(len(self.auth)):
                if abs(self.auth[j] - prev_auth[j]) > diff:
                    flag = 0
                    break
            for j in range(len(self.hub)):
                if abs(self.hub[j] - prev_hub[j]) > diff:
                    flag = 0
                    break
            if flag:
                break
        hub_auth_scores = []
        for node in base_set:
            hub_auth_scores.append([node, self.auth[node], self.hub[node]])
        return {
            'scores': hub_auth_scores,
            'root_set': root_set,
            'base_set': base_set
        }

    def _get_root_set(self, term):
        """
        Returns the root set for a given search term
        :param term: Search term
        :return: List of documents ids
        """
        return self.text_index.query_index(term)

    def _get_base_set(self, term):
        """
        Returns the base set for a given search term
        :param term: Search term
        :return: List of document ids
        """
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
        """
        Get the adjacency matrix for the base set
        :param base_set: List of document ids in the base set
        :return: Adjacency matrix
        """
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
        """
        Updates the auth and hub scores
        :param base_set: List of document ids in the base set
        :param adj_matrix: Adj matrix of the nodes in base set
        :return: void
        """
        for node in base_set:
            self._update_auth(node, adj_matrix)
        for node in base_set:
            self._update_hub(node, adj_matrix)
        self._normalize_auth_hub(base_set)

    def _update_auth(self, node, adj_matrix):
        """
        Updates the auth score of documents in base set
        :param node: Web graph node
        :param adj_matrix: Adj Matrix for the base set
        :return: void
        """
        if node in adj_matrix['in']:
            self.auth[node] = sum(self.hub[i] for i in adj_matrix['in'][node])

    def _update_hub(self, node, adj_matrix):
        """
        Updates the hub score of documents in base set
        :param node: Web graph node
        :param adj_matrix: Adj Matrix for the base set
        :return: void
        """
        if node in adj_matrix['out']:
            self.hub[node] = sum(self.auth[i] for i in adj_matrix['out'][node])

    def _normalize_auth_hub(self, base_set):
        """
        Normalizes the hub and auth scores.
        :param base_set: List of document ids in the base set.
        :return: void
        """
        auth_sum = (sum(self.auth[i] for i in base_set))
        hub_sum = (sum(self.hub[i] for i in base_set))
        for node in base_set:
            self.auth[node] /= auth_sum
            self.hub[node] /= hub_sum


