import websockets
import asyncio
import json
import random

#   Variabilă globală este folosită pentru ca atunci când
# această aplicație client s-a conectat cu succes deja la
# server să nu mai facă reîncercări atunci când server-ul
# se oprește.
GLOBAL_conectat_la_server = False


# Afișează datele trimise în format JSON la consolă
def citireDateSenzor (mesaj_server):
    date_senzor = json.loads(mesaj_server)
    id_senzor = date_senzor['id_senzor']

    print(f"Datele de la senzorul {id_senzor} sunt urmatoarele:")
    print("    Valoare temperatura:", "%.2f" % date_senzor['temperatura'])
    print("    Momentul inregistrarii:", date_senzor['timpul'])


#   Construiește un mesaj JSON care cere aleator date
# de la un senzor fictiv printr-un id unic
async def creeazaCerereDateSenzori ():
    lista_id_senzori = [1, 4, 6]

    id_senzor = random.choice(lista_id_senzori)
    mesaj = {
        'id_senzor': id_senzor
    }

    return json.dumps(mesaj)

#   Se ocupă de primirea și citirea datelor de la senzori
# care sunt trimise în format JSON
async def citireMesajeServer (conexiune: websockets.WebSocketClientProtocol):
    lista_mesaje_primite = []
    numar_mesaj = 1
    async for mesaj_server in conexiune:
        if (mesaj_server == "TRIMIS"):
            print("\nDatele au fost receptionate.\n")
            break
        
        print("Mesajul numarul", numar_mesaj, "a fost primit.")

        lista_mesaje_primite.append(mesaj_server)
        numar_mesaj += 1
    
    print("*** Citire date primite ***")
    for date_senzor in lista_mesaje_primite:
        citireDateSenzor(date_senzor)
    
    print()

#   Se comunică cu server-ul constant, până când
# fie utilizatorul acestei aplicații oprește această
# aplicație prin Control-C, fie atunci când server-ul
# este oprit
async def comunicareCuServer (conexiune):
    while True:
        try:
            mesaj_cerere_date_senzori = await creeazaCerereDateSenzori()
            await conexiune.send(mesaj_cerere_date_senzori)
            await citireMesajeServer(conexiune)

            await asyncio.sleep(random.uniform(0.75, 2.00))
        except websockets.exceptions.ConnectionClosed:
            print("Server-ul a fost oprit. Se inchide aplicatia")
            break

#   Funcția de conectare la server din care se realizează
# conexiunea cu server-ul pentru cererea datelor de
# la senzori fictivi
async def conectareLaServer (adresa, numar_port):
    global GLOBAL_conectat_la_server

    url = f"ws://{adresa}:{numar_port}"

    try:
        async with websockets.connect(url) as conexiune:
            GLOBAL_conectat_la_server = True
            print("Conexiune reusita.\n")

            await comunicareCuServer(conexiune)
    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Eroare conexiune cu server: {e}")
    except OSError:
        print("Server indisponibil/inexistent.")
    except Exception as e:
        print(f"O exceptie neasteptata: {e}")
    
#   Funcția principală în care se fac încercări limitate
# de conectare la server, până când fie conexiunea
# către server a fost stabilită, fie atunci când numărul
# de încercări a depășit, cazul ulterior făcând această
# aplicație să se oprească automat
async def mainClient():
    global GLOBAL_conectat_la_server

    numar_reincercari = 1
    adresa_server = "localhost"
    numar_port_server = 9180
    numar_incercare = 1
    timp_asteptare_inainte_de_incercare = 3

    try:
        while (numar_incercare <= (numar_reincercari + 1)):
            try:
                print(f"({numar_incercare}) Se incearca conectarea la server")
                await conectareLaServer(adresa_server, numar_port_server)
            except Exception as e:
                print(f"O exceptie neasteptata: {e}")
            
            if (GLOBAL_conectat_la_server == True):
                break
            
            numar_incercare += 1

            if (numar_incercare <= (numar_reincercari + 1)):
                print(f"Astept {timp_asteptare_inainte_de_incercare} secunde")
                await asyncio.sleep(timp_asteptare_inainte_de_incercare)
    except asyncio.exceptions.CancelledError:
            print("\nSe opreste aplicatia in acest moment.")


if __name__ == "__main__":
    random.seed(462)

    asyncio.run(mainClient())