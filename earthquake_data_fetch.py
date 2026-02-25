import requests
import pandas as pd
from datetime import datetime
import time

BASE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

all_earthquakes = []

start_year = 2020
end_year = 2025

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        
        start_date = f"{year}-{month:02d}-01"
        
        if month == 12:
            end_date = f"{year + 1}-01-01"
        else:
            end_date = f"{year}-{month + 1:02d}-01"
            
        print(f"Fetching data for {start_date}...")

        params = {
            "format": "geojson",
            "starttime": start_date,
            "endtime": end_date,
            "minmagnitude": 4.0
        }
        
        response = requests.get(BASE_URL, params=params)
        
        if response.status_code == 200:
            data = response.json()
            earthquakes = data["features"]
            print(f"Found {len(earthquakes)} earthquakes!")

            for eq in earthquakes:
                
                props = eq["properties"]
                geom = eq["geometry"]["coordinates"]
                
                record = {
                    "id": eq["id"],
                    "mag": props.get("mag"),
                    "place": props.get("place"),
                    "time": datetime.fromtimestamp(props["time"] / 1000),
                    "updated": datetime.fromtimestamp(props["updated"] / 1000),
                    "status": props.get("status"),
                    "tsunami": props.get("tsunami"),
                    "sig": props.get("sig"),
                    "net": props.get("net"),
                    "nst": props.get("nst"),
                    "dmin": props.get("dmin"),
                    "rms": props.get("rms"),
                    "gap": props.get("gap"),
                    "magType": props.get("magType"),
                    "type": props.get("type"),
                    "magError": props.get("magError"),
                    "depthError": props.get("depthError"),
                    "magNst": props.get("magNst"),
                    "locationSource": props.get("locationSource"),
                    "magSource": props.get("magSource"),
                    "types": props.get("types"),
                    "ids": props.get("ids"),
                    "sources": props.get("sources"),
                    "longitude": geom[0],
                    "latitude": geom[1],
                    "depth_km": geom[2]
                }
                
                all_earthquakes.append(record)
        else:
            print(f"Failed to get data for {start_date}")
            
        time.sleep(1)

df = pd.DataFrame(all_earthquakes)

print(f"Total earthquakes collected: {len(df)}")
print(df.head())

df.to_csv("data/earthquakes_raw.csv", index=False)
print("Data saved to data/earthquakes_raw.csv")