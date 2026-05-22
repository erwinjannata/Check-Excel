import pandas as pd

source = pd.read_csv(
    rf"C:\Users\Lenovo\Downloads\Outbound_21May_2026_9767043.csv",
    encoding="iso-8859-1", low_memory=False)

# Close
closed_mask = source["STATUS_POD"].isin(
    ["Success", "Return Shipper", "Destroyed", "Missing"])
closed = source[closed_mask]
closed["TGL_ENTRY"] = pd.to_datetime(closed["TGL_ENTRY"])
closed_groups = closed.groupby(closed["TGL_ENTRY"].dt.strftime("%B %Y"))
for month, group in closed_groups:
    group.to_csv(
        rf"results\outbound\Close_{month}.csv", index=False)

# AWB Cancel
cancel_mask = source["AWB_CANCEL"] == "Y"
cancel = source[cancel_mask]
if not cancel.empty:
    cancel["TGL_ENTRY"] = pd.to_datetime(cancel["TGL_ENTRY"])
    cancel_groups = cancel.groupby(cancel["TGL_ENTRY"].dt.to_period("Y"))
    for month, group in cancel_groups:
        group.to_csv(rf"results\outbound\Cancel_{month}.csv", index=False)

# Auto Close
autoclose_mask = source["CODING"].isin(
    ["CL1", "CL2", "CL4", "D24", "D25", "D26", "D30", "D37", "R24", "R25", "R26", "R30", "R37"])
autoclose = source[autoclose_mask]
if not autoclose.empty:
    autoclose["TGL_ENTRY"] = pd.to_datetime(autoclose["TGL_ENTRY"])
    autoclose_groups = autoclose.groupby(
        autoclose["TGL_ENTRY"].dt.to_period("Y"))
    for month, group in autoclose_groups:
        group.to_csv(rf"results\outbound\AutoClose_{month}.csv", index=False)

# Open
# Remove the closed, cancel, and autoclose from main dataframe first
source = source[~(closed_mask | cancel_mask | autoclose_mask)]
source["TGL_ENTRY"] = pd.to_datetime(source["TGL_ENTRY"])
open_groups = source.groupby(
    source["TGL_ENTRY"].dt.to_period("Y"))
for year, group in open_groups:
    group.to_csv(
        rf"results\outbound\00. AMI open outbound {year}.csv", index=False)
