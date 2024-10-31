import datetime
import threading
import asyncio
import json

import numpy


GLOBAL__numar_port_server = 9687
GLOBAL__server = None
GLOBAL__numar_date_initiale = 50
GLOBAL__date_client = []

GLOBAL__media_valori = 0
GLOBAL__deviatia_standard = 0
GLOBAL__prag_dorit = 2


def detecteazaAnomalie (valoare_repectionata):
    global GLOBAL__prag_dorit
    
    if numpy.abs(valoare_repectionata - GLOBAL__media_valori) > GLOBAL__prag_dorit * GLOBAL__deviatia_standard:
        return True
    
    return False

def stabilesteValoriStatisticeDinDateInitiale ():
    global GLOBAL__deviatia_standard
    global GLOBAL__media_valori
    global GLOBAL__date_client

    valori = [bucata_date_client['valoare'] for bucata_date_client in GLOBAL__date_client]
    GLOBAL__media_valori = numpy.mean(valori)
    GLOBAL__deviatia_standard = numpy.std(valori)

#   Adună datele de la client în mod continuu, primele *GLOBAL__numar_date_initiale*
# fiind presupuse ca fiind date corecte, urmând ca restul datelor ce sunt
# trimise de către client să fie verificate pentru anomalii
async def colecteazaDateClient (citire: asyncio.StreamReader, scriere: asyncio.StreamWriter):
    global GLOBAL__numar_date_initiale
    adresa_client = scriere.get_extra_info("peername")

    while True:
        mesaj_client = await citire.read(256)
        if (not mesaj_client):
            print("Conexiunea cu clientul", adresa_client, "a fost oprita!")
            break

        # mesaj_client_json = .decode()
        mesaj_client_decodat = json.loads(mesaj_client)

        if (GLOBAL__numar_date_initiale > 0):
            GLOBAL__numar_date_initiale -= 1

            GLOBAL__date_client.append(mesaj_client_decodat)
            print(mesaj_client_decodat['moment_timp'], "->", mesaj_client_decodat['valoare'])

            if (GLOBAL__numar_date_initiale == 0):
                print("Datele ce sunt trimise din acest moment sunt verificate, la fiecare recepționare")
                stabilesteValoriStatisticeDinDateInitiale()
        else:
            if (detecteazaAnomalie(mesaj_client_decodat['valoare']) == True):
                print("Anomalie detectata:", mesaj_client_decodat['valoare'])
                print("  Anomalia este din momentul de timp", mesaj_client_decodat['moment_timp'])
            else:
                # print(mesaj_client_decodat['moment_timp'], "->", mesaj_client_decodat['valoare'])
                GLOBAL__date_client.append(mesaj_client_decodat)


async def executaServer ():
    global GLOBAL__semnal_oprire_proce
    global GLOBAL__server

    GLOBAL__server = await asyncio.start_server(colecteazaDateClient, "0.0.0.0", GLOBAL__numar_port_server)

    print("Ascult pe portul %d" % (GLOBAL__numar_port_server))
    async with GLOBAL__server:
        await GLOBAL__server.serve_forever()


if __name__ == "__main__":
    asyncio.run(executaServer())
    