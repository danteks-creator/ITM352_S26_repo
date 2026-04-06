# read in a csv file amd create  a dataframe
# rpint out useful info

import pandas as pd
import numpy as np
import pyarrow as pa

filename = "https://drive.google.com/uc?id=1ujY0WCcePdotG2xdbLyeECFW9lCJ4t-K"

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.float_format', '{:,.2f}'.format)  # Format float numbers to 2 decimal places

df = pd.read_csv(filename, engine='pyarrow')
df ['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')  # Convert order_date to datetime, coerce errors to NaT

#coerce quantity and unit_price to numeric, setting errors to NaN
df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')  
df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')
df['sales'] = pd.to_numeric(df['quantity'] * df['unit_price'], errors='coerce')  # Convert sales to numeric, coerce errors to NaN

# support common state column names used in class datasets
state_col = 'customer_state'

pivot_table = df.pivot_table(
                            values='sales', 
                            index= 'sales_region', 
                            columns='order_type', 
                            aggfunc=[np.sum, np.mean],
                            margins=True, 
                            margins_name='Total Sales')

print(pivot_table)