X_file = './corpus_mecab.txt'
Y_file = './corpus_predict.txt'

X_data = open(X_file, 'r')
Y_data = open(Y_file, 'r')

X_lines = X_data.readlines()
Y_lines = Y_data.readlines()

