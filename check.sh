#!/usr/bin/env bash

for folder in $(ls -d -1 */); do
  echo "Found folder: ${folder}"
  cd "${folder}"

  for file in $(ls -1); do
    echo "Checking file: ${file}"
    ~/go/bin/csvlint "${file}"
  done

  cd ..
done
