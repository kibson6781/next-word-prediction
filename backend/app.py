from flask import Flask, request, jsonify
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

model = load_model("model.h5")
tokenizer = pickle.load(open("tokenizer.pkl", "rb"))
max_len = 10

def predict_next(seed_text, next_words):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_len-1, padding='pre')

        predicted = np.argmax(model.predict(token_list), axis=-1)[0]

        for word, index in tokenizer.word_index.items():
            if index == predicted:
                seed_text += " " + word
                break
    return seed_text

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    text = data["text"]
    num = int(data["num"])

    result = predict_next(text, num)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
