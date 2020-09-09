#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

echo "NOYB"
./.exporter/noyb_exporter.py
noybCounter=$(wc -l < noyb.csv)
sed -i "s/%%NOYB_COUNTER%%/$noybCounter/g" upload/index.html
mv noyb.csv upload

echo "GENERIC CSV"
./.exporter/generic_csv_exporter.py
generalCounter=$(wc -l < generic.csv)
sed -i "s/%%GENERIC_COUNTER%%/$generalCounter/g" upload/index.html
mv generic.csv upload

echo "GENERIC HTML"
./.exporter/generic_html_exporter.py
mv generic.html upload
mv qrcodes upload

echo "GENERIC PDF"
weasyprint upload/generic.html upload/generic.pdf

echo "UPLOAD"
ls -hall upload
