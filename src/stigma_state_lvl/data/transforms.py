""" contains transforms to build the analytic dataset and add associated metadata """

from pandas.api.types import CategoricalDtype
import pandas as pd

# TODO: create separate namespaces for fxns that only transform data, transform data + metadata, [DONE] transform row in `df.apply`
def categorical_to_numeric(data:pd.Series,meta,mapping):
    """
    
    takes a categorical variable (or variable that is intended to be converted to a categorical)
     from the source data 
    to the target dataset and oreganizes the relevant field-level metadata including:
    1. any metadata inputted from the getgo
    2. `enumLabels`
    3. additional annotation in description surrounding transforms from source categorical field

    NOTE
    -----
    data: series or array 
    meta: 

    TODO
    ------
    create default option (if no mappings) to map the categorical codes +1 as enumLabels

    """
    categorytype = CategoricalDtype(ordered=True,categories=mapping.keys())
    categoricaldata = data.astype(categorytype)
    numericdata = categoricaldata.replace(mapping)

    meta = dict(meta)
    meta["description"] += "\n"
    meta["description"] += "- **Transform**:Replaced value labels with integer codes (see `enumLabels`)"
    meta["enumLabels"] = {str(val):key for key,val in mapping.items()}

    if meta.get("constraints"):
        meta.update(enums)
    else:
        meta["constraints"] = {"enum":list(mapping.values())}
    
    return numericdata,meta

def impute_mean(data,meta):
    """ 
    Takes a dataframe and frictionless metadata field (or descriptor)
    and imputes mean and notes in metadata field description
    """
    data = data.copy()
    meta = dict(meta)
    meta["description"] += "\n"
    meta["description"] += f"- **Imputation**: Imputed the mean (`{data.mean()[0]}`)"
    data.fillna(data.mean(),inplace=True)

    return data,meta

def impute_mode(data,meta):
    data = data.copy()
    meta = dict(meta)
    meta["description"] += "\n"
    meta["description"] += "**Imputation**: Most frequent value (mode)"
    data.fillna(data.mode()[0],inplace=True)

    return data,meta

def compute_mean(data,meta):
    data = data.copy()
    meta = dict(meta)
    meta["description"] += "\n"
    meta["description"] += f"**Transform**: The mean of `{'`,`'.join(data.columns.tolist())}`"
    return data.mean(axis=1),meta

def reassign_psu_and_strata(strata_df:pd.DataFrame):
    """ 
    reassigns names to psu and strata groupings
    such that it (1) collapses strata containing
    only one PSU and (2) renames PSUs so no psu dupcliate
    names (which can happen for psus in different strata -- eg PSU =1 in strta=5 and psu = 1 in strata = 7)
    
    """ 
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
    return strata_df


class applyfxns:
    """ per row functions that can be input into a df.apply(fxn) call
    e.g., `transforms.applyfxns.determine_political_strength`
    """
    @staticmethod
    def determine_political_strength(row):

        """ assign values based on values in other political party
        fields
        """ 
        if row.lean_demo_or_repub == "Lean Democrat":
            return "Lean Democrat"
        elif row.lean_demo_or_repub == "Lean Republican":
            return "Lean Republican"
        elif row.strong_republican == "Not so strong Republican":
            return "Not so strong Republican"
        elif row.strong_republican == "Strong Republican":
            return "Strong Republican"
        elif row.strong_democrat == "Not so strong Democrat":
            return "Not so strong Democrat"
        elif row.strong_democrat == "Strong Democrat":
            return "Strong Democrat"
        elif row.party_affiliation in ["Independent","None of these"]:
            return "Don't Lean/Independent/None"
        else:
            return None