from bs4 import BeautifulSoup
from jinja2 import Template
from pathlib import Path

with open("kml_template.jinja") as f_template:
    template = Template(f_template.read())

def format_county_kml(kml_file_name):
    with open(kml_file_name, "r") as f_kml:
        soup = BeautifulSoup(f_kml, 'xml')

        # retrieve county name for jinja2 template
        name = soup.find("name").get_text()

        # prepare placemarks for insertion into jinja2 template
        # - a county can include multiple placemarks/boundaries
        boundaries = []
        for boundary in soup.find_all("Placemark"):
            # do not include Point placemark
            if boundary.find("Point"):
                continue
            # remove style (will be applied in Google My Maps anyways)
            boundary.find('styleUrl').extract()

            # replace line boundary with polygon for optional shading
            boundary = str(boundary)
            boundary = boundary.replace("<LineString>", "<Polygon><outerBoundaryIs><LinearRing>")
            boundary = boundary.replace("</LineString>", "</LinearRing></outerBoundaryIs></Polygon>")
            boundaries.append(boundary)
        return boundaries

def render_template(state, boundaries):
    with open(f"Grouped Counties/{state} Counties.kml", "w") as f_output:
        f_output.write(template.render(name=f"{state} Counties", placemarks='\n\n'.join(boundaries)))
    print(f"finished {state}...")

# creates KML file county map for each state
state = "AK" # first state alphabetically
boundaries = []
for file in sorted(Path("Counties/").iterdir()):
    if not file.is_file() or ".kml" not in file.name:
        continue
    cur_state = file.name[:2]
    if state != cur_state:
        render_template(state=state, boundaries=boundaries)
        boundaries = []
        state = cur_state
    boundaries.extend(format_county_kml(file))
    
render_template(state=state, boundaries=boundaries)