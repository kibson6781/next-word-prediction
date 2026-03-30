# Next Word Predictor

Next word prediction using Python n-gram model.

- **Backend** → Python Flask → hosted on **Render**
- **Frontend** → React → hosted on **GitHub Pages**

---

## Folder structure

```
next-word-predictor/
├── backend/
│   ├── app.py               Python Flask API
│   ├── requirements.txt     Python packages
│   └── render.yaml          Render deploy config
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js           React app
│   │   ├── App.css          Styles
│   │   └── index.js
│   ├── package.json
│   └── .env.production      Put your Render URL here
├── .gitignore
└── README.md
```

---

## Step 1 — Upload to GitHub

1. Go to github.com → New repository → name it `next-word-predictor`
2. Upload all files (keep the folder structure exactly as above)
3. Commit

---

## Step 2 — Deploy backend on Render (free)

1. Go to render.com → New → Web Service
2. Connect your GitHub repo
3. Fill in:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Click Deploy
5. Copy your URL — looks like: `https://next-word-predictor-api.onrender.com`

---

## Step 3 — Deploy frontend to GitHub Pages

1. Open `frontend/.env.production` and replace the URL:
```
REACT_APP_API_URL=https://your-actual-app.onrender.com
```

2. Open `frontend/package.json` and replace the homepage:
```
"homepage": "https://YOUR_GITHUB_USERNAME.github.io/next-word-predictor"
```

3. Run these commands:
```bash
cd frontend
npm install
npm run deploy
```

4. Go to your GitHub repo → Settings → Pages → set branch to `gh-pages`

Your live site: `https://YOUR_USERNAME.github.io/next-word-predictor`

---

## Run locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```
