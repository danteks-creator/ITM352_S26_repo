# get public license data from the city of chicago's data protal

import pandas as pd
from sodapy import Socrata

#create a sodapy <list> to acccess the city of chicago's data portal
client = Socrata("data.cityofchicago.org", None)

#specify the 10th file for liscence data
json_data = client.get("c7ck-4j2a", limit=500)

results = client.get("c7ck-4j2a", limit=500)
#convert the json data to a pandas dataframe
df = pd.DataFrame.from_records(results)

print(df.head())

vehicles_get_fuel_sources = df["vehicles_get_fuel_sources"].value_counts()

print("vehicles_get_fuel_sources")

