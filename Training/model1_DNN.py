import os
import sys
import numpy as np
import pandas as pd
# from keras.utils import up_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Embedding.model1_embedding import embedding

def make_model(input_number, hidden_layers, output_number):
    model = Sequential()
    model.add(Dense(hidden_layers[0], activation='relu', input_shape=(input_number,), name='Hidden-1'))
    model.add(Dense(hidden_layers[1], activation='relu', name='Hidden-2'))
    # model.add(Dropout(0.2))
    model.add(Dense(output_number, activation='softmax'))
    model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    kbs_mini = embedding('../kbs_mini.csv')
    kbs_mini_shuffled = kbs_mini.sample(frac=1).reset_index(drop=True)

    y = kbs_mini_shuffled[['first_rate']]
    X = kbs_mini_shuffled[kbs_mini_shuffled.columns.difference(['first_rate'])]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False, random_state=1004)

    # print('==== y ====')
    # print(y)
    # print('==== X ====')
    # print(X)
    print('X_train size:', X_train.shape)
    print('X_test size:', X_test.shape)
    print('y_train size:', y_train.shape)
    print('y_test size:', y_test.shape)

    # print('==== X_train ====')
    # print(X_train)
    # print('==== X_test ====')
    # print(X_test)
    # print('==== y_train ====')
    # print(y_train)
    # print('==== y_test ====')
    # print(y_test)

    seq_model = make_model(12, [32, 32], 1)
    seq_model.summary()
    train_history = seq_model.fit(X_train, y_train)
    # train_history = train_history.train_history

    loss_and_metric = seq_model.evaluate(X_train, y_train)
    print ("train, loss and metric: {}".format(loss_and_metric))
    loss_and_metric = seq_model.evaluate(X_test, y_test)
    print ("test, loss and metric: {}".format(loss_and_metric))
    