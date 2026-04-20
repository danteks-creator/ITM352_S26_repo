"""Create scatter plots of fare vs trip miles from Trips from area 8.json."""

import json
from json import JSONDecodeError
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def find_column(df: pd.DataFrame, candidates: tuple[str, ...]) -> str:
	"""Return the first matching column from candidate names."""
	normalized = {column.lower(): column for column in df.columns}
	for candidate in candidates:
		match = normalized.get(candidate.lower())
		if match is not None:
			return match
	raise KeyError(f"Could not find any of these columns: {', '.join(candidates)}")


def load_dataframe(data_file: Path) -> pd.DataFrame:
	"""Load JSON trip records into a DataFrame."""
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
	data_file = Path(__file__).with_name("Trips from area 8.json")
	if not data_file.exists():
		raise FileNotFoundError(
			f"Could not find {data_file.name} in the same folder as Ex5.py."
		)

	df = load_dataframe(data_file)
	fare_col = find_column(df, ("fare", "Fare"))
	miles_col = find_column(df, ("trip_miles", "trip miles", "miles", "Trip Miles", "tripMiles"))

	plot_df = df[[fare_col, miles_col]].copy()
	plot_df[fare_col] = pd.to_numeric(plot_df[fare_col], errors="coerce")
	plot_df[miles_col] = pd.to_numeric(plot_df[miles_col], errors="coerce")
	plot_df = plot_df.dropna()

	if plot_df.empty:
		raise ValueError("No valid fare/trip miles rows found after cleaning.")

	x = plot_df[fare_col]
	y = plot_df[miles_col]

	# (a) Scatter with plt.scatter()
	plt.figure(figsize=(8, 5))
	plt.scatter(x, y)
	plt.title("Fare vs Trip Miles (plt.scatter)")
	plt.xlabel("Fare")
	plt.ylabel("Trip Miles")
	plt.tight_layout()
	plt.savefig("Ex5_scatter_scatter.png")
	plt.close()

	# (b) Same scatter using plt.plot() with no line and point marker
	plt.figure(figsize=(8, 5))
	plt.plot(x, y, linestyle="none", marker=".")
	plt.title("Fare vs Trip Miles (plt.plot, no line)")
	plt.xlabel("Fare")
	plt.ylabel("Trip Miles")
	plt.tight_layout()
	plt.savefig("Ex5_scatter_plot_none.png")
	plt.close()

	# (c) Fancier style
	plt.figure(figsize=(8, 5))
	plt.plot(x, y, linestyle="none", marker="v", color="cyan", alpha=0.2)
	plt.title("Fare vs Trip Miles (Fancy Style)")
	plt.xlabel("Fare")
	plt.ylabel("Trip Miles")
	plt.tight_layout()
	plt.savefig("Ex5_scatter_fancy.png")
	plt.close()

	corr = x.corr(y)
	print(f"Rows plotted: {len(plot_df)}")
	print(f"Correlation (fare vs trip miles): {corr:.3f}")
	print("Saved Ex5_scatter_scatter.png")
	print("Saved Ex5_scatter_plot_none.png")
	print("Saved Ex5_scatter_fancy.png")


if __name__ == "__main__":
	main()
