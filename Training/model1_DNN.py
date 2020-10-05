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

def make_model():
    model = Sequential()
    model.add(Dense(32, activation='relu', input_shape=(12,)))
    model.add(Dense(32, activation='relu'))
    # model.add(Dropout(0.2))
    model.add(Dense(1))

    # model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    model.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])
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

    # k=5
    # num_val_samples = len(kbs_mini_shuffled)
    # num_epochs = 500
    # all_mae_histories = []
    # for i in range(k):
    #     print('처리 중인 폴드 #', i)
    #     val_data = X[i*num_val_samples:(i+1)*num_val_samples]
    #     val_targets = y[i*num_val_samples:(i+1)*num_val_samples]
    #     partial_train_data = np.concatenate(
    #         [X[:i*num_val_samples],
    #         X[(i+1)*num_val_samples:]],
    #     axis=0)
    #     partial_train_targets = np.concatenate(
    #         [y[:i*num_val_samples],
    #         y[(i+1)*num_val_samples:]],
    #     axis=0)


    #     seq_model = make_model()

    #     history = seq_model.fit(partial_train_data, partial_train_targets, validation_data=(val_data, val_targets),epochs=num_epochs, batch_size=1, verbose=0)
    #     mae_history = history.history['val_mean_absolute_error']
    #     all_mae_histories.append(mae_history)
    # train_history = train_history.train_history

    # average_mae_history = [np.mean([x[i] for x in all_mae_histories]) for i in range(num_epochs)]

    seq_model = make_model()
    seq_model.fit(X_train, y_train, epochs=500, batch_size=2, verbose=0)

    y_predict = seq_model.predict(X_test)
    print(y_train)
    print(y_predict)
    print(y_test)
    loss_and_metric = seq_model.evaluate(X_train, y_train)
    print ("train, loss and metric: {}".format(loss_and_metric))
    loss_and_metric = seq_model.evaluate(X_test, y_test)
    print ("test, loss and metric: {}".format(loss_and_metric))

    # import matplotlib.pyplot as plt

    # plt.plot(range(1, len(average_mae_history) + 1), average_mae_history)
    # plt.xlabel('Epochs')
    # plt.ylabel('Validation MAE')
    # plt.show()