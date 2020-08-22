#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

mkdir upload

figlet "NOYB"
./.exporter/noyb_exporter.py
mv noyb.csv upload

figlet "GENERAL CSV"
./.exporter/general_csv_exporter.py
mv general.csv upload

figlet "GENERAL MD"
./.exporter/general_markdown_exporter.py
mv general.md upload

now=$(TZ=Europe/Vienna date +"%A, %m.%d.%Y %T %:z")
sed -i "s/%%DATE%%/$now/g" .exporter/download.html
mv .exporter/download.html upload/index.html

figlet "UPLOAD"
ls -hall upload
