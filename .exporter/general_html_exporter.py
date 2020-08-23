#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################
# Genereller Exporter #
#        HTML         #
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
outFile = workDir + "/general.html"
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
        outFileHandler.write("""<!DOCTYPE html>
            <html lang="de">
            <head>
              <meta charset="utf-8">
              <link rel="stylesheet" type="text/css" href="style.css">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>
                Export
              </title>
            </head>
            <body>
              <h1>
                Genereller Export
              </h1>
              <div id="listContainer">""")
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
                            outFileHandler.write("<div class=\"listItem\">")
                            outFileHandler.write("<h2>" + record["Name"] + "</h2>\n")
                            outFileHandler.write("<strong>" + record["Name_Lang"] + "</strong><br>\n")
                            outFileHandler.write("<p>" + record["Adresse"] + "<br>\n")
                            outFileHandler.write(record["PLZ"] + " " + record["Ort"] + "</p>\n")
                            if record["E-Mail"]:
                                outFileHandler.write("<span>Mail: <a href=\"mailto:" + record["E-Mail"] + "\">" + record["E-Mail"] + "</a></span><br>\n")

                            if record["Tel"]:
                                outFileHandler.write("<span>Tel:  <a href=\"tel:" + record["Tel"] + "\">" + record["Tel"] + "</a></span><br>\n")

                            if record["Fax"]:
                                 outFileHandler.write("<span>Fax: " + record["Fax"] + "</span><br>\n")

                            outFileHandler.write("<p><i>Letzte Prüfung am: " + record["Pruefung"] + "</i></p>\n")
                            outFileHandler.write("</div>\n\n")

                    except IOError:
                        logger.critical("Cant write to file!")

# Footer
try:
    with open(outFile, "a+") as outFileHandler:
        outFileHandler.write("""</div> <!-- This is the end of the listWrapper -->
                <p>
                Lizenz: <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International</a><br>
                <a href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/blob/master/docs/mitwirkende.md" target="_blank">Mitwirkende</a><br>
                <a href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/issues/new" target="_blank" class="important">Neuen Datensatz einreichen</a>
              </p>
            </body>
            </html>
        """)
except IOError:
    logger.critical("Cant write to file!")
