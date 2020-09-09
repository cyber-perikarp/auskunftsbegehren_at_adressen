#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################
# Genereller Exporter #
#        HTML         #
#######################

import csv
import os
import sys
import qrcode
import hashlib
import urllib.parse

# In diesem Ordner sind wir
workDir = os.path.dirname(os.path.realpath(__file__)) + "/.."

# Hardgecodede Parameter
outFile = workDir + "/generic.html"
csvFile = workDir + "/upload/generic.csv"
qrcodeFolder = workDir + "/qrcodes/"

def writeRecord(outFileHandler, record):
    # TODO: Library suchen für das
    outFileHandler.write("<div class=\"listItem {0}\">".format(record["Ebene"])) # Das ist der Container eines Datensatzes
    outFileHandler.write("<h4 class=\"title is-4\">{0}</h4>\n".format(record["Name"])) # Kurzbezeichnung
    outFileHandler.write("<p><strong>{0}</strong></p>\n".format(record["Name_Lang"])) # Langname

    addressWithoutPoBox = record["Adresse"].split(", Postfach", 1)[0]
    addressWithoutPoBox = addressWithoutPoBox.replace(", Postfach", "").strip() # Postfach entfernen aus der Adresse

    address = addressWithoutPoBox + ", " + record["PLZ"] + " " + record["Ort"] + ", Österreich" # Adresse in einer Zeile
    urlencodesAddress = urllib.parse.quote(address.strip()) # Adresse URL-Encoden und Whitespaces entfernen
    mapLink = "https://www.google.at/maps/place/" + urlencodesAddress

    outFileHandler.write("<p><a href=\"{0}\" target=\"_blank\">{1}<br>\n".format(mapLink, record["Adresse"])) # Straße, Hausnummer, Postfach
    outFileHandler.write("{0} {1}</a></p>\n".format(record["PLZ"], record["Ort"])) # PLZ und Ort

    outFileHandler.write("<p>Typ: <em>{0}</em></p>".format(record["Typ"])) # Typ der Firma; Branche steht schon in der Überschrift
    if record["E-Mail"]: # Email nur anzeigen wenn vorhanden, mit Icon
        outFileHandler.write("<span class=\"icon-email screenOnly\"></span><span class=\"marginLeft\">Mail:</span> <a href=\"mailto:{0}\">{1}</a><br>\n".format(record["E-Mail"], record["E-Mail"]))

    if record["Tel"]: # Telefon nur anzeigen wenn vorhanden, mit Icon
        qrcodeImage = qrcode.make("TEL:" + record["Tel"]) # TEL: sagt dass der QR Code eine Telefonnummer ist
        qrcodeMd5HashOfName = hashlib.md5(record["Name"].encode("utf-8")).hexdigest() # Wir wollen den md5 Hash des Namens
        qrcodeFileNameAndPath = qrcodeFolder + "/" + qrcodeMd5HashOfName + ".png"

        try:
            qrcodeImage.save(qrcodeFileNameAndPath)
        except:
            print("Cant write QR Code to file!")
            exit(1)

        outFileHandler.write("<span class=\"icon-phone screenOnly\"></span><span class=\"marginLeft\">Tel:</span> <a href=\"tel:{1}\">{2}</a><span class=\"icon-qrcode marginLeft screenOnly desktopOnly lightbox\" data-featherlight=\"qrcodes/{0}.png\"></span><br>\n".format(qrcodeMd5HashOfName, record["Tel"], record["Tel"]))

    if record["Fax"]: # Fax nur anzeigen wenn vorhanden, mit Icon
        outFileHandler.write("<span class=\"icon-fax screenOnly\"></span><span class=\"marginLeft\">Fax:</span> {0}<br>\n".format(record["Fax"]))

    outFileHandler.write("<p>Letzte Prüfung am: <em>{0}</em></p>\n".format(record["Pruefung"])) # Das ist die Beschreibung wann der Datensatz das letzte mal geprüft wurde
    outFileHandler.write("</div> <!-- List Item End -->\n\n") # Container Ende

# Header schreiben
try:
    with open(outFile, "w") as outFileHandler:
        outFileHandler.write("""<!DOCTYPE html>
            <html lang="de">
            <head>
                <meta charset="utf-8">
                <link rel="stylesheet" media="screen" href="css/bulma.css">
                <link rel="stylesheet" media="screen" href="css/featherlight.css">
                <link rel="stylesheet" type="text/css" href="css/style.css">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>
                    Export
                </title>
            </head>
            <body onload="redirectOrUpdateVisible()" onhashchange="redirectOrUpdateVisible();" class="has-navbar-fixed-top">
                <header class="screenOnly">
                    <nav class="navbar is-fixed-top" aria-label="Hauptmenü">
                      <div class="navbar-brand">
                        <a class="navbar-item" href="/">
                          <img src="img/cyber-perikarp-logo.png" height="28" alt="Cyber Perikarp Logo">
                        </a>

                        <a role="button" id="navbar-burger" class="navbar-burger burger" aria-label="menu" aria-expanded="false" data-target="mainNav">
                          <span aria-hidden="true"></span>
                          <span aria-hidden="true"></span>
                          <span aria-hidden="true"></span>
                        </a>
                      </div>

                      <div id="mainNav" class="navbar-menu">
                        <div class="navbar-start">
                          <a class="navbar-item" href="#Bund">
                            Bund
                          </a>
                          <a class="navbar-item" href="#Privat">
                            Privat
                          </a>
                          <a class="navbar-item" href="#Burgenland">
                            Burgenland
                          </a>
                          <a class="navbar-item" href="#Kärnten">
                            Kärnten
                          </a>
                          <a class="navbar-item" href="#Niederösterreich">
                            Niederösterreich
                          </a>
                          <a class="navbar-item" href="#Oberösterreich">
                            Oberösterreich
                          </a>
                          <a class="navbar-item" href="#Salzburg">
                            Salzburg
                          </a>
                          <a class="navbar-item" href="#Steiermark">
                            Steiermark
                          </a>
                          <a class="navbar-item" href="#Tirol">
                            Tirol
                          </a>
                          <a class="navbar-item" href="#Vorarlberg">
                            Vorarlberg
                          </a>
                          <a class="navbar-item" href="#Wien">
                            Wien
                          </a>
                        </div>

                        <div class="navbar-end">
                          <div class="navbar-item">
                            <div class="buttons">
                              <a class="button is-link is-light" target="_blank" href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/blob/master/docs/mitwirkende.md">
                                <strong>Mitwirkende</strong>
                              </a>
                              <a class="button is-link is-light" target="_blank" href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/issues/new">
                                <strong>Neuer Datensatz</strong>
                              </a>
                            </div>
                          </div>
                        </div>
                      </div>
                    </nav>
              </header>
              <div id="mainContainer">""")
except IOError:
    print("Cant write header to file!")
    exit(1)

# Wir brauchen ein neues dict, weil wir die überschriften schreiben wollen
recordsDict = {}

# csv lesen und parsen
with open(csvFile, newline='') as csvFileReader:
    readFile = csv.DictReader(csvFileReader)

    for record in readFile: # Das geht durch alle Datensätze ...
        if not record["Ebene"] in recordsDict: # ... und wenn die "Ebene", d.h. "Bund", "Steiermark", "Privat" etc. noch nicht vorhanden ist ...
            recordsDict[record["Ebene"]] = {} # ... wird sie dem Dict hinzugefügt, und ebenfalls als dict initialisiert

        if not record["Branche"] in recordsDict[record["Ebene"]]: # Hier passiert das gleiche wie oben mit den Ebenen, nur mit den Branchen
            recordsDict[record["Ebene"]][record["Branche"]] = {}

        lastChecked = record["Pruefung"].replace(".", "-") # Hier und in den nächsten zwei Zeilen wird eine eindeutige ID für jeden Datensatz generiert
        nameForId = record["Name"].replace(" ", "-").lower()
        id = record["Ebene"] + "_" + record["Branche"] + "_" + lastChecked + "_" + nameForId

        recordsDict[record["Ebene"]][record["Branche"]][id] = record # Hier fügen wir dann den Datensatz dem großen dict hinzu

try:
    with open(outFile, "a+") as outFileHandler:
        for administrationLevel in recordsDict:
            print("Writing administration Level: " + administrationLevel)

            outFileHandler.write("<div class=\"administrationLevelContainer filter\" id=\"{0}\">".format(administrationLevel)) # Das ist der "Ebene" Container
            outFileHandler.write("<h2 class=\"strong title\">{0}</h2>".format(administrationLevel))

            for type in recordsDict[administrationLevel]:
                print("Writing type: " + type)
                outFileHandler.write("<div class=\"typeContainer {0}\">".format(type)) # Das ist der "Branche" Container
                outFileHandler.write("<h3 class=\"strong subtitle\">{0}</h3>".format(type))

                outFileHandler.write("<div class=\"itemContainer\">") # Hier ist der Item Container - Hierdrauf wirkt das CSS Grid
                for record in recordsDict[administrationLevel][type]:
                    writeRecord(outFileHandler, recordsDict[administrationLevel][type][record]) # Hier schreiben wir den Datensatz
                outFileHandler.write("</div><!-- end of {0} itemContainer -->".format(recordsDict[administrationLevel][type][record]["Name"])) # Ende des itemContainer

                outFileHandler.write("</div><!-- end of {0} typeContainer -->".format(type)) # Ende des Branchen Containers

            outFileHandler.write("</div><!-- end of {0} administrationLevelContainer -->".format(administrationLevel)) # Ende des Ebenen Containers

except IOError:
    print("Cant write record to file!")
    exit(1)

# Footer
try:
    with open(outFile, "a+") as outFileHandler:
        outFileHandler.write("""</div> <!-- This is the end of the mainContainer -->
                <footer>
                    <p>
                    <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.de" target="_blank">
                        <img src="img/by-sa.svg" alt="Creative Commons Attribution-ShareAlike 4.0 International">
                    </a><br>
                    <a href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/blob/master/docs/mitwirkende.md" class="screenOnly" target="_blank">
                        Mitwirkende
                    </a><br>
                    <a href="https://github.com/cyber-perikarp/auskunftsbegehren_at_adressen/issues/new" target="_blank" class="important screenOnly">
                        Neuen Datensatz einreichen
                    </a>
                  </p>
                </footer>
                <script src="js/jquery-3.5.1.js"></script>
                <script src="js/featherlight.js"></script>
                <script src="js/filter.js"></script>
                <script src="js/generic-html-export.js"></script>
            </body>
            </html>
        """)
except IOError:
    print("Cant write footer to file!")
    exit(1)
