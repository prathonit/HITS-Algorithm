import os
import config
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from text_index import TextIndex
from web_graph import Graph


class Crawler:
    """
    Crawler Class
    Crawls the dataset and indexes the documents.
    """
    def __init__(self):
        if os.path.exists(config.TEXT_INDEX_PATH):
            os.remove(config.TEXT_INDEX_PATH)
        self.text_index = TextIndex()
        self.g = Graph()
        self.stop_words = stopwords.words("english")
        self.ps = PorterStemmer()
        self.tokenizer = RegexpTokenizer(r"\w+")

    def crawl(self):
        """
        Crawls the dataset and build index for each document.
        :return: void
        """
        for i in range(len(self.g.web_graph.nodes)):
            doc_id = i
            doc_content = self.g.get_content(i)
            doc_content = self.pre_process(doc_content)
            self.text_index.build_index(doc_id, doc_content)
        self.text_index.save_index()

    def pre_process(self, content):
        """
        Pre-process the content of the document.
        :param content: Body of the document
        :return: Contents of the document tokenized to a list
        """
        w = self.tokenizer.tokenize(content)
        w = [x.lower() for x in w]
        w = self.remove_stopwords(self.stop_words, w)
        self.stem_words(w)
        return w

    @staticmethod
    def remove_stopwords(stop_words, words):
        """
        Removes stopwords from a list of words
        :param stop_words: list of stop words
        :param words: list of words to process
        :return: list of words
        """
        output = []
        for word in words:
            if word not in stop_words:
                output.append(word)
        return output

    def stem_words(self, words):
        """
        Stems words from a list of words.
        :param words: list of words
        :return: list of stemmed words
        """
        for i in range(len(words)):
            words[i] = self.ps.stem(words[i])


