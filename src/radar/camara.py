import httpx

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"


def buscar_deputados(uf: str) -> list[dict]:
    resposta = httpx.get(
        f"{BASE_URL}/deputados",
        
        params={"siglaUf": uf, "ordem": "ASC", "ordenarPor": "nome"},
        headers={"Accept": "application/json"},
        timeout=30,
    )
    resposta.raise_for_status()
    return resposta.json()["dados"]

def buscar_votos(id_votacao: str) -> list[dict]:
    resposta = httpx.get(
        f"{BASE_URL}/votacoes/{id_votacao}/votos",
        headers={"Accept": "application/json"},
        timeout=30,
    )
    resposta.raise_for_status()
    return resposta.json()["dados"]