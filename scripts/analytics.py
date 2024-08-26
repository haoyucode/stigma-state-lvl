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
#  'age4',
#  'racethnicity',
#  'educ5',
 'ss_a_historywork',
 'ss_b_historymarry',
 'ss_historysteal',
 'ss_historyhighrisk',
 'ss_c_currentwork',
 'ss_d_currentmarry',
 'ss_e_dangerous',
 'ss_f_trust',
 'ss_currentsteal',
 'ss_currenthighrisk',
 'ss_6_past',
 'ss_6_current',
 'stigma_6item_composite',
 'ss_10_past',
 'ss_10_current',
 'stigma_10item_composite',
 'race_whiteadvantage',
 'race_successful',
 'race_prison',
 'race_socservices',
 'race_minadvantage',
 'race_rich',
 'race_whiteblame',
 'racial_privilege'
]
for name in field_names:
    ycol =name
    print(ycol)
    natl_estimates = models.get_national_estimates(df, ycol=ycol)
    natl_estimates.to_csv(modelpath/f"national-{ycol}-estimates.csv")
    
    df_oversampled = df.loc[df.psu_oversample.notna()] # filter out records not in oversampled states
    state_estimates = models.get_state_estimates(df_oversampled, ycol=ycol)
    state_estimates.to_csv(modelpath/f"state-{ycol}-estimates.csv")