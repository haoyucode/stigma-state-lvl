""" utilities to support analyses """ 
import pandas as pd 
import numpy as np
#from scipy.stats import bootstrap
from scipy.stats._resampling import _bca_interval
import plotly.express as px

#parallel processing
from joblib import Parallel, delayed
import multiprocessing
# get bootstrap samples
# NOTE: scipy bootstrap does not capability to adjust probability (weights) of each resample.
 # two options to add weights: fork scipy and add option to add weights to internal resample function
 # or, use pandas sample function to compute bootstrap distribution and use scipy/custom fxn (or other fxn to compute BCa/or other intervals)
# the following could be added to scipy.stats._resampling._bootstrap_resample 
# (it's used in pandas sampling with weighting uses random.Generator.choice after standardizing weights):
# ```random_state.choice(obj_len, size=size, replace=replace, p=weights).astype(
#         np.intp, copy=False
#     )```
# 

def _get_weighted_bootstrap_sample(df,varcol,weightcol):
    """ 
    for a given dataframe, get one bootstrap replicate
    given probability of weights

    note the sample method uses random.Generator.choice after standardizing weights:
    random_state.choice(obj_len, size=size, replace=replace, p=weights).astype(
        np.intp, copy=False
    """ 
    sample = df.sample(
        n=len(df),
        replace=True, 
        weights=weightcol)
    return sample

def _compute_weighted_bootstrap_estimate(df,statistic,varcol,weightcol):
    """ compute a bootstrapped estimate with a given pandas method
    """

    sample = _get_weighted_bootstrap_sample(df,varcol,weightcol)
    
    #TODO: make more flexible with bivariate stats and additional params inputted into statistic
    # If using bca_interval, statistic function must have axis parameter
    estimate = statistic(sample[varcol].T.values,axis=-1) #get statistic over each variable
    return estimate


def bootstrap_pandas(df,
    varcol,
    weightcol,
    statistic,
    n_samples,
    confidence_level=.9,
    digits=2):
    """ 
    computes mean and 90% CIs (currently just BCa with scipy's method used in its bootstrap function)
    Can add other methods as appropriates (eg percentiles just using np.percentile)
    
    TODO: add additional kwargs for statistic (necessary for more complex stats such as mediation)
    """ 

    # change to list so read in as dataframe (list of arrays (structure for dataframe) needed for scipy bootstrap fxns)
    varcol = [varcol] if isinstance(varcol,str) else varcol
    assert isinstance(weightcol,str) and weightcol in df.columns,"weightcol must be name of a column in df"
    
    df = df[varcol+[weightcol]].copy()

    bootstrap_distribution = np.concatenate([
       _compute_weighted_bootstrap_estimate(df,statistic,varcol,weightcol)
       for i in range(n_samples)
    ],axis=-1)
    
    est = np.mean(bootstrap_distribution).round(digits)
    se = np.std(bootstrap_distribution).round(digits)
    # # compute accelerated bootstrap (BCa) -- see scipy bootstrap fxn
    # # from scipy.stats._resampling import _bca_interval
    # #https://github.com/scipy/scipy/blob/c1ed5ece8ffbf05356a22a8106affcd11bd3aee0/scipy/stats/_resampling.py#L596
    # # NOTE: this will only work for univariate stats - need to make custom function for more complex use cases
    # alpha = (1 - confidence_level)/2
    # bca_interval = _bca_interval(
    #     data=list(df[varcol].T.values), # transpose so each var is one array. Outer object needs to be list (inner can be a numpy array)
    #     statistic=statistic,
    #     axis=-1, 
    #     alpha=alpha,
    #     theta_hat_b=bootstrap_distribution, 
    #     batch=None
    #     )[:2]

    # # NOTE: scipy bootstrap uses _resample._percentile_along_axis which
    #     # is same as np.percentile for 1D bootstrap distribution. 
    #     # if groups, need to iterate over groups as in the scipy fxn
    #     # but here we are using the outer pandas groupby method for groups
    # bca_ci = np.percentile(
    #     bootstrap_distribution,[bca_interval[0]*100,bca_interval[1]*100]
    # ).round(digits)
    percentile_ci = np.percentile(
        bootstrap_distribution,[5,95]
    ).round(digits)
    summary = {
        "bootstrap_distribution":bootstrap_distribution,
        "mean":est,
        "standard_error":se,
        # "bca_lower_ci":bca_ci[0],
        # "bca_upper_ci":bca_ci[1],
        "percentile_lower_ci":percentile_ci[0],
        "percentile_upper_ci":percentile_ci[1]
    }
    return summary

def parallel_groupby_apply(df,groupby_name,func,funcargs):
    """ 
    computes a function as you would input into the .apply
    method. 

    func should return a pandas dataframe or series (or dictionary that can be converted
    into dataframe).
    
    returns a dataframe with group names as indices and 

    

    """
    def _group_func(name,groupdf,funcargs=funcargs):
        """
         the wrapper that uses the inputted func,adds the group name,
        and returns the result as a dataframe object
        """
        returned_group = func(df=groupdf,**funcargs)
        return (name,returned_group)

    grouped_df = df.groupby(groupby_name)
    
    returned_groups = Parallel(n_jobs=multiprocessing.cpu_count())(
        delayed(_group_func)(name=name,groupdf=groupdf) 
        for name, groupdf in grouped_df)
    
    return returned_groups

def concat_groupby(groups):
    """ concats a groupby object 
    or groupby-like object (eg a list of tuple[name,group])
    """ 
    grouped_df = pd.DataFrame(
    [pd.Series(group,name=name) 
    for name,group in state_bootstrap_stats])
    return grouped_df