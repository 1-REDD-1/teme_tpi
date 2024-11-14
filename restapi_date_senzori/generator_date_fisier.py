import csv
import datetime
import random


def genereazaDateTemperatura (temperatura_dorita):
    interval_variatie = 1.1
    variatie = -interval_variatie + (random.random() * 2 * interval_variatie)
    valoare_generata = temperatura_dorita + variatie

    return ('temp', "%.2f" % valoare_generata)

def genereazaDateUmiditate (umiditatea_dorita):
    interval_variatie = 1.4
    variatie = -interval_variatie + (random.random() * 2 * interval_variatie)
    valoare_generata = umiditatea_dorita + variatie

    return ('umid', "%.2f" % valoare_generata)

def genereazaDate ():
    data_timp_baza = datetime.datetime.fromisoformat("2024-11-01T15:00:00")
    timestamp_curent = data_timp_baza.timestamp()
    functii_tip_senzor = [genereazaDateTemperatura, genereazaDateUmiditate]
    lista_parametrii_functii = [24.0, 49.0]

    i = 0
    with open("date_senzori.csv", "w") as fisier_date_senzori:
        scriitor_fisier_csv = csv.writer(fisier_date_senzori)
        while (i < 128):
            id_senzor = i % 2
            date_generate = functii_tip_senzor[id_senzor](lista_parametrii_functii[id_senzor])
            scriitor_fisier_csv.writerow((timestamp_curent, *date_generate))

            timestamp_curent += 5
            i += 1
    
        fisier_date_senzori.flush()
        fisier_date_senzori.close()