import random
from faker import Faker
from unidecode import unidecode

fake = Faker("pl_PL")

def generuj_dane():
    with open("wiadomosci.txt", "r", encoding="utf-8") as file:
        wiadomosci = file.readlines()
    
    losowa_wiadomosc = random.choice(wiadomosci).strip()
    imie_w_wiadomosci = losowa_wiadomosc.split()[-1]

    IMIE = imie_w_wiadomosci.replace(".", "")
    domeny = ["gmail.com", "onet.pl", "wp.pl", "interia.pl", "yahoo.com"]
    EMAIL = unidecode(f"{imie_w_wiadomosci.lower()}{fake.last_name().lower()}@{random.choice(domeny)}")
    TELEFON = fake.phone_number().replace("+48", "")
    
    return IMIE, EMAIL, TELEFON, losowa_wiadomosc