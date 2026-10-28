import httpx

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


def buscar_deputados(uf: str) -> list[dict]:
    resposta = httpx.get(
        f"{BASE_URL}/deputados",
        
        params={"siglaUf": uf, "ordem": "ASC", "ordenarPor": "nome", "itens": 10},
        headers={"Accept": "application/json"},
        timeout=30,
    )
    resposta.raise_for_status()
    print(resposta.json()["links"])
    return resposta.json()["dados"]