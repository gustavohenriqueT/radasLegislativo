import httpx

BASE_URL = "https://dadosabertos.camara.leg.br/api/v2"
PLENARIO = 180


def _requisitar(url: str, params: dict | None = None) -> dict:
    resposta = httpx.get(
        url,
        params=params,
        headers={"Accept": "application/json"},
        timeout=30,
    )
    resposta.raise_for_status()
    return resposta.json()


def _listar(caminho: str, params: dict) -> list[dict]:
    url = f"{BASE_URL}{caminho}"
    itens = []

    while url:
        corpo = _requisitar(url, params)
        itens.extend(corpo["dados"])

        links = corpo["links"]
        url = next((link["href"] for link in links if link["rel"] == "next"), None)
        params = None # type: ignore

    return itens


def buscar_deputados(uf: str) -> list[dict]:
    return _listar(
        "/deputados",
        {"siglaUf": uf, "ordem": "ASC", "ordenarPor": "nome", "itens": 100},
    )


def buscar_votacoes(data_inicio: str, data_fim: str) -> list[dict]:
    return _listar(
        "/votacoes",
        {
            "idOrgao": PLENARIO,
            "dataInicio": data_inicio,
            "dataFim": data_fim,
            "itens": 100,
        },
    )


def buscar_votos(id_votacao: str) -> list[dict]:
    return _requisitar(f"{BASE_URL}/votacoes/{id_votacao}/votos")["dados"]