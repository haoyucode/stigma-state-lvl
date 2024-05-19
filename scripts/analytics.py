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
for field in resource.schema.fields:
    if field.custom.get("custom",{}).get("derived") or field.custom.get("derived"):
        ycol = field.name
        natl_estimates = models.get_national_estimates(df, ycol=ycol)
        natl_estimates.to_csv(modelpath/f"national-{ycol}-estimates.csv")
        state_estimates = models.get_state_estimates(df, ycol=ycol)
        state_estimates.to_csv(modelpath/f"state-{ycol}-estimates.csv")