"""
Next Word Prediction API — Flask + Bidirectional LSTM
"""

import os, json, pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

app = Flask(__name__)
CORS(app)

# ── Config ──────────────────────────────────────────
MODEL_PATH     = "models/lstm_model.h5"
TOKENIZER_PATH = "models/tokenizer.pkl"
MAX_SEQ_LEN    = 50
EMBEDDING_DIM  = 128
LSTM_UNITS     = 256
DROPOUT        = 0.3
EPOCHS         = 30
BATCH_SIZE     = 64

CORPUS = """
The quick brown fox jumps over the lazy dog near the river bank.
Machine learning is a subset of artificial intelligence that enables systems to learn.
Deep learning uses neural networks with many layers to model complex patterns in data.
Natural language processing allows computers to understand and generate human language.
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
Space exploration continues to inspire generations of scientists engineers and dreamers alike.
The internet has fundamentally changed the way people communicate collaborate and share information.
Renewable energy sources like solar and wind power are key to a sustainable future.
Artificial intelligence is transforming industries from healthcare to finance and beyond.
The brain is the most complex organ in the human body with billions of neurons.
Language is the primary means by which humans express thoughts emotions and ideas.
Mathematics is the universal language of science and the foundation of modern technology.
"""

# ── Train helpers ────────────────────────────────────
def build_sequences(tokenizer, text):
    seqs = []
    for line in text.strip().split("\n"):
        line = line.strip()
        if not line: continue
        enc = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(enc)):
            seqs.append(enc[:i+1])
    padded = pad_sequences(seqs, maxlen=MAX_SEQ_LEN, padding="pre")
    X = padded[:, :-1]
    y = tf.keras.utils.to_categorical(padded[:, -1], num_classes=len(tokenizer.word_index)+1)
    return X, y

def build_model(vocab_size):
    m = Sequential([
        Embedding(vocab_size, EMBEDDING_DIM, input_length=MAX_SEQ_LEN-1),
        Bidirectional(LSTM(LSTM_UNITS, return_sequences=True)),
        Dropout(DROPOUT),
        Bidirectional(LSTM(LSTM_UNITS // 2)),
        Dropout(DROPOUT),
        Dense(256, activation="relu"),
        Dropout(DROPOUT),
        Dense(vocab_size, activation="softmax"),
    ])
    m.compile(loss="categorical_crossentropy",
              optimizer=tf.keras.optimizers.Adam(0.001),
              metrics=["accuracy"])
    return m

def train_and_save():
    os.makedirs("models", exist_ok=True)
    tok = Tokenizer(oov_token="<OOV>")
    tok.fit_on_texts(CORPUS.strip().split("\n"))
    vocab_size = len(tok.word_index) + 1
    X, y = build_sequences(tok, CORPUS)
    model = build_model(vocab_size)
    cb = [EarlyStopping(monitor="loss", patience=5, restore_best_weights=True),
          ModelCheckpoint(MODEL_PATH, save_best_only=True, monitor="loss")]
    model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, callbacks=cb, verbose=1)
    model.save(MODEL_PATH)
    with open(TOKENIZER_PATH, "wb") as f: pickle.dump(tok, f)
    print("[INFO] Model saved.")
    return model, tok

# ── Load or train ────────────────────────────────────
if os.path.exists(MODEL_PATH) and os.path.exists(TOKENIZER_PATH):
    print("[INFO] Loading saved model...")
    model = load_model(MODEL_PATH)
    with open(TOKENIZER_PATH, "rb") as f: tokenizer = pickle.load(f)
else:
    print("[INFO] Training new model...")
    model, tokenizer = train_and_save()

vocab_size = len(tokenizer.word_index) + 1

# ── Prediction ───────────────────────────────────────
def predict_next_words(seed, n_words, temperature=1.0, top_k=5):
    result, steps = [], []
    current = seed.lower().strip()
    for step in range(n_words):
        tokens = tokenizer.texts_to_sequences([current])[0]
        tokens = pad_sequences([tokens], maxlen=MAX_SEQ_LEN-1, padding="pre")
        probs = model.predict(tokens, verbose=0)[0]
        probs = np.log(probs + 1e-10) / temperature
        probs = np.exp(probs) / np.exp(probs).sum()
        top_idx = probs.argsort()[-top_k:][::-1]
        candidates = [{"word": tokenizer.index_word.get(i,""), "probability": round(float(probs[i]*100),2)}
                      for i in top_idx if tokenizer.index_word.get(i,"") not in ("","<OOV>")]
        if not candidates: break
        top_p = np.array([c["probability"] for c in candidates])
        top_p = top_p / top_p.sum()
        chosen = candidates[np.random.choice(len(candidates), p=top_p)]["word"]
        result.append(chosen)
        steps.append({"step": step+1, "input": current, "candidates": candidates, "chosen": chosen})
        current += " " + chosen
    return {"seed": seed, "predicted_words": result,
            "full_sentence": seed + " " + " ".join(result), "steps": steps}

def beam_search(seed, n_words, beam_width=5):
    tokens = tokenizer.texts_to_sequences([seed.lower()])[0]
    beams = [{"tokens": tokens, "score": 0.0, "words": []}]
    for _ in range(n_words):
        new_beams = []
        for beam in beams:
            padded = pad_sequences([beam["tokens"]], maxlen=MAX_SEQ_LEN-1, padding="pre")
            probs = model.predict(padded, verbose=0)[0]
            for idx in probs.argsort()[-beam_width:][::-1]:
                word = tokenizer.index_word.get(idx, "")
                if not word or word == "<OOV>": continue
                new_beams.append({"tokens": beam["tokens"]+[idx],
                                  "score": beam["score"] - np.log(probs[idx]+1e-10),
                                  "words": beam["words"]+[word]})
        beams = sorted(new_beams, key=lambda x: x["score"])[:beam_width]
    return [{"sentence": seed+" "+" ".join(b["words"]), "words": b["words"],
             "score": round(b["score"],4)} for b in beams[:3]]

# ── Routes ───────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok", "vocab_size": vocab_size, "model": "Bidirectional LSTM"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    seed = data.get("seed_text","").strip()
    n    = int(data.get("n_words", 5))
    temp = float(data.get("temperature", 1.0))
    topk = int(data.get("top_k", 5))
    mode = data.get("mode", "sample")
    if not seed: return jsonify({"error": "seed_text required"}), 400
    if not 1 <= n <= 50: return jsonify({"error": "n_words must be 1-50"}), 400
    if mode == "beam":
        beams = beam_search(seed, n)
        return jsonify({"seed": seed, "mode": "beam_search",
                        "beam_results": beams,
                        "full_sentence": beams[0]["sentence"] if beams else seed})
    result = predict_next_words(seed, n, temp, topk)
    result["mode"] = "sampling"
    return jsonify(result)

@app.route("/vocab")
def vocab():
    return jsonify({"vocab_size": vocab_size,
                    "sample_words": list(tokenizer.word_index.keys())[:50]})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
