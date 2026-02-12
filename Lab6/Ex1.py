conditions = ("happy","sad","fear","surprise")

#Write code that uses a conditional expression (do not use an if-statement or ternary expression) to 
#print “true” if the last element is “happy” and there are more than 3 elements, or “false” if it is not.
result = conditions[-1] == "happy" and len(conditions) > 3
print(result)