import random
import json
from faker import Faker
from unidecode import unidecode

fake = Faker("pl_PL")

def generuj_dane():
    with open("wiadomosci.txt", "r", encoding="utf-8") as file:
        wiadomosci = file.readlines()
    
    dane = []
    for wiadomosc in wiadomosci:
        losowa_wiadomosc = wiadomosc.strip()
        imie_w_wiadomosci = losowa_wiadomosc.split()[-1]

        IMIE = imie_w_wiadomosci.replace(".", "")
        domeny = ["gmail.com", "onet.pl", "wp.pl", "interia.pl", "yahoo.com"]
        EMAIL = unidecode(f"{imie_w_wiadomosci.lower()}{fake.last_name().lower()}@{random.choice(domeny)}")
        TELEFON = fake.phone_number().replace("+48", "")
        
        # Tworzymy słownik z danymi
        wynik = {
            "IMIE": IMIE,
            "EMAIL": EMAIL,
            "TELEFON": TELEFON,
            "losowa_wiadomosc": losowa_wiadomosc
        }
        
        # Dodajemy wynik do listy
        dane.append(wynik)
    
    # Zwracamy dane w formacie JSON
    return json.dumps(dane, ensure_ascii=False, indent=4)

# Zapisujemy wynik do pliku JSON
with open("wynik.json", "w", encoding="utf-8") as f:
    f.write(generuj_dane())

print("Dane zostały zapisane do wynik.json")
