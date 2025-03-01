# Questo script carica un dataset contenente dati preparati sui giocatori di calcio da un file CSV. Successivamente, analizza il dataset suddividendo le variabili in categorie predefinite e produce diverse visualizzazioni per ciascuna categoria. Le visualizzazioni includono istogrammi, box plot e heatmap di correlazione. Inoltre, il valore relativo al giocatore Francesco Acerbi viene evidenziato in ogni visualizzazione.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data_prepared_path = '../../Data Preparation/final_data/final_data_cleaned.csv'
data_prepared = pd.read_csv(data_prepared_path)

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

acerbi_values = data_prepared[data_prepared['Nome Giocatore'] == 'F. Acerbi'].iloc[0]

for nome_categoria, variabili in categorie.items():
    fig, axes = plt.subplots(len(variabili), 1, figsize=(15, 2*len(variabili)))
    for i, var in enumerate(variabili):
        ax = axes[i] if len(variabili) > 1 else axes
        sns.histplot(data_prepared[var], kde=True, ax=ax)
        ax.set_title(f'Distribuzione di {var}')
        if var in acerbi_values:
            ax.axvline(acerbi_values[var], color='red', linestyle='--', label='Acerbi')
            ax.legend()
    plt.tight_layout()
    fig.savefig(f'{nome_categoria}_histograms.png')

    fig, ax = plt.subplots(figsize=(18, len(variabili)*0.75))
    sns.boxplot(data=data_prepared[variabili], orient="h", palette="Set2", ax=ax)
    ax.set_title(f'Box Plot per Identificare Outlier in {nome_categoria}')
    for i, var in enumerate(variabili):
        if var in acerbi_values:
            ax.scatter(acerbi_values[var], i, color='red', s=50, label='Acerbi' if i == 0 else "")
    ax.legend()
    fig.savefig(f'{nome_categoria}_boxplot.png')

    fig, ax = plt.subplots(figsize=(18, len(variabili)*0.75))
    corr = data_prepared[variabili].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title(f'Heatmap di Correlazione tra le Variabili di {nome_categoria}')
    fig.savefig(f'{nome_categoria}_correlation.png')