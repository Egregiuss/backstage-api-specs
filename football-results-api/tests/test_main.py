from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_list_fixtures_empty():
    response = client.get("/fixtures")
    assert response.status_code == 200
    assert response.json() == []

def test_list_teams_empty():
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == []

def test_get_fixture_not_found():
    response = client.get("/fixtures/nonexistent")
    assert response.status_code == 404

def test_get_team_not_found():
    response = client.get("/teams/nonexistent")
    assert response.status_code == 404
