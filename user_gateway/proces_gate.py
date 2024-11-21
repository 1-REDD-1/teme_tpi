import websockets
import asyncio
import random
import json
import datetime


#   Generează date prin utilizarea intervalelor predefinite
# în formatul JSON
def genereazaDate (id_senzor):
    date = {'id_senzor': id_senzor}
    lista_senzori = {
        1: 'temperatura',
        4: 'temperatura',
        6: 'temperatura'
    }

    lista_intervale_senzori = {
        1: [19.0, 22.0],
        4: [39.0, 56.0],
        6: [23.0, 29.0]
    }

    date[lista_senzori[id_senzor]] = random.uniform(*lista_intervale_senzori[id_senzor])
    date['timpul'] = datetime.datetime.now().ctime()

    return json.dumps(date)
    

#   Gestionează conexiunea continuă cu clientul care
# cere date de la senzori fictivi
async def gestionareConexiuneClient (client_websocket: websockets.WebSocketServerProtocol):
    try:
        async for date_client in client_websocket:
            mesaj_client = json.loads(date_client)
            numar_mesaje_de_trimis = random.randint(1, 4)

            print("Numarul de date de trimis catre client de la senzorul", mesaj_client['id_senzor'], "cerut:", numar_mesaje_de_trimis)
            for i in range(0, numar_mesaje_de_trimis):
                date_senzor = genereazaDate(mesaj_client['id_senzor'])
                await client_websocket.send(date_senzor)

                await asyncio.sleep(random.uniform(0.20, 1.20))
            
            await client_websocket.send("TRIMIS")
    except websockets.exceptions.ConnectionClosed:
        print("Conexiunea cu client este inchisa.")
    

#   Funcția principală de inițializare și executare
# a server-ului
async def mainServer ():
    numar_port = 9180
    adresa = "localhost"

    try:
        async with websockets.serve(gestionareConexiuneClient, adresa, numar_port) as server:
            print("Server-ul functioneaza la adresa ws://" + adresa + " pe portul " + str(numar_port))
            await server.serve_forever()
    except asyncio.exceptions.CancelledError:
        print("\nServer-ul este oprit.")

if __name__ == "__main__":
    random.seed(26794)

    asyncio.run(mainServer())