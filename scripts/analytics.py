# %%
from stigma_state_lvl import models
import frictionless
from pathlib import Path

# %%
package = frictionless.Package.from_descriptor("datapackage.json")
resource = package.get_resource("wave1-with-states-processed")
df = resource.to_pandas()

modelpath = Path(__file__).parents[1].joinpath("models")
modelpath.mkdir(exist_ok=True)
field_names = [
    "ss_6_past",
    "ss_6_current",
    "ss_10_past",
    "ss_10_current",
    "racial_privilege",
    'expanded_10item_stigma',
    'stigma_scale_score'

]
for name in field_names:
    ycol =name
    print(ycol)
    natl_estimates = models.get_national_estimates(df, ycol=ycol)
    natl_estimates.to_csv(modelpath/f"national-{ycol}-estimates.csv")
    
    df_oversampled = df.loc[df.psu_oversample.notna()] # filter out records not in oversampled states
    state_estimates = models.get_state_estimates(df_oversampled, ycol=ycol)
    state_estimates.to_csv(modelpath/f"state-{ycol}-estimates.csv")