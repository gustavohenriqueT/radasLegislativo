from radar.camara import buscar_deputados

deputados = buscar_deputados("SP")
print(f"{len(deputados)} deputados")
for dep in deputados[:5]:
    print(dep["id"], dep["nome"], dep["siglaPartido"])