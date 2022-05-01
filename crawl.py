import networkx as nx
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from text_index import TextIndex
from web_graph import Graph


class Crawler:
    def __init__(self):
        self.text_index = TextIndex()
        self.g = Graph()
        self.stop_words = stopwords.words("english")
        self.ps = PorterStemmer()
        self.tokenizer = RegexpTokenizer(r"\w+")

    def crawl(self):
        for i in range(len(self.g.web_graph.nodes)):
            doc_id = i
            doc_content = self.g.get_content(i)
            doc_content = self.pre_process(doc_content)
            self.text_index.build_index(doc_id, doc_content)
        self.text_index.save_index()

    def pre_process(self, content):
        w = self.tokenizer.tokenize(content)
        w = [x.lower() for x in w]
        w = self.remove_stopwords(self.stop_words, w)
        self.stem_words(w)
        return w

    @staticmethod
    def remove_stopwords(stop_words, words):
        output = []
        for word in words:
            if word not in stop_words:
                output.append(word)
        return output

    def stem_words(self, words):
        for i in range(len(words)):
            words[i] = self.ps.stem(words[i])


