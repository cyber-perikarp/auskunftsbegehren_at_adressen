#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

mkdir upload

now=$(TZ=Europe/Vienna date +"%A, %d.%m.%Y %T %:z")
sed -i "s/%%DATE%%/$now/g" .exporter/download.html
mv .exporter/download.html upload/index.html

mv .exporter/style.css upload

figlet "NOYB"
./.exporter/noyb_exporter.py
noybCounter=$(wc -l < noyb.csv)
sed -i "s/%%NOYB_COUNTER%%/$now/g" upload/index.html
mv noyb.csv upload

figlet "GENERAL CSV"
./.exporter/general_csv_exporter.py
generalCounter=$(wc -l < general.csv)
sed -i "s/%%GENERAL_COUNTER%%/$now/g" upload/index.html
mv general.csv upload

figlet "GENERAL HTML"
./.exporter/general_html_exporter.py
mv general.html upload

figlet "GENERAL PDF"
wkhtmltopdf --page-size A4 --enable-local-file-access --footer-left "https://auskunftsbegehren-adressen.cyber-perikarp.eu/" --footer-right "Seite [page] von [topage]" upload/general.html upload/general.pdf

figlet "UPLOAD"
ls -hall upload
