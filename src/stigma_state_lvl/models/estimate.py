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

def get_national_estimates(df,ycol): 

    estimator = TaylorEstimator("mean")
    estimator.estimate(
        y=sub_df_1[col],
        samp_weight=sub_df_1["weight2"],
        stratum=sub_df_1["strata_fullsample"],
        psu=sub_df_1["psu_fullsample"],
    )
    estimates = estimator.to_dataframe()

    estimates.insert(1,"_domain","")
    estimates.insert(0,"geo","nation")
    estimates.insert(0,"var",col)

    return estimates


def get_domain_estimates(df,ycol,domaincol,stratacol,psucol):

    estimator = TaylorEstimator("mean")
    estimator.estimate(
        y=df[ycol],
        samp_weight=df["weight2"],
        stratum=sub_df_1[stratacol],
        psu=sub_df_1[psucol],
        domain=df[domaincol]
    )
    return estimator.to_dataframe()

#NOTE: in 4/20 meeting notebook, `estimator_df = sub_df_1_as_oversample_states[sub_df_1_as_oversample_states["partyid5_strong_d"] == 1]`
# in addition to strong_r. I'm wondering why the reasoning behind this..
def get_state_estimates(df,ycol):

    stratacol = "strata_oversample"
    psucol = "psu_oversample"
    domaincol = "state_cd"

    estimates = get_domain_estimates(df,ycol,domaincol=domaincol,stratacol=stratacol,psucol=psucol)
    estimates.insert(0,"geo","state")
    estimates.insert(0,"var",ycol)

    return estimates





