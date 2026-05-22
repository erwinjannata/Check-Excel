import pandas as pd

source = pd.read_csv(
    rf"C:\Users\Lenovo\Downloads\Inbound_21May_2026(1)_9767050.csv",
    encoding="iso-8859-1", low_memory=False)

# Close
# Success
sd_mask = (source["STATUS_POD"] == "Success") & (
    source["WUS_REMARKS"].str.contains("@SCAN DELIVERED", na=False))
sukses_delivered = source[sd_mask]
source = source[~sd_mask]

sdrw_mask = (source["STATUS_POD"] == "Success") & (
    source["RUNSHEET_NO"].str.contains("DRW", na=False))
sukses_drw = source[sdrw_mask]
source = source[~sdrw_mask]

sna_mask = (source["STATUS_POD"] == "Success") & (
    ~source["RUNSHEET_COURIER_ID"].str.contains("AMI", na=False))
sukses_non_ami = source[sna_mask]
source = source[~sna_mask]

ssn_mask = (source["STATUS_POD"] == "Success") & (
    source["SCO_NO"].fillna("").str.strip() != "")
sukses_sco_number = source[ssn_mask]
source = source[~ssn_mask]

# Return Shipper
rd_mask = (source["STATUS_POD"] == "Return Shipper") & (
    source["WUS_REMARKS"].str.contains("@SCAN DELIVERED", na=False))
return_delivered = source[rd_mask]
source = source[~rd_mask]

rdrt_mask = (source["STATUS_POD"] == "Return Shipper") & (
    source["RUNSHEET_NO"].str.contains("DRT", na=False))
return_drt = source[rdrt_mask]
source = source[~rdrt_mask]

rnc_mask = (source["STATUS_POD"] == "Return Shipper") & (
    source["RUNSHEET_COURIER_NAME"].fillna("").str.strip() == "")
return_no_courier = source[rnc_mask]
source = source[~rnc_mask]

closed = pd.concat(
    [sukses_delivered, sukses_drw, sukses_non_ami, sukses_sco_number, return_delivered, return_drt, return_no_courier], ignore_index=True)

closed["INBOUND_MANIFEST_DATE"] = pd.to_datetime(
    closed["INBOUND_MANIFEST_DATE"])
closed_groups = closed.groupby(
    closed["INBOUND_MANIFEST_DATE"].dt.strftime("%B %Y"))

for month, group in closed_groups:
    group.to_csv(rf"results\inbound\Close_{month}.csv", index=False)

# Auto Close
autoclose_mask = source["CODING"].isin(
    ["CL1", "CL2", "CL4", "D24", "D25", "D26", "D30", "D37", "R24", "R25", "R26", "R30", "R37"])
autoclose = source[autoclose_mask]
if not autoclose.empty:
    source = source[~autoclose_mask]
    autoclose["INBOUND_MANIFEST_DATE"] = pd.to_datetime(
        autoclose["INBOUND_MANIFEST_DATE"])
    autoclose_groups = autoclose.groupby(
        autoclose["INBOUND_MANIFEST_DATE"].dt.to_period("Y"))
    for month, group in autoclose_groups:
        group.to_csv(rf"results\inbound\AutoClose_{month}.csv", index=False)

# Sukses UnHRS
unhrs_mask = source["STATUS_POD"].isin(["Success", "Return Shipper"])
unhrs = source[unhrs_mask]
if not unhrs.empty:
    source = source[~unhrs_mask]
    unhrs["INBOUND_MANIFEST_DATE"] = pd.to_datetime(
        unhrs["INBOUND_MANIFEST_DATE"])
    unhrs_groups = unhrs.groupby(
        unhrs["INBOUND_MANIFEST_DATE"].dt.to_period("Y"))
    for year, group in unhrs_groups:
        group.to_csv(
            rf"results\inbound\00. Sukses inbound AMI un-HRS {year}.csv", index=False)


# Open
source["INBOUND_MANIFEST_DATE"] = pd.to_datetime(
    source["INBOUND_MANIFEST_DATE"], errors="coerce")

latest_period = source["INBOUND_MANIFEST_DATE"].dt.to_period("Y").max()
source["group_period"] = source["INBOUND_MANIFEST_DATE"].dt.to_period(
    "Y").fillna(latest_period)

for period, group in source.groupby("group_period"):
    group.drop(columns="group_period").to_csv(
        rf"results\inbound\00. AMI open inbound {period}.csv", index=False)
