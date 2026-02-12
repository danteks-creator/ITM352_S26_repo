def determine_progress1(hits, spins):
	if spins == 0:
		return "Get going!"
	
	hits_spins_ratio = hits / spins
 
	if hits_spins_ratio > 0:
		progress = "On your way!"
		if hits_spins_ratio >= 0.25:
			progress = "Almost there!"
			if hits_spins_ratio >= 0.5:
				if hits < spins:
					progress = "You win!"
	else:
		progress = "Get going!"
 
	return progress


def test_determine_progress(determine_progress_func):
	"""
	Test function that uses assert to check all possible return values.
	Takes the determine_progress function as an argument.
	"""
	
	# Test case 1: "Get going!" - when spins == 0
	assert determine_progress_func(0, 0) == "Get going!", "Failed: spins == 0"
	assert determine_progress_func(5, 0) == "Get going!", "Failed: any hits with spins == 0"
	
	# Test case 2: "Get going!" - when hits_spins_ratio <= 0 (hits == 0, spins > 0)
	assert determine_progress_func(0, 10) == "Get going!", "Failed: 0 hits with positive spins"
	assert determine_progress_func(0, 1) == "Get going!", "Failed: 0/1 ratio"
	
	# Test case 3: "On your way!" - when 0 < ratio < 0.25
	assert determine_progress_func(1, 10) == "On your way!", "Failed: ratio 0.1"
	assert determine_progress_func(2, 10) == "On your way!", "Failed: ratio 0.2"
	assert determine_progress_func(1, 5) == "On your way!", "Failed: ratio 0.2"
	
	# Test case 4: "Almost there!" - when 0.25 <= ratio < 0.5
	assert determine_progress_func(25, 100) == "Almost there!", "Failed: ratio 0.25"
	assert determine_progress_func(3, 10) == "Almost there!", "Failed: ratio 0.3"
	assert determine_progress_func(4, 10) == "Almost there!", "Failed: ratio 0.4"
	
	# Test case 5: "You win!" - when ratio >= 0.5 AND hits < spins
	assert determine_progress_func(5, 10) == "You win!", "Failed: ratio 0.5, hits < spins"
	assert determine_progress_func(6, 10) == "You win!", "Failed: ratio 0.6, hits < spins"
	assert determine_progress_func(50, 100) == "You win!", "Failed: ratio 0.5 exactly"
	assert determine_progress_func(99, 100) == "You win!", "Failed: ratio 0.99, hits < spins"
	
	# Edge case: "Almost there!" - when hits == spins (ratio = 1.0, but NOT hits < spins)
	# This reveals a bug: when hits == spins, ratio >= 0.5 but hits < spins is False
	assert determine_progress_func(10, 10) == "Almost there!", "Failed: hits == spins"
	
	# Edge case: "Almost there!" - when hits > spins (impossible in real scenario but tests logic)
	assert determine_progress_func(15, 10) == "Almost there!", "Failed: hits > spins"
	
	print("All tests passed!")


# Run the test function
test_determine_progress(determine_progress1)

