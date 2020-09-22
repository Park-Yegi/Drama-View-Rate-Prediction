from gensim.models import Word2Vec

corpus_fname = "./corpus_mecab.txt"
model_fname = "./word2vec"

corpus= [sent.strip().split(" ") for sent in open(corpus_fname, 'r').readlines()]
model = Word2Vec(corpus)
model.save(model_fname)

model.init_sims(replace=True)
print(model.wv.most_similar("비밀의숲2", topn=70))