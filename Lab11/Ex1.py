# read in a csv file amd create  a dataframe
# rpint out useful info

import pandas as pd
import numpy as np
import pyarrow as pa

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd.set_option('display.max_columns', None)  # Show all columns

df = pd.read_csv(filename, engine='pyarrow')
df ['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')  # Convert order_date to datetime, coerce errors to NaT

#coerce quantity and unit_price to numeric, setting errors to NaN
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')  
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['sales'] = pd.to_numeric(df['quantity'] * df['unit_price'], errors='coerce')  # Convert sales to numeric, coerce errors to NaN

pivot_table = df.pivot_table(df,
                             index='sales_region')

print(df.head(5))
