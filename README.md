stigma-state-lvl
==============================

State level analyses of opioid use disorder (OUD) using the JCOIN 
MAARC Stigma Survey Protocol 2 ("in-depth")

## Usage

1. In a virtual environment, get all packages used and dependencies in addition to the local module in `src`:
    - If using pip/python/venv module: `pip install -f requirements.txt`
    - [RECOMMENDED] If using conda/mamba: `conda env create -f conda-environment-lock.yaml`
    ::important:: Remember to activate this virtual env before continuing!

2. Run from CLI: `dvc fetch` : download all files from remote.
3. Run from CLI: `python scripts/data.py` TOODO: make function and put into `report.ipynb` to make easier (or use snakeMake?)
    !important The `datapackage.json` is thought of as the metadata providing a starting point for understanding the data in the repository.
4. `report.ipynb` : use the metadata, model, and visualization functions to make a report. This notebook's goal is to not only
    report out on selected variable estimations but also to demostrate the utility of frictionless in the context of an analytic 
    report/explroation.


## Project Organization

Inspired by [cookie cutter for data science template]("https://drivendata.github.io/cookiecutter-data-science/")


    
```
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling. NOTE: analytic dataset
    │   └── raw            <- The original, immutable data dump NOTE: data pulled from P drive
    │
    ├── docs               <- A default ~~Sphinx~~ (markdown) project
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- [NOT USED CURRENTLY] Data dictionaries, manuals, and all other explanatory materials. NOTE -- could put "human rendered" schema here and other manuals or pdfs.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    ├── requirements-lock.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── transform.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions NOTE: in this case we are just estimating the point estimates/variance of variables of interest
    │   │   ├── estimates.py
    │   │  
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py <- contains bar charts of estimates and usa maps for state estimates

```

## Saving and committing notebooks
commit jupyter notebook without output to git and keep output locally: 
https://gist.github.com/33eyes/431e3d432f73371509d176d0dfb95b6e

NOTE: 
- you have to have activated a virtualenv with nbconvert installed at the time you add/commit a jupyter nb for this to work 



