from radar.camara import buscar_votos

votos = buscar_votos("2351506-122")
print(f"{len(votos)} votos")
for voto in votos[:5]:
    deputado = voto["deputado_"]
    print(deputado["nome"], deputado["siglaPartido"], voto["tipoVoto"])

from radar.organizacao import agrupar_votos

grupos = agrupar_votos(votos)
for tipo, nomes in grupos.items():
    print(f"\n{tipo} ({len(nomes)})")
    for nome in nomes:
        print(f"  {nome}")