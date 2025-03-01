# Questo script carica dati da diversi file CSV relativi a statistiche di gioco per diverse categorie di giocatori di calcio,
# li aggrega, li combina in un unico DataFrame e li salva in un nuovo file CSV chiamato "kickest_data_cleaned.csv".

import pandas as pd

datasets = {
    "goal_tiri": {
        "2022_2023": "../../Data Retrieval/kickest_data/kickest_data_GoalTiri_2022_2023.csv",
        "2023_2024": "../../Data Retrieval/kickest_data/kickest_data_GoalTiri_2023_2024.csv"
    },
    "passaggi": {
        "2022_2023": "../../Data Retrieval/kickest_data/kickest_data_Passaggi_2022_2023.csv",
        "2023_2024": "../../Data Retrieval/kickest_data/kickest_data_Passaggi_2023_2024.csv"
    },
    "portieri": {
        "2022_2023": "../../Data Retrieval/kickest_data/kickest_data_Portiere_2022_2023.csv",
        "2023_2024": "../../Data Retrieval/kickest_data/kickest_data_Portiere_2023_2024.csv"
    },
    "generale": {
        "2022_2023": "../../Data Retrieval/kickest_data/kickest_data_Generale_2022_2023.csv",
        "2023_2024": "../../Data Retrieval/kickest_data/kickest_data_Generale_2023_2024.csv"
    },
    "azioni_difensive": {
        "2022_2023": "../../Data Retrieval/kickest_data/kickest_data_AzioniDifensive_2022_2023.csv",
        "2023_2024": "../../Data Retrieval/kickest_data/kickest_data_AzioniDifensive_2023_2024.csv"
    }
}

def load_and_combine_data(category):
    dfs = [pd.read_csv(f'../Data Retrieval/{path}') for path in datasets[category].values()]
    combined = pd.concat(dfs, ignore_index=True)
    return combined

def prepare_dataset(dataset, rename_columns, percent_columns=[]):
    dataset = dataset.rename(columns=rename_columns)
    for col in percent_columns:
        dataset[col] = dataset[col].apply(lambda x: x if 0 <= x <= 100 else x / 100)
    return dataset

def reduce_and_aggregate(combined_df, columns):
    reduced_df = combined_df[columns]
    aggregated_df = reduced_df.groupby(['Giocatore']).mean().reset_index()
    return aggregated_df

columns_to_keep = {
    "goal_tiri": ['Giocatore', 'Presenze', 'Minuti', 'Goal', 'Tiri Porta', 'Dribb Riusciti', 'Chance Fallite', 'Dribb Tentati'],
    "passaggi": ['Giocatore', 'Presenze', 'Minuti', 'Passaggi', 'Pass Riusciti', '% Pass Riusciti', 'Pass Chiave', 'Chance Create', 'Cross', 'Cross Riusciti'],
    "portieri": ['Giocatore', 'Presenze', 'Minuti', 'Parate', 'Clean Sheet', 'Goal Subiti', 'Rig Parati', 'Rig Subiti'],
    "generale": ['Giocatore', 'Presenze', 'Minuti', 'Goal', 'Pass Riusciti', 'Falli', 'Falli Subiti', 'Gialli', 'Rossi', 'Pall Rubati', 'Tackle', 'Clean Sheet'],
    "azioni_difensive": ['Giocatore', 'Presenze', 'Minuti', 'Intercetti', 'Rubati', 'Duelli Vinti', 'Duelli Persi', 'Errori Dec', 'Autogol', 'Tackle']
}

aggregated_data = {}
for category, columns in columns_to_keep.items():
    combined_df = load_and_combine_data(category)
    aggregated_data[category] = reduce_and_aggregate(combined_df, columns)

merged_data = aggregated_data["goal_tiri"]
for category in ['passaggi', 'portieri', 'generale', 'azioni_difensive']:
    if category != "goal_tiri":
        merged_data = pd.merge(merged_data, aggregated_data[category],
                               on=['Giocatore'],
                               how='outer', suffixes=('', f'_{category}'))

merged_data.columns = merged_data.columns.str.strip()
merged_data.fillna(0, inplace=True)

merged_data.to_csv("kickest_data_cleaned.csv", index=False)
print("Merge completato e file salvato.")
