# 🔮 NextWordAI — Advanced Next Word Prediction with Bidirectional LSTM

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-FF6F00?logo=tensorflow&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![CI](https://github.com/yourusername/next-word-prediction/actions/workflows/ci.yml/badge.svg)

**Predict the next N words from any seed phrase using a deep Bidirectional LSTM model.**  
Features sampling with temperature control, beam search decoding, step-by-step visualization, and a fully interactive dark-mode React UI.

[Demo](#demo) · [Quick Start](#quick-start) · [API Reference](#api-reference) · [Architecture](#architecture)

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Bidirectional LSTM** | Two stacked BiLSTM layers for rich contextual understanding |
| 🎲 **Temperature Sampling** | Control creativity from conservative (0.1) to wild (2.0) |
| 🔭 **Beam Search** | Deterministic decoding returning top-3 candidate sequences |
| 🎯 **Top-K Filtering** | Choose from top K candidates at each prediction step |
| 📊 **Step-by-Step Breakdown** | Visualize candidate probabilities per prediction step |
| 🔁 **Custom Corpus Training** | POST your own corpus to `/retrain` and get a fresh model |
| 🐳 **Docker Ready** | One command to spin up frontend + backend |
| 🧪 **Pytest + CI** | GitHub Actions runs tests on every push |

---

## 🖼 Demo

```
Seed:      "machine learning is"
n_words:   8
Mode:      Sampling (temp=1.0, top_k=5)

Output:    "machine learning is a subset of artificial intelligence
            that enables systems"
```

---

## 🏗 Project Structure

```
next-word-prediction/
├── backend/
│   ├── app.py               # Flask API (predict, beam search, retrain, health)
│   ├── train_model.py       # Standalone training script with argparse
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── models/              # Auto-created on first run (gitignored)
│   │   ├── lstm_model.h5
│   │   └── tokenizer.pkl
│   └── tests/
│       └── test_app.py
│
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js            # Root component + API calls
│   │   ├── App.css
│   │   ├── index.js
│   │   ├── index.css         # Design tokens (CSS variables)
│   │   └── components/
│   │       ├── Header.js/.css
│   │       ├── PredictionPanel.js/.css   # Inputs, sliders, presets
│   │       ├── ResultPanel.js/.css       # Animated sentence output
│   │       ├── StepsVisualizer.js/.css   # Per-step probability bars
│   │       ├── BeamResults.js/.css       # Beam search candidates
│   │       └── Footer.js/.css
│   ├── package.json
│   ├── Dockerfile
│   ├── nginx.conf
│   └── .env.example
│
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI pipeline
├── docker-compose.yml
└── .gitignore
```

---

## 🚀 Quick Start

### Option A — Docker (recommended)

```bash
git clone https://github.com/yourusername/next-word-prediction.git
cd next-word-prediction

docker compose up --build
```

- Frontend → http://localhost:3000  
- Backend  → http://localhost:5000

> **Note:** The backend trains the model automatically on first boot (~2 min). Subsequent starts load the saved model instantly.

---

### Option B — Local Development

#### 1. Backend (Flask + TensorFlow)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train model (optional — app.py trains automatically if no model found)
python train_model.py

# Start Flask server
python app.py
# → http://localhost:5000
```

#### 2. Frontend (React)

```bash
cd frontend

# Install dependencies
npm install

# Copy env
cp .env.example .env

# Start dev server
npm start
# → http://localhost:3000
```

---

## 🎛 Training Your Own Model

Use the standalone training script with your own text corpus:

```bash
# Train with built-in corpus
python backend/train_model.py

# Train with custom .txt file
python backend/train_model.py --corpus path/to/my_corpus.txt

# Advanced: tune hyperparameters
python backend/train_model.py \
  --corpus my_corpus.txt \
  --epochs 50 \
  --units 512 \
  --embed_dim 256 \
  --dropout 0.3 \
  --batch_size 128 \
  --lr 0.0005

# All options
python backend/train_model.py --help
```

**Corpus tips:**
- One sentence per line works best
- 500–5000 sentences gives good vocabulary coverage
- More data = better predictions (use Project Gutenberg, Wikipedia dumps, etc.)

---

## 📡 API Reference

### `GET /health`

```json
{
  "status": "ok",
  "vocab_size": 312,
  "model": "Bidirectional LSTM"
}
```

---

### `POST /predict`

```json
{
  "seed_text":   "machine learning is",
  "n_words":     5,
  "temperature": 1.0,
  "top_k":       5,
  "mode":        "sample"
}
```

**Sampling response:**
```json
{
  "seed": "machine learning is",
  "mode": "sampling",
  "predicted_words": ["a", "subset", "of", "AI", "that"],
  "full_sentence": "machine learning is a subset of AI that",
  "steps": [
    {
      "step": 1,
      "input": "machine learning is",
      "candidates": [
        { "word": "a",    "probability": 34.2 },
        { "word": "the",  "probability": 21.0 },
        ...
      ],
      "chosen": "a"
    },
    ...
  ]
}
```

**Beam search response (mode: "beam"):**
```json
{
  "seed": "machine learning",
  "mode": "beam_search",
  "full_sentence": "machine learning is a subset of artificial",
  "beam_results": [
    { "sentence": "machine learning is a subset of artificial", "score": 3.21, "words": [...] },
    { "sentence": "machine learning enables systems to learn",  "score": 3.85, "words": [...] },
    { "sentence": "machine learning and deep learning models",  "score": 4.10, "words": [...] }
  ]
}
```

---

### `POST /retrain`

Retrain the model on a custom corpus at runtime:

```bash
curl -X POST http://localhost:5000/retrain \
  -H "Content-Type: application/json" \
  -d '{"corpus": "Your first sentence.\nYour second sentence.\n..."}'
```

---

### `GET /vocab`

Returns vocabulary size and a sample of known words.

---

## 🏛 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     React Frontend                       │
│  PredictionPanel → fetch POST /predict → ResultPanel    │
│                           ↓                             │
│              StepsVisualizer / BeamResults               │
└───────────────────────────┬─────────────────────────────┘
                            │ HTTP / JSON
┌───────────────────────────▼─────────────────────────────┐
│                   Flask REST API                         │
│  /predict  →  temperature sampling  /  beam search      │
│  /retrain  →  re-fit tokenizer + train new LSTM         │
│  /health   →  status + vocab size                       │
└───────────────────────────┬─────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────┐
│               Bidirectional LSTM Model                   │
│                                                         │
│  Input tokens (padded)                                  │
│       ↓                                                 │
│  Embedding(vocab, 128)                                  │
│       ↓                                                 │
│  BiLSTM(256) → return_sequences=True                    │
│       ↓                                                 │
│  Dropout(0.3)                                           │
│       ↓                                                 │
│  BiLSTM(128)                                            │
│       ↓                                                 │
│  Dropout(0.3)                                           │
│       ↓                                                 │
│  Dense(256, relu)                                       │
│       ↓                                                 │
│  Dense(vocab_size, softmax) → probability distribution  │
└─────────────────────────────────────────────────────────┘
```

---

## 🧪 Running Tests

```bash
cd backend
pip install pytest
pytest tests/ -v
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built with ❤️ using TensorFlow · Flask · React
</div>
