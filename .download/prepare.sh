#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

mkdir upload
mkdir qrcodes

now=$(TZ=Europe/Vienna date +"%A, %d.%m.%Y %T %:z")
sed -i "s/%%DATE%%/$now/g" .download/index.html

rsync -avP .download/ upload/

find upload/js/ -type f \
    -name "*.js" ! -name "*.min.*" ! -name "vfs_fonts*" \
    -exec echo {} \; \
    -exec uglifyjs {} --comments -c -m -o {} \;

find upload/css/ -type f \
    -name "*.css" ! -name "*.min.*" \
    -exec echo {} \; \
    -exec uglifycss {} --output {} \;
