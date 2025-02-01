from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_links(base_url, max_page):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    links = []
    for page in range(2, max_page + 1):
        driver.get(f"{base_url}?viewType=listing&limit=72&page={page}")
        time.sleep(5)
        links += [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "a[data-cy='listing-item-link']") if a.get_attribute("href") and "/pl/oferta/" in a.get_attribute("href")]
        print(f"Pobrano linki ze strony {page}")

    driver.quit()

    with open("otodom_links.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(links))

    print(f"Zapisano {len(links)} linków do otodom_links.txt")