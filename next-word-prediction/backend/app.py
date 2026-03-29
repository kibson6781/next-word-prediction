"""
Next Word Prediction API - Flask + LSTM (TensorFlow/Keras)
"""

import os
import json
import numpy as np
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

# TensorFlow/Keras
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

app = Flask(__name__)
CORS(app)

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
MODEL_PATH    = "models/lstm_model.h5"
TOKENIZER_PATH = "models/tokenizer.pkl"
MAX_SEQ_LEN   = 50
EMBEDDING_DIM = 128
LSTM_UNITS    = 256
DROPOUT_RATE  = 0.3
EPOCHS        = 30
BATCH_SIZE    = 64

# Sample corpus for training (expandable — swap with your own text file)
CORPUS = """
The quick brown fox jumps over the lazy dog near the river bank.
Machine learning is a subset of artificial intelligence that enables systems to learn and improve.
Deep learning uses neural networks with many layers to model complex patterns in data.
Natural language processing allows computers to understand and generate human language text.
Python is a versatile programming language widely used in data science and web development.
The future of artificial intelligence is bright with endless possibilities and innovations.
Data science combines statistics mathematics and programming to extract insights from data.
Neural networks are inspired by the biological structure of the human brain neurons.
Recurrent neural networks are particularly well suited for sequential data like text.
Long short term memory networks solve the vanishing gradient problem in deep learning.
The sun rises in the east and sets in the west every single day without fail.
Knowledge is power and education is the key to unlocking a better future for all.
Science and technology continue to transform the world in remarkable and unexpected ways.
The ocean covers more than seventy percent of the surface of the planet Earth.
Climate change is one of the greatest challenges facing humanity in the twenty first century.
Creativity and innovation drive progress and lead to groundbreaking discoveries in all fields.
The history of computing dates back to the early mechanical calculating machines of the past.
Quantum computing promises to revolutionize the way we solve complex computational problems.
Biodiversity is essential for maintaining healthy ecosystems and sustainable life on Earth.
Space exploration continues to inspire generations of scientists engineers and dreamers alike.
The internet has fundamentally changed the way people communicate collaborate and share information.
Renewable energy sources like solar and wind power are key to a sustainable future.
Artificial intelligence is transforming industries from healthcare to finance and beyond.
The brain is the most complex organ in the human body with billions of neurons.
Language is the primary means by which humans express thoughts emotions and ideas.
Mathematics is the universal language of science and the foundation of modern technology.
The stock market reflects the collective expectations of millions of investors around the world.
Philosophy asks the deepest questions about existence knowledge values reason mind and language.
Music has the power to evoke emotions and connect people across cultures and generations.
The digital revolution has changed every aspect of modern life and continues to evolve.
"""

# ─────────────────────────────────────────────
# TRAINING UTILITIES
# ─────────────────────────────────────────────
def build_training_data(tokenizer, corpus_text):
    sequences = []
    for line in corpus_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        encoded = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(encoded)):
            seq = encoded[:i + 1]
            sequences.append(seq)

    padded = pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding="pre")
    X = padded[:, :-1]
    y = padded[:, -1]
    y = tf.keras.utils.to_categorical(y, num_classes=len(tokenizer.word_index) + 1)
    return X, y


def build_model(vocab_size):
    model = Sequential([
        Embedding(vocab_size, EMBEDDING_DIM, input_length=MAX_SEQ_LEN - 1),
        Bidirectional(LSTM(LSTM_UNITS, return_sequences=True)),
        Dropout(DROPOUT_RATE),
        Bidirectional(LSTM(LSTM_UNITS // 2)),
        Dropout(DROPOUT_RATE),
        Dense(256, activation="relu"),
        Dropout(DROPOUT_RATE),
        Dense(vocab_size, activation="softmax"),
    ])
    model.compile(
        loss="categorical_crossentropy",
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        metrics=["accuracy"],
    )
    return model


def train_and_save():
    os.makedirs("models", exist_ok=True)

    tokenizer = Tokenizer(oov_token="<OOV>", filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
    tokenizer.fit_on_texts(CORPUS.strip().split("\n"))

    vocab_size = len(tokenizer.word_index) + 1
    print(f"[INFO] Vocabulary size: {vocab_size}")

    X, y = build_training_data(tokenizer, CORPUS)
    print(f"[INFO] Training samples: {len(X)}")

    model = build_model(vocab_size)
    model.summary()

    callbacks = [
        EarlyStopping(monitor="loss", patience=5, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True, monitor="loss"),
    ]

    model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=callbacks, verbose=1)

    model.save(MODEL_PATH)
    with open(TOKENIZER_PATH, "wb") as f:
        pickle.dump(tokenizer, f)

    print("[INFO] Model and tokenizer saved.")
    return model, tokenizer


# ─────────────────────────────────────────────
# LOAD OR TRAIN MODEL
# ─────────────────────────────────────────────
if os.path.exists(MODEL_PATH) and os.path.exists(TOKENIZER_PATH):
    print("[INFO] Loading existing model...")
    model = load_model(MODEL_PATH)
    with open(TOKENIZER_PATH, "rb") as f:
        tokenizer = pickle.load(f)
else:
    print("[INFO] Training new model...")
    model, tokenizer = train_and_save()

vocab_size = len(tokenizer.word_index) + 1


# ─────────────────────────────────────────────
# PREDICTION UTILITIES
# ─────────────────────────────────────────────
def predict_next_words(seed_text: str, n_words: int, temperature: float = 1.0, top_k: int = 5):
    """
    Predict `n_words` next words given `seed_text`.
    Returns the full predicted sentence and per-step top candidates.
    """
    result_words  = []
    steps_detail  = []
    current_text  = seed_text.lower().strip()

    for step in range(n_words):
        token_list = tokenizer.texts_to_sequences([current_text])[0]
        token_list = pad_sequences([token_list], maxlen=MAX_SEQ_LEN - 1, padding="pre")

        probs = model.predict(token_list, verbose=0)[0]

        # Apply temperature scaling
        probs = np.log(probs + 1e-10) / temperature
        probs = np.exp(probs)
        probs = probs / probs.sum()

        # Top-K candidates
        top_indices = probs.argsort()[-top_k:][::-1]
        candidates  = []
        for idx in top_indices:
            word = tokenizer.index_word.get(idx, "")
            if word and word != "<OOV>":
                candidates.append({"word": word, "probability": float(round(probs[idx] * 100, 2))})

        # Sample from top-K
        top_probs = np.array([c["probability"] for c in candidates])
        top_probs = top_probs / top_probs.sum()
        chosen    = np.random.choice(len(candidates), p=top_probs)
        next_word = candidates[chosen]["word"]

        result_words.append(next_word)
        steps_detail.append({
            "step": step + 1,
            "input": current_text,
            "candidates": candidates,
            "chosen": next_word,
        })
        current_text += " " + next_word

    return {
        "seed": seed_text,
        "predicted_words": result_words,
        "full_sentence": seed_text + " " + " ".join(result_words),
        "steps": steps_detail,
    }


def beam_search(seed_text: str, n_words: int, beam_width: int = 5):
    """Beam search decoding for more coherent predictions."""
    token_list = tokenizer.texts_to_sequences([seed_text.lower()])[0]
    beams = [{"tokens": token_list, "score": 0.0, "words": []}]

    for _ in range(n_words):
        new_beams = []
        for beam in beams:
            padded = pad_sequences([beam["tokens"]], maxlen=MAX_SEQ_LEN - 1, padding="pre")
            probs  = model.predict(padded, verbose=0)[0]
            top_idx = probs.argsort()[-beam_width:][::-1]
            for idx in top_idx:
                word = tokenizer.index_word.get(idx, "")
                if not word or word == "<OOV>":
                    continue
                new_beams.append({
                    "tokens": beam["tokens"] + [idx],
                    "score":  beam["score"] - np.log(probs[idx] + 1e-10),
                    "words":  beam["words"] + [word],
                })
        beams = sorted(new_beams, key=lambda x: x["score"])[:beam_width]

    results = []
    for b in beams[:3]:
        results.append({
            "sentence": seed_text + " " + " ".join(b["words"]),
            "words":    b["words"],
            "score":    round(b["score"], 4),
        })
    return results


# ─────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "vocab_size": vocab_size, "model": "Bidirectional LSTM"})


@app.route("/predict", methods=["POST"])
def predict():
    data        = request.get_json()
    seed_text   = data.get("seed_text", "").strip()
    n_words     = int(data.get("n_words", 5))
    temperature = float(data.get("temperature", 1.0))
    top_k       = int(data.get("top_k", 5))
    mode        = data.get("mode", "sample")   # "sample" | "beam"

    if not seed_text:
        return jsonify({"error": "seed_text is required"}), 400
    if not 1 <= n_words <= 50:
        return jsonify({"error": "n_words must be between 1 and 50"}), 400

    if mode == "beam":
        beams  = beam_search(seed_text, n_words, beam_width=5)
        result = {
            "seed": seed_text,
            "mode": "beam_search",
            "beam_results": beams,
            "full_sentence": beams[0]["sentence"] if beams else seed_text,
        }
    else:
        result = predict_next_words(seed_text, n_words, temperature, top_k)
        result["mode"] = "sampling"

    return jsonify(result)


@app.route("/retrain", methods=["POST"])
def retrain():
    """Endpoint to retrain with custom corpus."""
    data        = request.get_json()
    custom_text = data.get("corpus", CORPUS)
    global model, tokenizer, vocab_size

    tokenizer = Tokenizer(oov_token="<OOV>")
    tokenizer.fit_on_texts(custom_text.strip().split("\n"))
    vocab_size = len(tokenizer.word_index) + 1

    X, y   = build_training_data(tokenizer, custom_text)
    model  = build_model(vocab_size)
    cb     = [EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)]
    model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=cb, verbose=0)

    model.save(MODEL_PATH)
    with open(TOKENIZER_PATH, "wb") as f:
        pickle.dump(tokenizer, f)

    return jsonify({"status": "retrained", "vocab_size": vocab_size})


@app.route("/vocab", methods=["GET"])
def vocab():
    words = list(tokenizer.word_index.keys())[:100]
    return jsonify({"vocab_size": vocab_size, "sample_words": words})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
