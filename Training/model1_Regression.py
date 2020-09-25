import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Embedding.model1_embedding import embedding

if __name__ == "__main__":
    kbs_mini = embedding('../kbs_mini.csv')
    kbs_mini_shuffled = kbs_mini.sample(frac=1).reset_index(drop=True)

    y = kbs_mini_shuffled[['first_rate']]
    X = kbs_mini_shuffled[kbs_mini_shuffled.columns.difference(['first_rate'])]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False, random_state=1004)

    reg = LinearRegression()
    reg.fit(X_train, y_train)
    # print('train score:', reg.score(X_train, y_train))
    y_pred = reg.predict(X_test)

    # print('X_train size:', X_train.shape)
    # print('X_test size:', X_test.shape)
    # print('y_train size:', y_train.shape)
    # print('y_test size:', y_test.shape)
    # print('y_pred size:', y_pred.shape)
    # print(y_pred)

    print(X_train.columns)
    print('Coefficients: \n', reg.coef_)
    print('Mean squared error: %.2f' % mean_squared_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print('Coefficient of determination: %.2f' % r2_score(y_test, y_pred))

    # Plot outputs
    plt.scatter(y_pred, y_test,  color='black')
    # plt.plot(X_test, y_pred, color='blue', linewidth=3)

    plt.xticks(())
    plt.yticks(())

    plt.show()

    