sentence = input("Enter a sentence: ")

#1. turn a string into a list of words

words = sentence.split(" ")
print("List of words: ", words)

#2. Reverse the lisy

words.reverse()
print("Reversed list of words: ", words)

# 3. join the reversed list back into a string
new_sentence = " ".join(words)
print("Reversed sentence: ", new_sentence)