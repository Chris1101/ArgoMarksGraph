# Argo Marks Graph
Strumento per visualizzare un grafico dei voti in Argo ScuolaNext.
###### [English Readme Version](https://github.com/Chris1101/ArgoMarksGraph/blob/master/README.md)

## Dipendenze
Python 3.6 o maggiore
> pip install -r requirements.txt

- matplotlib
- numpy
- requests

## Uso
    argo-marks-graph.py [OPTIONS]

    -h, --help                        Stampa il messaggio d'aiuto ed esce
    -s, --school CODICE               Codice della scuola [codice di 7 cifre]
    -u, --user NOMEUTENTE             Nome utente usato nel login
    -p, --password PASSWORD           Password usata nel login
    -f, --file NOMEFILE               Salva il grafico sul file indicato (solo .png)
    -b, --big                         Visualizza un grafico di dimensioni maggiori
    --save                            Salva la lista dei voti sul file username.txt
    --load                            Carica la lista dei voti dal file username.txt
    -v, --verbose                     Stampa i voti
