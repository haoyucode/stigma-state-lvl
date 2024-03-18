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
from samplics.estimation import TaylorEstimator

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
measure_list = ["stigma_scale_score","ss_6_past","ss_6_current","race_view_flag","partyid5_strong_d","partyid5_strong_r"]

def get_national_estimates(df,ycol): 

    estimator = TaylorEstimator("mean")
    estimator.estimate(
        y=sub_df_1[col],
        samp_weight=sub_df_1["weight2"],
        stratum=sub_df_1["vstrat32_corrected"],
        psu=sub_df_1["vpsu32_corrected"],
    )
    estimates = estimator.to_dataframe()

    estimates.insert(1,"_domain","")
    estimates.insert(0,"geo","nation")
    estimates.insert(0,"var",col)

    return estimates


def get_domain_estimates(df,col,domaincol):

    estimator = TaylorEstimator("mean")
    estimator.estimate(
        y=df[col],
        samp_weight=df["weight2"],
        stratum=df["vstrat32_corrected"],
        psu=df["vpsu32_corrected"],
        domain=df[domaincol]
    )
    return estimator.to_dataframe()

#estimator_df = sub_df_1_as_oversample_states[sub_df_1_as_oversample_states["partyid5_strong_d"] == 1]
def get_state_estimates(df,col):
    estimates = get_domain_estimates(df,col,domaincol="state_cd")
    estimates.insert(0,"geo","state")
    estimates.insert(0,"var",col)

    return estimates





