import asyncio
import ipaddress
import math
import argparse
import json
import datetime
import random


GLOBAL__numar_port_server = 9687
GLOBAL__numar_anomalii_dorite = 30
GLOBAL__sansa_producere_anomalie = 0.06
GLOBAL__descriere_program = \
"""
    Programul client se conecteaza la un server TCP care va tine
evidenta datelor trimise si de posibile anomalii ale acestora.
"""


def formatareTimp (data_timp: datetime.datetime):
    microsecunda = data_timp.microsecond
    secunda = '0' + str(data_timp.second) if (data_timp.second < 10) else str(data_timp.second)
    minut = '0' + str(data_timp.minute) if (data_timp.minute < 10) else str(data_timp.minute)
    ora = '0' + str(data_timp.hour) if (data_timp.hour < 10) else str(data_timp.hour)

    ziua = '0' + str(data_timp.day) if (data_timp.day < 10) else str(data_timp.day)
    luna = '0' + str(data_timp.month) if (data_timp.month < 10) else str(data_timp.month)
    anul = data_timp.year

    timp_formatat = "%s-%s-%s %s:%s:%s:%s" % (anul, luna, ziua, ora, minut, secunda, microsecunda)
    return timp_formatat

#   Generează un număr conform funcției date, dar cu anumite
# anomalii care sunt introduse în rezultat în mod aleator
def genereazaNumar (x):
    global GLOBAL__numar_anomalii_dorite
    global GLOBAL__sansa_producere_anomalie

    esinx = math.e ** (-math.sin(x))
    rezultat = abs(math.sin(x)) * esinx

    if ((random.random() < GLOBAL__sansa_producere_anomalie) and (GLOBAL__numar_anomalii_dorite != 0)):
        rezultat = rezultat * 21

        print("ANOMALIE INTRODUSA!  -> ", rezultat)
        GLOBAL__numar_anomalii_dorite -= 1
    
    return rezultat

async def comunicaDateCuServer (adresa_ip_server: ipaddress.IPv4Address):
    global GLOBAL__numar_port_server

    citire, scriere = await asyncio.open_connection(format(adresa_ip_server), GLOBAL__numar_port_server)

    print("Am realizat conexiunea cu server-ul", format(adresa_ip_server))

    x = 0
    while True:
        mesaj = {
            'moment_timp': formatareTimp(datetime.datetime.now()),
            'valoare': genereazaNumar(x)
        }

        mesaj_json = json.dumps(mesaj)

        scriere.write(mesaj_json.encode())
        await scriere.drain()

        await asyncio.sleep(0.15)
        x += 0.33
        print(mesaj_json)


def creeazaInterfataLinieDeComanda ():
    parsator_comenzi = argparse.ArgumentParser(
        prog="Tema cu asyncio, anomalii \"Client - Server (asyncio)\"",
        description=GLOBAL__descriere_program
    )

    parsator_comenzi.add_argument('-s', '--server', required=True, dest="server", metavar="Adresa IPv4")

    argumente = parsator_comenzi.parse_args()
    return argumente

def proceseazaArgumente (argumente: argparse.Namespace):
    adresa_ip_server = ipaddress.ip_address(argumente.server)

    return adresa_ip_server


if __name__ == "__main__":
    argumente = creeazaInterfataLinieDeComanda()
    adresa_ip_server = proceseazaArgumente(argumente)

    asyncio.run(comunicaDateCuServer(adresa_ip_server))