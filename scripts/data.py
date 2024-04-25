""" 

process data and save in data/processed folder
TODO: refactor code in the data module (right now I just copy/pasted the relevant code from the legacy notebook in `data`)
TODO: make custom Field objects and transform Steps to make metadata more readable

"""

# %%
# import packages
import os
import json
from pathlib import Path
import pandas as pd
import numpy as np
import pyreadstat
import frictionless as fl

from stigma_state_lvl.data import mappings, metadata, transforms
from stigma_state_lvl.data.metadata import fields

# %% [markdown]
# %%
# import data and metadata (data dictionaries)
# datapath = Path(__file__).parents[1]/"wave1.sav"
datapath = "../data/raw/wave1.sav"
sourcedf, sourcemeta = pyreadstat.read_sav(datapath, apply_value_formats=True)
source_variablelabels = {
    name.lower(): label for name, label in sourcemeta.column_names_to_labels.items()
}
# lower-case column names
sourcedf.columns = sourcedf.columns.str.lower()

# INITIATE TARGET SCHEMA AND DATAFRAME
# TODO: change df to targetdf in all below code
df = targetdf = sourcedf[["caseid"]].copy()

schema = fl.Schema(fields=[fl.Field.from_descriptor(metadata.fields.caseid)])

# POPULATE TARGET SCHEMA AND DF
for field in fields.demographic:
    field = fl.Field.from_descriptor(field)
    schema.add_field(field)
    targetdf[field.name] = sourcedf[field.name]

## 6 question
for name, mapping in mappings.stigma6.items():
    _meta = {
        "name": name,
        "description": source_variablelabels[name],
        "enumLabels": mapping,
        **metadata.stigma6,
    }
    data, meta = transforms.categorical_to_numeric(
        data=sourcedf[name], mapping=mapping, meta=_meta
    )
    targetdf[name] = data
    schema.add_field(fl.Field.from_descriptor(meta))

## 10 question
for name, mapping in mappings.stigma10.items():
    _meta = {
        "name": name,
        "description": source_variablelabels[name],
        "enumLabels": mapping,
        **metadata.stigma10,
    }
    data, meta = data.categorical_to_numeric(
        data=sourcedf[name], mapping=mapping, meta=_meta
    )
    targetdf[name] = data
    schema.add_field(fl.Field.from_descriptor(meta))

# current and past usage

## 6 question
for field in fields.ss_6_past:
    data = sourcedf[field["name"]].copy() # TODO: change to numeric (right now, already calculated so not doing)
    targetdf[meta["name"]] = data
    schema.add_field(fl.Field.from_descriptor(field))

meta = fl.Field.from_descriptor(fl.Field.from_descriptor(fields.derived_ss_6_past))
meta.description += ("\n**Transforms**\n"
            f"The mean of  `{'`,`'.join(ss_6_past_names)}`")
schema.add_field(meta)
df["ss_6_past"] = df[ss_6_past_names].mean(axis=1)

for field in fields.ss_6_current:
    data = sourcedf[field["name"]].copy() # TODO: change to numeric (right now, already calculated so not doing)
    targetdf[meta["name"]] = data
    schema.add_field(fl.Field.from_descriptor(field))


meta = fl.Field.from_descriptor(fields.derived_ss_6_current)
meta.description += ("\n**Transforms**\n"
            f"The mean of  `{'`,`'.join(ss_6_current_vars)}`")
schema.add_field(fl.Field.from_descriptor(meta))
df["ss_6_current"] = df[ss_6_current_vars].mean(axis=1)

## 10 question
ss_10_past_names = [field["name"] for field in fields.ss_10_past + fields.ss_6_past]
df["ss_10_past"] = df[ss_10_past_names].mean(axis=1)
meta.description += ("\n**Transforms**\n"
            f"The mean of  `{'`,`'.join(ss_10_past_names)}`")
schema.add_field(fl.Field.from_descriptor(meta))
df["ss_10_current"] = df[ss_10_past_names].mean(axis=1)

## Cobra racial awareness

for name, mapping in mappings.cobra.items():

    data, meta = data.categorical_to_numeric(
        data=sourcedf[name], mapping=mapping, meta=metadata.cobra
    )
    targetdf[name] = data
    schema.add_field(fl.Field.from_descriptor(meta))


df["racial_privilege"] = df[cobramap.keys()].sum(axis=1)
meta = fields.cobra_composite
meta.description += ("\n**Transforms**\n"
            f"The sum of  `{'`,`'.join(ss_10_past_names)}`")
schema.add_field(fl.Field.from_descriptor(meta))

vars_of_interest = [
    "stigma_scale_score",
    "expanded_10item_stigma",
    "personaluse_ever",
    "familyuse_ever",
    "personalcrimjust_ever",
    "familycrimjust_ever",
]


# clean up some of the categoricals to be consistently coded
df.familycrimjust_ever.replace({0: "No", 1: "Yes"}, inplace=True)
df.familyuse_ever.replace({" No": "No"}, inplace=True)
df.personalcrimjust_ever.replace(
    {
        "Yes, ever arrested or incarcerated": "Yes",
        "No, never arrested or incarcerated": "No",
    },
    inplace=True,
)


# %%

# # impute missing stigma scale score vals with median, impute missing personaluse_ever with mode, "No"
# replace missing values of personaluse_ever with mode value of 'No'
df.personaluse_ever.fillna("No", inplace=True)
df.familyuse_ever.fillna("No", inplace=True)
df.personalcrimjust_ever.fillna("No", inplace=True)
df.familycrimjust_ever.fillna("No", inplace=True)

# impute missing stigma scale score values as the median score
# TODO: compute based on individual scores
df["stigma_scale_score"].fillna(df["stigma_scale_score"].median(), inplace=True)
df["expanded_10item_stigma"].fillna(df["expanded_10item_stigma"].median(), inplace=True)


# %%
# add df column with state 2 letter code
# https://pythonfix.com/code/us-states-abbrev.py/
# state name to two letter code dictionary
for field in fields.jcoin_hub:
    field = fl.Field.from_descriptor(field)
    schema.add_field(field)
    targetdf[field.name] = sourcedf[field.name]

us_state_to_abbrev = package.get_resource("state-abbreviations").read_data()
state_cd = df.state.replace(us_state_to_abbrev)
df.insert(6, "state_cd", state_cd, True)

# %%
# Add jcoin information
jcoin_json = package.get_resource("jcoin-states").read_data()

jcoin_df = (
    pd.DataFrame(jcoin_json)
    .assign(hub_types=lambda df: df["hub"] + "(" + df["type"] + ")")
    .groupby("states")
    # make a list of the name and type of hub/study and how many hubs are in that state
    .agg({"hub_types": lambda s: ",".join(s), "hub": "count"})
    .reset_index()
    .rename(
        columns={
            "states": "state_cd",
            "hub": "jcoin_hub_count",
            "hub_types": "jcoin_hub_types",
        }
    )
)

jcoin_df["is_jcoin_state"] = True

# %%
jcoin_df.head()

# %%
df = df.merge(jcoin_df, on="state_cd", how="left")
df["jcoin_hub_types"].fillna("not JCOIN", inplace=True)
df["jcoin_hub_count"].fillna(0, inplace=True)
df["is_jcoin_state"].fillna(False, inplace=True)
df["is_jcoin_hub"] = np.where(df["jcoin_hub_types"] == "not JCOIN", "No", "Yes")


# %%
# join strata into dataset
df = df.merge(df, on="caseid", how="left")

pop_counts_by_sampletypexstate = (
    df.convert_dtypes()
    .assign(jcoin_hub_count=lambda df: df.jcoin_hub_count.astype(str))
    .groupby(["state_cd", "p_over"])["stigma_scale_score"]
    .count()
    .unstack(["p_over"])
)
pop_counts_by_sampletypexstate["total"] = pop_counts_by_sampletypexstate.sum(axis=1)

# %%
# merge jcoin info
pop_counts_by_sampletypexstate = (
    pop_counts_by_sampletypexstate.merge(jcoin_df, on="state_cd", how="left")
    .sort_values("total", ascending=False)
    .assign(
        jcoin_hub_count=lambda df: df.jcoin_hub_count.fillna(0).astype(int),
        jcoin_flag=lambda df: df.jcoin_flag.fillna(0).astype(int),
        jcoin_hub_types=lambda df: (
            np.where(
                df.jcoin_hub_types.isna() & df["AS oversample"] > 0,
                "non JCOIN comparison",
                np.where(
                    df.jcoin_hub_types.isna(), "non JCOIN gen pop", df.jcoin_hub_types
                ),
            )
        ),
    )
)


# strata/psus

for field in fields.sampling + fields.weights:
    field = fl.Field.from_descriptor(field)
    schema.add_field(field)
    targetdf[field.name] = sourcedf[field.name]


states_with_oversample_df = pop_counts_by_sampletypexstate[
    pop_counts_by_sampletypexstate["AS oversample"] > 0
]
states_with_oversample_list = states_with_oversample_df["state_cd"]
df_as_oversample_states = df[df["state_cd"].isin(states_with_oversample_list)]
# get caseids for survey respondents in oversampled states
caseid_in_as_oversample_state = df_as_oversample_states["caseid"]
strata_df = package.get_resource("strata-and-psu").to_pandas()
strata_df.columns = strata_df.columns.str.lower()
# get strata and cluster ids for survey respondents in oversampled states
strata_df_in_as_oversample_state = strata_df[
    strata_df["caseid"].isin(caseid_in_as_oversample_state)
]
# collapse strata containing only 1 PSU
onepsu = (
    strata_df[["vstrat32", "vpsu32"]]
    .drop_duplicates()
    .groupby("vstrat32")
    .count()
    .squeeze()
    .loc[lambda s: s == 1]
    .index
)
strata_df["vstrat32_corrected"] = strata_df["vstrat32"].where(
    cond=lambda s: ~s.isin(onepsu), other=-1
)
# rename PSUs so no duplicates
strata_df["vpsu32_corrected"] = strata_df.groupby(
    ["vstrat32_corrected", "vpsu32"]
).ngroup()

# ---------------------------------------------------

# collapse strata containing only 1 PSU
onepsu_in_as_oversample_state = (
    strata_df_in_as_oversample_state[["vstrat32", "vpsu32"]]
    .drop_duplicates()
    .groupby("vstrat32")
    .count()
    .squeeze()
    .loc[lambda s: s == 1]
    .index
)
strata_df_in_as_oversample_state["vstrat32_corrected"] = (
    strata_df_in_as_oversample_state["vstrat32"].where(
        cond=lambda s: ~s.isin(onepsu_in_as_oversample_state), other=-1
    )
)
# rename PSUs so no duplicates
strata_df_in_as_oversample_state["vpsu32_corrected"] = (
    strata_df_in_as_oversample_state.groupby(["vstrat32_corrected", "vpsu32"]).ngroup()
)


# %%
# join strata into dataset

fullsample_strata_df = strata_df.set_index("caseid")[
    ["vstrat32_corrected", "vpsu32_corrected"]
].rename(
    columns={
        "vstrat32_corrected": "strata_fullsample",
        "vpsu32_corrected": "psu_fullsample",
    }
)
oversample_strata_df = strata_df.set_index("caseid")[
    ["vstrat32_corrected", "vpsu32_corrected"]
].rename(
    columns={
        "vstrat32_corrected": "strata_oversample",
        "vpsu32_corrected": "psu_oversample",
    }
)
df = (
    df.set_index("caseid")
    .join(fullsample_strata_df)
    .join(oversample_strata_df)
    .assign(
        isin_state_with_oversample=lambda df: df.index.isin(
            caseid_in_as_oversample_state
        )
    )
)

resource = fl.Resource(data=df.to_dict(orient="records"),schema=schema)
resource.schema.to_yaml("schemas/processed/protocol2_wave1_analytic.yaml")
resource.write("data/processed/protocol2_wave1_analytic.csv")
