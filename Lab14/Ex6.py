"""Create a 3D plot of fare, trip miles, and dropoff area from trip data."""

import json
from json import JSONDecodeError
from pathlib import Path

import matplotlib
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D

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


def load_dataframe(data_file: Path) -> pd.DataFrame:
	"""Load the JSON file into a DataFrame."""
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
			f"Could not find {data_file.name} in the same folder as Ex6.py."
		)

	df = load_dataframe(data_file)

	fare_col = find_column(df, ("fare", "Fare"))
	miles_col = find_column(df, ("trip_miles", "trip miles", "miles", "Trip Miles", "tripMiles"))
	dropoff_col = find_column(
		df,
		(
			"dropoff_community_area",
			"dropoff community area",
			"dropoff_area",
			"dropoff area",
			"Dropoff Community Area",
		),
	)

	clean = df[[fare_col, miles_col, dropoff_col]].copy()
	clean[fare_col] = pd.to_numeric(clean[fare_col], errors="coerce")
	clean[miles_col] = pd.to_numeric(clean[miles_col], errors="coerce")
	clean[dropoff_col] = pd.to_numeric(clean[dropoff_col], errors="coerce")
	clean = clean.dropna()

	if clean.empty:
		raise ValueError("No valid fare, trip miles, and dropoff area rows found after cleaning.")

	# Keep the explicit Axes3D import as requested by the assignment.
	_ = Axes3D

	fig = plt.figure(figsize=(10, 7))
	ax = fig.add_subplot(111, projection="3d")
	ax.scatter(
		clean[fare_col],
		clean[miles_col],
		clean[dropoff_col],
		c=clean[dropoff_col],
		cmap="viridis",
		alpha=0.55,
		s=12,
	)
	ax.set_title("3D Plot: Fare, Trip Miles, and Dropoff Area")
	ax.set_xlabel("Fare")
	ax.set_ylabel("Trip Miles")
	ax.set_zlabel("Dropoff Area")
	plt.tight_layout()
	plt.savefig("Ex6_3d_fare_miles_dropoff.png")
	plt.close()

	print(f"Rows plotted: {len(clean)}")
	print("Saved plot to Ex6_3d_fare_miles_dropoff.png")


if __name__ == "__main__":
	main()
