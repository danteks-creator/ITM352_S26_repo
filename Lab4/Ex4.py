# try to append to a tuple.     IT WON'T WORK!
# Name: dante Saito
# date: Jan 31, 2026    

survey_respondents = (1012, 1035, 1021, 1053)
print("Original tuple of survey respondents:", survey_respondents)
survey_respondents.append(1054)  # This will raise an AttributeError    
#survey_respondents = survey_respondents + (1054,)
print("after adding 1054:", survey_respondents)
