#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################
# Genereller Exporter #
#         CSV         ä
#######################

import csv
import os
import logging
import chromalog
import sys
import argparse

# CLI Parameter
parser = argparse.ArgumentParser("general_exporter.py")
parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL")

args = vars(parser.parse_args())

# Logging stuff
loglevel = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")

chromalog.basicConfig(format="%(message)s", level=loglevel)
logger = logging.getLogger()

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

def checkIfFullRecord(record):
    if (not record["Id"]
        or not record["Name"]
        or not record["Name_Lang"]
        or not record["Adresse"]
        or not record["PLZ"]
        or not record["Land"]
        or not record["Pruefung"]):
            logger.error("Not exporting: " + record["Name"])
            return False
    return True

logger.debug(sorted(os.listdir(workDir)))

# Alle Unterordner laden, außer die die wir ignorieren wollen
for folder in [x for x in sorted(os.listdir(workDir)) if (os.path.isdir(x) and x not in foldersToIgnore)]:
    # Hier werden schon die csvs geladen
    for csvFile in [x for x in os.listdir(workDir + "/" + folder) if os.path.splitext(x)[1] == ".csv"]:
        # Pfad zur csv
        csvFile = workDir + "/" + folder + "/" + csvFile
        logger.info("Using File: " + csvFile)

        # csv lesen und parsen
        with open(csvFile, newline='') as csvFileReader:
            readFile = csv.DictReader(csvFileReader)
            for record in readFile:
                # Unvollständige Datensätze werden nicht eingefügt
                if (checkIfFullRecord(record)):
                    ort = plz[record["PLZ"]][0] # Im Fehlerfall fliegt hier eine Exception was die CI Pipeline abbricht
                    logger.info("Found city: " + ort + " for entry " + record["Name"])
