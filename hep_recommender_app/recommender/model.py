import numpy as np
from gensim.models import KeyedVectors


class GensimWrapper:
    """
    Wrapper around Gensim library with the basic functionalities we need, loading trained embeddings
    and predicting the most similar items
    """

    def __init__(self):
        self._model = None

    def load(self, model_path: str):
        """
        Loads trained embeddings
        """
        self._model = KeyedVectors.load_word2vec_format(model_path, binary=True)

    def most_similar(self, article: str, topn: int = 5):
        """
        Predicts most similar items
        """
        return [article[0] for article in self._model.similar_by_word(article, topn)]

    def mean_vector(self, articles: list):
        articles = [article for article in articles if article in self.vocabulary()]
        if len(articles) >= 1:
            return np.mean(self._model[articles], axis=0)
        else:
            return []

    def most_similar_by_vector(self, article, topn: int = 5):
        return [article[0] for article in self._model.similar_by_vector(article, topn)]

    def vocabulary(self):
        """
        Returns all articles which have embeddings
        """
        return [recid for recid in self._model.vocab]
