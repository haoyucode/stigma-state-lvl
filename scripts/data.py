""" 

process data and save in data/processed folder

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

# POPULATE TARGET SCHEMA AND DF WITH DEMOGRAPHICS
# %%
# add df column with state 2 letter code
# https://pythonfix.com/code/us-states-abbrev.py/
# state name to two letter code dictionary

us_state_to_abbrev = fl.Resource(path="data/state_abbrev_mappings.json").read_data()
state_cd = sourcedf.state.replace(us_state_to_abbrev)
targetdf["state_cd"] = state_cd
for field in fields.demographic:
    field = fl.Field.from_descriptor(field)
    schema.add_field(field)
    if not field.name in targetdf:
        targetdf[field.name] = sourcedf[field.name]

## political questions (rename to more human-readable names)
for field in fields.political:
    targetdf[field["name"]] = sourcedf[field["custom"]["jcoin:original_name"]]

targetdf["political_strength"] = targetdf.apply(transforms.applyfxns.determine_political_strength,axis=1)

## social stigma ############
### 10 question items (includes 6 item questions as well)
#### prepare individual items
for field in fields.ss_10_past + fields.ss_10_current:
    integer_coding = mappings.stigma10[field["name"]]
    data = sourcedf[field["name"]]
    data, field = transforms.categorical_to_numeric(data,field,integer_coding)
    data, field = transforms.impute_mode(data,field)
    targetdf[field["name"]] = data
    schema.add_field(fl.Field.from_descriptor(field))

#### compute composite items
ss_6_past = fields.ss_6_past_composite,fields.ss_6_past
ss_6_current = fields.ss_6_current_composite,fields.ss_6_current
ss_6 = fields.ss_6_composite,fields.ss_6_current + fields.ss_6_past
ss_10_past = fields.ss_10_past_composite,fields.ss_10_past
ss_10_current = fields.ss_10_current_composite,fields.ss_10_current
ss_10 = fields.ss_10_composite,fields.ss_10_current + fields.ss_10_past

for composite_field,input_fields in [ss_6_past,ss_6_current,ss_6,ss_10_past,ss_10_current,ss_10]:
    fieldnames = [field["name"] for field in input_fields]
    targetdf[composite_field["name"]],field = transforms.compute_mean(targetdf[fieldnames],composite_field)
    schema.add_field(fl.Field.from_descriptor(field))


## Cobra racial awareness

for field in fields.cobra_items:
    integer_coding = mappings.cobra[field["name"]]
    data = sourcedf[field["name"]]
    data, field = transforms.categorical_to_numeric(data,field,integer_coding)
    data, field = transforms.impute_mode(data,field)
    targetdf[field["name"]] = data
    schema.add_field(fl.Field.from_descriptor(field))

fieldnames = [field["name"] for field in fields.cobra_items]
composite_field = fields.cobra_composite
targetdf[composite_field["name"]],field = transforms.compute_mean(targetdf[fieldnames],composite_field)
schema.add_field(fl.Field.from_descriptor(field))

# vars_of_interest = [
#     "personaluse_ever",
#     "familyuse_ever",
#     "personalcrimjust_ever",
#     "familycrimjust_ever",
# ]
# for name in vars_of_interest:
#     targetdf[name] = sourcedf[name].copy()
#     schema.add_field(fl.Field.from_descriptor({"name":name,"type":"string"}))

# # clean up some of the categoricals to be consistently coded
# targetdf.familycrimjust_ever.replace({0: "No", 1: "Yes"}, inplace=True)
# targetdf.familyuse_ever.replace({" No": "No"}, inplace=True)
# targetdf.personalcrimjust_ever.replace(
#     {
#         "Yes, ever arrested or incarcerated": "Yes",
#         "No, never arrested or incarcerated": "No",
#     },
#     inplace=True,
# )


# # %%

# # # impute missing stigma scale score vals with median, impute missing personaluse_ever with mode, "No"
# # replace missing values of personaluse_ever with mode value of 'No'
# targetdf.personaluse_ever.fillna("No", inplace=True)
# targetdf.familyuse_ever.fillna("No", inplace=True)
# targetdf.personalcrimjust_ever.fillna("No", inplace=True)
# targetdf.familycrimjust_ever.fillna("No", inplace=True)

# # %%
##### Add jcoin information ####
jcoin_json = fl.Resource(path="data/jcoin_states.json").read_data()

jcoin_df = (
    pd.DataFrame(jcoin_json)
    .assign(jcoin_hub_types=lambda df: df["hub"] + "(" + df["type"] + ")")
    .groupby("states")
    # make a list of the name and type of hub/study and how many hubs are in that state
    .agg({"jcoin_hub_types": lambda s: ",".join(s), "hub": "count"})
    .reset_index()
    .rename(columns={"hub":"jcoin_hub_count","states":"state_cd"})
)

jcoin_df["is_jcoin_state"] = True

# %%
targetdf = targetdf.merge(jcoin_df, on="state_cd", how="left")
targetdf["jcoin_hub_types"].fillna("not JCOIN", inplace=True)
targetdf["jcoin_hub_count"].fillna(0, inplace=True)
targetdf["is_jcoin_state"].fillna(False, inplace=True)
targetdf["is_jcoin_hub"] = np.where(targetdf["jcoin_hub_types"] == "not JCOIN", "No", "Yes")

for field in fields.jcoin_hub:
    field = fl.Field.from_descriptor(field)
    schema.add_field(field)
# %%
# join strata into dataset
targetdf["p_over"] = sourcedf["p_over"].copy() #TODO: make part of sample and weighting fields
pop_counts_by_sampletypexstate = (
    targetdf.convert_dtypes()
    .assign(jcoin_hub_count=lambda df: df.jcoin_hub_count.astype(str))
    .groupby(["state_cd", "p_over"])
    .count()
    .iloc[:,0]
   .unstack(["p_over"])
   .assign(total=lambda df:df.sum(axis=1))
)

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

# for name in schema.field_names:
#     if not name in targetdf:
#         targetdf[name] = sourcedf[name]

resource = fl.Resource(data=targetdf[schema.field_names].fillna("").to_dict(orient="records"),schema=schema)

# make sure the new target dataset aligns with the schema (ie the expected datatypes etc)
report = resource.validate()
if not report.valid:
    print(report.to_summary())
    raise Exception("Analytic dataset not valid")

resource.schema.to_yaml("schemas/processed/protocol2_wave1_analytic.yaml")
resource.write("data/processed/protocol2_wave1_analytic.csv")
