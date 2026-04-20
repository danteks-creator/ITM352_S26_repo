"""Create a scatter plot of fare vs tips from trip data."""

import json
from json import JSONDecodeError
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def find_column(df: pd.DataFrame, candidates: tuple[str, ...]) -> str:
	"""Find a matching column name using case-insensitive lookup."""
	normalized = {column.lower(): column for column in df.columns}
	for candidate in candidates:
		matched = normalized.get(candidate.lower())
		if matched is not None:
			return matched
	raise KeyError(f"Could not find any of these columns: {', '.join(candidates)}")


def load_dataframe(data_file: Path) -> pd.DataFrame:
	"""Load trip JSON file into a DataFrame."""
	raw_text = data_file.read_text(encoding="utf-8-sig").strip()
	if not raw_text:
		raise ValueError(f"{data_file.name} is empty.")

	try:
		records = json.loads(raw_text)
	except JSONDecodeError as exc:
		raise ValueError(
			f"Invalid JSON in {data_file.name} at line {exc.lineno}, column {exc.colno}: {exc.msg}"
		) from exc

	if not isinstance(records, list):
		raise ValueError("Expected the JSON file to contain a list of trip records.")

	return pd.DataFrame(records)


def main() -> None:
	data_file = Path(__file__).with_name("Trips_Fri07072017T4 trip_miles gt1.json")
	if not data_file.exists():
		raise FileNotFoundError(
			f"Could not find {data_file.name} in the same folder as Ex4.py."
		)

	df = load_dataframe(data_file)

	fare_col = find_column(df, ("fare", "Fare"))
	tips_col = find_column(df, ("tips", "tip", "tip_amount", "tip amount", "Tips"))

	plot_df = df[[fare_col, tips_col]].copy()
	plot_df[fare_col] = pd.to_numeric(plot_df[fare_col], errors="coerce")
	plot_df[tips_col] = pd.to_numeric(plot_df[tips_col], errors="coerce")
	plot_df = plot_df.dropna()

	if plot_df.empty:
		raise ValueError("No valid fare/tip rows found after cleaning.")

	plt.figure(figsize=(8, 5))
	plt.scatter(plot_df[fare_col], plot_df[tips_col], alpha=0.6, edgecolors="none")
	plt.title("Fare vs Tips Scatter Plot")
	plt.xlabel("Fare")
	plt.ylabel("Tips")
	plt.tight_layout()
	plt.savefig("Ex4_fare_tips_scatter.png")
	plt.close()

	corr = plot_df[fare_col].corr(plot_df[tips_col])
	print(f"Rows plotted: {len(plot_df)}")
	print(f"Correlation (fare vs tips): {corr:.3f}")
	print("Saved scatter plot to Ex4_fare_tips_scatter.png")


if __name__ == "__main__":
	main()
