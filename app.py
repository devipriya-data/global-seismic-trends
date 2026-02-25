import streamlit as st
import pandas as pd
import sqlite3

# Page configuration
st.set_page_config(
    page_title="Global Seismic Trends",
    page_icon="🌍",
    layout="wide"
)

# Title
st.title("🌍 Global Seismic Trends: Data-Driven Earthquake Insights")
st.markdown("**Analyzing 95,693 earthquakes from 2020 to 2025**")
st.markdown("---")

# Connect to SQLite
conn = sqlite3.connect("earthquakes.db")

st.subheader("📋 All 30 SQL Queries with Results")
st.info("Click any query below to see the SQL code and results!")

queries = {
    "Q1: Top 10 Strongest Earthquakes": "SELECT id, place, mag, time, country FROM earthquakes ORDER BY mag DESC LIMIT 10",
    "Q2: Top 10 Deepest Earthquakes": "SELECT id, place, depth_km, mag, country FROM earthquakes ORDER BY depth_km DESC LIMIT 10",
    "Q3: Shallow High Magnitude Earthquakes": "SELECT id, place, depth_km, mag, country FROM earthquakes WHERE depth_km < 50 AND mag > 7.5 ORDER BY mag DESC",
    "Q4: Average Depth Per Country": "SELECT country, ROUND(AVG(depth_km),2) AS avg_depth, COUNT(*) AS total FROM earthquakes GROUP BY country ORDER BY avg_depth DESC LIMIT 15",
    "Q5: Average Magnitude Per Magnitude Type": "SELECT magType, ROUND(AVG(mag),2) AS avg_magnitude, COUNT(*) AS total FROM earthquakes GROUP BY magType ORDER BY avg_magnitude DESC",
    "Q6: Year With Most Earthquakes": "SELECT year, COUNT(*) AS total_earthquakes FROM earthquakes GROUP BY year ORDER BY total_earthquakes DESC",
    "Q7: Month With Most Earthquakes": "SELECT month, COUNT(*) AS total_earthquakes FROM earthquakes GROUP BY month ORDER BY total_earthquakes DESC",
    "Q8: Day of Week With Most Earthquakes": "SELECT day_of_week, COUNT(*) AS total_earthquakes FROM earthquakes GROUP BY day_of_week ORDER BY total_earthquakes DESC",
    "Q9: Earthquakes Per Hour": "SELECT strftime('%H', time) AS hour_of_day, COUNT(*) AS total FROM earthquakes GROUP BY hour_of_day ORDER BY hour_of_day ASC",
    "Q10: Most Active Reporting Network": "SELECT net, COUNT(*) AS total FROM earthquakes GROUP BY net ORDER BY total DESC",
    "Q11: Top 5 Most Significant Earthquakes": "SELECT place, country, sig, mag, depth_km FROM earthquakes ORDER BY sig DESC LIMIT 5",
    "Q12: Total Significance Per Country": "SELECT country, SUM(sig) AS total_significance, COUNT(*) AS total FROM earthquakes GROUP BY country ORDER BY total_significance DESC LIMIT 10",
    "Q13: Average Significance by Magnitude Category": "SELECT mag_category, ROUND(AVG(sig),2) AS avg_significance, COUNT(*) AS total FROM earthquakes GROUP BY mag_category ORDER BY avg_significance DESC",
    "Q14: Reviewed vs Automatic Earthquakes": "SELECT status, COUNT(*) AS total, ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM earthquakes),2) AS percentage FROM earthquakes GROUP BY status",
    "Q15: Count by Earthquake Type": "SELECT type, COUNT(*) AS total, ROUND(COUNT(*)*100.0/(SELECT COUNT(*) FROM earthquakes),2) AS percentage FROM earthquakes GROUP BY type ORDER BY total DESC",
    "Q16: Earthquakes by Data Type": "SELECT types, COUNT(*) AS total FROM earthquakes GROUP BY types ORDER BY total DESC LIMIT 10",
    "Q17: Average RMS and Gap Per Country": "SELECT country, ROUND(AVG(rms),3) AS avg_rms, ROUND(AVG(gap),2) AS avg_gap, COUNT(*) AS total FROM earthquakes GROUP BY country ORDER BY avg_gap ASC LIMIT 10",
    "Q18: Events With High Station Coverage": "SELECT place, country, nst, mag, depth_km FROM earthquakes WHERE nst > 50 ORDER BY nst DESC LIMIT 10",
    "Q19: Tsunamis Per Year": "SELECT year, SUM(tsunami) AS total_tsunamis, COUNT(*) AS total_earthquakes FROM earthquakes GROUP BY year ORDER BY year ASC",
    "Q20: Earthquakes by Magnitude Category": "SELECT mag_category, COUNT(*) AS total, ROUND(AVG(sig),2) AS avg_significance, SUM(tsunami) AS total_tsunamis FROM earthquakes GROUP BY mag_category ORDER BY total DESC",
    "Q21: Top 5 Countries Highest Average Magnitude": "SELECT country, ROUND(AVG(mag),2) AS avg_magnitude, COUNT(*) AS total, MAX(mag) AS max_magnitude FROM earthquakes WHERE year >= 2015 GROUP BY country HAVING COUNT(*) >= 10 ORDER BY avg_magnitude DESC LIMIT 5",
    "Q22: Countries With Shallow and Deep Earthquakes Same Month": "SELECT country, year, month, COUNT(CASE WHEN depth_category='Shallow' THEN 1 END) AS shallow_count, COUNT(CASE WHEN depth_category='Deep' THEN 1 END) AS deep_count FROM earthquakes GROUP BY country, year, month HAVING shallow_count > 0 AND deep_count > 0 ORDER BY country ASC LIMIT 10",
    "Q23: Year Over Year Growth Rate": "SELECT year, total_eq, LAG(total_eq) OVER (ORDER BY year) AS previous_year, ROUND((total_eq - LAG(total_eq) OVER (ORDER BY year))*100.0/LAG(total_eq) OVER (ORDER BY year),2) AS growth_rate FROM (SELECT year, COUNT(*) AS total_eq FROM earthquakes GROUP BY year) ORDER BY year",
    "Q24: Top 3 Most Seismically Active Regions": "SELECT country, COUNT(*) AS total, ROUND(AVG(mag),2) AS avg_magnitude, ROUND(COUNT(*)*AVG(mag),2) AS activity_score FROM earthquakes GROUP BY country HAVING COUNT(*) >= 100 ORDER BY activity_score DESC LIMIT 3",
    "Q25: Average Depth Near Equator Per Country": "SELECT country, ROUND(AVG(depth_km),2) AS avg_depth, COUNT(*) AS total, ROUND(AVG(mag),2) AS avg_mag FROM earthquakes WHERE latitude BETWEEN -5 AND 5 GROUP BY country ORDER BY avg_depth DESC LIMIT 10",
    "Q26: Countries Highest Ratio Shallow to Deep": "SELECT country, COUNT(CASE WHEN depth_category='Shallow' THEN 1 END) AS shallow, COUNT(CASE WHEN depth_category='Deep' THEN 1 END) AS deep, ROUND(COUNT(CASE WHEN depth_category='Shallow' THEN 1 END)*1.0/NULLIF(COUNT(CASE WHEN depth_category='Deep' THEN 1 END),0),2) AS ratio FROM earthquakes GROUP BY country HAVING deep > 0 ORDER BY ratio DESC LIMIT 10",
    "Q27: Magnitude Difference Tsunami vs No Tsunami": "SELECT CASE WHEN tsunami=1 THEN 'Tsunami' ELSE 'No Tsunami' END AS tsunami_status, COUNT(*) AS total, ROUND(AVG(mag),2) AS avg_magnitude, ROUND(AVG(depth_km),2) AS avg_depth FROM earthquakes GROUP BY tsunami_status",
    "Q28: Events With Lowest Data Reliability": "SELECT place, country, gap, rms, mag, ROUND((gap+rms*100),2) AS reliability_score FROM earthquakes ORDER BY reliability_score DESC LIMIT 10",
    "Q29: Consecutive Earthquakes Within 50km and 1 Hour": "SELECT e1.place AS eq1, e2.place AS eq2, e1.country, ROUND(e1.mag,2) AS mag1, ROUND(e2.mag,2) AS mag2 FROM earthquakes e1 JOIN earthquakes e2 ON e1.id!=e2.id AND e2.time BETWEEN e1.time AND datetime(e1.time, '+1 hour') AND (((e2.latitude-e1.latitude)*(e2.latitude-e1.latitude))+((e2.longitude-e1.longitude)*(e2.longitude-e1.longitude))) < 0.2 LIMIT 10",
    "Q30: Regions With Most Deep Focus Earthquakes": "SELECT country, COUNT(*) AS deep_count, ROUND(AVG(depth_km),2) AS avg_depth, ROUND(AVG(mag),2) AS avg_mag, MAX(depth_km) AS max_depth FROM earthquakes WHERE depth_km > 300 GROUP BY country ORDER BY deep_count DESC LIMIT 10"
}

for query_name, query_sql in queries.items():
    with st.expander(f"🔍 {query_name}"):
        st.code(query_sql, language="sql")
        try:
            result = pd.read_sql(query_sql, conn)
            st.dataframe(result, use_container_width=True)
        except Exception as e:
            st.error(f"Query error: {e}")

conn.close()

# Footer
st.markdown("---")
st.markdown("**Data Source:** USGS Earthquake API | **Project:** Global Seismic Trends | **Built with:** Python, MySQL, Streamlit")