from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict, Counter
import re

app = Flask(__name__)
CORS(app)

class NGramPredictor:
    def __init__(self, n=3):
        self.n = n
        self.ngrams = defaultdict(Counter)
        self.vocab = Counter()

    def tokenize(self, text):
        return re.findall(r"\b\w+(?:'\w+)?\b", text.lower())

    def train(self, corpus):
        words = self.tokenize(corpus)
        self.vocab.update(words)
        for size in range(1, self.n + 1):
            for i in range(len(words) - size):
                context = tuple(words[i: i + size])
                next_word = words[i + size]
                self.ngrams[context][next_word] += 1

    def predict(self, text, top_k=6):
        words = self.tokenize(text)
        if not words:
            return [{"word": w, "score": round(c / max(self.vocab.values()), 3)}
                    for w, c in self.vocab.most_common(top_k)]

        suggestions = Counter()
        for size in range(min(self.n, len(words)), 0, -1):
            context = tuple(words[-size:])
            if context in self.ngrams:
                suggestions.update(self.ngrams[context])
                break

        if not suggestions:
            return [{"word": w, "score": round(c / max(self.vocab.values()), 3)}
                    for w, c in self.vocab.most_common(top_k)]

        total = sum(suggestions.values())
        return [{"word": w, "score": round(c / total, 3)}
                for w, c in suggestions.most_common(top_k)]


CORPUS = """
the quick brown fox jumps over the lazy dog
a stitch in time saves nine lives
all that glitters is not gold
the early bird catches the worm every morning
to be or not to be that is the question
the best things in life are free
actions speak louder than words
time flies when you are having fun
every cloud has a silver lining
knowledge is power and power is knowledge
the pen is mightier than the sword
life is short but art is long
great minds think alike
rome was not built in a day
the grass is always greener on the other side
practice makes perfect when you work hard
the more you learn the more you know
machine learning is a subset of artificial intelligence
natural language processing helps computers understand human language
python is a popular programming language for data science
deep learning models require large amounts of training data
neural networks can recognize patterns in complex data sets
the algorithm processes the input and produces an output
data science combines statistics mathematics and programming skills
artificial intelligence is transforming the way we work
software engineers write code to solve real world problems
the weather is nice today and the sun is shining
i want to go to the store to buy some food
she went to the park and played with her friends
he loves to read books about science and technology
"""

model = NGramPredictor(n=3)
model.train(CORPUS)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json() or {}
    text = data.get("text", "").strip()
    top_k = min(int(data.get("top_k", 6)), 10)
    return jsonify({"suggestions": model.predict(text, top_k)})


@app.route("/train", methods=["POST"])
def train():
    data = request.get_json() or {}
    corpus = data.get("corpus", "").strip()
    if not corpus:
        return jsonify({"error": "corpus is required"}), 400
    model.train(corpus)
    return jsonify({"message": "Model updated", "vocab_size": len(model.vocab)})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "vocab_size": len(model.vocab)})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
