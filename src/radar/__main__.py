import argparse

from radar.coleta import coletar_periodo

parser = argparse.ArgumentParser(description="Coleta votações do Plenário da Câmara")
parser.add_argument("inicio", help="data inicial no formato AAAA-MM-DD")
parser.add_argument("fim", help="data final no formato AAAA-MM-DD")
args = parser.parse_args()

coletar_periodo(args.inicio, args.fim)
