# Argo Marks Graph

Strumento per visualizzare un grafico dei voti in Argo ScuolaNext.

## Dipendenze
Python 3.6 +
- matplotlib
- numpy
- requests
- json
- argparse

## Uso
    argo-marks-graph.py [OPTIONS]

    -h, --help                        Stampa il messaggio d'aiuto ed esce
    -s, --school CODICE               Imposta il codice della scuola
    -u, --user NOMEUTENTE             Imposta il nome utente
    -p, --password PASSWORD           Imposta la password dell'utente
    -f, --file NOMEFILE               Salva il grafico sul file indicato (.png)
