""" estimate models and create visualizations """

from stigma_state_level import models, visualization
import frictionless


measure_list = [
    "stigma_scale_score",
    "ss_6_past",
    "ss_6_current",
    "race_view_flag",
    "partyid5_strong_d",
    "partyid5_strong_r",
]

resource = frictionless.Resource(path="data/processed/protocol2_wave1_analytic.csv")
data = resource.to_pandas()
national_scalescore6_estimates = models.get_national_estimates(data)
national_scalescore6_plot = visualization.generate_bar_chart(national_scalescore6_estimates)
state_scalescore6_estimates = models.get_state_estimates()
state_scalescore6_plot = visualization.generate_bar_chart(estimate_df)
