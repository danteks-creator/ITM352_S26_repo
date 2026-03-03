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

#Rewrite the determine_progress1 function without using nested if-statements. 
#Do not use elif or else. Call it determine_progress2. 
#Use your test cases to ensure the function works as expected

def determine_progress2(hits, spins):
	if spins == 0:
		return "Get going!"
	
	hits_spins_ratio = hits / spins
 
	if hits_spins_ratio <= 0:
		return "Get going!"
	
	if hits_spins_ratio < 0.25:
		return "On your way!"
	
	if hits_spins_ratio < 0.5:
		return "Almost there!"
	
	if hits < spins:
		return "You win!"
	
	return "Almost there!"  # Covers the case when hits >= spins (ratio >= 0.5)


def determine_progress3(hits, spins):
	if spins == 0:
		return "Get going!"
	
	hits_spins_ratio = hits / spins
 
	if hits_spins_ratio <= 0:
		return "Get going!"
	elif hits_spins_ratio < 0.25:
		return "On your way!"
	elif hits_spins_ratio < 0.5:
		return "Almost there!"
	elif hits < spins:
		return "You win!"
	else:
		return "Almost there!"


def determine_progress4(hits, spins):
	"""
	Uses a list of progress messages and computes the appropriate index
	based on the conditional logic.
	"""
	progress_messages = ["Get going!", "On your way!", "Almost there!", "You win!"]
	
	if spins == 0:
		return progress_messages[0]
	
	hits_spins_ratio = hits / spins
	
	# Compute index based on conditional expressions
	if hits_spins_ratio <= 0:
		index = 0
	elif hits_spins_ratio < 0.25:
		index = 1
	elif hits_spins_ratio < 0.5:
		index = 2
	elif hits < spins:
		index = 3
	else:
		index = 2
	
	return progress_messages[index]


def determine_progress5_compact(hits, spins):
	"""
	More compact version using a single conditional expression to compute the index.
	"""
	progress_messages = ["Get going!", "On your way!", "Almost there!", "You win!"]
	
	if spins == 0:
		return progress_messages[0]
	
	hits_spins_ratio = hits / spins
	
	# Single expression to compute the index
	index = (
		0 if hits_spins_ratio <= 0 else
		1 if hits_spins_ratio < 0.25 else
		2 if hits_spins_ratio < 0.5 else
		3 if hits < spins else
		2
	)
	
	return progress_messages[index]


# Test all versions
test_determine_progress(determine_progress1)
test_determine_progress(determine_progress2)
test_determine_progress(determine_progress3)
test_determine_progress(determine_progress4)
test_determine_progress(determine_progress5_compact)


def determine_progress6(hits, spins):
	"""
	Uses a dictionary-based approach with lambda functions.
	No if-statements used - instead uses a list of (condition, message) tuples.
	Evaluates conditions in order and returns the first matching message.
	"""
	if spins == 0:
		return "Get going!"
	
	hits_spins_ratio = hits / spins
	
	# List of (condition, message) tuples evaluated in order
	conditions = [
		(hits_spins_ratio <= 0, "Get going!"),
		(hits_spins_ratio < 0.25, "On your way!"),
		(hits_spins_ratio < 0.5, "Almost there!"),
		(hits < spins, "You win!"),
	]
	
	# Return the message for the first true condition, default to "Almost there!"
	return next((msg for condition, msg in conditions if condition), "Almost there!")


def determine_progress7(hits, spins):
	"""
	Alternative approach using a clean list-based rule system.
	Each rule is a tuple of (condition_checker, message).
	Different style from determine_progress6.
	"""
	if spins == 0:
		return "Get going!"
	
	hits_spins_ratio = hits / spins
	
	# Define rules as a data structure
	rules = [
		(lambda r: r <= 0, "Get going!"),
		(lambda r: r < 0.25, "On your way!"),
		(lambda r: r < 0.5, "Almost there!"),
		(lambda r: hits < spins, "You win!"),  # Special condition for this one
	]
	
	# Evaluate rules in a clean functional style
	for checker, message in rules:
		try:
			# Pass ratio to simple conditions, but notice 4th rule uses hits directly
			if checker(hits_spins_ratio):
				return message
		except:
			continue
	
	return "Almost there!"


# Test the new no-if-statement versions
test_determine_progress(determine_progress6)