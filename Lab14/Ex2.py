"""Create a histogram of trip miles from a JSON data file."""

import json
from json import JSONDecodeError
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_trip_miles(data_file: Path) -> list[float]:
	"""Load trip mile values from a JSON file."""
	raw_text = data_file.read_text(encoding="utf-8-sig").strip()
	if not raw_text:
		raise ValueError(f"{data_file} is empty.")

	try:
		records = json.loads(raw_text)
	except JSONDecodeError as exc:
		raise ValueError(
			f"Invalid JSON in {data_file} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
		) from exc

	if not isinstance(records, list):
		raise ValueError("Expected the JSON file to contain a list of trip records.")

	possible_keys = ("trip_miles", "trip miles", "miles", "Trip Miles", "tripMiles")
	trip_miles: list[float] = []

	for record in records:
		if isinstance(record, dict):
			value = None
			for key in possible_keys:
				if key in record:
					value = record[key]
					break

			if value is None:
				continue

			try:
				trip_miles.append(float(value))
			except (TypeError, ValueError):
				continue

	if not trip_miles:
		raise ValueError(
			"No trip mile values were found. Check that the JSON file contains a field named "
			"trip_miles, trip miles, miles, Trip Miles, or tripMiles."
		)

	return trip_miles


def main() -> None:
	data_file = Path(__file__).with_name("Trips from area 8.json")
	if not data_file.exists():
		raise FileNotFoundError(
			f"Could not find {data_file.name} in the same folder as Ex3.py."
		)

	trip_miles = load_trip_miles(data_file)

	plt.hist(trip_miles, bins=20, edgecolor="black")
	plt.title("Trip Miles Histogram")
	plt.xlabel("Trip Miles")
	plt.ylabel("Frequency")
	plt.tight_layout()
	plt.savefig("Ex3_histogram.png")
	print(f"Created histogram from {len(trip_miles)} trip mile values.")
	print("Saved plot to Ex3_histogram.png")


if __name__ == "__main__":
	main()

