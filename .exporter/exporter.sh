#!/usr/bin/env bash
# Sebastian Elisa Pfeifer <sebastian@sebastian-elisa-pfeifer.eu>

# Quit on errors
set -e

# We are in a subfolder
cd $TRAVIS_BUILD_DIR

mkdir upload

figlet "NOYB"
./.exporter/noyb_exporter.py
mv noyb.csv upload

figlet "GENERAL"
./.exporter/general_exporter.py
mv general.csv upload

cat <<EOF >> upload/index.html
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<style>body{margin:40px auto;max-width:650px;line-height:1.6;font-size:18px;color:#444;padding:0 10px}h1,h2,h3{line-height:1.2}</style>
	<title>Datensatzdownload</title>
</head>
<body>
	<h1>
		Datensatzdownload
	</h1>
	<h2>
		Letztes Update: $(TZ=Europe/Vienna date +"%A, %m.%d.%Y %T %:z")
	</h2>
  <ul>
    <li>
      <a href="noyb.csv">
        Aufbereitet für NOYB
      </a>
    </li>
		<li>
      <a href="general.csv">
        Genereller Export
      </a>
    </li>
  </ul>
</body>
</html>
EOF

figlet "UPLOAD"
ls -hall upload
