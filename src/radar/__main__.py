from radar.camara import buscar_deputados, buscar_votacoes, buscar_votos
from radar.organizacao import agrupar_votos
from radar.banco import conectar, salvar_deputados
from radar.camara import buscar_deputados
from radar.banco import conectar, salvar_votacoes, salvar_votos
from radar.camara import buscar_votacoes, buscar_votos

deputados = buscar_deputados("SP")
with conectar() as conexao:
    salvar_deputados(conexao, deputados)
print(f"{len(deputados)} deputados salvos")

votacoes = buscar_votacoes("2026-05-01", "2026-05-31")

with conectar() as conexao:
    salvar_votacoes(conexao, votacoes)

    for votacao in votacoes:
        votos = buscar_votos(votacao["id"])
        if votos:
            salvar_votos(conexao, votacao["id"], votos)
            print(f"{votacao['id']}: {len(votos)} votos")

votos = buscar_votos("2351506-122")
print(f"{len(votos)} votos na votação 2351506-122")

grupos = agrupar_votos(votos)
for tipo, nomes in grupos.items():
    print(f"\n{tipo} ({len(nomes)})")
    for nome in nomes:
        print(f"  {nome}")

print(grupos.keys())