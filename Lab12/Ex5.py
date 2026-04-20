# get a json file from the city of chicago's data portal and analyze the driver types

from re import search

import pandas as pd
import requests

#create a query to get the data from the city of chicago's data portal

search_results = requests.get("https://data.cityofchicago.org/resource/c7ck-4j2a.json?$limit=500")

results_json = search_results.json()
#convert the json data to a pandas dataframe
df = pd.DataFrame.from_records(results_json)
print(df.head())
#count the number of different driver types in the data
driver_types = df["driver_types"].value_counts()
print("driver_types")
