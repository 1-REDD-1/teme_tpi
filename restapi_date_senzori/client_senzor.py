import csv
import requests
import time

import generator_date_fisier


def citesteDateCsvGenerate ():
    fisier_csv = open("date_senzori.csv", "r")
    date_csv = fisier_csv.readlines()

    fisier_csv.close()

    cititor_date_csv = csv.reader(date_csv)
    return cititor_date_csv

def trimitePeriodicDateSenzori (cititor_date_csv):
    adresa_server = "http://192.168.12.3"

    for rand_date in cititor_date_csv:
        date_senzor_json = {
            'timestamp': rand_date[0],
            'tip': rand_date[1],
            'valoare': rand_date[2]
        }

        raspuns = requests.post(adresa_server + "/senzori", json=date_senzor_json)

        if (raspuns.status_code == 200):
            print("Datele de la senzor au fost trimise!")
        else:
            print("Nu s-a putut trimite datele de la senzor")
        
        time.sleep(5)


if __name__ == "__main__":
    generator_date_fisier.genereazaDate()

    cititor_date_csv = citesteDateCsvGenerate()
    trimitePeriodicDateSenzori(cititor_date_csv)
