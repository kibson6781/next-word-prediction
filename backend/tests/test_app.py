import pytest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"

def test_predict_sample(client):
    r = client.post("/predict", json={"seed_text":"machine learning","n_words":3,"mode":"sample"})
    assert r.status_code == 200
    d = r.get_json()
    assert len(d["predicted_words"]) == 3

def test_predict_beam(client):
    r = client.post("/predict", json={"seed_text":"deep learning","n_words":3,"mode":"beam"})
    assert r.status_code == 200
    assert r.get_json()["mode"] == "beam_search"

def test_missing_seed(client):
    r = client.post("/predict", json={"n_words":3})
    assert r.status_code == 400
