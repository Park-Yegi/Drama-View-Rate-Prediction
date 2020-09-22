import sys
import numpy as np
import scipy.stats as st
from gensim.models import Word2Vec
from sklearn.preprocessing import normalize
from konlpy.tag import Mecab
from visualize_utils import visualize_words, visualize_between_words


class WordEmbeddingEvaluator:

    def __init__(self, vecs_txt_fname, vecs_bin_fname=None, method="word2vec", dim=100, tokenizer_name="mecab"):
        self.tokenizer = Mecab()
        self.tokenizer_name = tokenizer_name
        self.dim = dim
        self.method = method
        self.dictionary, self.words, self.vecs = self.load_vectors(vecs_txt_fname, method)


    def load_vectors(self, vecs_fname, method):
        if method == "word2vec":
            model = Word2Vec.load(vecs_fname)
            words = model.wv.index2word
            vecs = model.wv.vectors
        unit_vecs = normalize(vecs, norm='l2', axis=1)
        dictionary = {}
        for word, vec in zip(words, unit_vecs):
            dictionary[word] = vec
        return dictionary, words, unit_vecs


    def get_word_vector(self, word):
        if self._is_in_vocabulary(word):
            vector = self.dictionary[word]
        else:
            vector = np.zeros(self.dim)
        return vector

    # token vector들을 lookup한 뒤 평균을 취한다
    def get_sentence_vector(self, sentence):
        tokens = self.tokenizer.morphs(sentence)
        token_vecs = []
        for token in tokens:
            token_vecs.append(self.get_word_vector(token))
        return np.mean(token_vecs, axis=0)

    def _is_in_vocabulary(self, word):
        return word in self.dictionary.keys()


    def my_visualize_words(self, words_set, palette="Viridis256"):
        words = words_set
        vecs = np.array([self.get_sentence_vector(word) for word in words])
        visualize_words(words, vecs, palette, "./words.png")

    def my_visualize_between_words(self, words_set, palette="Viridis256"):
        words = words_set
        vecs = [self.get_sentence_vector(word) for word in words]
        visualize_between_words(words, vecs, palette, "./between_words.png")