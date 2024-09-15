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

def render_template(county, boundaries):
    with open(f"Formatted Counties/{county}.kml", "w") as f_output:
        f_output.write(template.render(name=f"{county}", placemarks='\n\n'.join(boundaries)))
    print(f"finished {county}...")

# creates KML file county map for each county
boundaries = []
for file in sorted(Path("Counties/").iterdir()):
    if not file.is_file() or ".kml" not in file.name:
        continue
    cur_county = file.name[:-4]
    render_template(county=cur_county, boundaries=format_county_kml(file))