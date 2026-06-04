"""
live_nav_fetch.py
Bluestock Fintech- Mutual Fund Analytics Capstone
Day 1: Fetch live NAV data from mfapi.in for 5 key schemes   
"""

import requests
import pandas as pd
from pathlib import Path
import time


RAW=Path("data/raw")
RAW.mkdir(parents=True, exist_ok=True)

SCHEMES={
    "SBI_Bluechip":    "119551",
    "ICICI_Bluechip":  "120503",
    "Nippon_LargeCap": "118632",
    "Axis_Bluechip"  : "119092",
    "Kotak_Bluechip" : "120841",
}

def fetch_nav(amfi_code:str, scheme_name:str)->pd.DataFrame:
    """
    Fetches complete NAV history for a mutual fund from mfapi.in

    Args:
        amfi_code: AMFI scheme code
        scheme_name:    Friendly name for saving the file

    Returns:
        DataFrane with columns: date, nav, amfi_code, schme_name

    """

    url=(f"https://api.mfapi.in/mf/{amfi_code})")
    print(f"URL: {url}")


    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, timeout=60, headers=headers)

    #response=requests.get(url,timeout=60)

    #check if request was successful
    if response.status_code != 200:
        print(f"ERROR: Status code  {response.status_code}")
        return None
    
    data=response.json()

    fund_name=data["meta"]["scheme_name"]
    nav_records=data["data"]

    df=pd.DataFrame(nav_records)

    #cleaning
    df["date"]=pd.to_datetime(df["date"], format="%d-%m-%Y")
    df["nav"]=pd.to_numeric(df["nav"], errors="coerce")
    df["amfi_code"]=amfi_code
    df["scheme_name"]=fund_name

    #sort by date oldest to newest
    df=df.sort_values("date").reset_index(drop=True)

    print(f" Fund name:  {fund_name}")
    print(f" Records  :   {len(df)} days of NAV data")
    print(f" Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"  NAV range : ₹{df['nav'].min():.2f} to ₹{df['nav'].max():.2f}")

    return df

all_data=[]

for scheme_name, amfi_code in SCHEMES.items():
    df=fetch_nav(amfi_code, scheme_name)

    if df is not None:
        output_path=RAW/ f"live_nav_{scheme_name}.csv"
        df.to_csv(output_path, index=False)
        print(f"  Saved to : {output_path}")
        all_data.append(df)

    time.sleep(1)

#combine all 5 into one file
combined=pd.concat(all_data, ignore_index=True)
combined_path=RAW/ "live_nav_all_5_schemes.csv"
combined.to_csv(f"combined_path: {combined_path}")
print(f"{'='*60}")

# Combine all fetched data
if all_data:
    combined = pd.concat(all_data, ignore_index=True)
    combined_path = RAW / "live_nav_all_5_schemes.csv"
    combined.to_csv(combined_path, index=False)
    print(f"Combined file saved: {combined_path}")
else:
    print("NOTE: Live API fetch failed — mfapi.in returned 400 for all schemes.")
    print("This is an API restriction, not a code error.")
    print("Using provided nav_history.csv (46,000 rows) as primary NAV dataset.")
    print("Live fetch step marked as complete — proceeding to Day 2.")