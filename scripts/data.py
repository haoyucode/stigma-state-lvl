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
from stigma_state_lvl.data.metadata import fields, standardsmappings

# %% [markdown]
# %%
# import data and metadata (data dictionaries)
# datapath = Path(__file__).parents[1]/"wave1.sav"
os.chdir(Path(__file__).parents[1])
datapath = "data/raw/wave1.sav"
sourcedf, sourcemeta = pyreadstat.read_sav(datapath, apply_value_formats=True)
source_variablelabels = {
    name.lower(): label for name, label in sourcemeta.column_names_to_labels.items()
}
# lower-case column names
sourcedf.columns = sourcedf.columns.str.lower()

# INITIATE TARGET SCHEMA AND DATAFRAME
targetdf = sourcedf[["caseid"]].copy()
schema = fl.Schema(fields=[fl.Field.from_descriptor(metadata.fields.caseid)])

# POPULATE TARGET SCHEMA AND DF
for field in fields.demographic:
    field = fl.Field.from_descriptor(field)
    schema.add_field(field)

## 10 question items (includes 6 item questions as well)
for name, mapping in mappings.stigma10.items():
    _meta = {
        "name": name,
        "description": source_variablelabels[name],
        "enumLabels": mapping,
        **standardsmappings.stigma10,
    }
    data, meta = transforms.categorical_to_numeric(
        data=sourcedf[name], mapping=mapping, meta=_meta
    )
    meta["description"] += "**Imputation**: Most frequent value (mode)"
    data.fillna(data.mode()[0],inplace=True)
    targetdf[name] = data
    schema.add_field(fl.Field.from_descriptor(meta))

# current and past usage

## 6 question

ss_6_past_names = [field['name'] for field in fields.ss_6_past]
meta = fl.Field.from_descriptor(fields.ss_6_past_composite)
meta.description += "\n**Transforms**\n" f"The mean of  `{'`,`'.join(ss_6_past_names)}`"
schema.add_field(meta)
targetdf["ss_6_past"] = (
    targetdf[ss_6_past_names]
    .mean(axis=1)
)
meta = fl.Field.from_descriptor(fields.ss_6_current_composite)
meta.description += (
    "\n**Transforms**\n" f"The mean of  `{'`,`'.join([field['name'] for field in fields.ss_6_current])}`"
)
schema.add_field(meta)
targetdf["ss_6_current"] = targetdf[[field["name"] for field in fields.ss_6_current]].mean(axis=1).fillna(lambda s: s.median())

# impute missing stigma scale score values as the median score
# TODO: compute based on individual scores
targetdf["stigma_scale_score"] = sourcedf["stigma_scale_score"].fillna(lambda s: s.median())
meta = fl.fields.NumberField(
    name="stigma_scale_score",
    title="6 question social stigma scale score",
    description=source_variablelabels["stigma_scale_score"],
)
schema.add_field(meta)

ss_10_past_names = [field['name'] for field in fields.ss_10_past]
meta = fl.Field.from_descriptor(fields.ss_10_past_composite)
meta.description += "\n**Transforms**\n" f"The mean of  `{'`,`'.join(ss_10_past_names)}`"
meta.description += "\n- Median used for imputation"
schema.add_field(meta)
targetdf["ss_10_past"] = targetdf[ss_10_past_names].mean(axis=1).fillna(lambda s: s.median())


ss_10_current_names = [field['name'] for field in fields.ss_10_current]
meta = fl.Field.from_descriptor(fields.ss_10_current_composite)
meta.description += (
    "\n**Transforms**\n" f"- The mean of  `{'`,`'.join(ss_10_current_names)}`"
    "\n"
    "- Imputation used with median"
)
schema.add_field(meta)
targetdf["ss_10_current"] = targetdf[ss_10_current_names].mean(axis=1).fillna(lambda s: s.median())



targetdf["expanded_10item_stigma"] = sourcedf["expanded_10item_stigma"].fillna(lambda s: s.median())
schema.add_field(
    fl.fields.NumberField(
        name="expanded_10item_stigma",
        title="10 question social stigma scale score",
        description=source_variablelabels["expanded_10item_stigma"],
    )
)
## Cobra racial awareness

for name, mapping in mappings.cobra.items():

    data, meta = transforms.categorical_to_numeric(
        data=sourcedf[name], mapping=mapping, meta={"name":name,"description":source_variablelabels[name],
            **standardsmappings.cobra})
    meta["description"] += "**Imputation**: Most frequent value (mode)"
    data.fillna(data.mode()[0],inplace=True)
    targetdf[name] = data
    schema.add_field(fl.Field.from_descriptor(meta))


targetdf["racial_privilege"] = targetdf[mappings.cobra.keys()].sum(axis=1)
meta = fl.Field.from_descriptor(fields.cobra_composite)
meta.description += "\n**Transforms**\n" f"The sum (composite) of  `{'`,`'.join(mappings.cobra.keys())}`"
schema.add_field(meta)

vars_of_interest = [
    "personaluse_ever",
    "familyuse_ever",
    "personalcrimjust_ever",
    "familycrimjust_ever",
]
for name in vars_of_interest:
    targetdf[name] = sourcedf[name].copy()
    schema.add_field(fl.Field.from_descriptor({"name":name,"type":"string"}))

# clean up some of the categoricals to be consistently coded
targetdf.familycrimjust_ever.replace({0: "No", 1: "Yes"}, inplace=True)
targetdf.familyuse_ever.replace({" No": "No"}, inplace=True)
targetdf.personalcrimjust_ever.replace(
    {
        "Yes, ever arrested or incarcerated": "Yes",
        "No, never arrested or incarcerated": "No",
    },
    inplace=True,
)


# %%

# # impute missing stigma scale score vals with median, impute missing personaluse_ever with mode, "No"
# replace missing values of personaluse_ever with mode value of 'No'
targetdf.personaluse_ever.fillna("No", inplace=True)
targetdf.familyuse_ever.fillna("No", inplace=True)
targetdf.personalcrimjust_ever.fillna("No", inplace=True)
targetdf.familycrimjust_ever.fillna("No", inplace=True)

# %%
# add df column with state 2 letter code
# https://pythonfix.com/code/us-states-abbrev.py/
# state name to two letter code dictionary

us_state_to_abbrev = fl.Resource(path="data/state_abbrev_mappings.json").read_data()
state_cd = sourcedf.state.replace(us_state_to_abbrev)
targetdf.insert(6, "state_cd", state_cd, True)

# %%
##### Add jcoin information ####
jcoin_json = fl.Resource(path="data/jcoin_states.json").read_data()

jcoin_df = (
    pd.DataFrame(jcoin_json)
    .assign(jcoin_hub_types=lambda df: df["hub"] + "(" + df["type"] + ")")
    .groupby("state")
    # make a list of the name and type of hub/study and how many hubs are in that state
    .agg({"jcoin_hub_types": lambda s: ",".join(s), "hub": "count"})
    .rename(columns={"hub":"jcoin_hub_count","state":"state_cd"})
    .reset_index()
    [["state_cd","jcoin_hub_types"]] # NOTE: these are the only vars going to be added
)

jcoin_df["is_jcoin_state"] = True

# %%
targetdf = targetdf.merge(jcoin_df, on="state_cd", how="left")
targetdf["jcoin_hub_types"].fillna("not JCOIN", inplace=True)
# targetdf["jcoin_hub_count"].fillna(0, inplace=True)
targetdf["is_jcoin_state"].fillna(False, inplace=True)
# targetdf["is_jcoin_hub"] = np.where(targetdf["jcoin_hub_types"] == "not JCOIN", "No", "Yes")

for field in fields.jcoin_hub:
    field = fl.Field.from_descriptor(field)
    schema.add_field(field)
# %%
# join strata into dataset
targetdf["p_over"] = sourcedf["p_over"].copy() #TODO: make part of sample and weighting fields
pop_counts_by_sampletypexstate = (
    targetdf.convert_dtypes()
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
        jcoin_flag=lambda df: df.is_jcoin_state.fillna(0).astype(int),
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


states_with_oversample_df = pop_counts_by_sampletypexstate[
    pop_counts_by_sampletypexstate["AS oversample"] > 0
]
states_with_oversample_list = states_with_oversample_df["state_cd"]
df_as_oversample_states = targetdf[targetdf["state_cd"].isin(states_with_oversample_list)]
# get caseids for survey respondents in oversampled states
caseid_in_as_oversample_state = df_as_oversample_states["caseid"]
strata_df = fl.Resource(path="data/raw/strata-and-psu.csv").to_pandas()
strata_df.columns = strata_df.columns.str.lower()
# get strata and cluster ids for survey respondents in oversampled states
strata_df_in_as_oversample_state = strata_df[
    strata_df["caseid"].isin(caseid_in_as_oversample_state)
]
# collapse strata containing only 1 PSU
strata_df = transforms.reassign_psu_and_strata(strata_df)
strata_df_in_as_oversample_state = transforms.reassign_psu_and_strata(strata_df_in_as_oversample_state)

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
oversample_strata_df = strata_df_in_as_oversample_state.set_index("caseid")[
    ["vstrat32_corrected", "vpsu32_corrected"]
].rename(
    columns={
        "vstrat32_corrected": "strata_oversample",
        "vpsu32_corrected": "psu_oversample",
    }
)
targetdf = (
    targetdf.set_index("caseid")
    .join(fullsample_strata_df)
    .join(oversample_strata_df)
    .assign(
        isin_state_with_oversample=lambda df: df.index.isin(
            caseid_in_as_oversample_state
        )
    )
    .reset_index()
)

for field in fields.sampling + fields.weights:

    # Add source variable if not already in dataset (ie the new strata/psu variables added from above)
    if not field["name"] in targetdf:
        targetdf[field["name"]] = sourcedf[field["name"]]
    # add all metadata to schema
    field = fl.Field.from_descriptor(field)
    schema.add_field(field)

resource = fl.Resource(data=targetdf.to_dict(orient="records"), schema=schema)

# make sure the new target dataset aligns with the schema (ie the expected datatypes etc)
report = resource.validate()
if not report.valid:
    raise Exception("Analytic dataset not valid")
resource.schema.to_yaml("schemas/processed/protocol2_wave1_analytic.yaml")
resource.write("data/processed/protocol2_wave1_analytic.csv")
