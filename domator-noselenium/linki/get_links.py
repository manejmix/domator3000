import requests

# Funkcja do pobierania danych i zapisywania ich do pliku
def fetch_and_save_data(page_start, page_end, filename):
    url_template = "{}" # zmień na adres url
    headers = {
        "accept": "*/*",
        "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\", \"Google Chrome\";v=\"132\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-nextjs-data": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
    }

    with open(filename, 'w') as file:
        # Iterowanie po stronach od 2 do 2500
        for page in range(page_start, page_end + 1):
            url = url_template.format(page)
            response = requests.get(url, headers=headers)
            
            # Logowanie pełnej odpowiedzi do konsoli
            print(f"Status code: {response.status_code}")
            print(f"Response content: {response.text[:500]}")  # Zapisuje tylko początek odpowiedzi, aby nie zalało konsoli

            if response.status_code == 200:
                try:
                    data = response.json()

                    # Zbieranie ID i URL w formacie "id, https://otodom.pl/oferta/{slug}"
                    ads = data['pageProps']['data']['searchAds']['items']
                    for ad in ads:
                        development_id = ad['id']
                        slug = ad['slug']
                        url = f"https://otodom.pl/pl/oferta/{slug}"
                        file.write(f"{development_id}, {url}\n")

                except KeyError as e:
                    print(f"Brak oczekiwanego klucza w odpowiedzi: {e}")
                    print("Pełna odpowiedź:", response.json())
            else:
                print(f"Nie udało się pobrać danych z strony {page}")

# Wywołanie funkcji dla stron od 2 do 2500
fetch_and_save_data(2, 2500, 'otodom_links.txt')
