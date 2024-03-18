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
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# %% [markdown]
# ### Data cleaning/pre-processing

# %%
# inputs
DATAPATH = "P:/3652/Common/HEAL/y3-task-c-collaborative-projects/jcoin-stigma/analyses/data/protocol2/"

# %%
mode_impute_vars = ss_10_full + race
mode_impute_vars


# %%


#df['salary'] = df['salary'].fillna(df['salary'].mode()[0])

sub_df_2[mode_impute_vars] = sub_df_2[mode_impute_vars].fillna(sub_df_2[mode_impute_vars].mode().iloc[0])

# check if missing values
print("missing values: ")
print(sub_df_2.isnull().sum())

# %%
# get all var types
print("var info: ")
print(sub_df_2.info())

# %%
#df['avg'] = df[['Monday', 'Tuesday']].mean(axis=1)

sub_df_2["ss_6_past"] = sub_df_2[ss_6_past].mean(axis=1)
sub_df_2["ss_6_current"] = sub_df_2[ss_6_current].mean(axis=1)

sub_df_2["ss_past"] = sub_df_2[ss_past].mean(axis=1)
sub_df_2["ss_current"] = sub_df_2[ss_current].mean(axis=1)

flag_threshold = 3

sub_df_2["race_view_flag"] = np.where((sub_df_2["race_whiteadvantage"] > flag_threshold) | (sub_df_2["race_rich"] > flag_threshold), 1, 0)

# %%
# get all var types
print("var info: ")
print(sub_df_2.info())

# %%
# check for missing 

print(sub_df_1.isnull().sum())


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

print(sub_df_1.isnull().sum())

# %%
# Add jcoin information
jcoin_json = json.loads(Path("jcoin_states.json").read_text())

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
sub_df_1.head()

# %%
# join strata into dataset
sub_df_1 = sub_df_1.merge(sub_df_2,on='caseid',how='left')


sub_df_1

# %%
sub_df_1.columns

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
pop_counts_by_sampletypexstate

# %%
states_with_oversample_df = pop_counts_by_sampletypexstate[pop_counts_by_sampletypexstate["AS oversample"] > 0]
states_with_oversample_list = states_with_oversample_df["state_cd"]

print(states_with_oversample_list)
states_with_oversample_df

# %%
print("N for Oversample, General and Total By State")
pop_counts_by_sampletypexstate.reset_index()

pop_counts_by_sampletypexstate.to_csv("state_counts.csv")


# %%
print("N All")
pop_counts_by_sampletypexstate.sum().to_frame().T

# %%
# get subset of surveyed people who live in states with an oversample to calculate state level stats

print(sub_df_1.columns)

sub_df_1_as_oversample_states = sub_df_1[sub_df_1["state_cd"].isin(states_with_oversample_list)]

sub_df_1_as_oversample_states

# %%
# get caseids for survey respondents in oversampled states
caseid_in_as_oversample_state = sub_df_1_as_oversample_states["caseid"]
caseid_in_as_oversample_state

# %% [markdown]
# ### National estimates

# %% [markdown]
# ### Add and correct strata and PSUs necessary for variance estimation 

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
strata_df

# %%
strata_df_in_as_oversample_state

# %%
sub_df_1

# %%
sub_df_1_as_oversample_states

# %%
# join strata into dataset
sub_df_1 = sub_df_1.set_index("caseid").join(strata_df.set_index('caseid'))

sub_df_1_as_oversample_states = sub_df_1_as_oversample_states.set_index("caseid").join(strata_df_in_as_oversample_state.set_index('caseid'))

# %%
print(sub_df_1.columns)
    
sub_df_1

# %%
print(sub_df_1_as_oversample_states.columns)

sub_df_1_as_oversample_states

# %% [markdown]
# ### Data overview (counts and missing values)

# %%
# o	table/bar: 
# 	point estimate + bootstrap CI; based on gen pop and weight1 
# o	table/bar: 
# 	point estimate + bootstrap CI; based on as oversample + gen pop and weight 2
# o	histogram: 
# 	distribution; based on as oversample + gen pop and weight 2
# 	distribution by personaluse_ever, familyuse_ever, personalcrimjust_ever, familycrimjust_ever; based on as oversample + gen pop and weight 2


# %%
sample_estimator_ss_6 = TaylorEstimator("mean")
sample_estimator_ss_6.estimate(
    y=sub_df_1["stigma_scale_score"],
    samp_weight=sub_df_1["weight2"],
    stratum=sub_df_1["vstrat32_corrected"],
    psu=sub_df_1["vpsu32_corrected"],
)
sample_estimator_ss_6_df = sample_estimator_ss_6.to_dataframe()

sample_estimator_ss_6_df.insert(1,"_domain","")
sample_estimator_ss_6_df.insert(0,"geo","nation")
sample_estimator_ss_6_df.insert(0,"var","ss_6")
sample_estimator_ss_6_df



# %%
sample_estimator_ss_6_past = TaylorEstimator("mean")
sample_estimator_ss_6_past.estimate(
    y=sub_df_1["ss_6_past"],
    samp_weight=sub_df_1["weight2"],
    stratum=sub_df_1["vstrat32_corrected"],
    psu=sub_df_1["vpsu32_corrected"],
)
sample_estimator_ss_6_past_df = sample_estimator_ss_6_past.to_dataframe()

sample_estimator_ss_6_past_df.insert(1,"_domain","")
sample_estimator_ss_6_past_df.insert(0,"geo","nation")
sample_estimator_ss_6_past_df.insert(0,"var","ss_6_past")
sample_estimator_ss_6_past_df

# %%
sample_estimator_ss_6_current = TaylorEstimator("mean")
sample_estimator_ss_6_current.estimate(
    y=sub_df_1["ss_6_current"],
    samp_weight=sub_df_1["weight2"],
    stratum=sub_df_1["vstrat32_corrected"],
    psu=sub_df_1["vpsu32_corrected"],
)
sample_estimator_ss_6_current_df = sample_estimator_ss_6_current.to_dataframe()

sample_estimator_ss_6_current_df.insert(1,"_domain","")
sample_estimator_ss_6_current_df.insert(0,"geo","nation")
sample_estimator_ss_6_current_df.insert(0,"var","ss_6_current")
sample_estimator_ss_6_current_df

# %%
sample_estimator_ss_6_df = pd.concat([sample_estimator_ss_6_df, sample_estimator_ss_6_past_df, sample_estimator_ss_6_current_df], axis = 0)
sample_estimator_ss_6_df

# %%
plot_df = sample_estimator_ss_6_df
plot_x_var = "var"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
state_estimator_ss_6 = TaylorEstimator("mean")
state_estimator_ss_6.estimate(
    y=sub_df_1_as_oversample_states["stigma_scale_score"],
    samp_weight=sub_df_1_as_oversample_states["weight2"],
    stratum=sub_df_1_as_oversample_states["vstrat32_corrected"],
    psu=sub_df_1_as_oversample_states["vpsu32_corrected"],
    domain=sub_df_1_as_oversample_states["state_cd"]
)
#state_mean_estimates = state_estimator.to_dataframe().rename(columns={"_domain":"state_cd","_estimate":"mean"})

state_estimator_ss_6_df = state_estimator_ss_6.to_dataframe().rename(columns={"_domain":"state_cd"})


#sample_estimator_ss_6_current_df.insert(1,"_domain","nation")
state_estimator_ss_6_df.insert(0,"geo","state")
state_estimator_ss_6_df.insert(0,"var","ss_6")
state_estimator_ss_6_df


# %%
state_estimator_ss_6_df.sort_values(by = ["_estimate"], inplace=True, ascending=True)

state_estimator_ss_6_df = state_estimator_ss_6_df\
    .merge(pop_counts_by_sampletypexstate,on='state_cd',how='left')

state_estimator_ss_6_df

# %%
plot_df = state_estimator_ss_6_df
plot_x_var = "state_cd"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
plot_df = state_estimator_ss_6_df
plot_x_var = "state_cd"
plot_color_by_var = "jcoin_flag"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", dodge=False, hue=plot_df[plot_color_by_var].astype("string"))

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
estimator_df = sub_df_1_as_oversample_states[sub_df_1_as_oversample_states["partyid5_strong_d"] == 1]
estimator_df

# %%

estimator_df = sub_df_1_as_oversample_states[sub_df_1_as_oversample_states["partyid5_strong_d"] == 1]
estimator_df

state_estimator_ss_6_strong_d = TaylorEstimator("mean")
state_estimator_ss_6_strong_d.estimate(
    y=estimator_df["stigma_scale_score"],
    samp_weight=estimator_df["weight2"],
    stratum=estimator_df["vstrat32_corrected"],
    psu=estimator_df["vpsu32_corrected"],
    domain=estimator_df["state_cd"]
)
#state_mean_estimates = state_estimator.to_dataframe().rename(columns={"_domain":"state_cd","_estimate":"mean"})

state_estimator_ss_6_strong_d_df = state_estimator_ss_6_strong_d.to_dataframe().rename(columns={"_domain":"state_cd"})


#sample_estimator_ss_6_current_df.insert(1,"_domain","nation")
state_estimator_ss_6_strong_d_df.insert(0,"geo","state")
state_estimator_ss_6_strong_d_df.insert(0,"var","ss_6")
state_estimator_ss_6_strong_d_df.insert(0,"filter_var","strong_d")
state_estimator_ss_6_strong_d_df

# %%
state_estimator_ss_6_past = TaylorEstimator("mean")
state_estimator_ss_6_past.estimate(
    y=sub_df_1_as_oversample_states["ss_6_past"],
    samp_weight=sub_df_1_as_oversample_states["weight2"],
    stratum=sub_df_1_as_oversample_states["vstrat32_corrected"],
    psu=sub_df_1_as_oversample_states["vpsu32_corrected"],
    domain=sub_df_1_as_oversample_states["state_cd"]
)
#state_mean_estimates = state_estimator.to_dataframe().rename(columns={"_domain":"state_cd","_estimate":"mean"})

state_estimator_ss_6_past_df = state_estimator_ss_6_past.to_dataframe().rename(columns={"_domain":"state_cd"})


#sample_estimator_ss_6_current_df.insert(1,"_domain","nation")
state_estimator_ss_6_past_df.insert(0,"geo","state")
state_estimator_ss_6_past_df.insert(0,"var","ss_6_past")
state_estimator_ss_6_past_df

# %%
# order state by same order as when sorting by ss_6
state_order_by_ss_6 = list(state_estimator_ss_6_df["state_cd"])
state_order_by_ss_6

state_estimator_ss_6_past_df = state_estimator_ss_6_past_df.iloc[state_estimator_ss_6_past_df["state_cd"].map({v: k for k, v in enumerate(state_order_by_ss_6)}).argsort()]


state_estimator_ss_6_past_df = state_estimator_ss_6_past_df\
    .merge(pop_counts_by_sampletypexstate,on='state_cd',how='left')

state_estimator_ss_6_past_df


# %%
state_estimator_ss_6_current = TaylorEstimator("mean")
state_estimator_ss_6_current.estimate(
    y=sub_df_1_as_oversample_states["ss_6_current"],
    samp_weight=sub_df_1_as_oversample_states["weight2"],
    stratum=sub_df_1_as_oversample_states["vstrat32_corrected"],
    psu=sub_df_1_as_oversample_states["vpsu32_corrected"],
    domain=sub_df_1_as_oversample_states["state_cd"]
)
#state_mean_estimates = state_estimator.to_dataframe().rename(columns={"_domain":"state_cd","_estimate":"mean"})

state_estimator_ss_6_current_df = state_estimator_ss_6_current.to_dataframe().rename(columns={"_domain":"state_cd"})


#sample_estimator_ss_6_current_df.insert(1,"_domain","nation")
state_estimator_ss_6_current_df.insert(0,"geo","state")
state_estimator_ss_6_current_df.insert(0,"var","ss_6_current")
state_estimator_ss_6_current_df

# %%
# order state by same order as when sorting by ss_6
state_order_by_ss_6 = list(state_estimator_ss_6_df["state_cd"])
state_order_by_ss_6

state_estimator_ss_6_current_df = state_estimator_ss_6_current_df.iloc[state_estimator_ss_6_current_df["state_cd"].map({v: k for k, v in enumerate(state_order_by_ss_6)}).argsort()]


state_estimator_ss_6_current_df = state_estimator_ss_6_current_df\
    .merge(pop_counts_by_sampletypexstate,on='state_cd',how='left')

state_estimator_ss_6_current_df

# %%
state_estimator_ss_6_together_df = pd.concat([state_estimator_ss_6_df,state_estimator_ss_6_past_df,state_estimator_ss_6_current_df], axis = 0)


# %%


## order ss_6 vars
#ss_6_var_order = ["ss_6_current","ss_6","ss_6_past"]
#state_estimator_ss_6_df = state_estimator_ss_6_df.iloc[state_estimator_ss_6_df["var"].map({v: k for k, v in enumerate(ss_6_var_order)}).argsort()]

# order state by same order as when sorting by ss_6
state_order_by_ss_6 = list(state_estimator_ss_6_df["state_cd"])
state_order_by_ss_6

state_estimator_ss_6_together_df = state_estimator_ss_6_together_df.iloc[state_estimator_ss_6_together_df["state_cd"].map({v: k for k, v in enumerate(state_order_by_ss_6)}).argsort()]


state_estimator_ss_6_together_df

# %%
plot_df = state_estimator_ss_6_together_df[state_estimator_ss_6_together_df["var"].isin(["ss_6","ss_6_past"])]
plot_x_var = "state_cd"
plot_color_by_var = "var"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", dodge=False, hue=plot_df[plot_color_by_var].astype("string"))
sns.move_legend(ax, "lower center", bbox_to_anchor=(.5, 1), ncol=2, title=None, frameon=False)
#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
plot_df = state_estimator_ss_6_together_df[state_estimator_ss_6_together_df["var"].isin(["ss_6_past"])]
plot_x_var = "state_cd"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
plot_df = state_estimator_ss_6_together_df[state_estimator_ss_6_together_df["var"].isin(["ss_6_current"])]
plot_x_var = "state_cd"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
# quick map of state level estimates

plot_df = state_estimator_ss_6_together_df[state_estimator_ss_6_together_df["var"].isin(["ss_6"])]

fig = px.choropleth(plot_df,
    locations="state_cd",
    locationmode="USA-states",
    scope="usa",
    color="_estimate",
    color_continuous_scale="Viridis_r")

fig.show()

# %%
# quick map of state level estimates

plot_df = state_estimator_ss_6_together_df[state_estimator_ss_6_together_df["var"].isin(["ss_6_past"])]

fig = px.choropleth(plot_df,
    locations="state_cd",
    locationmode="USA-states",
    scope="usa",
    color="_estimate",
    color_continuous_scale="Viridis_r")

fig.show()

# %%
# quick map of state level estimates

plot_df = state_estimator_ss_6_together_df[state_estimator_ss_6_together_df["var"].isin(["ss_6_current"])]

fig = px.choropleth(plot_df,
    locations="state_cd",
    locationmode="USA-states",
    scope="usa",
    color="_estimate",
    color_continuous_scale="Viridis_r")

fig.show()

# %%


party_d_estimator = TaylorEstimator("mean")
party_d_estimator.estimate(
    y=sub_df_1["stigma_scale_score"],
    samp_weight=sub_df_1["weight2"],
    stratum=sub_df_1["vstrat32_corrected"],
    psu=sub_df_1["vpsu32_corrected"],
    domain=sub_df_1["partyid5_strong_d"]
)


party_d_estimator_df = party_d_estimator.to_dataframe()

#party_d_estimator_df.insert(1,"_domain","nation")
party_d_estimator_df.insert(0,"geo","nation")
party_d_estimator_df.insert(0,"var","party_d")
print(party_d_estimator_df)

#---------------------------------------------------------------

party_r_estimator = TaylorEstimator("mean")
party_r_estimator.estimate(
    y=sub_df_1["stigma_scale_score"],
    samp_weight=sub_df_1["weight2"],
    stratum=sub_df_1["vstrat32_corrected"],
    psu=sub_df_1["vpsu32_corrected"],
    domain=sub_df_1["partyid5_strong_r"]
)


party_r_estimator_df = party_r_estimator.to_dataframe()

#party_r_estimator_df.insert(1,"_domain","nation")
party_r_estimator_df.insert(0,"geo","nation")
party_r_estimator_df.insert(0,"var","party_r")
print(party_r_estimator_df)

# %%
plot_df = party_d_estimator_df
plot_x_var = "_domain"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
plot_df = party_r_estimator_df
plot_x_var = "_domain"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
race_view_estimator = TaylorEstimator("mean")
race_view_estimator.estimate(
    y=sub_df_1["stigma_scale_score"],
    samp_weight=sub_df_1["weight2"],
    stratum=sub_df_1["vstrat32_corrected"],
    psu=sub_df_1["vpsu32_corrected"],
    domain=sub_df_1["race_view_flag"]
)


race_view_estimator_df = race_view_estimator.to_dataframe()

#party_r_estimator_df.insert(1,"_domain","nation")
race_view_estimator_df.insert(0,"geo","nation")
race_view_estimator_df.insert(0,"var","race_view_flag")
race_view_estimator_df

# %%
plot_df = race_view_estimator_df
plot_x_var = "_domain"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
#'race_whiteadvantage', 'race_rich'

race_views_1_estimator = TaylorEstimator("mean")
race_views_1_estimator.estimate(
    y=sub_df_1["stigma_scale_score"],
    samp_weight=sub_df_1["weight2"],
    stratum=sub_df_1["vstrat32_corrected"],
    psu=sub_df_1["vpsu32_corrected"],
    domain=sub_df_1["race_whiteadvantage"]
)

race_views_1_estimator_df = race_views_1_estimator.to_dataframe()

race_views_1_estimator_df.insert(0,"geo","nation")
race_views_1_estimator_df.insert(0,"var","race_whiteadvantage")
print(race_views_1_estimator_df)

race_views_2_estimator = TaylorEstimator("mean")
race_views_2_estimator.estimate(
    y=sub_df_1["stigma_scale_score"],
    samp_weight=sub_df_1["weight2"],
    stratum=sub_df_1["vstrat32_corrected"],
    psu=sub_df_1["vpsu32_corrected"],
    domain=sub_df_1["race_rich"]
)

race_views_2_estimator_df = race_views_2_estimator.to_dataframe()

race_views_2_estimator_df.insert(0,"geo","nation")
race_views_2_estimator_df.insert(0,"var","race_rich")
print(race_views_2_estimator_df)

# %%
plot_df = race_views_2_estimator_df
plot_x_var = "_domain"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%
race_views_1_estimates

# %%
race_views_2_estimates

# %%
# quick map of state level estimates

plot_df = state_estimator_ss_6_df[state_estimator_ss_6_df["var"].isin(["ss_6"])]

fig = px.choropleth(plot_df,
    locations="state_cd",
    locationmode="USA-states",
    scope="usa",
    color="_estimate",
    color_continuous_scale="Viridis_r")

fig.show()


# %%
# merge jcoin info
state_mean_estimates = state_mean_estimates\
    .merge(jcoin_df,on='state_cd',how='left')\
    .sort_values("mean",ascending=False)\
    .assign(
        jcoin_hub_count=lambda df:df.jcoin_hub_count.fillna(0).astype(int),
        jcoin_flag=lambda df:df.jcoin_flag.fillna(0).astype(int))

state_mean_estimates["jcoin_color"] = state_mean_estimates.jcoin_flag
state_mean_estimates.jcoin_color.replace({0:"blue",1:"red"},inplace=True)


state_mean_estimates.head()

# %% [markdown]
# ```{margin} 
# **To go to the data/study page on the HEAL Data Platform, follow this link:** my link
# ```

# %% [markdown]
# ```{margin} 
# **To go to an interactive analytic cloud workspace with the analysis code and data loaded, follow this link:** my link
# ```

# %% [markdown]
# Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sodales ut eu sem integer vitae justo eget. Pellentesque dignissim enim sit amet venenatis urna cursus. Sed faucibus turpis in eu mi bibendum. Scelerisque felis imperdiet proin fermentum leo. Volutpat est velit egestas dui id ornare arcu. Quis lectus nulla at volutpat diam ut venenatis tellus. Tellus pellentesque eu tincidunt tortor aliquam nulla facilisi cras. Pellentesque adipiscing commodo elit at imperdiet dui. 
# <br>

# %% [markdown]
# Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sodales ut eu sem integer vitae justo eget. Pellentesque dignissim enim sit amet venenatis urna cursus. Sed faucibus turpis in eu mi bibendum. Scelerisque felis imperdiet proin fermentum leo. Volutpat est velit egestas dui id ornare arcu. Quis lectus nulla at volutpat diam ut venenatis tellus. Tellus pellentesque eu tincidunt tortor aliquam nulla facilisi cras. Pellentesque adipiscing commodo elit at imperdiet dui. 
# <br><br>
# In hac habitasse platea dictumst quisque sagittis purus. Libero volutpat sed cras ornare. Sit amet consectetur adipiscing elit pellentesque habitant morbi tristique senectus. Auctor augue mauris augue neque gravida in fermentum et. Amet mattis vulputate enim nulla aliquet porttitor. Proin sed libero enim sed faucibus turpis in eu. Morbi tristique senectus et netus et malesuada. Feugiat sed lectus vestibulum mattis ullamcorper.

# %% [markdown]
# **Data Citation** 
# <br>
# Harold Pollack, Johnathon Schneider, Bruce Taylor. JCOIN 026: Brief Stigma Survey. Chicago, IL: Center for Translational Data Science HEAL Data Platform (distributor) via Center for Translational Data Science JCOIN Data Commons (repository & distributor), 2022-04-08. (HEAL Data Platform branded doi goes here)
# <br>
# **Brief Article Citation** 
# <br>
# What format should this be? 


