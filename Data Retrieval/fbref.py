# Questo script Python utilizza Selenium e BeautifulSoup per estrarre dati dai giocatori di calcio su FBref.
# In particolare, cerca giocatori difensori presenti in file CSV, cerca i loro dati su FBref estraendo diverse tabelle
# di statistiche e salva i dati in file CSV separati. Se i dati di un giocatore sono già presenti, salta il processo di ricerca
# e estrazione. Infine, salva l'elenco dei giocatori non trovati in un file .txt.

import csv
import os
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Legge i nomi dei difensori da file CSV
def read_defenders_from_csv(file_path):
    defenders = []
    with open(file_path, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Salta l'intestazione
        for row in reader:
            defenders.append(row[1])  # Nome del difensore nella seconda colonna
    return defenders

# Formattazione del nome del giocatore per l'utilizzo come nome di directory
def format_player_name(player_name):
    return player_name.replace(' ', '_').replace('.', '_')

# Crea una directory per il giocatore se non esiste
def create_player_directory(player_name):
    directory_path = os.path.join('fbref_data', format_player_name(player_name))
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    return directory_path

# Controlla se i dati del giocatore sono già presenti
def player_data_already_exists(player_name):
    directory_path = os.path.join('fbref_data', format_player_name(player_name))
    return os.path.exists(directory_path) and len(os.listdir(directory_path)) > 0

# Accetta i cookies se presenti
def accept_cookies():
    try:
        agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[mode='primary'][size='large']"))
        )
        agree_button.click()
    except Exception:
        pass

# Chiude eventuali popup
def close_popup():
    try:
        close_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "modal-close"))
        )
        close_button.click()
        print("Popup chiuso.")
    except TimeoutException:
        print("Nessun popup da chiudere.")

# Estrae e salva i dati da una tabella specifica
def extract_and_save_table_data(table_id, player_name):
    directory_path = create_player_directory(player_name)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, table_id)))
    except TimeoutException:
        print(f"Table {table_names[table_id]} not found for {player_name}.")
        return
    html = driver.find_element(By.ID, table_id).get_attribute('outerHTML')
    soup = BeautifulSoup(html, 'html.parser')
    headers = [th.text.strip() for th in soup.find_all('th')]
    rows = [[ele.text.strip() for ele in tr.find_all(['td', 'th'])] for tr in soup.find_all('tr')]
    file_name = os.path.join(directory_path, f"{format_player_name(player_name)}_{table_names[table_id]}.csv")
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Data saved for {player_name} - {table_names[table_id]}.")

# Effettua la ricerca e selezione del giocatore su FBref
def search_and_select_player(player_name):
    if player_data_already_exists(player_name):
        print(f"Dati già presenti per {player_name}, salto il giocatore.")
        return True

    driver.get("https://fbref.com/it/")
    accept_cookies()
    close_popup()
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='search'].ac-input"))
    )
    search_box.clear()
    search_box.send_keys(player_name)
    time.sleep(5)

    try:
        all_suggestions = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.ac-suggestion"))
        )
        if all_suggestions:
            driver.execute_script("arguments[0].click();", all_suggestions[0])
            return False
        else:
            print(f"Nessun suggerimento trovato per {player_name}.")
            players_not_found.append(player_name)
            return True
    except TimeoutException:
        print(f"Il giocatore {player_name} non è stato trovato.")
        players_not_found.append(player_name)
        return True

# Esegue lo scraping dei dati del giocatore
def scrape_player_data(player_name):
    time.sleep(5)
    for table_id in table_names:
        extract_and_save_table_data(table_id, player_name)

# Salva l'elenco dei giocatori non trovati
def save_players_not_found():
    if players_not_found:
        with open(os.path.join('fbref_data', 'players_not_found.txt'), 'w', encoding='utf-8') as f:
            for player in players_not_found:
                f.write(f"{player}\n")
        print("Elenco dei giocatori non trovati salvato in players_not_found.txt.")

# Inizializzazione delle variabili e dei servizi
defenders_2022_2023 = read_defenders_from_csv('kickest_data/kickest_data_AzioniDifensive_2022_2023.csv')
defenders_2023_2024 = read_defenders_from_csv('kickest_data/kickest_data_AzioniDifensive_2023_2024.csv')
players = list(set(defenders_2022_2023 + defenders_2023_2024))
players = sorted(players)

webdriver_service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=webdriver_service)

# Mappatura dei nomi delle tabelle FBref con i loro nomi
table_names = {
    "stats_passing_dom_lg": "Passaggi",
    "stats_passing_types_dom_lg": "TipoPassaggi",
    "stats_gca_dom_lg": "CreazioneGolTiri",
    "stats_defense_dom_lg": "AzioniDifensive"
}

# Inizializzazione dell'elenco dei giocatori non trovati
players_not_found = []

try:
    for player in players:
        if not search_and_select_player(player):
            scrape_player_data(player)
finally:
    driver.quit()
    save_players_not_found()
