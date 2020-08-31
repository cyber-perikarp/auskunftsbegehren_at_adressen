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

def writeRecord(outFileHandler, record):
    # TODO: Library suchen für das
    outFileHandler.write("<div class=\"listItem {0}\">".format(record["Ebene"]))
    outFileHandler.write("<h4>{0}</h4>\n".format(record["Name"]))
    outFileHandler.write("<p><strong>{0}</strong></p>\n".format(record["Name_Lang"]))
    outFileHandler.write("<p>{0}<br>\n".format(record["Adresse"]))
    outFileHandler.write("{0} {1}</p>\n".format(record["PLZ"], record["Ort"]))
    outFileHandler.write("<p>Typ: <em>{0}</em></p>".format(record["Typ"]))
    if record["E-Mail"]:
        outFileHandler.write("<span class=\"icon-mail screenOnly\"></span><span class=\"marginLeft\">Mail:</span> <a href=\"mailto:{0}\">{1}</a><br>\n".format(record["E-Mail"], record["E-Mail"]))

    if record["Tel"]:
        outFileHandler.write("<span class=\"icon-phone screenOnly\"></span><span class=\"marginLeft\">Tel:</span> <a href=\"tel:{0}\">{1}</a><br>\n".format(record["Tel"], record["Tel"]))

    if record["Fax"]:
        outFileHandler.write("<span class=\"icon-upload screenOnly\"></span><span class=\"marginLeft\">Fax:</span> {0}<br>\n".format(record["Fax"]))

    outFileHandler.write("<p>Letzte Prüfung am: <em>{0}</em></p>\n".format(record["Pruefung"]))
    outFileHandler.write("</div> <!-- List Item End -->\n\n")

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
              <div id="mainContainer">""")
except IOError:
    print("Cant write to file!")
    exit(1)

# Wir brauchen ein neues dict, weil wir die überschriften schreiben wollen
recordsDict = {}

# csv lesen und parsen
with open(csvFile, newline='') as csvFileReader:
    readFile = csv.DictReader(csvFileReader)

    for record in readFile:
        if not record["Ebene"] in recordsDict:
            print("Adding administration Level: " + record["Ebene"])
            recordsDict[record["Ebene"]] = {}

        if not record["Branche"] in recordsDict[record["Ebene"]]:
            print("Adding sector: " + record["Branche"])
            recordsDict[record["Ebene"]][record["Branche"]] = {}

        print("Processing entry: " + record["Name"])
        lastChecked = record["Pruefung"].replace(".", "-")
        nameForId = record["Name"].replace(" ", "-").lower()
        id = record["Ebene"] + "_" + record["Branche"] + "_" + lastChecked + "_" + nameForId

        recordsDict[record["Ebene"]][record["Branche"]][id] = record

try:
    with open(outFile, "a+") as outFileHandler:
        for administrationLevel in recordsDict:
            print("Writing administration Level: " + administrationLevel)

            outFileHandler.write("<div class=\"administrationLevelContainer filter {0}\">".format(administrationLevel))
            outFileHandler.write("<h2>{0}</h2>".format(administrationLevel))

            for type in recordsDict[administrationLevel]:
                print("Writing type: " + type)
                outFileHandler.write("<div class=\"typeContainer {0}\">".format(type))
                outFileHandler.write("<h3>{0}</h3>".format(type))

                outFileHandler.write("<div class=\"itemContainer\">")
                for record in recordsDict[administrationLevel][type]:
                    print("Writing entry: " + recordsDict[administrationLevel][type][record]["Name"])
                    writeRecord(outFileHandler, recordsDict[administrationLevel][type][record])
                outFileHandler.write("</div><!-- end of {0} itemContainer".format(recordsDict[administrationLevel][type][record]["Name"]))

                outFileHandler.write("</div><!-- end of {0} typeContainer -->".format(type))
                print("End of: " + type)

            outFileHandler.write("</div><!-- end of {0} administrationLevelContainer -->".format(administrationLevel))
            print("End of: " + administrationLevel)

except IOError:
    print("Cant write to file!")
    exit(1)

# Footer
try:
    with open(outFile, "a+") as outFileHandler:
        outFileHandler.write("""</div> <!-- This is the end of the mainContainer -->
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
