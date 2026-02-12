trip_duration = [1.1, 0.5, 2.5, 2.6]
trip_Fare = (5.5, 3.0, 10.0, 8.0)


taxiTrips = {
"miles": trip_duration,
"fares": trip_Fare
}

print(taxiTrips)

print(f"The third trip was {taxiTrips['miles'][2]} miles long.")
print(f" the fare for the third trip was ${taxiTrips['fares'][2]:.2f}.")
