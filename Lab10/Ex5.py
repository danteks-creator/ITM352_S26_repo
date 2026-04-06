# Read in a csv file of homes data and create a dataframe
# do some filtering and statistics on the data
import pandas as pd

df_homes = pd.read_csv('homes_data.csv')

#print out the shape of the dataframe and the first few rows
shape = df_homes.shape
print(f"the homes data has {shape[0]} rows and {shape[1]} columns")
print("\nFirst few rows:")
print(df_homes.head())

#select only the properties with 500 or more units
df_big_properties = df_homes[df_homes['units'] >= 500]
df_big_properties = df_big_properties.drop(columns=["id", "easement"])
print(df_big_properties.head(10))

# convert columns to appropriate data types
df_big_properties["sale_price"] = pd.to_numeric(df_big_properties["sale_price"], errors='coerce')
df_big_properties["land_sqfft"] = pd.to_numeric(df_big_properties["land_sqft"], errors='coerce')
df_big_properties["gross_sqft"] = pd.to_numeric(df_big_properties["gross_sqft"], errors='coerce')

#drop rows with missing values in the numeric columns
df_big_properties = df_big_properties.dropna()

#drop duplicate rows
df_big_properties = df_big_properties.drop_duplicates()

#print out the first 10 rows after cleaning
df_big_properties.head(10)
print(f"Number of big properties after cleaning: {len(df_big_properties)}")

# filter out zero sales
df_big_properties = df_big_properties[df_big_properties["sale_price"] > 0]
print(f"Number of big properties with non-zero sales: {len(df_big_properties)}")

#calulcate the average sales price per square feet for the big properties
df_big_properties["price_per_sqft"] = df_big_properties["sale_price"] / df_big_properties["gross_sqft"]
average_price_per_sqft = df_big_properties["price_per_sqft"].mean()
print(f"Average price per square foot for big properties: ${average_price_per_sqft:.2f}")