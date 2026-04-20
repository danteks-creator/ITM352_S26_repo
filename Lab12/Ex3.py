# parse the ITM department website to find the people (facuty, grad, lecturer)
import urllib.request
from bs4 import BeautifulSoup

ITM_url = "https://shidler.hawaii.edu/itm/people"

ITM_html = urllib.request.urlopen(ITM_url)
html_to_parse = BeautifulSoup(ITM_html, "html.parser")

print(html_to_parse.prettify())

# find and print just the names of the faculty members
line_of_faculty = html_to_parse.find_all("div", class_="views-field views-field-title")

itm_faculty = []
for person in list(line_of_faculty):
    name = person.find("a").text.strip()
    itm_faculty.append(name)
print("ITM Faculty: ")
print(itm_faculty)

