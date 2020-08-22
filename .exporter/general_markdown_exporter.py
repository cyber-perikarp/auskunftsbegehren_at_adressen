#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################
# Genereller Exporter #
#      Markdown       ä
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
outFile = workDir + "/general.md"
foldersToIgnore = [".", "..", ".exporter", "docs", "upload", ".git", ".github"]

# Postleitzahlendatenbank einlesen
plzFile = open(workDir + "/.exporter/plz_verzeichnis.csv", newline="")
plzDict = csv.DictReader(plzFile)
plz = {}
for row in plzDict:
    plz[row["PLZ"]] = (row["Ort"], row["Bundesland"])

def sanitizePhoneNumber(number):
    number = number.replace(" ", "")
    number = number.replace("-", "")
    number = number.replace("/", "")
    number = number.replace("(", "")
    number = number.replace(")", "")
    number = number.replace("'", "") # Wegen LibreOffice
    logger.debug("Sanitized Phone Number: " + number)
    return number

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

def populateGeneratedFields(record):
    # Alle leerzeichen, bindestriche, klammern etc aus telefon und faxnummer entfernen
    record["Tel"] = sanitizePhoneNumber(record["Tel"])
    record["Fax"] = sanitizePhoneNumber(record["Fax"])

    # Postleitzahl aus Postleitzahlendatenbank
    record["Ort"] = plz[record["PLZ"]][0]

    logger.debug("Found city: " + record["Ort"])

    return record

# Header schreiben
try:
    with open(outFile, "w") as outFileHandler:
        outFileHandler.write("# Genereller Export\n\n")
except IOError:
    logger.critical("Cant write to file!")

logger.debug(sorted(os.listdir(workDir)))

# Alle Unterordner laden, außer die die wir ignorieren wollen
for folder in [x for x in sorted(os.listdir(workDir)) if (os.path.isdir(x) and x not in foldersToIgnore)]:
    # Hier werden schon die csvs geladen
    for csvFile in [x for x in os.listdir(workDir + "/" + folder) if os.path.splitext(x)[1] == ".csv"]:
        # Pfad zur csv
        csvFile = workDir + "/" + folder + "/" + csvFile
        logger.info("Using File: " + csvFile)

        # Foldername schreiben!
        try:
            with open(outFile, "a+") as outFileHandler:
                outFileHandler.write("## " + folder + "\n")

        except IOError:
            logger.critical("Cant write to file!")

        # csv lesen und parsen
        with open(csvFile, newline='') as csvFileReader:
            readFile = csv.DictReader(csvFileReader)
            for record in readFile:
                # Unvollständige Datensätze werden nicht eingefügt
                if (checkIfFullRecord(record)):
                    logger.info("Processing entry: " + record["Name"])
                    record = populateGeneratedFields(record)
                    logger.debug(record)

                    # Content schreiben!
                    try:
                        with open(outFile, "a+") as outFileHandler:
                            outFileHandler.write("### " + record["Name"] + "\n")
                            outFileHandler.write("**" + record["Name_Lang"] + "**\n")
                            outFileHandler.write(record["Adresse"] + "\n")
                            outFileHandler.write(record["PLZ"] + " " + record["Ort"] + "\n\n")
                            if record["E-Mail"]:
                                outFileHandler.write("Mail: " + record["E-Mail"] + "\n")

                            if record["Tel"]:
                                outFileHandler.write("Tel: " + record["Tel"] + "\n")

                            if record["Fax"]:
                                 outFileHandler.write("Fax: " + record["Fax"] + "\n")

                            outFileHandler.write("*Letzte Prüfung am: " + record["Pruefung"] + "*\n\n")

                    except IOError:
                        logger.critical("Cant write to file!")
