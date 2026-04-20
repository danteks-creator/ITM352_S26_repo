# scrape data from the city of chicago's data portal
# print any line that has the <title> tag in it

import urllib.request
url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"

print ("Opening URL: " + url)
web_page = urllib.request.urlopen(url)

#iterate through each line in the web page, searching for the <title> tag
for line in web_page:
    line = line.decode("utf-8") # decode the line from bytes to a string
    if "<title>" in line: 
        print(line.strip()) # print the line, removing any leading/trailing whitespace

        