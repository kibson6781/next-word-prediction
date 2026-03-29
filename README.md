# 🔮 Next Word Prediction — Bidirectional LSTM

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.15-orange?logo=tensorflow)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![React](https://img.shields.io/badge/React-18-61DAFB?logo=react)

Predict the next N words from any seed phrase using a **Bidirectional LSTM** model.  
Features temperature sampling, beam search, and step-by-step probability visualization.

---

## 🚀 Quick Start

### Option 1 — Docker (easiest)
```bash
git clone https://github.com/YOUR_USERNAME/next-word-prediction.git
cd next-word-prediction
docker compose up --build
```
- Frontend → http://localhost:3000
- Backend  → http://localhost:5000

> Model trains automatically on first boot (~2 min)

---

### Option 2 — Manual

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 Bidirectional LSTM | Forward + backward context for richer predictions |
| 🎲 Temperature Sampling | Control creativity (0.1 = safe, 2.0 = wild) |
| 🔭 Beam Search | Top-3 most coherent sentence completions |
| 📊 Step Breakdown | See candidate probabilities at every prediction step |
| 🔁 Custom Corpus | POST to `/retrain` with your own text |

---

## 📡 API

### POST /predict
```json
{
  "seed_text": "machine learning is",
  "n_words": 5,
  "temperature": 1.0,
  "top_k": 5,
  "mode": "sample"
}
```

### GET /health
Returns model status and vocabulary size.

---

## 🏗 Project Structure
```
next-word-prediction/
├── backend/
│   ├── app.py            # Flask API
│   ├── requirements.txt
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── App.js        # All React components
│   │   └── App.css       # All styles
│   └── public/
├── docker-compose.yml
└── README.md
```

---

## 📄 License
MIT License
