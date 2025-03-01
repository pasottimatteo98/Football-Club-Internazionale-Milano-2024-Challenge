"""
Questo script si occupa di elaborare e aggregare dati provenienti da file CSV contenenti statistiche di giocatori di calcio,
ottenuti dal sito web FBRef. Il processo avviene in tre fasi:

1. Lettura e filtri dei dati:
   - I dati vengono letti da file CSV e filtrati per stagione, rimuovendo le colonne non necessarie.
   - I nomi dei giocatori vengono corretti seguendo alcune regole specifiche.

2. Unione e aggregazione dei file CSV:
   - Vengono cercate tutte le sottodirectory in una directory principale.
   - Per ogni sottodirectory, vengono letti i file CSV, filtrati e uniti in un unico DataFrame.
   - I dati aggregati vengono salvati in un nuovo file CSV per ogni sottodirectory.

3. Pulizia finale e aggregazione:
   - I file CSV aggregati vengono letti e i dati vengono aggregati per giocatore, calcolando le medie delle statistiche.
   - I dati vengono puliti eliminando le righe contenenti valori mancanti.
   - Il risultato finale viene salvato in un nuovo file CSV.

Le funzioni principali sono:
- correggi_nome_giocatore: Corregge il nome del giocatore secondo regole specifiche.
- leggi_e_filtra_csv: Legge e filtra i dati da un file CSV.
- unisci_e_aggrega_csv_in_directory: Unisce e aggrega i file CSV presenti nelle sottodirectory di una directory principale.
- unisci_file_merged_in_directory: Unisce tutti i file "_merged.csv" presenti nelle sottodirectory.
- aggrega_e_pulisci_dati: Aggrega e pulisce i dati per creare un file finale aggregato e pulito.
"""

import pandas as pd
import os

def correggi_nome_giocatore(nome):
    if '__' in nome:
        return nome.replace('__', '. ')
    elif '_' in nome:
        return nome.replace('_', ' ')
    return nome

def leggi_e_filtra_csv(file_path, stagioni, giocatore):
    df = pd.read_csv(file_path, skiprows=2)
    colonna_stagione = 'Stagione' if 'Stagione' in df.columns else 'Season'
    df = df[df[colonna_stagione].isin(stagioni)]
    df['Giocatore'] = correggi_nome_giocatore(giocatore)
    colonne_da_rimuovere = ['Età', 'Piazzamento', '90 min']
    df = df.drop(columns=colonne_da_rimuovere, errors='ignore')
    return df

def unisci_e_aggrega_csv_in_directory(directory, stagioni=['2022-2023', '2023-2024']):
    sottodirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    for sottodirectory in sottodirectories:
        dfs = []
        path_completo = os.path.join(directory, sottodirectory)
        file_csv = [f for f in os.listdir(path_completo) if f.endswith('.csv') and f"{sottodirectory}_merged.csv" not in f]
        for file in file_csv:
            file_path = os.path.join(path_completo, file)
            df = leggi_e_filtra_csv(file_path, stagioni, sottodirectory)
            dfs.append(df)

        if dfs:
            df_aggregato = pd.concat(dfs, ignore_index=True)
            colonna_stagione = 'Stagione' if 'Stagione' in df_aggregato.columns else 'Season'
            df_aggregato = df_aggregato.groupby(colonna_stagione).apply(lambda x: x.bfill().iloc[0]).reset_index(drop=True)
            df_aggregato = df_aggregato[['Giocatore'] + [col for col in df_aggregato.columns if col != 'Giocatore']]
            output_path = os.path.join(path_completo, f"{sottodirectory}_merged.csv")
            df_aggregato.to_csv(output_path, index=False)
            print(f"File aggregato creato con successo per {sottodirectory} in {output_path}")

def unisci_file_merged_in_directory(directory):
    subdirectories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    if subdirectories:
        dfs = []
        for subdir in subdirectories:
            subdir_path = os.path.join(directory, subdir)
            files_to_merge = [f for f in os.listdir(subdir_path) if f.endswith('_merged.csv')]
            for file in files_to_merge:
                file_path = os.path.join(subdir_path, file)
                dfs.append(pd.read_csv(file_path))
        df_merged = pd.concat(dfs, ignore_index=True)
        output_path = os.path.join(directory, 'merged_all.csv')
        df_merged.to_csv(output_path, index=False)
        print(f"Tutti i file sono stati uniti con successo in {output_path}")
    else:
        print("Nessuna sottodirectory trovata.")

def aggrega_e_pulisci_dati(file_path):
    df = pd.read_csv(file_path)
    df_cleaned = df.dropna(subset=['Giocatore', 'Stagione', 'Squadra'])
    columns_to_mean = df_cleaned.select_dtypes(include=['number']).columns.tolist()
    aggregation_functions = {col: 'mean' for col in columns_to_mean}
    aggregation_functions.update({'Squadra': 'first', 'Paese': 'first', 'Competizione': 'first'})
    aggregated_data = df_cleaned.groupby('Giocatore').agg(aggregation_functions).reset_index()

    output_path = 'fbref_data_cleaned.csv'
    aggregated_data.to_csv(output_path, index=False)
    print(f"Dati aggregati e puliti salvati in {output_path}")

unisci_e_aggrega_csv_in_directory('../../Data Retrieval/fbref_data')
unisci_file_merged_in_directory('../../Data Retrieval/fbref_data')
aggrega_e_pulisci_dati('../../Data Retrieval/fbref_data/merged_all.csv')
