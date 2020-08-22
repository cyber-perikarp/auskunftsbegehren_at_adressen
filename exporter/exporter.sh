#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

mkdir upload
figlet "NOYB"
./exporter/noyb_exporter.py
mv noyb.csv upload

cat <<EOF >> upload/index.html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Download</title>
</head>
<body>
  <ul>
    <li>
      <a href="noyb.csv">
        Aufbereitet für NOYB
      </a>
    </li>
  </ul>
</body>
</html>
EOF

figlet "UPLOAD"
ls -hall upload
