def test_enpoint_raiz(client):
    response = client.get("/health")

    assert response.json() == {"status": "ok"}