# Argo Marks Graph
A Tool for visualizing marks in Argo ScuolaNext.
###### [Italian Readme Version](https://github.com/Chris1101/ArgoMarksGraph/blob/master/README-IT.md)

## Dependencies
Python 3.6 or higher
- matplotlib
- numpy
- requests
- json
- argparse
- getpass

## Usage
    argo-marks-graph.py [OPTIONS]

    -h, --help                        Print this help and exit
    -s, --school CODE                 School code [7 digits code]
    -u, --user USERNAME               Username used for the login
    -p, --password PASSWORD           Password used for the login
    -f, --file FILENAME               Redirect the output to an image on the specified file (.png only)
