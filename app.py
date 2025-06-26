import streamlit as st
import pandas as pd
import psycopg2
def get_connection():
    return psycopg2.connect(
        host="localhost",         # your DB IP
        database="SecureCheck", # replace with your DB name
        user="postgres",     # replace with your username
        password="Santhosh9626967833", # replace with your password
        port="5432"               # default PostgreSQL port
    )
def  tpo10_vehicle_Number_involved_in_drug(conn):
    query="""
SELECT vehicle_number,COUNT(*) AS drug_related_count
FROM traffic_stop
WHERE drugs_related_stop = TRUE
GROUP BY vehicle_number
ORDER BY drug_related_count DESC LIMIT 10;"""
    return pd.read_sql(query, conn)

def most_frequently_searched(conn):
    query="""
SELECT vehicle_number,  COUNT(*) AS search_count
FROM traffic_stop
WHERE search_conducted = TRUE
GROUP BY vehicle_number
ORDER BY search_count DESC
LIMIT 1;"""
    return pd.read_sql(query, conn)


def  age_group_highest_arrest_rate(conn):
    query="""SELECT  driver_age,COUNT(*) AS total_stops,
SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests,
ROUND(100.0 * SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate_percentage
FROM traffic_stop
GROUP BY driver_age
ORDER BY arrest_rate_percentage DESC
LIMIT 1;"""
    return pd.read_sql(query, conn)

def gender_distribution(conn):
    query="""SELECT country_name,driver_gender,COUNT(*) AS stop_count
FROM traffic_stop
WHERE driver_gender IS NOT NULL AND country_name IS NOT NULL
GROUP BY country_name, driver_gender
ORDER BY country_name, stop_count DESC;"""
    return pd.read_sql(query, conn)

def gender_distribution_of_drivers(conn):
    query="""SELECT country_name,driver_gender,COUNT(*) AS stop_count
FROM traffic_stop
WHERE driver_gender IS NOT NULL AND country_name IS NOT NULL
GROUP BY country_name, driver_gender
ORDER BY country_name, stop_count DESC;"""
    return pd.read_sql(query, conn)

def race_and_gender_combination(conn):
    query="""SELECT driver_race,driver_gender,COUNT(*) AS total_stops,
SUM(CASE WHEN search_conducted = TRUE 
THEN 1 ELSE 0 END) AS total_searches,
ROUND(100.0 * SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS search_rate_percent
FROM traffic_stop
WHERE driver_race IS NOT NULL AND driver_gender IS NOT NULL
GROUP BY driver_race, driver_gender
ORDER BY search_rate_percent DESC
LIMIT 1;"""
    return pd.read_sql(query, conn)

def most_traffic_stops(conn):
    query="""SELECT EXTRACT(HOUR FROM stop_time::time) AS hour,
COUNT(*) AS stop_count
FROM traffic_stop
WHERE stop_time IS NOT NULL
GROUP BY hour
ORDER BY stop_count DESC
LIMIT 1;"""
    return pd.read_sql(query, conn)

def stop_duration_for_different_violations(conn):
    query="""SELECT violation,AVG(CASE 
WHEN stop_duration = '0-15 Min' THEN 7.5
WHEN stop_duration = '16-30 Min' THEN 23
WHEN stop_duration = '30+ Min' THEN 35 ELSE NULL END) 
AS avg_duration_minutes
FROM traffic_stop
WHERE stop_duration IS NOT NULL
GROUP BY violation
ORDER BY avg_duration_minutes DESC;"""
    return pd.read_sql(query, conn)

def  night_more_likely_to_lead_to_arrests(conn):
    query="""SELECT CASE WHEN EXTRACT(HOUR FROM stop_time::time) BETWEEN 5 AND 19 THEN 'Day'ELSE 'Night'END AS time_of_day,
COUNT(*) AS total_stops,
SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrests,
ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 2) 
AS arrest_rate_percent
FROM traffic_stop
WHERE stop_time IS NOT NULL
GROUP BY time_of_day
ORDER BY arrest_rate_percent DESC;"""
    return pd.read_sql(query, conn)

def violations_are_most_associated_searches_or_arrests(conn):
    query="""SELECT violation,COUNT(*) AS total_stops,
AVG(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS search_rate,
AVG(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_rate
FROM traffic_stop
GROUP BY violation
ORDER BY search_rate DESC;"""
    return pd.read_sql(query, conn)

def violations_common_among_younger_drivers_25(conn):
    query="""SELECT violation,COUNT(*) AS count
FROM traffic_stop
WHERE driver_age < 25
GROUP BY violation
ORDER BY count DESC;"""
    return pd.read_sql(query, conn)

def rarely_results_in_search_or_arrest(conn):
    query="""SELECT violation,COUNT(*) AS total_stops,
SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END) AS search_count,
ROUND(SUM(CASE WHEN search_conducted = TRUE THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 2) 
AS search_rate,SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_count,
ROUND(SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100, 2) 
AS arrest_rate
FROM traffic_stop
WHERE violation IS NOT NULL
GROUP BY violation
HAVING COUNT(*) > 100 
ORDER BY search_rate ASC, arrest_rate ASC;"""
    return pd.read_sql(query, conn)

def  highest_rate_of_drug_related_stops(conn):
    query="""SELECT country_name,COUNT(*) AS total_stops,
SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) AS drug_stops,
ROUND(SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END)::NUMERIC / COUNT(*) * 100, 2) 
AS drug_stop_rate
FROM traffic_stop
WHERE country_name IS NOT NULL
GROUP BY country_name
HAVING COUNT(*) > 50
ORDER BY drug_stop_rate DESC
LIMIT 1;"""
    return pd.read_sql(query, conn)

def arrest_rate_by_country_and_violation(conn):
    query="""SELECT violation,COUNT(*) AS total_vilation,
AVG(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS arrest_rate
FROM traffic_stop
GROUP BY violation;"""
    return pd.read_sql(query, conn)

def most_stops_with_search_conducted(conn):
    query="""SELECT country_name,COUNT(*) AS total_stops,
SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) AS drug_stops,
ROUND(1.0 * SUM(CASE WHEN drugs_related_stop = TRUE THEN 1 ELSE 0 END) / COUNT(*), 4) AS drug_rate
FROM traffic_stop
GROUP BY country_name
ORDER BY drug_rate DESC
LIMIT(1);"""
    return pd.read_sql(query, conn)

def Yearly_Breakdow(conn):
    query="""WITH stop_data AS (SELECT country_name,DATE_PART('year', stop_date) AS year,COUNT(*) AS total_stops,
SUM(CASE WHEN is_arrested = TRUE THEN 1 ELSE 0 END) AS total_arrests
FROM traffic_stop
WHERE stop_date IS NOT NULL AND country_name IS NOT NULL
GROUP BY country_name, DATE_PART('year', stop_date) )

SELECT country_name,year,total_stops,total_arrests,
ROUND((total_arrests::decimal / NULLIF(total_stops, 0)) * 100, 2) AS arrest_rate_percent,
SUM(total_stops) OVER (PARTITION BY country_name ORDER BY year ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_stops,
SUM(total_arrests) OVER (PARTITION BY country_name ORDER BY year ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_arrests
FROM stop_data
ORDER BY country_name, year;
"""
    return pd.read_sql(query, conn)

def Driver_Violation_Trends_Based_on_Age_and_Race(conn):
    query="""WITH age_grouped AS (SELECT *,CASE
WHEN driver_age IS NULL THEN 'Unknown'
WHEN driver_age < 18 THEN 'Under 18'
WHEN driver_age BETWEEN 18 AND 25 THEN '18-25'
WHEN driver_age BETWEEN 26 AND 35 THEN '26-35'
WHEN driver_age BETWEEN 36 AND 50 THEN '36-50'
WHEN driver_age > 50 THEN '51+'
ELSE 'Unknown'END AS age_group FROM traffic_stop)

SELECT age_group,driver_race,violation,COUNT(*) AS violation_count,
ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY age_group, driver_race), 2) AS violation_percent
FROM age_grouped
WHERE violation IS NOT NULL
GROUP BY age_group, driver_race, violation
ORDER BY age_group, driver_race, violation_count DESC;"""
    return pd.read_sql(query, conn)

def Time_Period_Analysis_of_Stops(conn):
    query="""WITH stop_time_parts AS (SELECT *,
EXTRACT(YEAR FROM stop_date) AS stop_year,
EXTRACT(MONTH FROM stop_date) AS stop_month,
EXTRACT(HOUR FROM stop_time) AS stop_hour
FROM traffic_stop
WHERE stop_date IS NOT NULL AND stop_time IS NOT NULL)

SELECT stop_year,stop_month,stop_hour,
COUNT(*) AS stop_count
FROM stop_time_parts
GROUP BY stop_year, stop_month, stop_hour
ORDER BY stop_year, stop_month, stop_hour;"""
    return pd.read_sql(query, conn)

def Violations_with_High_Search_and_Arrest_Rates(conn):
    query="""WITH violation_stats AS (SELECT violation,
COUNT(*) AS total_stops,
SUM(CASE WHEN search_conducted = true THEN 1 ELSE 0 END) AS total_searches,
SUM(CASE WHEN is_arrested = true THEN 1 ELSE 0 END) AS total_arrests
FROM traffic_stop
WHERE violation IS NOT NULL
GROUP BY violation),
with_rates AS (SELECT violation,total_stops,total_searches,total_arrests,
ROUND(100.0 * total_searches / NULLIF(total_stops, 0), 2) AS search_rate,
ROUND(100.0 * total_arrests / NULLIF(total_stops, 0), 2) AS arrest_rate
FROM violation_stats)
SELECT *,
RANK() OVER (ORDER BY search_rate DESC) AS search_rank,
RANK() OVER (ORDER BY arrest_rate DESC) AS arrest_rank
FROM with_rates
ORDER BY search_rate DESC, arrest_rate DESC;"""
    return pd.read_sql(query, conn)

def Driver_Demographics_by_Country(conn):
    query="""SELECT country_name,driver_gender,driver_race,
ROUND(AVG(driver_age::numeric), 1) AS avg_age,
COUNT(*) AS total_drivers
FROM traffic_stop
WHERE country_name IS NOT NULL
AND driver_gender IS NOT NULL
AND driver_race IS NOT NULL
AND driver_age IS NOT NULL
GROUP BY country_name, driver_gender, driver_race
ORDER BY country_name, total_drivers DESC;"""
    return pd.read_sql(query, conn)

def Top5_Violations_with_Highest_Arrest_Rates(conn):
    query="""SELECT violation,COUNT(*) AS total_stops,
SUM(CASE WHEN is_arrested = true THEN 1 ELSE 0 END) AS total_arrests,
ROUND(100.0 * SUM(CASE WHEN is_arrested = true THEN 1 ELSE 0 END) / COUNT(*), 2) AS arrest_rate
FROM traffic_stop
WHERE violation IS NOT NULL
GROUP BY violation
ORDER BY arrest_rate DESC
LIMIT 5;"""
    return pd.read_sql(query, conn)

general_queries = {
    "tpo10_drug_vehicle":tpo10_vehicle_Number_involved_in_drug,
            "most_search":most_frequently_searched,
            "age_group":age_group_highest_arrest_rate,
            "gender_vlue":gender_distribution,
            "gender_distribution":gender_distribution_of_drivers

}
Time_Duration_Based_queries = {
    "gender_race":race_and_gender_combination,
           "most_stops":most_traffic_stops,
           "stop_duration":stop_duration_for_different_violations,
           "lead_to_arrest":night_more_likely_to_lead_to_arrests,
           "searches_or_arrest":violations_are_most_associated_searches_or_arrests,
          

}
Violation_Based_queries = {
           "younger_driver_violatin":violations_common_among_younger_drivers_25,
           "rarely_arrest":rarely_results_in_search_or_arrest,
           "drug_stops":highest_rate_of_drug_related_stops,
           "rate_by_country":arrest_rate_by_country_and_violation,
           "search_conduct":most_stops_with_search_conducted,
}
queries_ = {
          "breakdown":Yearly_Breakdow,
          "driver_violation":Driver_Violation_Trends_Based_on_Age_and_Race,
          "time_period":Time_Period_Analysis_of_Stops,
          "high_arrest":Violations_with_High_Search_and_Arrest_Rates,
          "demographics_country":Driver_Demographics_by_Country,
          "top5_violation":Top5_Violations_with_Highest_Arrest_Rates,

}

st.title("👮 SecureCheck")

query_type = st.radio("Choose Query Category", [
    "👮 General Queries", 
    "📍 Location-Based Queries", 
    "⏰ Time-Based Queries", 
    "📊 queries"
])


if query_type == "👮 General Queries":
    selected_query = st.selectbox("Select a General Query", list(general_queries.keys()))
    selected_func =general_queries[selected_query]


elif query_type == "📍 Location-Based Queries":
    selected_query = st.selectbox("Select a Location-Based Query", list(Time_Duration_Based_queries.keys()))
    selected_func = Time_Duration_Based_queries[selected_query] 


elif query_type == "⏰ Time-Based Queries":
    selected_query = st.selectbox("Select a Location-Based Query", list(Violation_Based_queries.keys()))
    selected_func = Violation_Based_queries[selected_query]   


elif query_type == "📊 queries":
    selected_query = st.selectbox("Select a Location-Based Query", list(queries_.keys()))
    selected_func = queries_[selected_query]   


if st.button("Run Query"):
    with st.spinner("Running..."):
        conn = get_connection()
        df = selected_func(conn)
        conn.close()
        st.success("Done ✅")
        st.dataframe(df)    



conn = get_connection()
traffic_df = pd.read_sql("SELECT * FROM traffic_stop;", conn)
conn.close()

st.header("🔍 Get Stop Summary by Vehicle Number")

vehicle_input = st.text_input("Enter Vehicle Number")

if vehicle_input:
    person_df = traffic_df[traffic_df['vehicle_number'] == vehicle_input]

    if not person_df.empty:
        row = person_df.iloc[0]

        age = row['driver_age']
        gender = row['driver_gender']
        violation = row['violation']
        time = row['stop_time_p']
        search = row['search_conducted']
        outcome = row['stop_outcome']
        duration = row['stop_duration']
        drug = row['drugs_related_stop']

        summary = f"""🚗 A {age}-year-old {gender} driver was stopped for **{violation}** at **{time}**. \
{"A search was conducted" if search else "No search was conducted"}, and they received a **{outcome}**. \
The stop lasted **{duration} minutes** and {"was" if drug else "was not"} drug-related."""
        
        st.markdown(summary)
    else:
        st.error("❌ No record found for this vehicle number.")







































































































































