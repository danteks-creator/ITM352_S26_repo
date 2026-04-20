"""Create plots from trip data in Trips from area 8.json."""

import json
from json import JSONDecodeError
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_trip_dataframe(data_file: Path) -> pd.DataFrame:
	"""Load trip data from a JSON file into a DataFrame."""
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

	return pd.DataFrame(records)


def find_column(df: pd.DataFrame, candidates: tuple[str, ...]) -> str:
	"""Find a matching column name using case-insensitive comparison."""
	normalized = {column.lower(): column for column in df.columns}
	for candidate in candidates:
		column = normalized.get(candidate.lower())
		if column is not None:
			return column
	raise KeyError(f"Could not find any of these columns: {', '.join(candidates)}")


def plot_trip_miles_histogram(df: pd.DataFrame) -> None:
	"""Plot a histogram of trip miles."""
	miles_column = find_column(df, ("trip_miles", "trip miles", "miles", "Trip Miles", "tripMiles"))
	miles = pd.to_numeric(df[miles_column], errors="coerce").dropna()

	if miles.empty:
		raise ValueError("No valid trip miles values were found.")

	plt.figure(figsize=(8, 5))
	plt.hist(miles, bins=20, edgecolor="black")
	plt.title("Trip Miles Histogram")
	plt.xlabel("Trip Miles")
	plt.ylabel("Frequency")
	plt.tight_layout()
	plt.savefig("Ex3_trip_miles_histogram.png")
	plt.close()


def plot_payment_tip_totals(df: pd.DataFrame) -> None:
	"""Plot total tips by payment method after dropping rows with missing values."""
	payment_column = find_column(
		df,
		(
			"payment_type",
			"payment type",
			"payment_method",
			"payment method",
			"Payment Type",
		),
	)
	tips_column = find_column(df, ("tips", "tip", "tip_amount", "tip amount", "Tips"))

	summary = df[[payment_column, tips_column]].dropna().copy()
	summary[tips_column] = pd.to_numeric(summary[tips_column], errors="coerce")
	summary = summary.dropna()

	if summary.empty:
		raise ValueError("No valid payment method and tip rows were found after dropping NA values.")

	totals = summary.groupby(payment_column)[tips_column].sum().sort_values(ascending=False)

	plt.figure(figsize=(8, 5))
	plt.bar(totals.index.astype(str), totals.values, edgecolor="black")
	plt.title("Total Tips by Payment Method")
	plt.xlabel("Payment Method")
	plt.ylabel("Sum of Tips")
	plt.xticks(rotation=30, ha="right")
	plt.tight_layout()
	plt.savefig("Ex3_payment_method_tips.png")
	plt.close()


def main() -> None:
	data_file = Path(__file__).with_name("Trips from area 8.json")
	if not data_file.exists():
		raise FileNotFoundError(f"Could not find {data_file.name} in the same folder as Ex3.py.")

	df = load_trip_dataframe(data_file)
	plot_trip_miles_histogram(df)
	plot_payment_tip_totals(df)

	print(f"Loaded {len(df)} trip records.")
	print("Saved Ex3_trip_miles_histogram.png")
	print("Saved Ex3_payment_method_tips.png")


if __name__ == "__main__":
	main()
