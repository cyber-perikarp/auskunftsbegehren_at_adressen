#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import logging
import chromalog
import sys
import argparse

# CLI Parameter
parser = argparse.ArgumentParser("convert-to-sql.py")
parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL")

args = vars(parser.parse_args())

# Logging stuff
loglevel = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")

chromalog.basicConfig(format="%(message)s", level=loglevel)
logger = logging.getLogger()

# In diesem Ordner sind wir
workDir = os.path.dirname(os.path.realpath(__file__))

# Hardgecodede Parameter
outFile = workDir + "/noyb.csv"
csvHeader = ["status", "id", "display_name", "legal_name", "url", "department", "street_address", "city", "neighbourhood", "postal_code", "region", "country", "requires_identification", "operating_countries", "custom_identifier", "identifiers", "generic_url", "generic_email", "generic_note", "access_url", "access_email", "access_note", "deletion_url", "deletion_email", "deletion_note", "portability_url", "portability_email", "portability_note", "correction_url", "correction_email", "correction_note"]

# Postleitzahlendatenbank einlesen
plzDatei = open(workDir + "/plz_verzeichnis.csv", newline="")
plzDict = csv.DictReader(plzDatei)
plz = {}
for row in plzDict:
    plz[row["PLZ"]] = (row["Ort"], row["Bundesland"])

def sanitizePhoneNumber(number):
    number = number.replace(" ", "")
    number = number.replace("-", "")
    number = number.replace("/", "")
    number = number.replace("'", "") # Wegen LibreOffice
    return number

def checkIfFullRecord(record):
    if (not record["Id"]
        or not record["Name"]
        or not record["Name_Lang"]
        or not record["Branche"]
        or not record["Typ"]
        or not record["Adresse"]
        or not record["PLZ"]
        or not record["Land"]
        or not record["E-Mail"]):
            logger.error("Not exporting: " + record["Name"])
            return False
    return True

def populateGeneratedFields(record):
    # Alle leerzeichen, bindestriche, klammern etc aus telefon und faxnummer entfernen
    tel = sanitizePhoneNumber(record["Tel"])
    fax = sanitizePhoneNumber(record["Fax"])

    # Postleitzahl und Bundesland aus Postleitzahlendatenbank
    stadt = plz[record["PLZ"]][0]
    bundesland = plz[record["PLZ"]][1]

    # ID
    quelldatei = os.path.splitext(csvFile)[0].split("/")[-1]
    id = quelldatei + "_" + record["folder"] + "_" + record["Id"]

    recordToReturn = {}

    # Felder für noyb
    recordToReturn["status"] = ""
    recordToReturn["id"] = ""
    recordToReturn["display_name"] = record["Name"]
    recordToReturn["legal_name"] = record["Name_Lang"]
    recordToReturn["url"] = ""
    recordToReturn["department"] = ""
    recordToReturn["street_address"] = record["Adresse"]
    recordToReturn["city"] = stadt
    recordToReturn["neighbourhood"] = ""
    recordToReturn["postal_code"] = record["PLZ"]
    recordToReturn["region"] = bundesland
    recordToReturn["country"] = "AUSTRIA"
    recordToReturn["requires_identification"] = ""
    recordToReturn["operating_countries"] = ""
    recordToReturn["custom_identifier"] = id
    recordToReturn["identifiers"] = ""
    recordToReturn["generic_url"] = ""
    recordToReturn["generic_email"] = record["E-Mail"]
    recordToReturn["generic_note"] = "Phone: " + tel + ", Fax: " + fax
    recordToReturn["access_url"] = ""
    recordToReturn["access_email"] = ""
    recordToReturn["access_note"] = ""
    recordToReturn["deletion_url"] = ""
    recordToReturn["deletion_email"] = ""
    recordToReturn["deletion_note"] = ""
    recordToReturn["portability_url"] = ""
    recordToReturn["portability_email"] = ""
    recordToReturn["portability_note"] = ""
    recordToReturn["correction_url"] = ""
    recordToReturn["correction_email"] = ""
    recordToReturn["correction_note"] = ""

    return recordToReturn

# Header schreiben
try:
    with open(outFile, "w") as outFileHandler:
        logger.debug("Headers: " + str(csvHeader))
        writer = csv.DictWriter(outFileHandler, fieldnames=csvHeader)
        writer.writeheader()
except IOError:
    logger.error("Cant write to file!")

# Alle Unterordner die nicht mit . beginnen enthalten die csvs
for folder in [x for x in sorted(os.listdir(workDir)) if (os.path.isdir(x) and x[0] != ".")]:
    # Hier werden schon die csvs geladen
    for csvFile in [x for x in os.listdir(workDir + "/" + folder) if os.path.splitext(x)[1] == ".csv"]:
        # Pfad zur csv
        csvFile = workDir + "/" + folder + "/" + csvFile
        logger.info("Using File: " + csvFile)

        # csv lesen und parsen
        with open(csvFile, newline='') as csvFileReader:
            readFile = csv.DictReader(csvFileReader)
            for record in readFile:
                record["folder"] = folder # Wir brauchen das zum generieren der ID
                # Unvollständige Datensätze werden nicht eingefügt
                if (checkIfFullRecord(record)):
                    logger.info("Processing entry: " + record["Name"])
                    record = populateGeneratedFields(record)
                    logger.debug(record)

                    # CSV schreiben!
                    try:
                        with open(outFile, "a+") as outFileHandler:
                            writer = csv.DictWriter(outFileHandler, fieldnames=csvHeader)
                            writer.writerow(record)

                    except IOError:
                        logger.error("Cant write to file!")
