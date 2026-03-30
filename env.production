from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict, Counter
import re
import json

app = Flask(__name__)
CORS(app)

# ── N-gram model ──────────────────────────────────────────────────────────────

class NGramPredictor:
    def __init__(self, n=3):
        self.n = n                          # max n-gram size
        self.ngrams = defaultdict(Counter)  # context → {next_word: count}
        self.vocab = Counter()

    def tokenize(self, text: str) -> list[str]:
        return re.findall(r"\b\w+(?:'\w+)?\b", text.lower())

    def train(self, corpus: str):
        words = self.tokenize(corpus)
        self.vocab.update(words)
        for size in range(1, self.n + 1):
            for i in range(len(words) - size):
                context = tuple(words[i : i + size])
                next_word = words[i + size]
                self.ngrams[context][next_word] += 1

    def predict(self, text: str, top_k: int = 6) -> list[dict]:
        words = self.tokenize(text)
        if not words:
            # Return most common words from vocab
            return [{"word": w, "score": round(c / max(self.vocab.values()), 3)}
                    for w, c in self.vocab.most_common(top_k)]

        suggestions = Counter()
        # Try longest context first, fall back to shorter
        for size in range(min(self.n, len(words)), 0, -1):
            context = tuple(words[-size:])
            if context in self.ngrams:
                suggestions.update(self.ngrams[context])
                break  # use the most specific context found

        if not suggestions:
            return [{"word": w, "score": round(c / max(self.vocab.values()), 3)}
                    for w, c in self.vocab.most_common(top_k)]

        total = sum(suggestions.values())
        return [
            {"word": w, "score": round(c / total, 3)}
            for w, c in suggestions.most_common(top_k)
        ]


# ── Seed corpus ───────────────────────────────────────────────────────────────

SEED_CORPUS = """
The quick brown fox jumps over the lazy dog.
A stitch in time saves nine lives.
All that glitters is not gold but silver.
The early bird catches the worm every morning.
To be or not to be that is the question.
She sells seashells by the seashore down south.
The best things in life are free to everyone.
Actions speak louder than words in every situation.
Time flies when you are having fun with friends.
Every cloud has a silver lining in the end.
Knowledge is power and power is knowledge shared freely.
The pen is mightier than the sword in battle.
Life is short but art is long and beautiful.
Great minds think alike and fools seldom differ greatly.
Rome was not built in a single day or night.
Where there is smoke there is fire burning bright.
The grass is always greener on the other side.
A picture is worth a thousand beautiful words always.
You cannot judge a book by its colorful cover.
Practice makes perfect when you work hard every day.
The more you learn the more you know about everything.
In the beginning there was light and it was good.
People who live in glass houses should not throw stones.
The road to hell is paved with good intentions always.
Two heads are better than one when solving hard problems.
The customer is always right even when they are wrong.
Better safe than sorry is a good rule to follow.
Curiosity killed the cat but satisfaction brought it back again.
Every dog has its day in the warm summer sun.
The squeaky wheel gets the grease and the attention needed.
Machine learning is a subset of artificial intelligence today.
Natural language processing helps computers understand human language patterns.
Python is a popular programming language for data science projects.
Deep learning models require large amounts of training data always.
Neural networks can recognize patterns in complex data sets easily.
The algorithm processes the input and produces an output quickly.
Data science combines statistics mathematics and programming skills together nicely.
The model was trained on a large corpus of text.
Artificial intelligence is transforming the way we work and live.
Software engineers write code to solve real world problems efficiently.
"""

model = NGramPredictor(n=3)
model.train(SEED_CORPUS)

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()
    top_k = min(int(data.get("top_k", 6)), 10)
    suggestions = model.predict(text, top_k=top_k)
    return jsonify({"input": text, "suggestions": suggestions})


@app.route("/train", methods=["POST"])
def train():
    """Extend the model with user-supplied text."""
    data = request.get_json(silent=True) or {}
    corpus = data.get("corpus", "").strip()
    if not corpus:
        return jsonify({"error": "corpus field is required"}), 400
    model.train(corpus)
    return jsonify({"message": "Model updated", "vocab_size": len(model.vocab)})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "vocab_size": len(model.vocab), "ngram_contexts": len(model.ngrams)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
