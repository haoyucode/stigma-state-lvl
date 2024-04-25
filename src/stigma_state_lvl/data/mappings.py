""" 
mappings for replacing source variable values
with desired analytic values (e.g., categories to numeric for scale scores)

"""


likert_value_map = {
    "Strongly disagree": 1,
    "Somewhat disagree": 2,
    "Neither disagree nor agree": 3,
    "Somewhat agree": 4,
    "Strongly agree": 5,
}

reverse_likert_value_map = {
    "Strongly disagree": 5,
    "Somewhat disagree": 4,
    "Neither disagree nor agree": 3,
    "Somewhat agree": 2,
    "Strongly agree": 1,
}

stigma6 = {
    "ss_a_historywork":reverse_likert_value_map,
    "ss_b_historymarry":reverse_likert_value_map,
    "ss_c_currentwork":reverse_likert_value_map,
    "ss_d_currentmarry":reverse_likert_value_map,
    "ss_e_dangerous":likert_value_map,
    "ss_f_trust":likert_value_map
}


stigma10 = {
    **stigma6,
    "ss_historysteal":likert_value_map,
    "ss_historyhighrisk":likert_value_map,
    "ss_currentsteal":likert_value_map,
    "ss_currenthighrisk":likert_value_map
}
cobra = {
    ## cobra factor 1
    "race_successful":reverse_likert_value_map,
    "race_prison":reverse_likert_value_map,
    "race_socservices":reverse_likert_value_map,
    "race_minadvantage":reverse_likert_value_map,
    "race_rich":likert_value_map,
    "race_whiteblame":reverse_likert_value_map,
    #"race_discrimination",
    #"race_learnability",
    #"race_education",
    #"race_motivation",
    "race_whiteadvantage":likert_value_map
}
