# Questo script esegue il clustering dei giocatori di calcio utilizzando l'algoritmo K-Means su diverse categorie di statistiche.
# Viene utilizzato il metodo t-SNE per ridurre la dimensionalità a due dimensioni per visualizzare i cluster in un grafico interattivo con Plotly.
# Viene anche evidenziato il giocatore Francesco Acerbi nei grafici.

from sklearn.metrics.pairwise import euclidean_distances
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px

data = pd.read_csv('../../Data Preparation/final_data/final_data_cleaned.csv')

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

index_acerbi = data[data['Nome Giocatore'].str.contains('F. Acerbi', case=False)].index[0]

for categoria, colonne in categorie.items():
    X_categoria = data[colonne].fillna(0)
    scaler = StandardScaler()
    X_std = scaler.fit_transform(X_categoria)

    kmeans = KMeans(n_clusters=5, random_state=42).fit(X_std)
    labels = kmeans.labels_

    tsne = TSNE(n_components=2, random_state=42)
    X_tsne = tsne.fit_transform(X_std)


    df_tsne = pd.DataFrame(X_tsne, columns=['t-SNE 1', 't-SNE 2'])
    df_tsne['Cluster'] = labels
    df_tsne['Giocatore'] = data['Nome Giocatore']

    fig = px.scatter(df_tsne, x='t-SNE 1', y='t-SNE 2', color='Cluster',
                     hover_data=['Giocatore'], title=f'Cluster dei Giocatori - {categoria}')

    acerbi_points = df_tsne[df_tsne['Giocatore'].str.contains('F. Acerbi')]
    fig.add_traces(px.scatter(acerbi_points, x='t-SNE 1', y='t-SNE 2',
                              color_discrete_sequence=['red'],
                              hover_data=['Giocatore']).update_traces(marker_size=12, marker_symbol='cross').data)

    # Personalizzazione del grafico
    fig.update_traces(marker=dict(size=8, line=dict(width=2, color='DarkSlateGrey')))
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"),
                      legend_title_text='Cluster',
                      title_font_size=24)

    fig.write_html(f"../../Data Visualization/clustering/clustering_{categoria.replace(' ', '_')}.html")

    acerbi_tsne = X_tsne[index_acerbi].reshape(1, -1) # Reshape necessario per il calcolo delle distanze
    distanze = euclidean_distances(X_tsne, acerbi_tsne).reshape(-1) # Calcola e reshape delle distanze

    df_distanze = pd.DataFrame(data={'Giocatore': data['Nome Giocatore'], 'Distanza': distanze})
    df_distanze = df_distanze.sort_values(by='Distanza') # Ordinamento in base alla distanza

    giocatori_simili = df_distanze.iloc[1:6]['Giocatore'].values # Prende i primi 5 escluso il primo

    # Stampa dei giocatori più simili ad Acerbi per questa categoria
    print(f"Per la categoria '{categoria}', i 5 giocatori più simili a F. Acerbi sono: {', '.join(giocatori_simili)}")
