from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic keys
    assert "Chess Club" in data


def test_signup_success():
    email = "unittest@example.com"
    # ensure clean state
    activities["Chess Club"]["participants"] = [p for p in activities["Chess Club"]["participants"] if p != email]

    resp = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert resp.status_code == 200
    body = resp.json()
    assert "message" in body
    assert "activity" in body
    assert email in body["activity"]["participants"]


def test_signup_not_found():
    resp = client.post("/activities/Nonexistent%20Club/signup?email=a@b.com")
    assert resp.status_code == 404


def test_signup_full():
    # create a temporary full activity
    activities["Tiny Club"] = {
        "description": "temp",
        "schedule": "now",
        "max_participants": 1,
        "participants": ["x@x.com"]
    }
    resp = client.post("/activities/Tiny%20Club/signup?email=new@x.com")
    assert resp.status_code == 400
    # cleanup
    del activities["Tiny Club"]
