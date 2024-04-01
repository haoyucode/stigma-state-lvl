""" estimate models and create visualizations """

from stigma_state_lvl import models, visualization
import frictionless
from pathlib import Path

measure_list = [
    "stigma_scale_score",
    "ss_6_past",
    "ss_6_current",
    "race_view_flag",
    "partyid5_strong_d",
    "partyid5_strong_r",
]
#'expanded_10item_stigma'
package = frictionless.Package.from_descriptor("datapackage.json")
data = package.get_resource("wave1-with-states-processed").to_pandas()
national_scalescore6_estimates = models.get_national_estimates(
    data, ycol="stigma_scale_score"
)
# national_scalescore6_plot = visualization.generate_bar_chart(national_scalescore6_estimates)
national_scalescore6_estimates.to_csv(
    "data/processed/national-scalescore6-estimates.csv"
)

package.add_resource(
    frictionless.Resource(
    name="national_scalescore6_estimates",
    title="National stigma scale score (6 item) estimates",
    description="National stigma scale estimation and variances for the 6 stigma scale score",
    path="data/processed/national-scalescore6-estimates.csv",
)

)
state_scalescore6_estimates = models.get_state_estimates(
    data, ycol="stigma_scale_score"
)
state_scalescore6_estimates.to_csv("data/processed/state-scalescore6-estimates.csv")
package.add_resource(
    frictionless.Resource(
        name="state_scalescore6_estimates",
        title="Individual state-level stigma scale score (6 item) estimates",
        description="State-level stigma scale estimation and variances for the 6 stigma scale score",
        path="data/processed/state-scalescore6-estimates.csv",
    )
)


# write new descriptors to package
package.to_json("datapackage.json")
# state_scalescore6_plot = visualization.generate_bar_chart(estimate_df)
