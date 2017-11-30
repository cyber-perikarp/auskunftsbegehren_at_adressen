#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import argparse
import logging
import chromalog
import csv
import MySQLdb as db

chromalog.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger()

# In diesem Ordner sind wir
workDir = os.getcwd()

# CLI Parameter
parser = argparse.ArgumentParser("convert-to-sql.py")
parser.add_argument("host", help="Datenbankserver")
parser.add_argument("username", help="Datenbankbenutzer")
parser.add_argument("password", help="Datenbankpasswort")
parser.add_argument("database", help="Datenbank")

args = vars(parser.parse_args())

# Postleitzahlendatenbank einlesen
plzDatei = open('plz_verzeichnis.csv', newline='')
plz = csv.DictReader(plzDatei)

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
                id INT(5) NOT NULL UNIQUE AUTO_INCREMENT,
                idfile INT(5) NOT NULL,
                quelldatei VARCHAR(64) NOT NULL,
                name VARCHAR(128) NOT NULL,
                branche VARCHAR(32) NOT NULL,
                typ VARCHAR(32) NOT NULL,
                adresse VARCHAR(64) NOT NULL,
                plz INT(4) UNSIGNED NOT NULL,
                stadt VARCHAR(64) NOT NULL,
                land VARCHAR(16) NOT NULL,
                email VARCHAR(64),
                tel VARCHAR(32),
                fax VARCHAR(32),
                CONSTRAINT PK_table PRIMARY KEY (id,idfile,quelldatei)
            ) CHARACTER SET utf8 COLLATE utf8_general_ci;"""
            % (table,))
        logger.debug("Created.")
    else:
        cursor.execute("DROP TABLE %s;" % (table,))
        logger.debug("Deleted.")
        createOrUpdate(table)

def insertRecord(record, table):
    logger.info("Inserting Record: ".rstrip('\n') + record["Name"])
    try:
        insertString = """
            INSERT INTO %s (
                idfile,
                quelldatei,
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
                %s, /* Id aus der Datei */
                "%s", /* Dateiname */
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
                sanitizeInput(record["Id"].strip()), # Das heißt zwar ID, ist aber IDFile
                sanitizeInput(record["quelldatei"].strip()),
                sanitizeInput(record["Name"].strip()),
                sanitizeInput(record["Branche"].strip()),
                sanitizeInput(record["Typ"].strip()),
                sanitizeInput(record["Adresse"].strip()),
                sanitizeInput(record["PLZ"].strip()),
                sanitizeInput(record["Stadt"].strip()),
                sanitizeInput(record["Bundesland"].strip()),
                sanitizeInput(record["Land"].strip()),
                sanitizeInput(record["E-Mail"].strip()),
                sanitizeInput(record["Tel"].strip()),
                sanitizeInput(record["Fax"].strip()),
            )
        cursor.execute(insertString)
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
    return input

def checkIfFullRecord (record):
    if (not record["Id"]
        or not record["Branche"]
        or not record["Typ"]
        or not record["Adresse"]
        or not record["PLZ"]
        or not record["Stadt"]
        or not record["Land"]):
            logger.error("Not inserting: " + record["Name"])
            return False
    return True

def populateGeneratedFields(record):
    # Alle leerzeichen, bindestriche, klammern etc aus telefon und faxnummer entfernen
    record["Tel"] = sanitizePhoneNumber(record["Tel"])
    record["Fax"] = sanitizePhoneNumber(record["Fax"])
    record["quelldatei"] = os.path.splitext(csvFile)[0].split("/")[-1]

    # Postleitzahl und Bundesland aus Postleitzahlendatenbank
    PLZEintrag = [x for x in plz if x["PLZ"] == record["PLZ"]][0]
    record["Stadt"] = PLZEintrag["Ort"]
    record["Bundesland"] = PLZEintrag["Bundesland"]

    return record


# Alle Unterordner die nicht mit . beginnen enthalten die csvs
for table in [x for x in os.listdir(workDir) if (os.path.isdir(x) and x[0] != ".")]:
    logger.info("Creating Table %s: " % (table,))
    createOrUpdate(table)

    # Hier werden schon die csvs geladen
    for csvFile in [x for x in os.listdir(workDir + "/" + table) if os.path.splitext(x)[1] == ".csv"]:
        # Pfad zur csv
        csvFile = workDir + "/" + table + "/" + csvFile
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
connection.close()
