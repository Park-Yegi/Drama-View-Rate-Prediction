word_fname = "./kor_words.txt"
words_set = set(['비밀의숲2','비밀의숲','새','토일','주말','이날','예고','방영','말문','드디어','넷플릭스','소감','방송','출연','공개','오후','윤미래','드라마','포스터','최근','유튜브','윤세아','앞서','인터뷰','라이프','패션','인기리','타의','랭크','시상식','첫','포인트','발매','토일극','매주','다가오','주연','추종','캐스팅','배우','하반기','한편','기대','확정','OST','활약','한식','고급','에피소드','장면','극','올해','온라인','박지연','주말극','예정','끄덕여','재회','주점','코스모','발간','신규'])


from word_eval import WordEmbeddingEvaluator
model = WordEmbeddingEvaluator("./word2vec", method="word2vec", dim=100, tokenizer_name="mecab")
# model.my_visualize_words(words_set)
model.my_visualize_between_words(words_set)