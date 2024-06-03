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
        "type": "string",
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
        "description": "Highest educational degree based on 5 categories",
        "type": "string",
    },
]


jcoin_hub = [
    {
        "name": "jcoin_hub_count",
        "type": "integer",
        "description": "Number of hubs in a particular state",
    },
    {
        "name": "jcoin_hub_types",
        "type": "string",
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
    "type": "number",
    "title": "Unawareness of Racial Privilege ",
    "description": "Composite score for factor 1 in Color-Blind Racial Attitudes Scale.",
    **standardsmappings.cobra,
}

cobra_items = [
    {
        "name": "race_whiteadvantage",
        "description": "[White people in the U.S. have certain advantages because of the color of their skin.] Do you disagree or agree with the following statements?",
        "type": "integer",
    },
    {
        "name": "race_successful",
        "description": "[Race is very important in determining who is successful and who is not.] Do you disagree or agree with the following statements?",
        "type": "integer",
    },
    {
        "name": "race_prison",
        "description": "[Race plays an important role in who gets sent to prison.] Do you disagree or agree with the following statements?",
        "type": "integer",
    },
    {
        "name": "race_socservices",
        "description": "[Race plays a major role in the type of social services (such as type of health care or day care) that people receive in the U.S.] Do you disagree or agree with the following statements?",
        "type": "integer",
    },
    {
        "name": "race_minadvantage",
        "description": "[Racial and ethnic minorities in the U.S. have certain advantages because of the color of their skin.] Do you disagree or agree with the following statements?",
        "type": "integer",
    },
    {
        "name": "race_rich",
        "description": "[Everyone who works hard, no matter what race they are, has an equal chance to become rich.] Do you disagree or agree with the following statements?",
        "type": "integer",
    },
    {
        "name": "race_whiteblame",
        "description": "[White people are more to blame for racial discrimination than racial and ethnic minorities.] Do you disagree or agree with the following statements?",
        "type": "integer",
    },
]


ss_6_past = [
    {
        "section": "Social stigma",
        "name": "ss_a_historywork",
        "title": "Person with past OUD **work** closely",
        "description": (
            "[I would be willing to have a person with a past history of opioid use disorder start working closely with me on a job.]"
            "Do you disagree or agree with the following statements?"
        ),
        "type": "integer",
    },
    {
        "section": "Social stigma",
        "name": "ss_b_historymarry",
        "title": "Person with past OUD **marry** into family",
        "description":("[I would be comfortable having a person with a past history of opioid use disorder marry into my close or immediate family.] "
            "Do you disagree or agree with the following statements?"),
        "type": "integer",
    },
]

ss_6_current = [
    {
        "section": "Social stigma",
        "name": "ss_c_currentwork",
        "title": "Person with past OUD: **working** closely",
        "description": (
            "[I would be willing to have a person with a current opioid use disorder start working closely with me on a job.]"
            "Do you disagree or agree with the following statements?"
        ),
        "type": "integer",
    },
    {
        "section": "Social stigma",
        "name": "ss_d_currentmarry",
        "description": (
            "[I would be comfortable having a person with a current opioid use disorder marry into my close or immediate family.]"
            " Do you disagree or agree with the following statements?"
        ),
        "title": "Person with past OUD: **marrying** into family",
        "type": "integer",
    },
    {
        "section": "Social stigma",
        "name": "ss_e_dangerous",
        "title": "Person with current OUD: Dangerous",
        "description": (
            "[People with a current opioid use disorder are more dangerous than the general population.]"
            " Do you disagree or agree with the following statements?"
        ),
        "type": "integer",
    },
    {
        "name": "ss_f_trust",
        "title": "Person with current OUD: Cannot Trust",
        "description": (
            "[A person who currently has an opioid use disorder cannot be trusted.]"
            " Do you disagree or agree with the following statements?"
        ),
        "type": "integer",
    },
]

ss_6_current_composite = {
    "section": "Social stigma (6 question)",
    "name": "ss_6_current",
    "type": "number",
    "description": "Attitude towards opioid stigma for **current** users using 2 past user questions in 6 question stigma scale.",
}
ss_6_past_composite = {
    "section": "Social stigma (6 question)",
    "name": "ss_6_past",
    "type": "number",
    "description": (
        "Attitude towards opioid stigma for **past**"
        "users using 2 past user questions in 6 question stigma scale."
    ),
}
ss_6_composite = {
    "name": "stigma_6item_composite",
    "type": "number",
    "title": "6 question social stigma scale score",
    "description": "Composite score (derived from 6 questions) on attitude towards opioid stigma users",
}
ss_10_past = ss_6_past + [
    {
        "name": "ss_historysteal",
        "description": (
            "[A person who has a past history of opioid use disorder would be willing to steal money or valuable items in order to get drugs.] "
            "Do you disagree or agree with the following statements?"
        ),
        "type": "integer",
    },
    {
        "name": "ss_historyhighrisk",
        "description": (
            "[A person who has a past history of opioid use disorder is likely to experience personal problems that would make them a high-risk employee in my workplace.] "
            "Do you disagree or agree with the following statements?"
        ),
        "type": "integer",
    },
]

ss_10_current = ss_6_current + [
    {
        "name": "ss_currentsteal",
        "description": (
            "[A person who currently has an opioid use disorder would be willing to steal money or valuable items in order to get drugs.] "
            "Do you disagree or agree with the following statements?"
        ),
        "type": "integer",
    },
    {
        "name": "ss_currenthighrisk",
        "description": (
            "[A person who currently has an opioid use disorder is likely to experience personal problems that would make them a high-risk employee in my workplace.] "
            "Do you disagree or agree with the following statements?"
        ),
        "type": "integer",
    },
]

ss_10_current_composite = {
    "section": "Social stigma (10 question)",
    "name": "ss_10_current",
    "type": "number",
    "description": "Attitude towards opioid stigma for **current** users using all past user questions in 10 question stigma scale.",
}
ss_10_past_composite = {
    "section": "Social stigma (10 question)",
    "name": "ss_10_past",
    "type": "number",
    "description": (
        "Attitude towards opioid stigma for **past**"
        "users using all past user questions in 10 question stigma scale."
    ),
}

ss_10_composite = {
    "section": "Social stigma (10 question)",
    "name": "stigma_10item_composite",
    "title": "10 question social stigma scale score",
    "type": "number",
    "description": "Composite score (derived from 10 questions) on attitude towards opioid stigma users",
}

political = [
    {
        "section": "Political Party",
        "name": "party_affiliation",
        "title": "Political Party Affiliation (Democrat, Republican, Independent)",
        "description": "Do you consider yourself a Democrat, a Republican, an Independent or none of these?",
        "type": "string",
        "custom": {"jcoin:original_name": "pid1"},
    },
    {
        "section": "Political Party",
        "name": "strong_democrat",
        "title": "Strong Democrat",
        "description": "Do you consider yourself a strong or not so strong Democrat?",
        "type": "string",
        "custom": {"jcoin:original_name": "pida"},
    },
    {
        "section": "Political Party",
        "name": "strong_republican",
        "title": "String Republican",
        "description": "Do you consider yourself a strong or not so strong Republican?",
        "type": "string",
        "custom": {"jcoin:original_name": "pidb"},
    },
    {
        "section": "Political Party",
        "name": "lean_demo_or_repub",
        "title": "Lean Democrat or Republican",
        "type": "string",
        "custom": {"jcoin:original_name": "pidi"},
    },
]
political_strength = {
    "section": "Political Party",
    "name": "party_strength",
    "title": "Political Party Strength of Affiliation",
    "type": "string",
    "custom": {"jcoin:original_name": "partyid7"},
}
