from starlette.testclient import TestClient

from fact_getter import app

client = TestClient(app)


def test_cat_fact():
    response = client.get("/cat")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_kanye_fact():
    response = client.get("/kanye")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_inspirational_quote():
    response = client.get("/inspirational")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_design_quote():
    response = client.get("/design")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_simpsons_quote():
    response = client.get("/simpsons")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_swanson_quote():
    response = client.get("/swanson")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_chuck_norris_fact():
    response = client.get("/norris")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_trump_quote():
    response = client.get("/shitty-trump")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_rand_gif():
    response = client.get("/random_gif")
    assert response.status_code == 200
    assert "fact" in response.json().keys()


def test_warmup():
    response = client.get("/_ah/warmup")
    assert response.status_code == 200
    assert response.json() == {'Response Code': '418'}
