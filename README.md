# Argo Marks Graph

Strumento per visualizzare un grafico dei voti in Argo ScuolaNext.

## Dipendenze
Python 3.6 o maggiore
- matplotlib
- numpy
- requests
- json
- argparse

## Uso
    argo-marks-graph.py [OPTIONS]

    -h, --help                        Stampa il messaggio d'aiuto ed esce
    -s, --school CODICE               Codice della scuola [codice di 7 cifre]
    -u, --user NOMEUTENTE             Nome utente usato nel login
    -p, --password PASSWORD           Password usata nel login
    -f, --file NOMEFILE               Salva il grafico sul file indicato (solo .png)
