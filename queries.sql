USE earthquake_db;

SELECT id, place, mag, time, country
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;

SELECT id, place, depth_km, mag, country
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;

SELECT id, place, depth_km, mag, country, time
FROM earthquakes
WHERE depth_km < 50 
AND mag > 7.5
ORDER BY mag DESC;

SELECT country, 
       ROUND(AVG(depth_km), 2) AS avg_depth,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY country
ORDER BY avg_depth DESC
LIMIT 15;

SELECT magType,
       ROUND(AVG(mag), 2) AS avg_magnitude,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY magType
ORDER BY avg_magnitude DESC;

SELECT year,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY year
ORDER BY total_earthquakes DESC;

SELECT month,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY month
ORDER BY total_earthquakes DESC;

SELECT day_of_week,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY day_of_week
ORDER BY total_earthquakes DESC;

SELECT HOUR(time) AS hour_of_day,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY hour_of_day
ORDER BY hour_of_day ASC;

SELECT net,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY net
ORDER BY total_earthquakes DESC;

-- Query 11: Top 5 Places With Highest Significance Score
-- Note: Dataset does not have casualties column, using sig score as impact measure
SELECT place,
       country,
       sig,
       mag,
       depth_km
FROM earthquakes
ORDER BY sig DESC
LIMIT 5;

-- Query 12: Total Significance Score Per Country
-- Note: Using sig score as proxy for economic impact since dataset has no economic loss column
SELECT country,
       SUM(sig) AS total_significance,
       COUNT(*) AS total_earthquakes,
       ROUND(AVG(mag), 2) AS avg_magnitude
FROM earthquakes
GROUP BY country
ORDER BY total_significance DESC
LIMIT 10;

-- Query 13: Average Significance by Magnitude Category
-- Note: Using mag_category as proxy for alert level since dataset has no alert column
SELECT mag_category,
       ROUND(AVG(sig), 2) AS avg_significance,
       COUNT(*) AS total_earthquakes,
       ROUND(AVG(mag), 2) AS avg_magnitude
FROM earthquakes
GROUP BY mag_category
ORDER BY avg_significance DESC;

-- Query 14: Count of Reviewed vs Automatic Earthquakes
SELECT status,
       COUNT(*) AS total_earthquakes,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM earthquakes), 2) AS percentage
FROM earthquakes
GROUP BY status
ORDER BY total_earthquakes DESC;

-- Query 15: Count by Earthquake Type
SELECT type,
       COUNT(*) AS total_earthquakes,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM earthquakes), 2) AS percentage
FROM earthquakes
GROUP BY type
ORDER BY total_earthquakes DESC;

-- Query 16: Number of Earthquakes by Data Type
SELECT types,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY types
ORDER BY total_earthquakes DESC
LIMIT 10;

-- Query 17: Average RMS and Gap Per Country
SELECT country,
       ROUND(AVG(rms), 3) AS avg_rms,
       ROUND(AVG(gap), 2) AS avg_gap,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY country
ORDER BY avg_gap ASC
LIMIT 10;

-- Query 18: Events With High Station Coverage (nst > 50)
SELECT place,
       country,
       nst,
       mag,
       depth_km
FROM earthquakes
WHERE nst > 50
ORDER BY nst DESC
LIMIT 10;

-- Query 19: Number of Tsunamis Triggered Per Year
SELECT year,
       SUM(tsunami) AS total_tsunamis,
       COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY year
ORDER BY year ASC;

-- Query 20: Count Earthquakes by Magnitude Category as Alert Level
-- Note: Dataset has no alert column, using mag_category as alert level proxy
SELECT mag_category AS alert_level,
       COUNT(*) AS total_earthquakes,
       ROUND(AVG(sig), 2) AS avg_significance,
       SUM(tsunami) AS total_tsunamis
FROM earthquakes
GROUP BY mag_category
ORDER BY total_earthquakes DESC;

-- Query 21: Top 5 Countries With Highest Average Magnitude in Past 10 Years
SELECT country,
       ROUND(AVG(mag), 2) AS avg_magnitude,
       COUNT(*) AS total_earthquakes,
       MAX(mag) AS max_magnitude
FROM earthquakes
WHERE year >= 2015
GROUP BY country
HAVING COUNT(*) >= 10
ORDER BY avg_magnitude DESC
LIMIT 5;

-- Query 22: Countries That Have Experienced Both Shallow and Deep Earthquakes Within Same Month
SELECT country,
       year,
       month,
       COUNT(CASE WHEN depth_category = 'Shallow' THEN 1 END) AS shallow_count,
       COUNT(CASE WHEN depth_category = 'Deep' THEN 1 END) AS deep_count
FROM earthquakes
GROUP BY country, year, month
HAVING shallow_count > 0 AND deep_count > 0
ORDER BY country ASC
LIMIT 10;

-- Query 23: Year Over Year Growth Rate in Total Earthquakes Globally
SELECT year,
       total_earthquakes,
       LAG(total_earthquakes) OVER (ORDER BY year) AS previous_year,
       ROUND((total_earthquakes - LAG(total_earthquakes) OVER (ORDER BY year)) * 100.0 / 
       LAG(total_earthquakes) OVER (ORDER BY year), 2) AS growth_rate_percent
FROM (
    SELECT year, COUNT(*) AS total_earthquakes
    FROM earthquakes
    GROUP BY year
) yearly_counts
ORDER BY year;

-- Query 24: Top 3 Most Seismically Active Regions by Frequency and Average Magnitude
SELECT country,
       COUNT(*) AS total_earthquakes,
       ROUND(AVG(mag), 2) AS avg_magnitude,
       ROUND((COUNT(*) * AVG(mag)), 2) AS activity_score
FROM earthquakes
GROUP BY country
HAVING COUNT(*) >= 100
ORDER BY activity_score DESC
LIMIT 3;

-- Query 25: Average Depth of Earthquakes Within 5 Degrees of Equator Per Country
SELECT country,
       ROUND(AVG(depth_km), 2) AS avg_depth,
       COUNT(*) AS total_earthquakes,
       ROUND(AVG(mag), 2) AS avg_magnitude
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country
ORDER BY avg_depth DESC
LIMIT 10;

-- Query 26: Countries With Highest Ratio of Shallow to Deep Earthquakes
SELECT country,
       COUNT(CASE WHEN depth_category = 'Shallow' THEN 1 END) AS shallow_count,
       COUNT(CASE WHEN depth_category = 'Deep' THEN 1 END) AS deep_count,
       ROUND(COUNT(CASE WHEN depth_category = 'Shallow' THEN 1 END) * 1.0 / 
       NULLIF(COUNT(CASE WHEN depth_category = 'Deep' THEN 1 END), 0), 2) AS shallow_to_deep_ratio
FROM earthquakes
GROUP BY country
HAVING deep_count > 0
ORDER BY shallow_to_deep_ratio DESC
LIMIT 10;

-- Query 27: Average Magnitude Difference Between Earthquakes With and Without Tsunami
SELECT 
    CASE WHEN tsunami = 1 THEN 'Tsunami' ELSE 'No Tsunami' END AS tsunami_status,
    COUNT(*) AS total_earthquakes,
    ROUND(AVG(mag), 2) AS avg_magnitude,
    ROUND(AVG(depth_km), 2) AS avg_depth
FROM earthquakes
GROUP BY tsunami_status;

-- Query 28: Events With Lowest Data Reliability Using Gap and RMS
SELECT place,
       country,
       gap,
       rms,
       mag,
       ROUND((gap + rms * 100), 2) AS reliability_score
FROM earthquakes
ORDER BY reliability_score DESC
LIMIT 10;

-- Query 29: Pairs of Consecutive Earthquakes Within 50km and 1 Hour
SELECT 
    e1.place AS earthquake_1,
    e2.place AS earthquake_2,
    e1.country AS country,
    ROUND(e1.mag, 2) AS mag_1,
    ROUND(e2.mag, 2) AS mag_2,
    TIMESTAMPDIFF(MINUTE, e1.time, e2.time) AS minutes_apart,
    ROUND(111.195 * SQRT(POW(e2.latitude - e1.latitude, 2) + 
    POW((e2.longitude - e1.longitude) * COS(RADIANS(e1.latitude)), 2)), 2) AS distance_km
FROM earthquakes e1
JOIN earthquakes e2 
    ON e1.id != e2.id
    AND e2.time BETWEEN e1.time AND DATE_ADD(e1.time, INTERVAL 1 HOUR)
    AND ROUND(111.195 * SQRT(POW(e2.latitude - e1.latitude, 2) + 
    POW((e2.longitude - e1.longitude) * COS(RADIANS(e1.latitude)), 2)), 2) <= 50
LIMIT 10;

-- Query 30: Regions With Highest Frequency of Deep Focus Earthquakes (depth > 300km)
SELECT country,
       COUNT(*) AS deep_earthquake_count,
       ROUND(AVG(depth_km), 2) AS avg_depth,
       ROUND(AVG(mag), 2) AS avg_magnitude,
       MAX(depth_km) AS max_depth
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_earthquake_count DESC
LIMIT 10;