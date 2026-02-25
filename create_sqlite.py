import pandas as pd
import sqlite3

# Read cleaned CSV
df = pd.read_csv("data/earthquakes_cleaned.csv")

# Create SQLite database
conn = sqlite3.connect("earthquakes.db")
df.to_sql("earthquakes", conn, if_exists="replace", index=False)
conn.close()

print("SQLite database created successfully!")
print(f"Total rows: {len(df)}")