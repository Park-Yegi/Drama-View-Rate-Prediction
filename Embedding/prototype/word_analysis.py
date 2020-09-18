from konlpy.tag import Mecab

tokenizer = Mecab()
print(tokenizer.morphs("아버지가방에들어가신다"))