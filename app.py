from flask import Flask, render_template, request
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)

model = load_model("model.h5")
tokenizer = pickle.load(open("tokenizer.pkl", "rb"))
max_seq_len = 20  # adjust if needed

def predict_next_words(seed_text, next_words):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences(
            [token_list], maxlen=max_seq_len-1, padding='pre'
        )

        predicted = np.argmax(model.predict(token_list), axis=-1)[0]

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break

        seed_text += " " + output_word

    return seed_text

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        text = request.form["text"]
        num = int(request.form["num"])
        result = predict_next_words(text, num)

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
