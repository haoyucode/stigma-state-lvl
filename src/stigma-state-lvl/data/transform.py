""" 
Creates analytic dataset for analyses
TODO: create schema with additional metadata (ie descriptions for derived variables and scale groupings) for this dataset

"""
# %% [markdown]
# # Stigma against Opioid Use Disorder varies by Personal Use status

# %% [markdown]
# ```{margin} 
# **To follow the full analysis, click through the hidden analysis code below**
# ```


# %%
# import packages
import os
import json
from pathlib import Path
import pandas as pd
import numpy as np
import pyreadstat
# %% [markdown]
# ### Data cleaning/pre-processing
os.chdir(Path(__file__).parents[3])
# %%
# inputs
STATE_ABBREVIATIONS = "data/state_abbrev_mappings.json"
DATAPATH = "P:/3652/Common/HEAL/y3-task-c-collaborative-projects/jcoin-stigma/analyses/data/protocol2/"
DATA_FILE = DATAPATH+"3645_JCOIN_HEAL Initiative 2021_NORC_Jan2022_1.sav"
STRATA_FILE = DATAPATH+"VSTRAT_VPSU_Survey_2039_HEAL_MAIN_21_05_14.csv"

# %%
# import data and metadata (data dictionaries)
df, meta = pyreadstat.read_sav(DATA_FILE,apply_value_formats=True)


# %%

# lower-case column names 
df.columns = df.columns.str.lower()

# %%
vars_of_interest = ["caseid",'p_over','weight1','weight2','stigma_scale_score','expanded_10item_stigma','state','age4','racethnicity','educ5','personaluse_ever','familyuse_ever','personalcrimjust_ever','familycrimjust_ever']
categorical_vars = ['p_over','state','age4','racethnicity','educ5',
    'personaluse_ever','familyuse_ever',
    'personalcrimjust_ever','familycrimjust_ever']



# %%
# to enable more granular analysis of the stigma scale score(s) - e.g. parsing impact of current versus past OUD on stigma - bring in the individual ss questions

# ss_a_historywork - agree means low stigma/high val means low stigma
# ss_b_historymarry - agree means low stigma/high val means low stigma
# ss_c_currentwork - agree means low stigma/high val means low stigma
# ss_d_currentmarry - agree means low stigma/high val means low stigma

# -------- use the reverse coded for history and current work and marry vars - these ones are the only ss questions where agree means low stigma, using the reverse coded version brings them in line with the others for easier analysis

# ss_a_historywork_rev - already converted to numeric/high val means high stigma
# ss_b_historymarry_rev - already converted to numeric/high val means high stigma
# ss_c_currentwork_rev - already converted to numeric/high val means high stigma
# ss_d_currentmarry_rev - already converted to numeric/high val means high stigma

# ss_e_dangerous - agree means high stigma/high val means high stigma
# ss_f_ trust - agree means high stigma/high val means high stigma
# ss_history_steal - agree means high stigma/high val means high stigma
# ss_historyhighrisk - agree means high stigma/high val means high stigma
# ss_currentsteal - agree means high stigma/high val means high stigma
# ss_currenthighrisk - agree means high stigma/high val means high stigma

ss_6_past = ['ss_a_historywork_rev','ss_b_historymarry_rev']
ss_6_current = ['ss_c_currentwork_rev','ss_d_currentmarry_rev','ss_e_dangerous','ss_f_trust']

ss_6_full = ss_6_past + ss_6_current

ss_10_past = ['ss_historysteal', 'ss_historyhighrisk']
ss_10_current = ['ss_currentsteal', 'ss_currenthighrisk']

ss_10_full = ss_6_full + ss_10_past + ss_10_current

ss_past = ss_6_past + ss_10_past
ss_current = ss_6_current + ss_10_current





# %%
# to enable parsing of stigma by political affiliation, views on race/ethnicity, and experience of racial/ethnic discrimination bring in variables assessing those items

# political = ['pid1','pida','pidb','pidi','partyid7','partyid5']
political = ['partyid5']

race = ['race_whiteadvantage','race_rich']

# race_whiteadvanctage: [White people in the U.S. have certain advantages because of the color of their skin.] Do you disagree or agree with the following statements?
    # agree corresponds with recognition of white advantage; high vals = recognition of white advantage
    # reverse code this from likert vars so that high vals will now indicate lack of recognition of white advantage

# race_rich: [Everyone who works hard, no matter what race they are, has an equal chance to become rich.] Do you disagree or agree with the following statements?
    # agree corresponds with lack of recognition of white advantage; high vals = lack of recognition of white advantage
    # code this along with the likert vars where high vals = high stigma; in this case high vals = lack of recognition of white advantage

#discrimination_experience = ['times_atschool', 'times_hired', 'times_atwork', 'times_housing', 'times_medcare', 'times_restaurant', 'times_credit', 'times_street', 'times_police']

# possible approach: 
    # add count of dicrimination experiences (times) across categories
    # higher numbers mean more discrimination experience



# %%
likert_replace_vars = ['ss_e_dangerous','ss_f_trust','ss_historysteal', 'ss_historyhighrisk','ss_currentsteal', 'ss_currenthighrisk','race_rich']
likert_reverse_replace_vars = ['race_whiteadvantage']

# %%

#additional_vars_of_interest = ss_10_full + political + race + discrimination_experience
additional_vars_of_interest = ["caseid"] + ss_10_full + political + race 
all_vars_of_interest = vars_of_interest + additional_vars_of_interest



# %%
# narrow down the dataset to only a few interesting (and relatively clean, straightforward variables) - check for missingness and impute to fill in missing
sub_df_1 = df[vars_of_interest]
sub_df_2 = df[additional_vars_of_interest]


# %%
likert_replacer = {'Strongly disagree': 1, 
                   'Somewhat disagree': 2,
                   'Neither disagree nor agree': 3,
                   'Somewhat agree': 4, 
                   'Strongly agree': 5}

likert_reverse_replacer = {'Strongly disagree': 5, 
                           'Somewhat disagree': 4,
                           'Neither disagree nor agree': 3,
                           'Somewhat agree': 2, 
                           'Strongly agree': 1}

sub_df_2[likert_replace_vars].replace(likert_replacer, inplace=True)
sub_df_2[likert_replace_vars] = sub_df_2[likert_replace_vars].astype("float")

sub_df_2[likert_reverse_replace_vars].replace(likert_reverse_replacer, inplace=True)
sub_df_2[likert_reverse_replace_vars] = sub_df_2[likert_reverse_replace_vars].astype("float")

#sub_df_2['partyid5_any_d'] = np.where(sub_df_2['partyid5'] in ["Democrat","Lean Democrat"], 1,0)
sub_df_2['partyid5_strong_d'] = np.where(sub_df_2['partyid5'] == "Democrat", 1,0)
#sub_df_2['partyid5_any_r'] = np.where(sub_df_2['partyid5'] in ["Republican","Lean Republican"], 1,0)
sub_df_2['partyid5_strong_r'] = np.where(sub_df_2['partyid5'] == "Republican", 1,0)

sub_df_2.drop(['partyid5'], axis=1, inplace=True)
# %%
mode_impute_vars = ss_10_full + race
sub_df_2[mode_impute_vars] = sub_df_2[mode_impute_vars].fillna(sub_df_2[mode_impute_vars].mode().iloc[0])

sub_df_2["ss_6_past"] = sub_df_2[ss_6_past].mean(axis=1)
sub_df_2["ss_6_current"] = sub_df_2[ss_6_current].mean(axis=1)

sub_df_2["ss_past"] = sub_df_2[ss_past].mean(axis=1)
sub_df_2["ss_current"] = sub_df_2[ss_current].mean(axis=1)

flag_threshold = 3

sub_df_2["race_view_flag"] = np.where((sub_df_2["race_whiteadvantage"] > flag_threshold) | (sub_df_2["race_rich"] > flag_threshold), 1, 0)

# %%
# clean up some of the categoricals to be consistently coded
sub_df_1.familycrimjust_ever.replace({0:"No",1:"Yes"},inplace=True)
sub_df_1.familyuse_ever.replace({" No":"No"},inplace=True)
sub_df_1.personalcrimjust_ever.replace({"Yes, ever arrested or incarcerated":"Yes", "No, never arrested or incarcerated":"No"},inplace=True)



# %%

# impute any missing - confirm missing eliminated

# # impute missing stigma scale score vals with median, impute missing personaluse_ever with mode, "No"

# replace missing values of personaluse_ever with mode value of 'No'
sub_df_1.personaluse_ever.fillna('No',inplace=True)
#print(sub_df_1.isnull().sum())

sub_df_1.familyuse_ever.fillna('No',inplace=True)
#print(sub_df_1.isnull().sum())

sub_df_1.personalcrimjust_ever.fillna('No',inplace=True)
#print(sub_df_1.isnull().sum())

sub_df_1.familycrimjust_ever.fillna('No',inplace=True)
#print(sub_df_1.isnull().sum())


# impute missing stigma scale score values as the median score 
#sub_df_1['stigma_scale_score'].fillna(sub_df_1.groupby('time-point')['stigma_scale_score'].transform('median'),inplace=True)
sub_df_1['stigma_scale_score'].fillna(sub_df_1['stigma_scale_score'].median(),inplace=True)
sub_df_1['expanded_10item_stigma'].fillna(sub_df_1['expanded_10item_stigma'].median(),inplace=True)


# %%
# add df column with state 2 letter code
# https://pythonfix.com/code/us-states-abbrev.py/
# state name to two letter code dictionary
us_state_to_abbrev = json.loads(Path(STATE_ABBREVIATIONS).read_text())
state_cd = sub_df_1.state.replace(us_state_to_abbrev)
sub_df_1.insert(6,"state_cd",state_cd,True)

# %%
# Add jcoin information
jcoin_json = json.loads(Path("data/jcoin_states.json").read_text())

jcoin_df = (pd.DataFrame(jcoin_json)
    .assign(hub_types=lambda df:df["hub"]+"("+df["type"]+")")
    .groupby('states')
    # make a list of the name and type of hub/study and how many hubs are in that state
    .agg({"hub_types":lambda s:",".join(s),"hub":"count"})
    .reset_index()
    .rename(
        columns={"states":"state_cd",
        "hub":"jcoin_hub_count",
        "hub_types":"jcoin_hub_types"})
)

jcoin_df["jcoin_flag"] = 1

# %%
jcoin_df.head()

# %%
sub_df_1 = sub_df_1.merge(jcoin_df,on="state_cd",how="left")
sub_df_1["jcoin_hub_types"].fillna("not JCOIN",inplace=True)
sub_df_1["jcoin_hub_count"].fillna(0,inplace=True)
sub_df_1["jcoin_flag"].fillna(0,inplace=True)
sub_df_1["is_jcoin_hub"] = np.where(sub_df_1["jcoin_hub_types"]=="not JCOIN","No","Yes")


# %%
# join strata into dataset
sub_df_1 = sub_df_1.merge(sub_df_2,on='caseid',how='left')

# %%
# o	all: n/weighted n in genpop
# o	all:n/weighted n in as oversample
# o	all:n/weighted n in as oversample + gen pop(in oversampled state)
# o	per state: n/weighted n in as oversample
# o	missingness; imputation procedures

# %%
pop_counts_by_sampletypexstate = (
    sub_df_1
    .convert_dtypes()
    .assign(jcoin_hub_count=lambda df: df.jcoin_hub_count.astype(str))
    .groupby(['state_cd','p_over'])
    ["stigma_scale_score"]
    .count()
    .unstack(['p_over'])
)
pop_counts_by_sampletypexstate["total"] = pop_counts_by_sampletypexstate.sum(axis=1)

# %%
# merge jcoin info
pop_counts_by_sampletypexstate = pop_counts_by_sampletypexstate\
    .merge(jcoin_df,on='state_cd',how='left')\
    .sort_values("total",ascending=False)\
    .assign(
        jcoin_hub_count=lambda df:df.jcoin_hub_count.fillna(0).astype(int),
        jcoin_flag=lambda df:df.jcoin_flag.fillna(0).astype(int),
        jcoin_hub_types=lambda df:(
            np.where(df.jcoin_hub_types.isna() & df["AS oversample"]>0,"non JCOIN comparison",
                np.where(df.jcoin_hub_types.isna(),"non JCOIN gen pop",df.jcoin_hub_types)
        )
        
        ))


# %%
states_with_oversample_df = pop_counts_by_sampletypexstate[pop_counts_by_sampletypexstate["AS oversample"] > 0]
states_with_oversample_list = states_with_oversample_df["state_cd"]



sub_df_1_as_oversample_states = sub_df_1[sub_df_1["state_cd"].isin(states_with_oversample_list)]

# %%
# get caseids for survey respondents in oversampled states
caseid_in_as_oversample_state = sub_df_1_as_oversample_states["caseid"]

# %%
strata_df = pd.read_csv(STRATA_FILE)
strata_df.columns = strata_df.columns.str.lower()

# get strata and cluster ids for survey respondents in oversampled states
strata_df_in_as_oversample_state = strata_df[strata_df["caseid"].isin(caseid_in_as_oversample_state)]

# collapse strata containing only 1 PSU
onepsu = (
    strata_df[["vstrat32","vpsu32"]]
    .drop_duplicates()
    .groupby("vstrat32")
    .count()
    .squeeze()
    .loc[lambda s:s==1]
    .index
)
strata_df["vstrat32_corrected"] = strata_df["vstrat32"].where(cond=lambda s:~s.isin(onepsu),other=-1)
# rename PSUs so no duplicates
strata_df["vpsu32_corrected"] = strata_df.groupby(["vstrat32_corrected","vpsu32"]).ngroup()

#---------------------------------------------------

# collapse strata containing only 1 PSU
onepsu_in_as_oversample_state = (
    strata_df_in_as_oversample_state[["vstrat32","vpsu32"]]
    .drop_duplicates()
    .groupby("vstrat32")
    .count()
    .squeeze()
    .loc[lambda s:s==1]
    .index
)
strata_df_in_as_oversample_state["vstrat32_corrected"] = strata_df_in_as_oversample_state["vstrat32"].where(cond=lambda s:~s.isin(onepsu_in_as_oversample_state),other=-1)
# rename PSUs so no duplicates
strata_df_in_as_oversample_state["vpsu32_corrected"] = strata_df_in_as_oversample_state.groupby(["vstrat32_corrected","vpsu32"]).ngroup()


# %%
# join strata into dataset

fullsample_strata_df = (
    strata_df
    .set_index("caseid")
    [["vstrat32_corrected","vpsu32_corrected"]]
    .rename(columns={"vstrat32_corrected":"strata_fullsample","vpsu32_corrected":"psu_fullsample"})
)
oversample_strata_df = (
    strata_df
    .set_index("caseid")
    [["vstrat32_corrected","vpsu32_corrected"]]
    .rename(columns={"vstrat32_corrected":"strata_oversample","vpsu32_corrected":"psu_oversample"})
)
sub_df_1 = (
    sub_df_1
    .set_index("caseid")
    .join(fullsample_strata_df)
    .join(oversample_strata_df)
    .assign(isin_state_with_oversample=lambda df:df.index.isin(caseid_in_as_oversample_state))
)


sub_df_1.to_csv("data/processed/protocol2_wave1_analytic.csv")

