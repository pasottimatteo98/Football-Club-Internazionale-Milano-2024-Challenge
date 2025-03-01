"""
Questo script utilizza Selenium per estrarre dati dalla sezione difensiva di diverse pagine web di WhoScored e salvarli in file CSV.
Le URL delle pagine e i nomi dei file CSV sono definiti nell'elenco `urls`.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
import time
import os


# Definizione della directory dove verranno salvati i file CSV
csv_directory = "whoscored_data"
os.makedirs(csv_directory, exist_ok=True)  # Crea la directory se non esiste


urls = {

    # Napoli
    "whoscored_data_Napoli_SerieA_2022_2023": "https://it.whoscored.com/Teams/276/Archive/Italia-Napoli?stageId=21087",
    "whoscored_data_Napoli_SerieA_2023_2024": "https://it.whoscored.com/Teams/276/Show/Italia-Napoli",
    "whoscored_data_Napoli_ChampLeague_2022_2023": "https://it.whoscored.com/Teams/276/Archive/Italia-Napoli",

    # Lazio
    "whoscored_data_Lazio_SerieA_2022_2023": "https://it.whoscored.com/Teams/77/Archive/Italia-Lazio?stageId=21087",
    "whoscored_data_Lazio_SerieA_2023_2024": "https://it.whoscored.com/Teams/77/Show/Italia-Lazio",
    "whoscored_data_Lazio_EurLeague_2022_2023": "https://it.whoscored.com/Teams/77/Archive/Italia-Lazio",

    # Inter
    "whoscored_data_Inter_SerieA_2022_2023": "https://it.whoscored.com/Teams/75/Archive/Italia-Inter?stageId=21087",
    "whoscored_data_Inter_SerieA_2023_2024": "https://it.whoscored.com/Teams/75/Show/Italia-Inter",
    "whoscored_data_Inter_ChampLeague_2022_2023": "https://it.whoscored.com/Teams/75/Archive/Italia-Inter",

    # AC Milan
    "whoscored_data_Milan_SerieA_2022_2023": "https://it.whoscored.com/Teams/80/Archive/Italia-AC-Milan?stageId=21087",
    "whoscored_data_Milan_SerieA_2023_2024": "https://it.whoscored.com/Teams/80/Show/Italia-AC-Milan",
    "whoscored_data_Milan_ChampLeague_2022_2023": "https://it.whoscored.com/Teams/80/Archive/Italia-AC-Milan",

    # Atalanta
    "whoscored_data_Atalanta_SerieA_2022_2023": "https://it.whoscored.com/Teams/300/Archive/Italia-Atalanta",
    "whoscored_data_Atalanta_SerieA_2023_2024": "https://it.whoscored.com/Teams/300/Show/Italia-Atalanta",

    # Roma
    "whoscored_data_Roma_SerieA_2022_2023": "https://it.whoscored.com/Teams/84/Archive/Italia-Roma?stageId=21087",
    "whoscored_data_Roma_SerieA_2023_2024": "https://it.whoscored.com/Teams/84/Show/Italia-Roma",
    "whoscored_data_Roma_EurLeague_2022_2023": "https://it.whoscored.com/Teams/84/Archive/Italia-Roma",

    # Juventus
    "whoscored_data_Juventus_SerieA_2022_2023": "https://it.whoscored.com/Teams/87/Archive/Italia-Juventus?stageId=21087",
    "whoscored_data_Juventus_SerieA_2023_2024": "https://it.whoscored.com/Teams/87/Show/Italia-Juventus",
    "whoscored_data_Juventus_ChampLeague_2022_2023": "https://it.whoscored.com/Teams/87/Archive/Italia-Juventus",

    # Fiorentina
    "whoscored_data_Fiorentina_SerieA_2022_2023": "https://it.whoscored.com/Teams/73/Archive/Italia-Fiorentina",
    "whoscored_data_Fiorentina_SerieA_2023_2024": "https://it.whoscored.com/Teams/73/Show/Italia-Fiorentina",

    # Bologna
    "whoscored_data_Bologna_SerieA_2022_2023": "https://it.whoscored.com/Teams/71/Archive/Italia-Bologna",
    "whoscored_data_Bologna_SerieA_2023_2024": "https://it.whoscored.com/Teams/71/Show/Italia-Bologna",

    # Torino
    "whoscored_data_Torino_SerieA_2022_2023": "https://it.whoscored.com/Teams/72/Archive/Italia-Torino",
    "whoscored_data_Torino_SerieA_2023_2024": "https://it.whoscored.com/Teams/72/Show/Italia-Torino",

    # Monza
    "whoscored_data_Monza_SerieA_2022_2023": "https://it.whoscored.com/Teams/269/Archive/Italia-Monza",
    "whoscored_data_Monza_SerieA_2023_2024": "https://it.whoscored.com/Teams/269/Show/Italia-Monza",

    # Udinese
    "whoscored_data_Udinese_SerieA_2022_2023": "https://it.whoscored.com/Teams/86/Archive/Italia-Udinese",
    "whoscored_data_Udinese_SerieA_2023_2024": "https://it.whoscored.com/Teams/86/Show/Italia-Udinese",

    # Sassuolo
    "whoscored_data_Sassuolo_SerieA_2022_2023": "https://it.whoscored.com/Teams/2889/Archive/Italia-Sassuolo",
    "whoscored_data_Sassuolo_SerieA_2023_2024": "https://it.whoscored.com/Teams/2889/Show/Italia-Sassuolo",

    # Empoli
    "whoscored_data_Empoli_SerieA_2022_2023": "https://it.whoscored.com/Teams/272/Archive/Italia-Empoli",
    "whoscored_data_Empoli_SerieA_2023_2024": "https://it.whoscored.com/Teams/272/Show/Italia-Empoli",

    # Salernitana
    "whoscored_data_Salernitana_SerieA_2022_2023": "https://it.whoscored.com/Teams/143/Archive/Italia-Salernitana",
    "whoscored_data_Salernitana_SerieA_2023_2024": "https://it.whoscored.com/Teams/143/Show/Italia-Salernitana",

    # Lecce
    "whoscored_data_Lecce_SerieA_2022_2023": "https://it.whoscored.com/Teams/79/Archive/Italia-Lecce",
    "whoscored_data_Lecce_SerieA_2023_2024": "https://it.whoscored.com/Teams/79/Show/Italia-Lecce",

    # Verona
    "whoscored_data_Verona_SerieA_2022_2023": "https://it.whoscored.com/Teams/76/Archive/Italia-Verona",
    "whoscored_data_Verona_SerieA_2023_2024": "https://it.whoscored.com/Teams/76/Show/Italia-Verona",

    # Frosinone
    "whoscored_data_Frosinone_SerieA_2023_2024": "https://it.whoscored.com/Teams/2732/Show/Italia-Frosinone",

    # Genoa
    "whoscored_data_Genoa_SerieA_2023_2024": "https://it.whoscored.com/Teams/278/Show/Italia-Genoa",

    # Cagliari
    "whoscored_data_Cagliari_SerieA_2023_2024": "https://it.whoscored.com/Teams/78/Show/Italia-Cagliari",

    # Sampdoria
    "whoscored_data_Sampdoria_SerieA_2022_2023": "https://it.whoscored.com/Teams/271/Archive/Italia-Sampdoria",

    # Cremonese
    "whoscored_data_Cremonese_SerieA_2022_2023": "https://it.whoscored.com/Teams/2731/Archive/Italia-Cremonese",

    # Spezia
    "whoscored_data_Spezia_SerieA_2022_2023": "https://it.whoscored.com/Teams/1501/Archive/Italia-Spezia",


}

# Configurazione del WebDriver
webdriver_service = Service('chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
#options.add_argument('--headless')  # Se necessario, abilitare questa opzione per eseguire il browser in modalità headless
driver = webdriver.Chrome(service=webdriver_service, options=options)

# Funzione per accettare i cookie di WhoScored
def handle_whoscored_cookies(driver):
    try:
        cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[mode='primary'][size='large']")))
        cookie_button.click()
        print("Cookie WhoScored accettati.")
    except Exception as e:
        print("Bottone dei cookie WhoScored non trovato o non cliccabile.")

# Funzione per chiudere banner aggiuntivi
def close_additional_banner(driver):
    try:
        close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".webpush-swal2-close")))
        close_button.click()
        print("Banner aggiuntivo chiuso.")
    except Exception as e:
        print("Banner aggiuntivo non trovato o non cliccabile.")

# Funzione per navigare alla sezione difensiva della pagina
def navigate_to_defensive_section(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Dà tempo alla pagina di caricare dopo lo scrolling
    selected = False
    while not selected:
        try:
            defensive_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#team-squad-archive-stats-defensive']")))
            defensive_link.click()
            print("Sezione 'Difesa' selezionata con il primo selettore.")
            selected = True
        except Exception as e:
            print("Tentativo con il primo selettore fallito.")
            try:
                defensive_link_alt = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='#team-squad-stats-defensive']")))
                defensive_link_alt.click()
                print("Sezione 'Difesa' selezionata con il secondo selettore.")
                selected = True
            except Exception as e_alt:
                print("Anche il tentativo con il secondo selettore è fallito. ")
                time.sleep(2)

# Funzione per estrarre e salvare i dati difensivi
def scrape_defensive_data(url, file_name):
    driver.get(url)
    handle_whoscored_cookies(driver)
    time.sleep(3)
    close_additional_banner(driver)
    navigate_to_defensive_section(driver)
    time.sleep(5)

    all_data = []
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "statistics-table-defensive")))
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('div', id='statistics-table-defensive')
    if table:
        headers = [th.text.strip() for th in table.find_all('th')]
        all_data.append(headers)
        for row in table.find_all('tr')[1:]:
            row_data = [cell.text.strip() for cell in row.find_all('td')]
            if row_data:
                all_data.append(row_data)

    file_path = os.path.join(csv_directory, f'{file_name}.csv')
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(all_data)
    print(f"Dati salvati in '{file_name}.csv'.")

try:
    for file_name, url in urls.items():
        scrape_defensive_data(url, file_name)
finally:
    driver.quit()