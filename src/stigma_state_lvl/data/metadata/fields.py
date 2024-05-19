from . import standardsmappings

# TODO: add Fields object and inherit

caseid = {
    "name": "caseid",
    "title": "Case ID",
    "description": (
        "The unique identifier for the sampled Amerispeak participant.\n\n"
        " WARNING: this id is generated for this specific protocol/wave."
        "If using other waves within protocol or between protocols, "
        "this field should not be used and a crosswalk is required."
    ),
    "type": "integer",
}

weights = [
    {
        "section": "Sampling/weights",
        "name": "weight1",
        "title": "Weights: general",
        "description": "Post-stratification weights for general population. Participants that were sampled via state oversampling should NOT have this weight.",
        "type": "number",
    },
    {
        "section": "Sampling/weights",
        "name": "weight2",
        "title": "Weights: general and oversampled",
        "description": "Post-stratification weights for general and oversampled state population. Every record (participant) should have this weight.",
        "type": "number",
    },
    {
        "section": "Sampling/weights",
        "name": "p_over",
        "title": "Sample indicator",
        "description": "Indicates which sample the participant was from (Oversampled state or general population)",
        "constraints": {"enum": ["AS oversample", "Gen pop"]},
    },
]
demographic = [
    {
        "section": "Geographic Location",
        "name": "state_cd",
        "title": "2 letter state code",
        "description": "Identifies the [2 letter ISO code](https://en.wikipedia.org/wiki/ISO_3166-2:US) for the state",
        "constraints": {"pattern": "[A-Z][A-Z]"},
        "examples": ["MA", "IL", "KY"],
        "type": "string",
    },
    {
        "section": "Demographics",
        "name": "age4",
        "title": "Age - 4 Categories",
        "description": "",
        "type": "string",
    },
    {
        "section": "Demographics",
        "name": "racethnicity",
        "title": "Combined Race/Ethnicity",
        "description": "",
        "type": "string",
    },
    {
        "section": "Demographics",
        "name": "educ5",
        "title": "5-level education",
        "description": "",
        "type": "number",
    },
]


jcoin_hub = [
    {"name": "jcoin_hub_count", "description": "Number of hubs in a particular state"},
    {
        "name": "jcoin_hub_types",
        "description": "List of hubs with the type of study in parentheses OR not jcoin for this particular state",
        "examples": [
            "CoolHubName (Linkage), AnotherCoolHub (State policy rollout)",
            "Not JCOIN",
            "non JCOIN comparison",
        ],
    },
    {
        "name": "is_jcoin_state",
        "description": "Indicates whether or not state has at least one jcoin site",
        "type": "boolean",
    },
]

# Post-processing of stratum and cluster IDs
# Assign globally unique IDS for clusters
# Collapse strata with 1 cluster into a single ‘fake’ stratum – conservative; increases standard error by a small amount

# Use samplics python package implementation of Taylor linearization to estimate survey statistic point estimates and variance on these point estimates

sampling = [
    {
        "section": "Sampling/weights",
        "name": "strata_fullsample",
        "type": "integer",
        "title": "Strata: Full sample",
        "description": "The strata group identifier for the general population sample (for assoc weights, see `weight1`)",
    },
    {
        "section": "Sampling/weights",
        "name": "psu_fullsample",
        "type": "integer",
        "description": "The primary sampling unit (PSU) identifier for the general population sample (for assoc weights, see `weight1`)",
    },
    {
        "section": "Sampling/weights",
        "name": "strata_oversample",
        "type": "integer",
        "description": "The primary sampling unit (PSU) identifier for the genpop + oversample (for assoc weights, see `weight2`)",
    },
    {
        "section": "Sampling/weights",
        "name": "psu_oversample",
        "type": "integer",
        "description": "The strata group identifier for the genpop + oversample (for assoc weights, see `weight2`)",
    },
]

cobra_composite = {
    "name": "racial_privilege",
    "type": "integer",
    "title": "Unawareness of Racial Privilege ",
    "description": "Composite score for factor 1 in Color-Blind Racial Attitudes Scale.",
    **standardsmappings.cobra,
    "custom":{"derived":True}
}

ss_6_past = [
    {
        "section": "Social stigma",
        "name": "ss_a_historywork",
        "title": "Person with past OUD **work** closely",
    },
    {
        "section": "Social stigma",
        "name": "ss_b_historymarry",
        "title": "Person with past OUD **marry** into family",
    },
]


ss_6_current = [
    {
        "section": "Social stigma",
        "name": "ss_a_historywork",
        "title": "Person with past OUD: **working** closely",
    },
    {
        "section": "Social stigma",
        "name": "ss_b_historymarry",
        "title": "Person with past OUD: **marrying** into family",
    },
    {"name":"ss_e_dangerous"},
    {"name":"ss_f_trust"}
]
ss_6_current_composite = {
        "section": "Social stigma (6 question)",
        "name": "ss_6_current",
        "type": "number",
        "description": "Attitude towards opioid stigma for **current** users using 2 past user questions in 6 question stigma scale.",
        "custom": {"derived": True},
    }
ss_6_past_composite =  {
        "section": "Social stigma (6 question)",
        "name": "ss_6_past",
        "type": "number",
        "description": (
            "Attitude towards opioid stigma for **past**" 
            "users using 2 past user questions in 6 question stigma scale."
        ),
        "custom": {"derived": True},
    }
stigma6 = ss_6_current + ss_6_past

ss_10_past = ss_6_past + [
    {"name":"ss_historysteal"},
    {"name":"ss_historyhighrisk"}       
]

ss_10_current = ss_6_current + [
    {"name":"ss_currentsteal"},
    {"name":"ss_currenthighrisk"}       
]

ss_10_current_composite = {
        "section": "Social stigma (10 question)",
        "name": "ss_10_current",
        "type": "number",
        "description": "Attitude towards opioid stigma for **current** users using all past user questions in 10 question stigma scale.",
        "custom": {"derived": True},
    }
ss_10_past_composite =  {
        "section": "Social stigma (10 question)",
        "name": "ss_10_past",
        "type": "number",
        "description": (
            "Attitude towards opioid stigma for **past**" 
            "users using all past user questions in 10 question stigma scale."
        ),
        "custom": {"derived": True},
    }

stigma10 = ss_10_current + ss_10_past