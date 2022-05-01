import pickle
import config


class TextIndex:
    def __init__(self):
        try:
            with open(config.TEXT_INDEX_PATH, "rb") as f:
                self.text_index = pickle.load(f)
        except Exception as e:
            self.text_index = {}
            print(e)
            print("Failed to retrieve index")

    def build_index(self, document_id, content):
        for token in content:
            if token not in self.text_index:
                self.text_index[token] = []
            if len(self.text_index[token]) == 0 or self.text_index[token][-1] != document_id:
                self.text_index[token].append(document_id)

    def query_index(self, term):
        return self.text_index[term]

    def save_index(self):
        with open(config.TEXT_INDEX_PATH, "wb") as f:
            pickle.dump(self.text_index, f)
