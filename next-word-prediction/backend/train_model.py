"""
Standalone Training Script — Next Word Prediction LSTM
-------------------------------------------------------
Usage:
    python train_model.py                          # train with built-in corpus
    python train_model.py --corpus my_text.txt    # train with your own corpus
    python train_model.py --epochs 50 --units 512 # custom hyperparameters

Output:
    models/lstm_model.h5     — saved Keras model
    models/tokenizer.pkl     — fitted tokenizer
    models/training_log.json — loss/accuracy history
"""

import argparse
import os
import json
import pickle
import numpy as np

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

# ─── Default corpus ───────────────────────────────────────
DEFAULT_CORPUS = """
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


# ─── Argument parsing ────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(description="Train LSTM Next-Word Prediction model")
    p.add_argument("--corpus",      type=str,   default=None,  help="Path to .txt corpus file")
    p.add_argument("--epochs",      type=int,   default=30,    help="Training epochs")
    p.add_argument("--batch_size",  type=int,   default=64,    help="Batch size")
    p.add_argument("--units",       type=int,   default=256,   help="LSTM units")
    p.add_argument("--embed_dim",   type=int,   default=128,   help="Embedding dimension")
    p.add_argument("--dropout",     type=float, default=0.3,   help="Dropout rate")
    p.add_argument("--max_seq_len", type=int,   default=50,    help="Max sequence length")
    p.add_argument("--lr",          type=float, default=0.001, help="Learning rate")
    p.add_argument("--output_dir",  type=str,   default="models", help="Output directory")
    return p.parse_args()


# ─── Data preparation ────────────────────────────────────
def prepare_data(corpus_text: str, max_seq_len: int):
    tokenizer = Tokenizer(oov_token="<OOV>", filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n')
    tokenizer.fit_on_texts(corpus_text.strip().split("\n"))
    vocab_size = len(tokenizer.word_index) + 1

    sequences = []
    for line in corpus_text.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        encoded = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(encoded)):
            sequences.append(encoded[: i + 1])

    padded = pad_sequences(sequences, maxlen=max_seq_len, padding="pre")
    X = padded[:, :-1]
    y = tf.keras.utils.to_categorical(padded[:, -1], num_classes=vocab_size)
    return X, y, tokenizer, vocab_size


# ─── Model definition ────────────────────────────────────
def build_model(vocab_size: int, embed_dim: int, units: int, dropout: float, max_seq_len: int, lr: float):
    model = Sequential([
        Embedding(vocab_size, embed_dim, input_length=max_seq_len - 1),
        Bidirectional(LSTM(units, return_sequences=True)),
        Dropout(dropout),
        Bidirectional(LSTM(units // 2)),
        Dropout(dropout),
        Dense(256, activation="relu"),
        Dropout(dropout),
        Dense(vocab_size, activation="softmax"),
    ])
    model.compile(
        loss="categorical_crossentropy",
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
        metrics=["accuracy"],
    )
    model.summary()
    return model


# ─── Training ────────────────────────────────────────────
def train(args):
    # Load corpus
    if args.corpus:
        print(f"[INFO] Loading corpus from: {args.corpus}")
        with open(args.corpus, "r", encoding="utf-8") as f:
            corpus = f.read()
    else:
        print("[INFO] Using built-in corpus")
        corpus = DEFAULT_CORPUS

    # Prepare data
    print("[INFO] Preparing data…")
    X, y, tokenizer, vocab_size = prepare_data(corpus, args.max_seq_len)
    print(f"[INFO] Vocabulary size : {vocab_size}")
    print(f"[INFO] Training samples: {len(X)}")

    # Build model
    print("[INFO] Building model…")
    model = build_model(vocab_size, args.embed_dim, args.units, args.dropout, args.max_seq_len, args.lr)

    # Output directory
    os.makedirs(args.output_dir, exist_ok=True)
    model_path = os.path.join(args.output_dir, "lstm_model.h5")
    tok_path   = os.path.join(args.output_dir, "tokenizer.pkl")
    log_path   = os.path.join(args.output_dir, "training_log.json")

    # Callbacks
    callbacks = [
        EarlyStopping(monitor="loss", patience=5, restore_best_weights=True, verbose=1),
        ModelCheckpoint(model_path, save_best_only=True, monitor="loss", verbose=1),
        ReduceLROnPlateau(monitor="loss", factor=0.5, patience=3, verbose=1),
    ]

    # Train
    print("[INFO] Training…")
    history = model.fit(
        X, y,
        epochs=args.epochs,
        batch_size=args.batch_size,
        callbacks=callbacks,
        verbose=1,
    )

    # Save tokenizer
    with open(tok_path, "wb") as f:
        pickle.dump(tokenizer, f)
    print(f"[INFO] Tokenizer saved → {tok_path}")

    # Save training log
    log = {
        "epochs_run": len(history.history["loss"]),
        "final_loss": round(history.history["loss"][-1], 4),
        "final_accuracy": round(history.history["accuracy"][-1], 4),
        "vocab_size": vocab_size,
        "config": vars(args),
    }
    with open(log_path, "w") as f:
        json.dump(log, f, indent=2)

    print(f"\n✅ Training complete!")
    print(f"   Model    → {model_path}")
    print(f"   Tokenizer → {tok_path}")
    print(f"   Log       → {log_path}")
    print(f"   Final accuracy: {log['final_accuracy']*100:.1f}%")


if __name__ == "__main__":
    args = parse_args()
    train(args)
