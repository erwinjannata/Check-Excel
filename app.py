import pandas as pd

date_column = [
    "AWB", "TGL_ENTRY", "RECEIVING_DATE", "OUTBOUND_MANIFEST_DATE", "INBOUND_MANIFEST_DATE", "DATE_TRANSIT", "HVO_DATE", "HVI_DATE", "DATE_RUNSHEET", "TGL_RECEIVED", "TGL_UPDATE_STATUS_POD", "WUS_DATE", "DATE_1ST_ATTEMPT", "DATE_2ND_ATTEMPT", "DATE_LAST_ATTEMPT", "PRA_RUNSHEET_DATE", "CS3_DATE", "DATE_CONNOTE_RETURN_RT", "DATE_CONNOTE_RETURN_RF", "TRANSIT_MANIFEST_DATE", "IREG_DATE", "CLAIM_DATE", "HBG_DATE", "1ST_HVO_DATE", "LAST_HVO_DATE", "MANIFEST_TRANSIT_SUBAGEN_DATE", "MANIFEST_INBOUND_SUBAGEN_DATE", "LATEST_SM_DATE", "1ST_PREVIOUS_SM_DATE", "2ND_PREVIOUS_SM_DATE", "1ST_TRANSIT_MANIFEST_DATE", "2ND_TRANSIT_MANIFEST_DATE", "3RD_TRANSIT_MANIFEST_DATE", "LAST_TRANSIT_MANIFEST_DATE", "HO_COURIER_DATE", "WAREHOUSE_DATE", "OFFICE_DATE", "HACB_DATE", "HBAG_DATE", "PICKUP_DATE", "1ST_RUNSHEET_DATE", "LAST_DATE_DO", "DATE_RCW", "DATE_LPR", "DATE_RDO", "TGL_TARIK_REPORT",
]

source = pd.read_csv(
    rf"C:\Users\Lenovo\Downloads\Inbound_05Jun_2026_9810575.csv",
    encoding="iso-8859-1", low_memory=False)

data = pd.DataFrame(data=source, columns=date_column)


for x, cols in enumerate(date_column):
    if x != 0:
        data[cols] = pd.to_datetime(data[cols], format="mixed")
        data[cols] = data[cols].dt.date

with pd.ExcelWriter("excel.xlsx", engine="xlsxwriter") as writer:
    data.to_excel(writer, index=False)
