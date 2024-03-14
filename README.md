stigma-state-lvl
==============================

State level analyses of opioid use disorder (OUD) using the JCOIN 
MAARC Stigma Survey Protocol 2 ("in-depth")

Project Organization
------------

NOTE: only included what makes sense for now. below is the default cookiecutter data science structure.

- [ ] TODO: modify this to given directory (e.g., changed some of the src package names, changed docs to markdown
- [ ] TODO: port to the more updated v2 cookie cutter data science template -- it is currently on the v2 branch of the cookiecutter data science repo (note this moves to mkdocs as in 1)
- [ ] TODO: replace requirements.txt with the "locked" version (ChatGPT says using "locked" version is better for analytic repos for reproducibility and supporting both an unlocked and locked is possible but may increase complexity)
    - NOTE: talked to Phil - he mentioned this may be overkill for most analyses. However, lets keep in here and decide at next "reorg" step as I think it could be still good for a proof of concept.
- [ ] TODO: Makefile: Windows does not support Makefiles -- one potential solution is to use docker. I commented on this issue [in cookiecutter-datascience here](https://github.com/drivendata/cookiecutter-data-science/issues/333)
- [ ] TODO: use datapackage.json in Makefile for any documentation or views (ie data dictionary, graphs etc)
comfortability using mkdocs -- may not need this but put here just in case)
    

    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>



Old Readme
------
# stigma-state-lvl
state level oud stigma estimate collaboration work with b. taylor and p. lamuda

# Usage

Get all packages used and dependencies:
`pip install -f requirements.txt`

# notebooks

`personaluse_ever_protocol2<latestn>.ipynb` contains the latest analysis.

Functions for this notebook have been refactored to `utils.py`


`strata-and-clusters-exploration`
contains exploration to identify the proper 
groups with the goal of understanding how to 
make correct bootstrap weights
