# Global Seismic Trends: Data-Driven Earthquake Insights

## Project Overview
This project analyzes 95,693 global earthquake records from 2020-2025 using Python, MySQL, and Streamlit to identify seismic patterns, trends, and risk zones.

## Domain
- Disaster Management
- Geoscience
- Seismology

## Skills Used
- Python for Data Analytics
- Regular Expressions (Regex)
- SQL & Relational Database Management
- Streamlit Dashboard Development

## Project Structure
```
Capstone Guvi project - 1/
├── data/
│   ├── earthquakes_raw.csv        # Raw data from USGS API
│   └── earthquakes_cleaned.csv    # Cleaned and processed data
├── earthquake_data_fetch.py       # Fetches data from USGS API
├── data_cleaning.py               # Cleans and preprocesses data
├── data_push.py                   # Pushes data to MySQL
├── queries.sql                    # All 30 SQL queries
├── app.py                         # Streamlit dashboard
└── README.md                      # Project documentation
```

## How to Run

### Requirements
```bash
pip install requests pandas sqlalchemy pymysql streamlit plotly mysql-connector-python
```

### Step 1 - Fetch Data from USGS API
```bash
python earthquake_data_fetch.py
```

### Step 2 - Clean Data
```bash
python data_cleaning.py
```

### Step 3 - Push to MySQL
```bash
python data_push.py
```

### Step 4 - Run Streamlit App
```bash
streamlit run app.py
```

## Database Details
- Database: earthquake_db
- Table: earthquakes
- Total Records: 95,693
- Total Features: 28 columns
- Time Period: 2020 - 2025

## Key Findings
- **Indonesia** has the most earthquakes (9,251 in 5 years)
- **Fiji** has the deepest earthquakes (over 660km deep)
- **2025** had the most earthquakes with 28.97% growth from 2024
- **August** is the most seismically active month
- **Tsunami earthquakes** are shallower (47km) and stronger (mag 5.48) on average
- **Turkey 2023** and **Myanmar 2025** were the most significant disasters
- **Indonesia, Russia, Japan** are the top 3 most seismically active regions

## Data Source
USGS Earthquake API: https://earthquake.usgs.gov/fdsnws/event/1/query

## Project By
- **Name:** Devipriya
- **Course:** GUVI + HCL Data Science
- **Project:** Global Seismic Trends