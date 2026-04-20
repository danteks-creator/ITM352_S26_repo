"""Create a heatmap from pickup and dropoff community areas."""

from pathlib import Path

import matplotlib
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def find_column(df: pd.DataFrame, candidates: tuple[str, ...]) -> str:
	"""Return the first matching column name using case-insensitive lookup."""
	normalized = {column.lower(): column for column in df.columns}
	for candidate in candidates:
		match = normalized.get(candidate.lower())
		if match is not None:
			return match
	raise KeyError(f"Could not find any of these columns: {', '.join(candidates)}")


def main() -> None:
	csv_file = Path(__file__).with_name("taxi trips Fri 7_7_2017.csv")
	if not csv_file.exists():
		raise FileNotFoundError(
			f"Could not find {csv_file.name} in the same folder as Ex8.py."
		)

	df = pd.read_csv(csv_file)

	pickup_col = find_column(
		df,
		(
			"pickup_community_area",
			"pickup community area",
			"Pickup Community Area",
		),
	)
	dropoff_col = find_column(
		df,
		(
			"dropoff_community_area",
			"dropoff community area",
			"Dropoff Community Area",
		),
	)

	areas = df[[pickup_col, dropoff_col]].copy()
	areas[pickup_col] = pd.to_numeric(areas[pickup_col], errors="coerce")
	areas[dropoff_col] = pd.to_numeric(areas[dropoff_col], errors="coerce")
	areas = areas.dropna()

	if areas.empty:
		raise ValueError("No valid pickup/dropoff rows remain after dropping missing values.")

	# Use integer area IDs for a clean matrix index/columns.
	areas[pickup_col] = areas[pickup_col].astype(int)
	areas[dropoff_col] = areas[dropoff_col].astype(int)

	matrix = pd.crosstab(areas[pickup_col], areas[dropoff_col])

	plt.figure(figsize=(12, 10))
	sns.heatmap(matrix, cmap="YlGnBu")
	plt.title("Taxi Trips Heatmap: Pickup vs Dropoff Community Area")
	plt.xlabel("Dropoff Community Area")
	plt.ylabel("Pickup Community Area")
	plt.tight_layout()
	plt.savefig("Ex8_pickup_dropoff_heatmap.png")
	plt.close()

	print(f"Rows used for heatmap: {len(areas)}")
	print("Saved plot to Ex8_pickup_dropoff_heatmap.png")


if __name__ == "__main__":
	main()
