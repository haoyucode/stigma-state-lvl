""" contains transforms to build the analytic dataset and add associated metadata """

from pandas.api.types import CategoricalDtype

def categorical_to_numeric(data,meta,mapping,impute=True):
    """
    
    takse a set of mappings and converts a categorical variable from the source data 
    to the target dataset and oreganizes the relevant field-level metadata including:
    1. any metadata inputted from the getgo (defaults to no metadata)
    1. `enumLabels`
    2. additional annotation in description surrounding transforms

    NOTE
    -----
    data: series or array contains `mappings`
    mappings: the key-value mapping to replace category values
    imput:If impute is True, imputes the mode and metadata about transform (defaults to true)


    TODO
    ------
    create default option (if no mappings) to map the categorical codes +1 as enumLabels

    """
    categorytype = CategoricalDtype(ordered=True,categories=mapping.keys())
    categoricaldata = data.astype(categorytype)

    meta["description"] += "\n"
    meta["description"] += "**Transform steps**"
    meta["description"] += "\n"

    if impute:
        meta["description"] += f"- Imputed the mode (`{categoricaldata.mode()[0]}`)"
        categoricaldata.fillna(categoricaldata.mode(),inplace=True)

    meta["description"] += "- Replaced value labels with integer codes (see `enumLabels`)"
    meta["type"] = "integer"
    meta["enumLabels"] = {str(val):key for key,val in mapping.items()}
    meta["constraints"] = {"enum":list(mapping.values())}
    
    numericdata = categoricaldata.replace(mapping)

    return numericdata,meta

def impute_mean(data,meta):
    data = data.copy()
    meta = dict(meta)
    meta["description"] += "\n"
    meta["description"] += "**Transform steps**"
    meta["description"] += "\n"

    if impute:
        meta["description"] += f"- Imputed the mean (`{data.mean()[0]}`)"
        data.fillna(data.mean(),inplace=True)

    meta["description"] += "- Replaced value labels with integer codes (see `enumLabels`)"
    meta["type"] = "number"

    return data,meta