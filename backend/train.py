import numpy as np
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

data = [
    "narendra modi is a prime minister of india",
    "virat kohli is a great cricketer",
    "elon musk is ceo of tesla",
    "india is a beautiful country",
    "artificial intelligence is the future"
]

tokenizer = Tokenizer()
tokenizer.fit_on_texts(data)
total_words = len(tokenizer.word_index) + 1

input_sequences = []
for line in data:
    token_list = tokenizer.texts_to_sequences([line])[0]
    for i in range(1, len(token_list)):
        input_sequences.append(token_list[:i+1])

max_len = max(len(x) for x in input_sequences)
input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_len, padding='pre'))

X = input_sequences[:, :-1]
y = input_sequences[:, -1]

model = Sequential([
    Embedding(total_words, 10, input_length=max_len-1),
    LSTM(100),
    Dense(total_words, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')
model.fit(X, y, epochs=200)

model.save("model.h5")
pickle.dump(tokenizer, open("tokenizer.pkl", "wb"))
