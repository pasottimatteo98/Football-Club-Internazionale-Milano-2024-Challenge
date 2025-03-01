# Questo script utilizza il fuzzy matching per trovare corrispondenze tra nomi di giocatori di calcio provenienti da diversi dataset: Kickest, Whoscored e Fbref.
# In particolare, carica i tre dataset, abbrevia i nomi dei giocatori nel dataset di Whoscored, crea una lista unica di nomi giocatori da Kickest e Fbref, e applica il fuzzy matching per trovare la migliore corrispondenza per ogni giocatore nel dataset di Whoscored rispetto alla lista unica di nomi.
# Successivamente, unisce i dataset di Kickest e Fbref utilizzando i nomi dei giocatori come chiave di unione e quindi unisce il risultato con il dataset di Whoscored utilizzando la corrispondenza trovata ('Giocatore_Match') come chiave di unione.
# Infine, salva il dataset finale in un file CSV chiamato 'final_data.csv'.

from fuzzywuzzy import process, fuzz
import pandas as pd

kickest_df = pd.read_csv('../kickest/kickest_data_cleaned.csv')
whoscored_df = pd.read_csv('../whoscored/whoscored_data_cleaned.csv')
fbref_df = pd.read_csv('../fbref/fbref_data_cleaned.csv')

def migliore_corrispondenza(nome, lista_nomi, soglia=95):
    match = process.extractOne(nome, lista_nomi, score_cutoff=soglia)
    return match[0] if match else None

def abbrevia_nome(nome_completo):
    parti = nome_completo.split()
    if len(parti) > 1:
        return f"{parti[0][0]}. {' '.join(parti[1:])}"
    else:
        return nome_completo

whoscored_df['Giocatore'] = whoscored_df['Giocatore'].apply(abbrevia_nome)

lista_nomi_unici = pd.concat([kickest_df['Giocatore'], fbref_df['Giocatore']]).unique()

whoscored_df['Giocatore_Match'] = whoscored_df['Giocatore'].apply(lambda x: migliore_corrispondenza(x, lista_nomi_unici))

df_unito = pd.merge(kickest_df, fbref_df, on='Giocatore', how='outer')
df_finale = pd.merge(df_unito, whoscored_df, left_on='Giocatore', right_on='Giocatore_Match', how='left')

df_finale.to_csv('final_data.csv', index=False)
