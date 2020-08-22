#!/usr/bin/env python3
# -*- coding: utf-8 -*-

######################
# THIS IS DEPRECATED #
######################

import csv
import os
import argparse
import logging
import chromalog
import sys
import MySQLdb as db

# CLI Parameter
parser = argparse.ArgumentParser("convert-to-sql.py")
parser.add_argument("host", help="Datenbankserver")
parser.add_argument("username", help="Datenbankbenutzer")
parser.add_argument("password", help="Datenbankpasswort")
parser.add_argument("database", help="Datenbank")
parser.add_argument("--loglevel", help="DEBUG, INFO, ERROR, CRITICAL")

args = vars(parser.parse_args())

loglevel = getattr(sys.modules["logging"], args["loglevel"].upper() if args["loglevel"] else "INFO")

chromalog.basicConfig(format="%(message)s", level=loglevel)
logger = logging.getLogger()

# In dieser Tabelle landen die Daten
table = "adressdaten"

# In diesem Ordner sind wir
workDir = os.path.dirname(os.path.realpath(__file__))

# Postleitzahlendatenbank einlesen
plzDatei = open(workDir + '/plz_verzeichnis.csv', newline='')
plzDict = csv.DictReader(plzDatei)
plz = {}
for row in plzDict:
    plz[row["PLZ"]] = (row["Ort"], row["Bundesland"])

# Verbinde zum MySQL Server
try:
    connection = db.Connection(host=args["host"], port=3306, user=args["username"], passwd=args["password"], db=args["database"], charset='UTF8')
    cursor = connection.cursor()
    cursor.execute("SET NAMES UTF8;")
except Exception as e:
    logger.critical(e)

def createOrUpdate(table):
    try:
        cursor.execute("SELECT 1 FROM %s LIMIT 1;" % (table,))
    except:
        cursor.execute(
            """CREATE TABLE %s (
                id VARCHAR(64) NOT NULL UNIQUE,
                name VARCHAR(128) NOT NULL,
                branche VARCHAR(32) NOT NULL,
                typ VARCHAR(32) NOT NULL,
                adresse VARCHAR(64) NOT NULL,
                plz INT(4) UNSIGNED NOT NULL,
                stadt VARCHAR(64) NOT NULL,
                bundesland VARCHAR(64) NOT NULL,
                land VARCHAR(16) NOT NULL,
                email VARCHAR(64),
                tel VARCHAR(32),
                fax VARCHAR(32),
                PRIMARY KEY (id)
            ) CHARACTER SET utf8 COLLATE utf8_general_ci;"""
            % (table,))
        logger.info("Created.")
    else:
        cursor.execute("DROP TABLE %s;" % (table,))
        logger.info("Deleted.")
        createOrUpdate(table)

def insertRecord(record, table):
    logger.info("Inserting Record: ".rstrip('\n') + record["Name"])
    try:
        insertString = """
            INSERT INTO %s (
                id,
                name,
                branche,
                typ,
                adresse,
                plz,
                stadt,
                bundesland,
                land,
                email,
                tel,
                fax
            ) VALUES (
                "%s", /* Id aus der Datei + Dateiname */
                "%s", /* Name */
                "%s", /* Branche */
                "%s", /* Typ */
                "%s", /* Adresse */
                %s, /* PLZ */
                "%s", /* Stadt */
                "%s", /* Bundesland */
                "%s", /* Land */
                "%s", /* E-Mail */
                "%s", /* Tel */
                "%s" /* Fax */
            );
            """ % (
                table,
                sanitizeInput(record["Id"]) + "-" + sanitizeInput(record["Quelldatei"]),
                sanitizeInput(record["Name"]),
                sanitizeInput(record["Branche"]),
                sanitizeInput(record["Typ"]),
                sanitizeInput(record["Adresse"]),
                sanitizeInput(record["PLZ"]),
                sanitizeInput(record["Stadt"]),
                sanitizeInput(record["Bundesland"]),
                sanitizeInput(record["Land"]),
                sanitizeInput(record["E-Mail"]),
                sanitizeInput(record["Tel"]),
                sanitizeInput(record["Fax"]),
            )
        logger.debug(insertString)
        result = cursor.execute(insertString)
        logger.debug(result)
    except Exception as e:
        logger.critical(".. ERROR")
    else:
        logger.info(".. OK")

def sanitizePhoneNumber(number):
    number = number.replace(" ", "")
    number = number.replace("-", "")
    number = number.replace("/", "")
    number = number.replace("'", "") # Wegen LibreOffice
    return number

def sanitizeInput(input):
    input = input.replace("(", "")
    input = input.replace(")", "")
    input = input.replace("\"", "'")  # !@?!&$!
    return input.strip()

def checkIfFullRecord (record):
    if (not record["Id"]
        or not record["Branche"]
        or not record["Typ"]
        or not record["Adresse"]
        or not record["PLZ"]
        or not record["Land"]):
            logger.error("Not inserting: " + record["Name"])
            return False
    return True

def populateGeneratedFields(record):
    # Alle leerzeichen, bindestriche, klammern etc aus telefon und faxnummer entfernen
    record["Tel"] = sanitizePhoneNumber(record["Tel"])
    record["Fax"] = sanitizePhoneNumber(record["Fax"])
    record["Quelldatei"] = os.path.splitext(csvFile)[0].split("/")[-1]

    # Postleitzahl und Bundesland aus Postleitzahlendatenbank
    record["Stadt"] = plz[record["PLZ"]][0]
    record["Bundesland"] = plz[record["PLZ"]][1]

    return record


logger.info("Creating Table adressdaten: ")
createOrUpdate(table)

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
                # Unvollständige Datensätze werden nicht eingefügt
                if (checkIfFullRecord(record)):
                    record = populateGeneratedFields(record)
                    insertRecord(record, table)

cursor.close()
connection.commit()
connection.close()
