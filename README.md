# domator3000

Aplikacja pozwala przyśpieszyć poszukiwanie mieszkania poprzez automatyzacje zapytań na ogłoszenia. W pierwszej kolejności pobieramy wklejamy taki link, wpisujemy ile chcemy pobrać stron. Pobieramy i klikamy przetwórz. Formularz automatycznie się uzupełni i wyślę, na dodatek w pliku wiadomosci.txt możemy dodać własną customową wiadomość. Skrypt wybiera losowo. 

## Funkcje

- **Pobieranie linków**: Aplikacja pozwala na pobranie linków z podanej strony Otodom, z uwzględnieniem maksymalnej liczby stron do przeszukania.
- **Przetwarzanie linków**: Pobrane linki są automatycznie przetwarzane poprzez wypełnianie formularzy kontaktowych na stronach ofert.

## Wymagania

- Python 3.8+
- Zainstalowane zależności z pliku `requirements.txt`

## Instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/manejmix/domator3000.git
   cd domator3000
    python main.py
    wklej link np; https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/mazowieckie/warszawa/warszawa/warszawa
    podaj max_pages jakie chcesz przetworzyć
    śmigaj
   ```


## Wersja no-selenium
   ```
   sudo apt update
   sudo apt install nodejs npm
   npm install node-fetch
   git clone https://github.com/manejmix/domator3000.git
   node wyslij.js
   ```

   
## Jałmużna
[LINK](https://buycoffee.to/manejmix)


         
