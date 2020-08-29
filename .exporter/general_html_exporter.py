#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################
# Genereller Exporter #
#        HTML         #
#######################

import csv
import os
import sys

# In diesem Ordner sind wir
workDir = os.path.dirname(os.path.realpath(__file__)) + "/.."

# Hardgecodede Parameter
outFile = workDir + "/general.html"
csvFile = workDir + "/upload/general.csv"

def writeRecord(record):
    # TODO: Library suchen für das
    try:
        with open(outFile, "a+") as outFileHandler:
            outFileHandler.write("<div class=\"listItem {0}\">".format(record["Ebene"]))
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
            outFileHandler.write("</div> <!-- List Item End -->\n\n")

    except IOError:
        print("Cant write to file!")
        exit(1)

# Header schreiben
try:
    with open(outFile, "w") as outFileHandler:
        outFileHandler.write("""<!DOCTYPE html>
            <html lang="de">
            <head>
              <meta charset="utf-8">
              <link rel="stylesheet" media="screen" href="mini-default.min.css">
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
                    <button class="btn" onclick="filterSelection('Bund')">Bund</button>
                    <button class="btn" onclick="filterSelection('Burgenland')">Burgenland</button>
                    <button class="btn" onclick="filterSelection('Kärnten')">Kärnten</button>
                    <button class="btn" onclick="filterSelection('Niederösterreich')">Niederösterreich</button>
                    <button class="btn" onclick="filterSelection('Oberösterreich')">Oberösterreich</button>
                    <button class="btn" onclick="filterSelection('Salzburg')">Salzburg</button>
                    <button class="btn" onclick="filterSelection('Steiermark')">Steiermark</button>
                    <button class="btn" onclick="filterSelection('Tirol')">Tirol</button>
                    <button class="btn" onclick="filterSelection('Vorarlberg')">Vorarlberg</button>
                    <button class="btn" onclick="filterSelection('Wien')">Wien</button>
                    <button class="btn" onclick="filterSelection('Privat')">Privat</button>
                    </div>
              </header>
              <div id="listContainer">""")
except IOError:
    print("Cant write to file!")
    exit(1)

# csv lesen und parsen
with open(csvFile, newline='') as csvFileReader:
    readFile = csv.DictReader(csvFileReader)
    for record in readFile:
        print("Processing entry: " + record["Name"])

        # Content schreiben!
        writeRecord(record)

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
                <script src="filter.js"></script>
            </body>
            </html>
        """)
except IOError:
    print("Cant write to file!")
    exit(1)
