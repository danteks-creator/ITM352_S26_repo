responses = [5, 7, 3, 8]
respondent_Ids = [1012, 1035, 1021, 1052]

survey_dict = dict(zip(respondent_Ids, responses))
print("survey responses with respondent IDs:", survey_dict)

print(f"respondent {respondent_Ids[2]} gave a response of {survey_dict[respondent_Ids[2]]}." 
)