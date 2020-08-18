#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian @ sebastian - elisa - pfeifer.eu>

# Quit on errors
set -e

# Iterate through all folder
for folder in $(ls -d -1 */); do
  echo "Found folder: ${folder}"
  cd "${folder}"

  # And now check all the files
  for file in $(ls -1); do
    echo "Checking file: ${file}"
    csvlint "${file}"
  done

  cd ..
done
