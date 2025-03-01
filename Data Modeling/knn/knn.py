import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import plotly.express as px

# Carica i dati
data = pd.read_csv('../../Data Preparation/final_data/final_data_cleaned.csv')

# Verifica se Acerbi è presente nel dataset
acerbi_stats = data[data['Nome Giocatore'].str.contains('Acerbi', case=False)]

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

# Rimuovi la colonna del nome per i calcoli
data_no_name = data.drop('Nome Giocatore', axis=1)

# Standardizza i dati (opzionale ma raccomandato per KNN)
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_no_name)
data_scaled = pd.DataFrame(data_scaled, columns=data_no_name.columns)

# Indice di Acerbi nel dataset scalato
acerbi_index_scaled = data_scaled.index[acerbi_stats.index[0]]

for categoria, features in categorie.items():
    # Seleziona solo le colonne rilevanti per la categoria
    X_categoria = data_scaled[features]

    # Addestra KNN su questa categoria
    knn = NearestNeighbors(n_neighbors=6)  # 5 + Acerbi stesso
    knn.fit(X_categoria)

    # Trova i vicini più prossimi per Acerbi
    distances, indices = knn.kneighbors(X_categoria.iloc[[acerbi_index_scaled]])

    # Estrai gli indici dei giocatori simili (escludendo Acerbi)
    similar_players_indices = indices[0][1:]  # Ometti Acerbi dai risultati finali
    similar_players_names = data.loc[similar_players_indices, 'Nome Giocatore']

    # Crea DataFrame per il grafico senza includere Acerbi
    similar_players_df = pd.DataFrame({
        'Nome Giocatore': similar_players_names.values,
        'Distanza Euclidea': distances[0][1:]  # Escludi la distanza di Acerbi, che sarebbe 0
    })

    # Visualizzazione interattiva con Plotly
    fig = px.bar(similar_players_df, x='Nome Giocatore', y='Distanza Euclidea',
                 title=f"Giocatori simili a Francesco Acerbi per {categoria}",
                 text='Distanza Euclidea')

    # Personalizza grafico
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', xaxis_tickangle=-45,
                      xaxis_title=None, yaxis_title="Distanza Euclidea",
                      title_font_size=20, title_x=0.5)

    # Salva la figura
    fig.write_html(f"../../Data Visualization/knn/knn_{categoria.replace(' ', '_')}.html")