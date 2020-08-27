#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

now=$(TZ=Europe/Vienna date +"%A, %d.%m.%Y %T %:z")
sed -i "s/%%DATE%%/$now/g" .exporter/index.html
mv .download/index.html upload/index.html

mv .download/style.css upload
mv .download/filter.js upload
mv .download/mini-default.min.css upload
