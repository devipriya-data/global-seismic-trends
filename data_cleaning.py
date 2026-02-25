import pandas as pd
import re

df = pd.read_csv("/Users/devipriya/Desktop/Coding/Capstone Guvi project - 1/data/earthquakes_raw.csv")

print(f"Shape: {df.shape}")

print(df.head())

print(df.columns.tolist())

df["time"] = pd.to_datetime(df["time"])
df["updated"] = pd.to_datetime(df["updated"])

print("Time columns converted")
print(df["time"].dtype)

def extract_country(place):
    if pd.isna(place):
        return "Unknown"
 
    match = re.search(r",\s*([^,]+)$", place)
    if match:
        return match.group(1).strip()
    else:
        return place.strip()


df["country"] = df["place"].apply(extract_country)

print("Country extracted")
print(df["country"].value_counts().head(10))

df["year"] = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"] = df["time"].dt.day
df["day_of_week"] = df["time"].dt.day_name()

def depth_category(depth):
    if pd.isna(depth):
        return "Unknown"
    elif depth < 70:
        return "Shallow"
    elif depth < 300:
        return "Intermediate"
    else:
        return "Deep"

df["depth_category"] = df["depth_km"].apply(depth_category)

def mag_category(mag):
    if pd.isna(mag):
        return "Unknown"
    elif mag < 5.0:
        return "Minor"
    elif mag < 6.0:
        return "Moderate"
    elif mag < 7.0:
        return "Strong"
    else:
        return "Major"

df["mag_category"] = df["mag"].apply(mag_category)

print("Derived columns added")
print(df[["time", "year", "month", "day_of_week", "depth_category", "mag_category"]].head())

print("Missing values in each column:")
print(df.isnull().sum())

text_columns = ["magType", "status", "type", "net", "sources", "types"]

for col in text_columns:
    df[col] = df[col].str.strip()
    df[col] = df[col].str.lower()

print("Text columns cleaned")
print(df[["magType", "status", "type", "net"]].head())

numeric_columns = ["mag", "depth_km", "nst", "dmin", "rms", "gap", "sig"]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("Numeric columns cleaned")
print(df[numeric_columns].dtypes)


columns_to_drop = ["magError", "depthError", "magNst", "locationSource", "magSource"]

df = df.drop(columns=columns_to_drop)

print("Empty columns dropped")
print(f"New shape: {df.shape}")
print(f"Remaining columns: {df.columns.tolist()}")


partially_missing = ["nst", "dmin", "rms", "gap"]

for col in partially_missing:
    df[col] = df[col].fillna(df[col].median())

print("Missing values filled")
print(f"Total missing values remaining: {df.isnull().sum().sum()}")

df.to_csv("/Users/devipriya/Desktop/Coding/Capstone Guvi project - 1/data/earthquakes_cleaned.csv", index=False)

print(f"Cleaned data saved")
print(f"Final shape: {df.shape}")
print(df.head())