# 📘 Project Description
SecureCheck is a real-time traffic stop monitoring and analytics system designed for police checkposts. The system captures vehicle data during stops, analyzes patterns using SQL queries, and displays insights through an interactive Streamlit dashboard. It improves accountability, enables faster decision-making, and highlights key trends such as traffic timing, violation patterns, and demographic breakdowns.

🔍 Description in Detail:
"SecureCheck" is a digital solution to modernize traditional police logbooks. The project starts with data collection from traffic stops—including vehicle number, driver details, reason for stop, and document status.

Then we perform:

🔄 Data Cleaning
Removed duplicates, handled missing entries, and converted columns (like date/time) into usable formats using pandas.

📊 Data Analysis
With cleaned data, we explored:

Most common stop reasons

Time and date patterns

Gender and region-based trends

Repeated offenders and expired documents

🗄️ SQL Querying
The processed data is stored in a PostgreSQL database. Over 15 custom SQL queries were written and categorized:

Aggregations (E.G,total stops per day)

Joins (E.G,vehicle + driver info)

Date-based filters (last 7 days)

String searches (vehicles with “TN” prefix)

🌐 Streamlit Dashboard
A real-time dashboard was built using Streamlit:

Visual charts (bar, line, pie)

KPI boxes ( today’s total stops)

Search/filter options for fast access

Auto-alerts for expired licenses or documents

This makes SecureCheck ideal for police departments needing better visibility, accountability, and real-time insights into on-ground operations.

