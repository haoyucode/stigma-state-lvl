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
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


def generate_bar_chart(estimate_df):
    ax = sns.barplot(data=estimate_df, x="var", y="_estimate", color="dodgerblue", dodge=False)
    ax.errorbar(data=estimate_df, x="var", y='_estimate', yerr=[estimate_df["_estimate"] - estimate_df["_lci"],estimate_df["_uci"] - estimate_df["_estimate"]], ls='', color='black')
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(),rotation=45,horizontalalignment='right')

    return ax

def generate_state_estimate_map(estimate_df):
    # quick map of state level estimates

    fig = px.choropleth(estimate_df,
        locations="state_cd",
        locationmode="USA-states",
        scope="usa",
        color="_estimate",
        color_continuous_scale="Viridis_r")

    return fig
