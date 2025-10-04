def test_health(client):
    r = client.get("/health/live")
    assert r.status_code == 200
