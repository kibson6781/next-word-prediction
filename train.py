import numpy as np
import pickle
import os

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

# Load dataset
file_path = os.path.join("data", "dataset.txt")
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

corpus = text.lower().split("\n")

# Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1

# Create sequences
input_sequences = []
for line in corpus:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        input_sequences.append(token_list[:i+1])

# Padding
max_seq_len = max(len(x) for x in input_sequences)
input_sequences = np.array(
    pad_sequences(input_sequences, maxlen=max_seq_len, padding='pre')
)

X = input_sequences[:, :-1]
y = input_sequences[:, -1]

# LSTM Model
model = Sequential()
model.add(Embedding(total_words, 50, input_length=max_seq_len-1))
model.add(LSTM(150))
model.add(Dense(total_words, activation='softmax'))

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')

print("Training model...")
model.fit(X, y, epochs=30, verbose=1)

# Save
model.save("model.h5")
pickle.dump(tokenizer, open("tokenizer.pkl", "wb"))

print("Model trained and saved!")
