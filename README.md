# Next Word Predictor 🔮

N-gram statistical next-word prediction app.

| Layer | Technology | Hosting |
|-------|-----------|---------|
| Backend | Python · Flask | **Render** (free) |
| Frontend | React 18 | **GitHub Pages** (free) |

---

## Architecture

```
User types in browser
      ↓
GitHub Pages  (React frontend)
      ↓  POST /predict
Render.com    (Flask + n-gram model)
      ↓
JSON suggestions returned
```

---

## 🚀 Deploy in 3 steps

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "feat: next word predictor"
# create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/next-word-predictor.git
git push -u origin main
```

---

### Step 2 — Deploy backend on Render (free)

1. Go to **https://render.com** → New → **Web Service**
2. Connect your GitHub repo
3. Set these settings:

| Field | Value |
|-------|-------|
| Root directory | `backend` |
| Runtime | `Python 3` |
| Build command | `pip install -r requirements.txt` |
| Start command | `gunicorn app:app` |

4. Click **Deploy** — wait ~2 min
5. Copy your URL: `https://next-word-predictor-api.onrender.com`

> ⚠️ Free Render services sleep after 15 min of inactivity. First request may take ~30s to wake up.

---

### Step 3 — Deploy frontend to GitHub Pages

1. Edit `frontend/.env.production` — paste your Render URL:
```
REACT_APP_API_URL=https://next-word-predictor-api.onrender.com
```

2. Edit `frontend/package.json` — update `homepage`:
```json
"homepage": "https://YOUR_USERNAME.github.io/next-word-predictor"
```

3. Deploy:
```bash
cd frontend
npm install
npm run deploy
```

4. Go to your repo → **Settings → Pages** → set source to `gh-pages` branch

✅ Your app is live at: `https://YOUR_USERNAME.github.io/next-word-predictor`

---

## Local development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm start
# → http://localhost:3000
```

---

## API reference

### `POST /predict`
```json
{ "text": "the quick brown", "top_k": 6 }
```
```json
{
  "suggestions": [
    { "word": "fox", "score": 0.84 },
    { "word": "bear", "score": 0.16 }
  ]
}
```

### `POST /train`
```json
{ "corpus": "Your custom training text here." }
```

### `GET /health`
```json
{ "status": "ok", "vocab_size": 247, "ngram_contexts": 589 }
```

---

## Project structure

```
next-word-predictor/
├── backend/
│   ├── app.py              Flask API + n-gram model
│   ├── requirements.txt    flask, flask-cors, gunicorn
│   └── render.yaml         Render deploy config
├── frontend/
│   ├── src/
│   │   ├── App.js          React component
│   │   └── App.css         Styling
│   ├── .env.production     → set your Render URL here
│   ├── .env.local          → local dev URL
│   └── package.json        includes gh-pages deploy script
└── README.md
```

---

## License

MIT
