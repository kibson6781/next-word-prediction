"""
Basic tests for the Flask API.
Run: pytest tests/ -v
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import app only after path setup
from app import app as flask_app, predict_next_words, beam_search


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ── Health endpoint ────────────────────────────────────────
def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "ok"
    assert "vocab_size" in data


# ── Predict endpoint ───────────────────────────────────────
def test_predict_sample(client):
    payload = {
        "seed_text": "machine learning is",
        "n_words": 3,
        "temperature": 1.0,
        "top_k": 5,
        "mode": "sample",
    }
    res = client.post("/predict", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert "full_sentence" in data
    assert "predicted_words" in data
    assert len(data["predicted_words"]) == 3


def test_predict_beam(client):
    payload = {
        "seed_text": "deep learning",
        "n_words": 4,
        "mode": "beam",
    }
    res = client.post("/predict", json=payload)
    assert res.status_code == 200
    data = res.get_json()
    assert data["mode"] == "beam_search"
    assert len(data["beam_results"]) > 0


def test_predict_missing_seed(client):
    res = client.post("/predict", json={"n_words": 3})
    assert res.status_code == 400


def test_predict_invalid_nwords(client):
    res = client.post("/predict", json={"seed_text": "hello", "n_words": 100})
    assert res.status_code == 400


# ── Vocab endpoint ─────────────────────────────────────────
def test_vocab(client):
    res = client.get("/vocab")
    assert res.status_code == 200
    data = res.get_json()
    assert "vocab_size" in data
    assert isinstance(data["sample_words"], list)


# ── Utility functions ──────────────────────────────────────
def test_predict_next_words_returns_correct_count():
    result = predict_next_words("the future of", 5)
    assert len(result["predicted_words"]) == 5
    assert result["seed"] == "the future of"


def test_beam_search_returns_list():
    results = beam_search("machine learning", 3, beam_width=3)
    assert isinstance(results, list)
    assert len(results) > 0
    assert "sentence" in results[0]
    assert "score" in results[0]
