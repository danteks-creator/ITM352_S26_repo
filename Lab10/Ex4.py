# read a json file of taxi trip data and create a data frame
# calculate the median fare
import json
from json import JSONDecodeError
from pathlib import Path
import pandas as pd

data_file = Path(__file__).with_name('Taxi_Trips.json')

try:
	raw_text = data_file.read_text(encoding='utf-8-sig').strip()
	if not raw_text:
		raise ValueError(f'{data_file} is empty.')

	records = json.loads(raw_text)
	taxi_df = pd.DataFrame(records)
except JSONDecodeError as exc:
	raise ValueError(
		f'Invalid JSON in {data_file} at line {exc.lineno}, column {exc.colno}: {exc.msg}'
	) from exc

fare = taxi_df['fare']

print('Fare summary statistics:')
print('Count:', fare.count())
print('Mean:', fare.mean())
print('Median:', fare.median())
print('Min:', fare.min())
print('Max:', fare.max())
print('Std Dev:', fare.std())
print('Variance:', fare.var())
print('25th percentile:', fare.quantile(0.25))
print('75th percentile:', fare.quantile(0.75))