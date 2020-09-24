import numpy as np
import pandas as pd
from keras.utils import up_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout

def make_model(input_number, hidden_layers, output_number):
    model = Sequential()
    model.add(Dense(hidden_layers[0], activation='relu', input_shape=(input_number,), name='Hidden-1'))
    model.add(Dense(hidden_layers[1], activation='relu', name='Hidden-2'))
    model.add(Dropout(0.2))
    model.add(Dense(output_number, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model