import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.manifold import TSNE
import plotly.express as px
from scipy.spatial.distance import cdist
import numpy as np
import tensorflow as tf
import random as python_random


# Funzione per addestrare l'autoencoder per una data categoria
def train_autoencoder(data_scaled, input_dim, encoding_dim=8):
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(encoding_dim, activation='relu')(input_layer)
    decoded = Dense(input_dim, activation='sigmoid')(encoded)

    autoencoder = Model(input_layer, decoded)
    encoder = Model(input_layer, encoded)

    autoencoder.compile(optimizer=Adam(), loss='mean_squared_error')
    autoencoder.fit(data_scaled, data_scaled, epochs=100, batch_size=256, shuffle=True, validation_split=0.2, verbose=0)

    return encoder


# Caricamento dei dati
data = pd.read_csv('../../Data Preparation/final_data/final_data_cleaned.csv')

# Settaggio del seed
seed_value = 3
np.random.seed(seed_value)
python_random.seed(seed_value)
tf.random.set_seed(seed_value)

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
# Scaler per la normalizzazione dei dati
scaler = MinMaxScaler()

for categoria, colonne in categorie.items():
    data_categoria = data[colonne]
    data_categoria_scaled = scaler.fit_transform(data_categoria.fillna(0))

    input_dim = data_categoria_scaled.shape[1]
    encoder = train_autoencoder(data_categoria_scaled, input_dim)

    encoded_data = encoder.predict(data_categoria_scaled)
    tsne = TSNE(n_components=2, perplexity=30, n_iter=300)
    tsne_results = tsne.fit_transform(encoded_data)

    acerbi_index = data[data['Nome Giocatore'].str.contains('F. Acerbi', case=False)].index[0]
    distances = cdist(encoded_data[[acerbi_index]], encoded_data, 'euclidean').flatten()
    closest_indices = distances.argsort()[1:6]
    closest_players = data.iloc[closest_indices]['Nome Giocatore']

    df_tsne = pd.DataFrame(tsne_results, columns=['Dim1', 'Dim2'])
    df_tsne['Player'] = data['Nome Giocatore']
    df_tsne['Is_Acerbi'] = data['Nome Giocatore'].str.contains('F. Acerbi', case=False)

    fig = px.scatter(df_tsne, x='Dim1', y='Dim2', color='Is_Acerbi', hover_data=['Player'],
                     title=f"Riduzione della dimensionalità per {categoria} - Acerbi evidenziato",
                     color_continuous_scale=['blue', 'red'])  # Colori per distinguere Acerbi

    # Personalizzazione specifica per Acerbi
    acerbi_points = df_tsne[df_tsne['Is_Acerbi'] == True]
    fig.add_traces(px.scatter(acerbi_points, x='Dim1', y='Dim2', color_discrete_sequence=['red'],
                              hover_data=['Player']).update_traces(marker=dict(size=12, symbol='star')).data)

    fig.update_layout(legend_title_text='Acerbi')
    fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')),
                      selector=dict(mode='markers'))

    fig.write_html(f"../../Data Visualization/autoencoder/autoencoder_{categoria.replace(' ', '_')}.html")

    print(f"Top 5 giocatori simili ad Acerbi per la categoria '{categoria}':\n{', '.join(closest_players)}\n")