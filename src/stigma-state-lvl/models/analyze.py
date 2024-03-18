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
from utils import *
from samplics.estimation import TaylorEstimator
pd.set_option('mode.chained_assignment', None)

# %% [markdown]

# %%
# o	table/bar: 
# 	point estimate + bootstrap CI; based on gen pop and weight1 
# o	table/bar: 
# 	point estimate + bootstrap CI; based on as oversample + gen pop and weight 2
# o	histogram: 
# 	distribution; based on as oversample + gen pop and weight 2
# 	distribution by personaluse_ever, familyuse_ever, personalcrimjust_ever, familycrimjust_ever; based on as oversample + gen pop and weight 2


# %% [markdown]
## General population

# %%
measure_list = ["stigma_scale_score","ss_6_past","ss_6_current",]

def get_national_estimates(df,ycol): 

    sample_estimator_ss_6 = TaylorEstimator("mean")
    sample_estimator_ss_6.estimate(
        y=sub_df_1[col],
        samp_weight=sub_df_1["weight2"],
        stratum=sub_df_1["vstrat32_corrected"],
        psu=sub_df_1["vpsu32_corrected"],
    )
    sample_estimator_ss_6_df = sample_estimator_ss_6.to_dataframe()

    sample_estimator_ss_6_df.insert(1,"_domain","")
    sample_estimator_ss_6_df.insert(0,"geo","nation")
    sample_estimator_ss_6_df.insert(0,"var","ss_6")

    return sample_estimator_ss_6_df



def get_state_estimates(df,col):
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


    # %%
    state_estimator_ss_6_df.sort_values(by = ["_estimate"], inplace=True, ascending=True)

    state_estimator_ss_6_df = state_estimator_ss_6_df\
        .merge(pop_counts_by_sampletypexstate,on='state_cd',how='left')

    return state_estimator_ss_6_df

# %%
plot_df = sample_estimator_ss_6_df
plot_x_var = "var"

ax = sns.barplot(data=plot_df, x=plot_x_var, y="_estimate", color="dodgerblue", dodge=False)

#plt.draw()
ax.errorbar(data=plot_df, x=plot_x_var, y='_estimate', yerr=[plot_df["_estimate"] - plot_df["_lci"],plot_df["_uci"] - plot_df["_estimate"]], ls='', color='black')
ax.set_xticks(ax.get_xticks())
ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

# %%

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

