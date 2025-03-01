# Questo script carica un dataset contenente dati sui giocatori di calcio da un file CSV. Dopodiché, identifica i dati relativi al giocatore Francesco Acerbi all'interno del dataset. Definisce una serie di categorie di statistiche di gioco e per ciascuna categoria calcola la distanza euclidea tra i dati di Acerbi e quelli di tutti gli altri giocatori. Poi, trova i 5 giocatori più simili ad Acerbi in base alla distanza euclidea per ciascuna categoria e crea un grafico a barre interattivo utilizzando Plotly per visualizzare questi risultati. Infine, salva ogni grafico come file HTML.

from scipy.spatial.distance import euclidean
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot


# Carica il dataset
data = pd.read_csv('../../Data Preparation/final_data/final_data_cleaned.csv')

# Identifica Acerbi nel dataset
acerbi_row = data[data['Nome Giocatore'].str.contains('F. Acerbi', case=False)]

categorie = {
    "Statistiche di Gioco": [
        "Partite Giocate",
        "Minuti Giocati"
    ],
    "Realizzazione e Attacco": [
        "Gol Fatti",
        "Tiri in Porta",
        "Occasioni Sprecate",
        "Tiri Effettuati",
        "Attacchi",
        "Palloni Persi",
        "Conversioni"
    ],
    "Abilità Tecniche": [
        "Dribbling Riusciti",
        "Dribbling Tentati",
        "Cross Riusciti",
        "Passaggi Chiave",
        "Occasioni Create",
        "Azione Creata",
        "Assist",
        "Azione Gol Creata"
    ],
    "Passaggi": [
        "Totale Passaggi",
        "Passaggi Riusciti",
        "Percentuale Passaggi Riusciti",
        "Passaggi Live",
        "Passaggi Dead",
        "Passaggi Completati",
        "Passaggi Penetranti nell'Area",
        "Cross nell'Area di Rigore",
        "Passaggi Progressivi",
        "Passaggi Filtranti"
    ],
    "Difesa": [
        "Palloni Rubati",
        "Tackle Riusciti",
        "Intercept",
        "Palloni Recuperati",
        "Duelli Aerei/Terra Vinti",
        "Duelli Aerei/Terra Persi",
        "Blocchi Effettuati",
        "Tackle + Intercettazioni",
        "Azione Difensiva",
        "Contropiedi Vinti"
    ],
    "Disciplina e Errori": [
        "Falli Subiti",
        "Cartellini Gialli",
        "Cartellini Rossi",
        "Errori Decisionali",
        "Errori",
        "Falli Commessi",
        "Fuorigioco"
    ],
    "Contributo Senza Palla": [
        "Porta Invulnerata",
        "Salvataggi",
        "Contropiedi",
        "Transizioni Difensive",
        "Transizioni Centrali",
        "Transizioni Offensive"
    ],
    "Metriche Avanzate": [
        "Expected Assists Gol",
        "Expected Assists",
        "Differenza tra Assist Attesi e Gol"
    ],
    "Altre Statistiche": [
        "Palle Ferme",
        "Entrate nel Terzo Finale",
        "Palla in Gioco",
        "Palla Fuori Gioco",
        "Punizioni",
        "Scambi Palla",
        "Rimesse Laterali",
        "Calci d'Angolo",
        "Divise",
        "Direzione",
        "Posizioni di Fuorigioco",
        "Contesti",
        "Interceptazioni",
        "Spazi",
        "Dribbling",
        "Respinte",
        "Valutazione Giocatore",
        "Distanza Totale Percorsa",
        "Distanza Progressiva",
        "Tentativi"
    ]
}

colonne_total = data.columns.drop(['Nome Giocatore'])
categorie["Total"] = colonne_total

def calculate_distances(data, acerbi_data, category_columns):
    distances = data.apply(lambda row: euclidean(row, acerbi_data), axis=1)
    return distances

def top_5_similar_players(data, dist_column):
    filtered_data = data[~data['Nome Giocatore'].str.contains('F. Acerbi', case=False)]
    return filtered_data.sort_values(by=dist_column).head(5)

for categoria, colonne in categorie.items():
    acerbi_data = acerbi_row[colonne].iloc[0].fillna(0)
    data[f'Distanza_{categoria}'] = calculate_distances(data[colonne].fillna(0), acerbi_data, colonne)
    top_players = top_5_similar_players(data, f'Distanza_{categoria}')
    nomi_giocatori = top_players['Nome Giocatore']
    distanze = top_players[f'Distanza_{categoria}']

    fig = go.Figure(go.Bar(
        x=distanze,
        y=nomi_giocatori,
        orientation='h',
        text=distanze,
        textposition='auto',
    ))
    fig.update_traces(marker_color='blue', marker_line_color='rgb(8,48,107)',
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(
        title=f"Top 5 giocatori simili ad Acerbi per {categoria}",
        xaxis_title="Distanza Euclidea",
        yaxis_title="Giocatori",
        yaxis={'categoryorder': 'total ascending'},
        font=dict(
            size=12,
        )
    )
    file_name = f"../../Data Visualization/distance/distance_{categoria.replace(' ', '_')}.html"
    plot(fig, filename=file_name, auto_open=False)