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
from collections import OrderedDict
from operator import getitem

# CLI Parameter
parser = argparse.ArgumentParser("generic_csv_exporter.py")
parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL")

args = vars(parser.parse_args())

# Logging stuff
loglevel = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")

chromalog.basicConfig(format="%(message)s", level=loglevel)
logger = logging.getLogger()

# In diesem Ordner sind wir
workDir = os.path.dirname(os.path.realpath(__file__)) + "/.."

# Hardgecodede Parameter
outFile = workDir + "/generic.csv"
csvHeader = ["Name", "Name_Lang", "Branche", "Typ", "Adresse", "PLZ", "Ort", "Ebene", "E-Mail", "Homepage", "Tel", "Fax", "Datenquelle", "Pruefung"]
foldersToIgnore = [".", "..", ".exporter", "docs", "upload", ".git", ".github"]
administrationLevels = {
    "bund": "Bund",
    "burgenland": "Burgenland",
    "kaernten": "Kärnten",
    "niederoesterreich": "Niederösterreich",
    "oberoesterreich": "Oberösterreich",
    "privat": "Privat",
    "salzburg": "Salzburg",
    "steiermark": "Steiermark",
    "tirol": "Tirol",
    "vorarlberg": "Vorarlberg",
    "wien": "Wien"
}

# Postleitzahlendatenbank einlesen
plzFile = open(workDir + "/.exporter/plz_verzeichnis.csv", newline="")
plzDict = csv.DictReader(plzFile)
plz = {}
for row in plzDict:
    plz[row["PLZ"]] = (row["Ort"], row["Bundesland"])

# Alle leerzeichen, bindestriche, klammern etc aus telefon und faxnummer entfernen
def sanitizePhoneNumber(number):
    number = number.replace(" ", "")
    number = number.replace("-", "")
    number = number.replace("/", "")
    number = number.replace("(", "")
    number = number.replace(")", "")
    number = number.replace("'", "") # Wegen LibreOffice
    number = number.replace("‘", "") # Auch wegen LibreOffice
    logger.debug("Sanitized Phone Number: " + number)
    return number

# Hier wird geprüft ob die notwendigen Felder vorhanden sind
def checkIfFullRecord(record):
    if (not record["Id"]
        or not record["Name"]
        or not record["Name_Lang"]
        or not record["Adresse"]
        or not record["PLZ"]
        or not record["Pruefung"]):
            logger.error("Not exporting: " + record["Name"])
            return False
    return True

def populateGeneratedFields(record):
    record["Tel"] = sanitizePhoneNumber(record["Tel"])
    record["Fax"] = sanitizePhoneNumber(record["Fax"])

    # Postleitzahl aus Postleitzahlendatenbank
    record["Ort"] = plz[record["PLZ"]][0]

    record["Ebene"] = ' '.join([administrationLevels.get(i, i) for i in record["Ordner"].split()])

    logger.debug("Found city: " + record["Ort"])

    return record

# Header schreiben
try:
    with open(outFile, "w") as outFileHandler:
        logger.debug("Headers: " + str(csvHeader))
        writer = csv.DictWriter(outFileHandler, fieldnames=csvHeader)
        writer.writeheader()
except IOError:
    logger.critical("Cant write to file!")
    exit(1)

logger.debug(sorted(os.listdir(workDir)))

recordsToWrite = []
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
                record["Ordner"] = folder # Wir brauchen das zum sortieren später

                # Unvollständige Datensätze werden nicht eingefügt
                if (checkIfFullRecord(record)):
                    logger.debug("Processing entry: " + record["Name"])
                    record = populateGeneratedFields(record)
                    logger.debug(record)
                    recordsToWrite.append(record)

sortedRecords = sorted(recordsToWrite, key = lambda tup: (tup["Ordner"], tup["Branche"], tup["Typ"], tup["Name"]))
logger.debug(sortedRecords)

for entry in sortedRecords:
    # CSV schreiben!
    try:
        with open(outFile, "a+") as outFileHandler:
            del entry["Ordner"]
            del entry["Id"]

            logger.debug("Writing entry: " + entry["Name"])

            writer = csv.DictWriter(outFileHandler, fieldnames=csvHeader)
            writer.writerow(entry)

    except IOError:
        logger.critical("Cant write to file!")
        exit(1)
