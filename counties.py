import re
import csv

state_regex = re.compile(r's = "([^"]+)"')
county_regex = re.compile(r'c = "([^"]+)"')


with open("source.html", "r") as f_input, open("counties.csv", "w", newline="") as f_output:
    csv_writer = csv.writer(f_output)
    csv_writer.writerow(["State", "County"])
    
    input = [i.strip() for i in f_input.readlines()]
    entry_flag = False
    state = ''
    for line in input:
        if entry_flag: # get county from this line and add to entry
            entry_flag = False
            county = re.search(county_regex, line)
            if not county:
                raise ValueError(f"Invalid Source HTML format: {line}")
            county = county.group(1)
            csv_writer.writerow([state, county])
        else: # search for state
            if 's = "' in line:
                entry_flag = True
                state = re.search(state_regex, line).group(1)
