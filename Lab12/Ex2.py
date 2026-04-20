# Grab data one month interest data from the treasury website
import ssl
import pandas as pd
import urllib.request
import lxml

url = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202603"

# open the url and use it to read html into a dataframe 
ssl._create_default_https_context = ssl._create_unverified_context

print ("Opening URL: " + url)
web_page = urllib.request.urlopen(url)
data_frame = pd.read_html(web_page, header=0)[0]

# print(data_frame(0).info())
# print(data_frame(0))

#extract the 1 month interest rate data
one_month_data = data_frame[0].loc[:, "1 Mo"]
print(f"One month interest rate data: \n{one_month_data}")






