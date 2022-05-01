from text_index import TextIndex
from web_graph import Graph
from crawl import Crawler


class HITS:
    def __init__(self):
        self.crawler = Crawler()
        self.crawler.crawl()
        self.text_index = TextIndex()
        self.g = Graph()

    def get_root_set(self, term):
        return self.text_index.query_index(term)

    def get_base_set(self, term):
        root_set = self.get_root_set(term)
        base_set = []
        for node in root_set:
            print(base_set)
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


h = HITS()
print(h.get_base_set('spaceflight'))
