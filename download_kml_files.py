from urllib.request import urlretrieve
from pathlib import Path

import time
import csv

with open("counties.csv", "r", newline='') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        state, county = row['State'], row['County']
        url = f"https://transition.fcc.gov/fcc-bin/contourplot.kml?state={state}&county={county}&.kml"
        url = url.replace(" ", "+")
        filename = f"Counties/{state}, {county}.kml"
        if Path(filename).exists():
            print(f"Skipping {filename} ...")
            continue

        urlretrieve(url, filename)
        print(f"Downloading {filename} ...")
        time.sleep(0.5)        