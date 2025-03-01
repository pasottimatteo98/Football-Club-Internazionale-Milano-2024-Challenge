# Questo script aggrega dati statistici di giocatori di calcio provenienti da diverse competizioni e stagioni per diverse squadre di Serie A.
# Per ciascuna squadra, carica i dati da file CSV, li pulisce e li aggrega calcolando la media delle statistiche per ogni giocatore su tutte le competizioni e stagioni.
# Infine, i dati aggregati vengono salvati in un file CSV chiamato "whoscored_data_cleaned.csv".

import pandas as pd
import os
import re

nomi_squadre = [
    "Atalanta", "Bologna", "Cagliari", "Cremonese", "Empoli", "Fiorentina", "Frosinone",
    "Genoa", "Inter", "Juventus", "Lazio", "Lecce", "Milan", "Monza",
    "Napoli", "Roma", "Salernitana", "Sampdoria", "Sassuolo", "Spezia",
    "Torino", "Udinese", "Verona"
]

def clean_player_name(player):
    cleaned_name = re.sub(r"^\d+", "", player)
    cleaned_name = re.sub(r",.*", "", cleaned_name)
    cleaned_name = re.sub(r"\d+$", "", cleaned_name)
    return cleaned_name.strip()

def load_and_clean_data(squadra, competizione, anno, base_path):
    file_path = f"{base_path}/whoscored_data_{squadra}_{competizione}_{anno}.csv"
    if os.path.exists(file_path):
        temp_df = pd.read_csv(file_path)
        temp_df['Nome_Originale'] = temp_df['Giocatore']
        temp_df['Giocatore_Pulito'] = temp_df['Giocatore'].apply(clean_player_name)
        temp_df['Competizione'] = competizione
        temp_df['Squadra'] = squadra[:3].upper()
        return temp_df
    return pd.DataFrame()

def aggregate_data(dfs):
    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        combined['Giocatore'] = combined['Giocatore_Pulito']
        combined.drop(columns=['Giocatore_Pulito', 'Nome_Originale'], inplace=True)

        numeric_cols = ['Cont', 'Inter', 'Falli', 'Fuorig', 'Spaz', 'Drib', 'Respinte', 'Autogol', 'Rating']
        for col in numeric_cols:
            combined[col] = pd.to_numeric(combined[col], errors='coerce')
        combined.fillna(0, inplace=True)

        aggregated = combined.groupby('Giocatore').agg({col: 'mean' for col in numeric_cols}).reset_index()
        aggregated[numeric_cols] = aggregated[numeric_cols].round(2)
        return aggregated
    else:
        return pd.DataFrame()

def aggregate_team_data(squadra, base_path="../Data Retrieval/whoscored_data"):
    competizioni_anni = [('SerieA', '2022_2023'), ('ChampLeague', '2023_2024'), ('EurLeague', '2023_2024')]
    dfs = [load_and_clean_data(squadra, comp, anno, base_path) for comp, anno in competizioni_anni]
    return aggregate_data([df for df in dfs if not df.empty])

base_path = "../../Data Retrieval/whoscored_data"
dfs_aggregati = [aggregate_team_data(squadra, base_path) for squadra in nomi_squadre]
final_df = pd.concat(dfs_aggregati, ignore_index=True) if dfs_aggregati else pd.DataFrame()

if not final_df.empty:
    final_df.to_csv('whoscored_data_cleaned.csv', index=False)
    print("Dati salvati correttamente nel file 'whoscored_data_cleaned.csv'.")
else:
    print("Nessun dato da salvare.")
