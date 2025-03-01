# Questo script si occupa di pulire e preparare un dataset contenente dati sui giocatori di calcio provenienti da diverse fonti. Inizialmente, il dataset viene caricato da un file CSV denominato 'final_data.csv'. Successivamente, vengono rinominate le colonne del dataset per uniformità e coerenza utilizzando un dizionario di mapping predefinito. Viene inoltre rimossa una serie di colonne non rilevanti o ridondanti. Dopodiché, vengono identificate e rimosse le colonne duplicate o simili, nonché le colonne con valori NaN o tutte le righe di valori 0.
# Successivamente, le colonne numeriche vengono normalizzate utilizzando lo scaler MinMaxScaler di scikit-learn. Infine, il dataset pulito viene salvato in un nuovo file CSV chiamato 'final_data_cleaned.csv'.

import pandas as pd
from sklearn.preprocessing import MinMaxScaler


df = pd.read_csv('final_data.csv')

df = df.rename(columns={"Giocatore_x": "Giocatore", "Giocatore_Match": "GiocatoreVerifica"})

colonne_rinominate = {
    "Giocatore": "Nome Giocatore",
    "Presenze": "Partite Giocate",
    "Minuti": "Minuti Giocati",
    "Goal": "Gol Fatti",
    "Tiri Porta": "Tiri in Porta",
    "Dribb Riusciti": "Dribbling Riusciti",
    "Chance Fallite": "Occasioni Sprecate",
    "Dribb Tentati": "Dribbling Tentati",
    "Presenze_passaggi": "Partite - Passaggi",
    "Minuti_passaggi": "Minuti - Passaggi",
    "Passaggi": "Totale Passaggi",
    "Pass Riusciti": "Passaggi Riusciti",
    "% Pass Riusciti": "Percentuale Passaggi Riusciti",
    "Pass Chiave": "Passaggi Chiave",
    "Chance Create": "Occasioni Create",
    "Cross Riusciti": "Cross Riusciti",
    "Clean Sheet": "Porta Invulnerata",
    "Falli Subiti": "Falli Subiti",
    "Gialli": "Cartellini Gialli",
    "Rossi": "Cartellini Rossi",
    "Pall Rubati": "Palloni Rubati",
    "Tackle": "Tackle Riusciti",
    "Presenze_azioni_difensive": "Partite - Azioni Difensive",
    "Minuti_azioni_difensive": "Minuti - Azioni Difensive",
    "Intercetti": "Intercept",
    "Rubati": "Palloni Recuperati",
    "Duelli Vinti": "Duelli Aerei/Terra Vinti",
    "Duelli Persi": "Duelli Aerei/Terra Persi",
    "Errori Dec": "Errori Decisionali",
    "Tackle_azioni_difensive": "Tackle - Azioni Difensive",
    "Cntrs": "Contropiedi",
    "Contr. vinti": "Contropiedi Vinti",
    "Treq. dif.": "Transizioni Difensive",
    "Treq. cen.": "Transizioni Centrali",
    "Treq. off.": "Transizioni Offensive",
    "Att": "Attacchi",
    "Persi": "Palloni Persi",
    "Blocchi": "Blocchi Effettuati",
    "Tiri": "Tiri Effettuati",
    "Passaggio": "Tipo Passaggio",
    "Int": "Intercettazioni",
    "Tkl+Int": "Tackle + Intercettazioni",
    "Salvat.": "Salvataggi",
    "Err.": "Errori",
    "SCA": "Azione Creata",
    "Passaggio Live": "Passaggi Live",
    "Passaggio Dead": "Passaggi Dead",
    "A": "Assist",
    "Def.": "Azione Difensiva",
    "GCA": "Azione Gol Creata",
    "Compl.": "Passaggi Completati",
    "Tent,": "Tentativi",
    "Dist. Tot.": "Distanza Totale Percorsa",
    "Dist. Prog.": "Distanza Progressiva",
    "Assist": "Assist",
    "xAG": "Expected Assists Gol",
    "xA": "Expected Assists",
    "A-xAG": "Differenza tra Assist Attesi e Gol",
    "PF": "Palle Ferme",
    "1/3": "Entrate nel Terzo Finale",
    "PPA": "Passaggi Penetranti nell'Area",
    "Cross in area": "Cross nell'Area di Rigore",
    "PrgP": "Passaggi Progressivi",
    "In gioco": "Palla in Gioco",
    "Non in gioco": "Palla Fuori Gioco",
    "Pun.": "Punizioni",
    "PassFil": "Passaggi Filtranti",
    "Scambi": "Scambi Palla",
    "Rimesse in gioco": "Rimesse Laterali",
    "Angoli": "Calci d'Angolo",
    "Conv.": "Conversioni",
    "Div.": "Divise",
    "Dir.": "Direzione",
    "Fuorigioco": "Posizioni di Fuorigioco",
    "Age": "Età",
    "90s": "Minuti per 90s",
    "Tkl": "Tackle Totali",
    "TklW": "Tackle Vinti",
    "Def 3rd": "Azione Difensiva Terzo Campo",
    "Mid 3rd": "Azione Difensiva Zona Centrale",
    "Att 3rd": "Azione Difensiva Zona Attacco",
    "Tkl%": "Percentuale Tackle Riusciti",
    "Lost": "Palloni Persi",
    "Blocks": "Blocchi Totali",
    "Sh": "Tiri Subiti",
    "Pass": "Passaggi Subiti",
    "Clr": "Disimpegni",
    "Err": "Errori",
    "PassLive": "Passaggi Live",
    "PassDead": "Passaggi su Palla Morta",
    "TO": "Turnover",
    "Fld": "Fallo",
    "Def": "Difesa",
    "Cmp": "Competizioni",
    "Cmp%": "Percentuale Competizioni Vinte",
    "TotDist": "Distanza Totale Percorsa",
    "PrgDist": "Distanza Progressiva Percorsa",
    "Ast": "Assist",
    "KP": "Passaggi Chiave",
    "CrsPA": "Cross Perfetti nell'Area",
    "Live": "In Gioco",
    "Dead": "Fuori Gioco",
    "FK": "Calci di Punizione",
    "TB": "Through Balls",
    "Sw": "Switches",
    "Crs": "Cross",
    "TI": "Throw Ins",
    "CK": "Corner Kicks",
    "In": "Ingressi",
    "Out": "Uscite",
    "Str": "Strutture",
    "Off": "Offsides",
    "Cont": "Contesti",
    "Inter": "Interceptazioni",
    "Falli": "Falli Commessi",
    "Fuorig": "Fuorigioco",
    "Spaz": "Spazi",
    "Drib": "Dribbling",
    "Respinte": "Respinte",
    "Rating": "Valutazione Giocatore"
    }

colonne_non_rilevanti = ['Squadra','Paese', 'Competizione', 'Giocatore_y', 'GiocatoreVerifica', 'Età',
                         'Presenze_portieri', 'Minuti_portieri', 'Parate', 'Clean Sheet_portieri', 'Goal Subiti',
                         'Rig Parati', 'Rig Subiti']

df = df.drop(columns=colonne_non_rilevanti, errors='ignore')
df = df.rename(columns=colonne_rinominate)

colonne_duplicate_simili = [col for col in df.columns if '_generale' in col or col.endswith(('.1', '.2', '.3', 'y', 'x'))]
df = df.drop(columns=colonne_duplicate_simili, errors='ignore')
df = df.loc[:, ~df.columns.duplicated()]
df.fillna(0, inplace=True)
df = df.loc[:, (df != 0).any(axis=0)]

data_numerica = df.select_dtypes(include=['float64', 'int64'])
min_max_scaler = MinMaxScaler()
data_normalizzata = min_max_scaler.fit_transform(data_numerica)
df[data_numerica.columns] = data_normalizzata

df.to_csv('final_data_cleaned.csv', index=False)

print("Il dataset pulito è stato salvato come 'final_data_cleaned.csv'.")
