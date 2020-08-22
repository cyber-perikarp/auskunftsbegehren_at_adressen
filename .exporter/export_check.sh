#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

sum=0

cd upload

# And now check all the files
for file in $(ls -1 *.csv); do
  echo "Checking file: ${file}"

  # Count the lines in the file
  tmp=$(wc -l < ${file})
  lines=$(echo "${tmp}-1" | bc)
  echo "file contains ${lines} entries"

  # Check the file
  /tmp/go/bin/csvlint "${file}"

  # Add number of entries to total sum
  sum=$(echo "${sum}+${lines}" | bc)

  echo -e "\r"
done

echo "Number of entries: ${sum}"
figlet "EXPORT CHECK"
figlet "PASSED"
