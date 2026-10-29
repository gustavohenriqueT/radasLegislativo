import os

import psycopg

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://radar:radar@localhost:5432/radar"
)


def conectar() -> psycopg.Connection:
    return psycopg.connect(DATABASE_URL)


def salvar_deputados(conexao: psycopg.Connection, deputados: list[dict]) -> None:
    with conexao.cursor() as cursor:
        cursor.executemany(
            """
            insert into deputados (id, nome, sigla_uf, url_foto)
            values (%(id)s, %(nome)s, %(siglaUf)s, %(urlFoto)s)
            on conflict (id) do update set
                nome = excluded.nome,
                sigla_uf = excluded.sigla_uf,
                url_foto = excluded.url_foto
            """,
            deputados,
        )


def _para_booleano(valor: int | None) -> bool | None:
    if valor is None:
        return None
    return bool(valor)


def salvar_votacoes(conexao: psycopg.Connection, votacoes: list[dict]) -> None:
    linhas = [
        {
            "id": votacao["id"],
            "data": votacao["data"],
            "descricao": votacao["descricao"],
            "aprovacao": _para_booleano(votacao["aprovacao"]),
            "id_proposicao": int(votacao["id"].split("-")[0]),
        }
        for votacao in votacoes
    ]

    with conexao.cursor() as cursor:
        cursor.executemany(
            """
            insert into votacoes (id, data, descricao, aprovacao, id_proposicao)
            values (
                %(id)s, %(data)s, %(descricao)s, %(aprovacao)s,
                (select id from proposicoes where id = %(id_proposicao)s)
            )
            on conflict (id) do update set
                descricao = excluded.descricao,
                aprovacao = excluded.aprovacao
            """,
            linhas,
        )


def salvar_votos(
    conexao: psycopg.Connection, id_votacao: str, votos: list[dict]
) -> None:
    deputados = [voto["deputado_"] for voto in votos]
    linhas = [
        {
            "id_votacao": id_votacao,
            "id_deputado": voto["deputado_"]["id"],
            "tipo_voto": voto["tipoVoto"],
            "sigla_partido": voto["deputado_"]["siglaPartido"],
        }
        for voto in votos
    ]

    with conexao.cursor() as cursor:
        cursor.executemany(
            """
            insert into deputados (id, nome, sigla_uf, url_foto)
            values (%(id)s, %(nome)s, %(siglaUf)s, %(urlFoto)s)
            on conflict (id) do nothing
            """,
            deputados,
        )
        cursor.executemany(
            """
            insert into votos (id_votacao, id_deputado, tipo_voto, sigla_partido)
            values (%(id_votacao)s, %(id_deputado)s, %(tipo_voto)s, %(sigla_partido)s)
            on conflict (id_votacao, id_deputado) do update set
                tipo_voto = excluded.tipo_voto,
                sigla_partido = excluded.sigla_partido
            """,
            linhas,
        )


def listar_ids_proposicoes(conexao: psycopg.Connection) -> set[int]:
    with conexao.cursor() as cursor:
        cursor.execute("select id from proposicoes")
        return {linha[0] for linha in cursor.fetchall()}


def salvar_proposicao(conexao: psycopg.Connection, proposicao: dict) -> None:
    with conexao.cursor() as cursor:
        cursor.execute(
            """
            insert into proposicoes (
                id, sigla_tipo, numero, ano, ementa,
                data_apresentacao, url_inteiro_teor
            )
            values (
                %(id)s, %(siglaTipo)s, %(numero)s, %(ano)s, %(ementa)s,
                %(dataApresentacao)s, %(urlInteiroTeor)s
            )
            on conflict (id) do update set
                ementa = excluded.ementa,
                url_inteiro_teor = excluded.url_inteiro_teor
            """,
            proposicao,
        )
