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
                adresse VARCHAR(64) NOT NULL,
                plz INT(4) UNSIGNED NOT NULL,
                stadt VARCHAR(64) NOT NULL,
                land VARCHAR(16) NOT NULL,
                email VARCHAR(64),
                tel VARCHAR(32),
                fax VARCHAR(32),
                PRIMARY KEY (id)
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
                id,
                name,
                branche,
                adresse,
                plz,
                stadt,
                land,
                email,
                tel,
                fax
            ) VALUES (
                "%s", /* Id */
                "%s", /* Name */
                "%s", /* Branche */
                "%s", /* Adresse */
                %s, /* PLZ */
                "%s", /* Stadt */
                "%s", /* Land */
                "%s", /* E-Mail */
                "%s", /* Tel */
                "%s" /* Fax */
            );
            """ % (
                table,
                sanitizeInput(record["Id"].strip()),
                sanitizeInput(record["Name"].strip()),
                sanitizeInput(record["Branche"].strip()),
                sanitizeInput(record["Adresse"].strip()),
                sanitizeInput(record["PLZ"].strip()),
                sanitizeInput(record["Stadt"].strip()),
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

# Alle Unterordner die nicht mit . beginnen enthalten die csvs
for name in os.listdir(workDir):
    if (os.path.isdir(name) and name[0] != "."):
        logger.info("Creating Table %s: " % (name,))
        createOrUpdate(name)

        csvFiles = os.listdir(workDir + "/" + name)
        # Hier werden schon die csvs geladen
        for csvFile in csvFiles:
            # Pfad zur csv
            csvFile = workDir + "/" + name + "/" + csvFile
            # Nur die csvs!
            if (os.path.splitext(csvFile)[1] == ".csv"):
                logger.info("Using File: " + csvFile)
                # csv lesen und parsen
                with open(csvFile, newline='') as csvFileReader:
                    readFile = csv.DictReader(csvFileReader)
                    for record in readFile:
                        # Unvollständige Datensätze werden nicht eingefügt
                        if not record["Id"] or not record["Branche"] or not record["Adresse"] or not record["PLZ"] or not record["Stadt"] or not record["Land"]:
                            logger.error("Not inserting: " + record["Name"])
                        else:
                            # Email, Fax und Telefon sind keine Pflichtfelder
                            if not record["E-Mail"]:
                                record["E-Mail"] = ""
                            elif not record["Tel"]:
                                record["Tel"] = ""
                            elif not record["Fax"]:
                                record["Fax"] = ""
                            
                            # Alle leerzeichen, bindestriche, klammern etc aus telefon und faxnummer entfernen
                            record["Tel"] = sanitizePhoneNumber(record["Tel"])
                            record["Fax"] = sanitizePhoneNumber(record["Fax"])

                            # Die ID ist das Sourcefile + die ID
                            record["Id"] = record["Id"] + os.path.splitext(csvFile)[0].split("/")[-1]
                            insertRecord(record, name)
            else:
                logger.warning("Not using File: " + csvFile)
