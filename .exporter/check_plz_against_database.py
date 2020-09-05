#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################################
# Prüft die Datensätze gegen die PLZ Datenbank #
################################################

import csv
import os

# In diesem Ordner sind wir
workDir = os.path.dirname(os.path.realpath(__file__)) + "/.."

# Hardgecodede Parameter
foldersToIgnore = [".", "..", ".exporter", "docs", "upload", ".git", ".github"]

# Postleitzahlendatenbank einlesen
plzFile = open(workDir + "/.exporter/plz_verzeichnis.csv", newline="")
plzDict = csv.DictReader(plzFile)
plz = {}
for row in plzDict:
    plz[row["PLZ"]] = (row["Ort"], row["Bundesland"])

# Alle Unterordner laden, außer die die wir ignorieren wollen
for folder in [x for x in sorted(os.listdir(workDir)) if (os.path.isdir(x) and x not in foldersToIgnore)]:
    # Hier werden schon die csvs geladen
    for csvFile in [x for x in os.listdir(workDir + "/" + folder) if os.path.splitext(x)[1] == ".csv"]:
        # Pfad zur csv
        csvFile = workDir + "/" + folder + "/" + csvFile

        # csv lesen und parsen
        with open(csvFile, newline='') as csvFileReader:
            readFile = csv.DictReader(csvFileReader)
            for record in readFile:
                # Unvollständige Datensätze werden nicht eingefügt
                if record["PLZ"]:
                    ort = plz[record["PLZ"]][0] # Im Fehlerfall fliegt hier eine Exception was die CI Pipeline abbricht
