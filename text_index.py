import pickle
import config


class TextIndex:
    """
    TextIndex Class
    This class initializes a text index. It has methods to add terms to the index and also to retrieve documents.
    The index is stored and retrieved form a .pickle file to save runtime.
    """
    def __init__(self):
        try:
            with open(config.TEXT_INDEX_PATH, "rb") as f:
                self.text_index = pickle.load(f)
        except Exception as e:
            self.text_index = {}
            print(e)
            print("Failed to retrieve index")

    def build_index(self, document_id, content):
        """
        Adds words to the text index
        :param document_id: unique id of the document
        :param content: content of the document tokenized to a list
        :return: void
        """
        for token in content:
            if token not in self.text_index:
                self.text_index[token] = []
            if len(self.text_index[token]) == 0 or self.text_index[token][-1] != document_id:
                self.text_index[token].append(document_id)

    def query_index(self, term):
        """
        Queries the index for a term.
        :param term: Query term
        :return: A list of matching document ids
        """
        if term not in self.text_index:
            return []
        return self.text_index[term]

    def save_index(self):
        """
        Saves the index to a pickle file.
        :return: void
        """
        with open(config.TEXT_INDEX_PATH, "wb") as f:
            pickle.dump(self.text_index, f)
