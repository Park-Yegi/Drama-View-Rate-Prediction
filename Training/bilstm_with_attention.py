import pandas as pd
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
from tensorflow.keras.layers import Dense, Embedding, Bidirectional, LSTM, Concatenate, Dropout
from tensorflow.keras import Input, Model
from tensorflow.keras import optimizers
import os

df = pd.read_csv('../overview_2.csv')
df_shuffled = df.sample(frac=1).reset_index(drop=True)

# print(df)
print(df_shuffled)

X = df_shuffled.loc[:, 'overview']
y = df_shuffled.loc[:, 'label']

row_count = X.shape[0]
train_size = int(row_count*9/10)

X_train = X.iloc[:train_size]
y_train = y.iloc[:train_size]
X_test = X.iloc[train_size:]
y_test = y.iloc[train_size:]

# print(max(len(l) for l in X_train))
# 985
# print(sum(map(len, X_train))/len(X_train))
# about 163

vocab_size = 50000
max_len = 300
X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

class BahdanauAttention(tf.keras.Model):
    def __init__(self, units):
        super(BahdanauAttention, self).__init__()
        self.W1 = Dense(units)
        self.W2 = Dense(units)
        self.V = Dense(1)

    def call(self, values, query):
        hidden_with_time_axis = tf.expand_dims(query, 1)

        score = self.V(tf.nn.tanh(
            self.W1(values) + self.W2(hidden_with_time_axis)))

        attention_weights = tf.nn.softmax(score, axis=1)

        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights

sequence_input = Input(shape=(max_len,), dtype='int32')
embedded_sequences = Embedding(vocab_size, 256, input_length=max_len, mask_zero=True)(sequence_input)

lstm = Bidirectional(LSTM(128, dropout=0.3, return_sequences=True, return_state=True, recurrent_activation='relu', recurrent_initializer='glorot_uniform'))(embedded_sequences)
lstm, forward_h, forward_c, backward_h, backward_c = Bidirectional(LSTM(128, dropout=0.2, return_sequences=True, return_state=True, recurrent_activation='relu', recurrent_initializer='glorot_uniform'))(lstm)

print(lstm.shape, forward_h.shape, forward_c.shape, backward_h.shape, backward_c.shape)

# state_h = Concatenate()([forward_h, backward_h])
# state_c = Concatenate()([forward_c, backward_c])

# attention = BahdanauAttention(64)
# context_vector, attention_weights = attention(lstm, state_h)

# dense1 = Dense(20, activation='relu')(context_vector)
# dropout = Dropout(0.5)(dense1)
# output = Dense(1, activation='sigmoid')(dropout)
# model = Model(inputs=sequence_input, outputs = output)

# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# early_stoppping_callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0, patience=1, verbose=0, mode='auto')


# history = model.fit(X_train, y_train, epochs=10, batch_size = 256, validation_data=(X_test, y_test), verbose=1, callbacks=[early_stoppping_callback])

# print("\n test accuracy: %.4f" % (model.evaluate(X_test, y_test)[1]))