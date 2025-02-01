import os
import random
import time
import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from multiprocessing import Process
from generate_data import generuj_dane
from get_links import get_links

def random_delay(min_time, max_time):
    time.sleep(random.uniform(min_time, max_time))

def load_links(file_path):
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Plik {file_path} nie został znaleziony.")
        return []

def save_processed_link(file_path, link):
    with open(file_path, "a") as file:
        file.write(link + "\n")

def process_links(links):
    driver = webdriver.Chrome()
    driver.maximize_window()
    actions = ActionChains(driver)
    
    try:
        accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_button.click()
        print("Ciasteczka zaakceptowane.")
    except Exception as e:
        print("Nie udało się znaleźć przycisku 'Akceptuję':", e)

    for link in links:
        try:
            IMIE, EMAIL, TELEFON, WIADOMOSC = generuj_dane()
            driver.get(link)
            print(f"Otwieram link: {link}")
            random_delay(1, 2)

            form_fields = {
                "imie": (By.CSS_SELECTOR, '[data-testid="frontend.ad.contact-form.field-name"]', IMIE),
                "email": (By.CSS_SELECTOR, '[data-testid="frontend.ad.contact-form.field-email"]', EMAIL),
                "telefon": (By.CSS_SELECTOR, '[data-testid="frontend.ad.contact-form.field-phone"]', TELEFON),
                "wiadomosc": (By.NAME, "message", WIADOMOSC),
            }

            for field, (by, selector, value) in form_fields.items():
                input_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((by, selector)))
                actions.click(input_element).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(Keys.DELETE).perform()
                input_element.clear()
                input_element.send_keys(value)
                random_delay(1, 2)

            driver.find_element(By.CSS_SELECTOR, 'button[data-cy="contact-form.submit-button"]').click()
            print(f"Wysłano wiadomość dla linku: {link}")
            save_processed_link("processed_links.txt", link)
            random_delay(1, 2)
        except Exception as e:
            print(f"Błąd podczas przetwarzania linku {link}: {e}")

    driver.quit()

def start_processing():
    links_file = "otodom_links.txt"
    all_links = load_links(links_file)
    if not all_links:
        messagebox.showerror("Błąd", "Brak linków do przetworzenia.")
        return

    split_index = len(all_links) // 2
    p1 = Process(target=process_links, args=(all_links[:split_index],))
    p2 = Process(target=process_links, args=(all_links[split_index:],))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    messagebox.showinfo("Sukces", "Przetwarzanie zakończone.")

def fetch_links():
    base_url = base_url_entry.get()
    max_page = max_page_entry.get()
    if not base_url or not max_page:
        messagebox.showerror("Błąd", "Proszę podać URL i maksymalną liczbę stron.")
        return

    try:
        max_page = int(max_page)
        get_links(base_url, max_page)
        messagebox.showinfo("Sukces", "Linki zostały pobrane.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się pobrać linków: {e}")

# Tworzenie interfejsu graficznego
root = tk.Tk()
root.title("Otodom Link Processor")

tk.Label(root, text="URL strony:").grid(row=0, column=0, padx=10, pady=10)
base_url_entry = tk.Entry(root, width=50)
base_url_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Maksymalna liczba stron:").grid(row=1, column=0, padx=10, pady=10)
max_page_entry = tk.Entry(root, width=50)
max_page_entry.grid(row=1, column=1, padx=10, pady=10)

fetch_button = tk.Button(root, text="Pobierz linki", command=fetch_links)
fetch_button.grid(row=2, column=0, columnspan=2, pady=10)

process_button = tk.Button(root, text="Przetwórz linki", command=start_processing)
process_button.grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()