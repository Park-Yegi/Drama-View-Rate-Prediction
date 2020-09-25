import os
import sys
import numpy as np
import pandas as pd
import pydotplus

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.tree import export_graphviz

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Embedding.model1_embedding import embedding


if __name__ == "__main__":
    kbs_mini = embedding('../kbs_mini.csv')
    kbs_mini_shuffled = kbs_mini.sample(frac=1).reset_index(drop=True)

    y = kbs_mini_shuffled[['first_rate']]
    X = kbs_mini_shuffled[kbs_mini_shuffled.columns.difference(['first_rate'])]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False, random_state=1004)

    reg = RandomForestRegressor(max_depth=2, random_state=0)
    reg.fit(X_train, y_train.values.ravel())
    y_pred = reg.predict(X_test)
    
    print('Mean squared error: %.2f' % mean_squared_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print('Coefficient of determination: %.2f' % r2_score(y_test, y_pred))

    # for i in range(47):
    #     # print(y_test.iloc[i, ['first_rate']], ',', y_pred[i])
    #     print(y_test['first_rate'].iloc[i], ',', y_pred[i])

    dt_dot_data = export_graphviz(reg.estimators_[5], out_file=None, feature_names=X_test.columns, filled=True, rounded=True)
    dt_graph = pydotplus.graph_from_dot_data(dt_dot_data)
    image = dt_graph.create_png()