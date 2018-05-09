# Argo Marks Graph

A Tool for visualizing marks in Argo ScuolaNext.

## Dependencies
Python 3.6 +
- matplotlib
- numpy
- requests
- json
- argparse

## Usage
    argo-marks-graph.py [OPTIONS]

    -h, --help                        Print this help and exit
    -s, --school CODE                 Sets the school code [xxxxxxx]
    -u, --user USERNAME               Sets the username used for the login
    -p, --password PASSWORD           Sets the password used for the login
    -f, --file FILENAME               Redirect the output to a image on the specified file (Only .png is supported)
