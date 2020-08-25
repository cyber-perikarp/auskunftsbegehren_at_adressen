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
              <link rel="stylesheet" media="screen" href="https://cdnjs.cloudflare.com/ajax/libs/mini.css/3.0.1/mini-default.min.css">
              <link rel="stylesheet" type="text/css" href="style.css">
              <meta name="viewport" content="width=device-width, initial-scale=1">
              <title>
                Export
              </title>
            </head>
            <body>
              <header>
                  <h1 class="center">
                    Genereller Export
                  </h1>
                  <div id="buttonContainer" class="center screenOnly">
                    <button class="btn" onclick="filterSelection('bund')">Bund</button>
                    <button class="btn" onclick="filterSelection('burgenland')">Burgenland</button>
                    <button class="btn" onclick="filterSelection('kaernten')">Kärnten</button>
                    <button class="btn" onclick="filterSelection('niederoesterreich')">Niederösterreich</button>
                    <button class="btn" onclick="filterSelection('oberoesterreich')">Oberösterreich</button>
                    <button class="btn" onclick="filterSelection('salzburg')">Salzburg</button>
                    <button class="btn" onclick="filterSelection('steiermark')">Steiermark</button>
                    <button class="btn" onclick="filterSelection('tirol')">Tirol</button>
                    <button class="btn" onclick="filterSelection('vorarlberg')">Vorarlberg</button>
                    <button class="btn" onclick="filterSelection('wien')">Wien</button>
                    <button class="btn" onclick="filterSelection('privat')">Privat</button>
                    </div>
              </header>
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
                            outFileHandler.write("<div class=\"listItem {0}\">".format(os.path.splitext(csvFile)[0].split("/")[-2]))
                            outFileHandler.write("<h2>{0}</h2>\n".format(record["Name"]))
                            outFileHandler.write("<strong>{0}</strong><br>\n".format(record["Name_Lang"]))
                            outFileHandler.write("<p>{0}<br>\n".format(record["Adresse"]))
                            outFileHandler.write("{0} {1}</p>\n".format(record["PLZ"], record["Ort"]))
                            if record["E-Mail"]:
                                outFileHandler.write("<span><span class=\"icon-mail screenOnly\"></span> Mail: <a href=\"mailto:{0}\">{1}</a></span><br>\n".format(record["E-Mail"], record["E-Mail"]))

                            if record["Tel"]:
                                outFileHandler.write("<span><span class=\"icon-phone screenOnly\"></span> Tel: <a href=\"tel:{0}\">{1}</a></span><br>\n".format(record["Tel"], record["Tel"]))

                            if record["Fax"]:
                                outFileHandler.write("<span><span class=\"icon-upload screenOnly\"></span> Fax: {0}</span><br>\n".format(record["Fax"]))

                            outFileHandler.write("<p><em>Letzte Prüfung am: {0}</em></p>\n".format(record["Pruefung"]))
                            outFileHandler.write("</div>\n\n")

                    except IOError:
                        logger.critical("Cant write to file!")

# Footer
try:
    with open(outFile, "a+") as outFileHandler:
        outFileHandler.write("""</div> <!-- This is the end of the listWrapper -->
                <footer>
                    <p>
                    Lizenz: <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International</a><br>
                    <a href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/blob/master/docs/mitwirkende.md" target="_blank">Mitwirkende</a><br>
                    <a href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/issues/new" target="_blank" class="important">Neuen Datensatz einreichen</a>
                  </p>
                </footer>
            </body>
            <script src="filter.js"></script>
            </html>
        """)
except IOError:
    logger.critical("Cant write to file!")
