#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

find upload/css/ -type f \
    -name "*.css" ! -name "*.min.*" \
    -exec uglifycss {} --output {} \;

find upload/ -type f \
    -name "*.html" ! -name "*.html.*" \
    -exec minify {} --type html -o {} \;

rm -rf upload/*.sh
