# Create a list of tuples that are percentiles of
# household items
import numpy as np

hh_income = [
    (10, 14629),
    (20, 25826),
    (30, 36177),
    (40, 47024),
    (50, 59324),
    (60, 75000),
    (70, 100000),
    (80, 125000),
    (90, 150000),
]

hh_income_array = np.array(hh_income)

# Report the dimensions of the array, and the number of elements in the array
print("Dimensions of the array:", hh_income_array.ndim)
print("Dimensions v2: ", hh_income_array.shape)
print("Number of elements in the array:", hh_income_array.size)

for i in range(len(hh_income_array)):
    print(i, hh_income_array[i][0], hh_income_array[i][1])