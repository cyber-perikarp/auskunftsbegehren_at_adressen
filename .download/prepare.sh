#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

now=$(TZ=Europe/Vienna date +"%A, %d.%m.%Y %T %:z")
sed -i "s/%%DATE%%/$now/g" .download/index.html
cp .download/index.html upload/index.html

cp .download/style.css upload
cp .download/jquery-3.5.1.min.js upload
cp .download/filter.js upload
cp .download/mini-default.min.css upload
