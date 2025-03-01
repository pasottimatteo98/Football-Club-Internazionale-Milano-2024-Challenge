# Questo script Python utilizza Selenium e BeautifulSoup per estrarre dati da diverse pagine su Kickest.it.
# Gli URL specificati corrispondono a pagine con statistiche di giocatori di calcio per diverse stagioni e categorie.
# I dati estratti vengono salvati in file CSV corrispondenti.

import csv
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Definizione della directory dove verranno salvati i file CSV
csv_directory = "kickest_data"
os.makedirs(csv_directory, exist_ok=True)

# Elenco degli URL da visitare con i nomi dei file CSV corrispondenti
urls = {
    "kickest_data_Generale_2023_2024": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone?positions=2",
    "kickest_data_GoalTiri_2023_2024": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone?category=2&positions=2",
    "kickest_data_Passaggi_2023_2024": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone?category=3&positions=2",
    "kickest_data_AzioniDifensive_2023_2024": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone?category=4&positions=2",
    "kickest_data_Portiere_2023_2024": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone?category=5&positions=2",

    "kickest_data_Generale_2022_2023": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone/2022-2023?positions=2",
    "kickest_data_GoalTiri_2022_2023": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone/2022-2023?category=2&positions=2",
    "kickest_data_Passaggi_2022_2023": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone/2022-2023?category=3&positions=2",
    "kickest_data_AzioniDifensive_2022_2023": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone/2022-2023?category=4&positions=2",
    "kickest_data_Portiere_2022_2023": "https://www.kickest.it/it/serie-a/statistiche/giocatori/tabellone/2022-2023?category=5&positions=2",
}

# Inizializzazione del servizio WebDriver e delle opzioni del browser
webdriver_service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
#options.add_argument('--headless')
driver = webdriver.Chrome(service=webdriver_service, options=options)

# Gestione dei cookie e dei banner pubblicitari
def handle_cookies_and_banners():
    try:
        # Attendi e chiudi il banner dei cookie se presente
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".iubenda-cs-accept-btn.iubenda-cs-btn-primary")))
        cookie_button.click()
        print("Cookie accettati.")

        # Attendi 15 secondi prima di cercare e cliccare sul bottone successivo
        time.sleep(15)
        close_ad_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "adk-closing-x-desktop")))
        close_ad_button.click()
        print("Pubblicità chiusa.")

    except Exception as e:
        print("Elemento non trovato o non cliccabile.")

# Funzione per estrarre e salvare i dati da una pagina specifica
def scrape_and_save(url, file_name):
    driver.get(url)
    handle_cookies_and_banners()  # Gestisci cookie e banner per ogni nuova pagina

    all_data = []

    while True:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "statsTable")))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Estrarre l'header solo se all_data è vuoto
        if not all_data:
            table = soup.find('table', id='statsTable')
            headers = [th.text.strip() for th in table.find('thead').find_all('th')]
            all_data.append(headers)

        # Estrazione dei dati
        table = soup.find('table', id='statsTable')
        for row in table.find('tbody').find_all('tr'):
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            all_data.append(row_data)

        # Tentativo di cliccare sul "Next" e attesa per il caricamento della nuova pagina
        next_page_link = driver.find_elements(By.CSS_SELECTOR, "li.paginationjs-next:not(.disabled) a")
        if next_page_link:
            driver.execute_script("arguments[0].click();", next_page_link[0])
            time.sleep(5)  # Attesa arbitraria, considera di utilizzare WebDriverWait per elementi specifici
        else:
            break

    # Scrivere i dati in un file CSV
    file_path = os.path.join(csv_directory, f'{file_name}.csv')
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(all_data)
    print(f"Dati salvati in '{file_name}.csv'.")

try:
    for file_name, url in urls.items():
        scrape_and_save(url, file_name)
finally:
    driver.quit()
