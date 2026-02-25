import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("/Users/devipriya/Desktop/Coding/Capstone Guvi project - 1/data/earthquakes_cleaned.csv")

print(f"Loaded {len(df)} rows")

engine = create_engine("mysql+pymysql://root:root123@127.0.0.1/earthquake_db")

df.to_sql("earthquakes", con=engine, if_exists="replace", index=False)

print("Data pushed to MySQL successfully!")
print(f"Total rows in database: {len(df)}")