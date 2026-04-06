import csv
import os

filename = "Taxi_1000.csv"

if os.path.exists(filename):
	with open(filename) as csvfile:
		csv_reader = csv.reader(csvfile)

		total_fare = 0.0
		max_distance = 0.0
		qualifying_count = 0
		total_rows = 0

		for row_number, line in enumerate(csv_reader):
			if row_number == 0:
				fare_index = line.index("Fare")
				distance_index = line.index("Trip Miles")
				continue

			total_rows += 1
			trip_fare = float(line[fare_index])
			trip_distance = float(line[distance_index])

			if trip_fare > 10:
				total_fare += trip_fare
				qualifying_count += 1
				if trip_distance > max_distance:
					max_distance = trip_distance

		if qualifying_count > 0:
			average_fare = total_fare / qualifying_count
			print(f"Rows read: {total_rows}")
			print(f"Rows with fare > $10: {qualifying_count}")
			print(f"Total fare (fare > $10): ${total_fare:.2f}")
			print(f"Average fare (fare > $10): ${average_fare:.2f}")
			print(f"Max trip distance (fare > $10): {max_distance}")
		else:
			print(f"Rows read: {total_rows}")
			print("No trips found with fare greater than $10.")
else:
	print(f"Error: The file '{filename}' does not exist.")