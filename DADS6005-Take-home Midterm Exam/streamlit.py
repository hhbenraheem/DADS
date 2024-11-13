import pandas as pd
import streamlit as st
from pinotdb import connect
import plotly.express as px
from datetime import datetime
import pytz

st.set_page_config(layout="wide")
st.title("Real-Time Page Visit Tracking Dashboard")

# Set timezone to Bangkok (GMT+7)
bangkok_tz = pytz.timezone("Asia/Bangkok")
now = datetime.now(bangkok_tz)
dt_string = now.strftime("%d %B %Y %H:%M:%S")
st.write(f"Last update (GMT+7): {dt_string}")

# Connect to Pinot
conn = connect(host='localhost', port=8099, path='/query/sql', scheme='http')

# Set auto-refresh to 2 seconds
refresh_rate = 2  # seconds

# Auto-refresh the page using JavaScript
refresh_script = f"""
<script>
setTimeout(function() {{
    location.reload();
}}, {refresh_rate * 1000});
</script>
"""
st.markdown(refresh_script, unsafe_allow_html=True)

curs = conn.cursor()

# Visualization 1: Page Visits by Country and Gender
st.subheader("1. Page Visits by Country and Gender")
country_options = st.multiselect("Filter by Country", options=['United States', 'Canada', 'Other'])
gender_options = st.multiselect("Filter by Gender", options=['MALE', 'FEMALE', 'OTHER'])

query1 = """
SELECT COUNTRY, GENDER, COUNT(USERID) as PageViews
FROM Consolidate 
GROUP BY COUNTRY, GENDER
"""
curs.execute(query1)
df_visits_gender = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

if country_options:
    df_visits_gender = df_visits_gender[df_visits_gender['COUNTRY'].isin(country_options)]
if gender_options:
    df_visits_gender = df_visits_gender[df_visits_gender['GENDER'].isin(gender_options)]

fig1 = px.bar(df_visits_gender, x="PageViews", y="COUNTRY", color="GENDER", 
              title="Page Visits by Country and Gender", orientation='h')
fig1.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', xaxis_title="Total Visits", yaxis_title=None)
st.plotly_chart(fig1)

# Visualization 2: Average VIEWTIME per POPULATION by Country
st.subheader("2. Average ViewTime per Capita by Country")
query2 = """
SELECT COUNTRY, SUM(VIEWTIME) as TotalViewTime, SUM(POPULATION) as Population
FROM Consolidate 
GROUP BY COUNTRY
"""
curs.execute(query2)
df_viewtime_population = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
df_viewtime_population['ViewTimePerCapita'] = df_viewtime_population['TotalViewTime'] / df_viewtime_population['Population']

fig2 = px.bar(df_viewtime_population, x="COUNTRY", y="ViewTimePerCapita", 
              title="Average ViewTime per Capita by Country", text="ViewTimePerCapita")
fig2.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig2.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', xaxis_title="Country", yaxis_title="ViewTime per Capita (seconds)")
st.plotly_chart(fig2)

# Visualization 3: Regional Popularity Over Time
st.subheader("3. Regional Popularity Based on Page Views")
query3 = """
SELECT REGIONNAME, SUM(VIEWCOUNT) AS TotalViews
FROM CountryViews_Tumbling
GROUP BY REGIONNAME
"""
curs.execute(query3)
df_region_popularity = pd.DataFrame(curs, columns=[item[0] for item in curs.description])
fig3 = px.pie(df_region_popularity, values="TotalViews", names="REGIONNAME", 
              title="Regional Popularity Based on Page Views")
fig3.update_traces(textposition='inside', textinfo='percent+label')
fig3.update_layout(showlegend=True)
st.plotly_chart(fig3)

# Visualization 4: Average Page Visits per Session by Country
st.subheader("4. Average Page Visits per Session by Country")
query4 = """
SELECT COUNTRY, AVG(PAGEVISITCOUNT) AS AvgPageVisitsPerSession, COUNT(*) AS TotalSessions
FROM Continent_Session_Analysis
GROUP BY COUNTRY
"""
curs.execute(query4)
df_avg_page_visits = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

fig4 = px.bar(df_avg_page_visits, x="COUNTRY", y="AvgPageVisitsPerSession", text="AvgPageVisitsPerSession",
              title="Average Page Visits per Session by Country")
fig4.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig4.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', xaxis_title="Country", yaxis_title="Avg Page Visits per Session")
st.plotly_chart(fig4)

# Visualization 5: Live Page Views by Region and Average Session Length by Country
st.subheader("5. Live Page Views by Region and Average Session Length by Country")

# Query for Total Page Views by Region
query5a = """
SELECT REGIONNAME, SUM(VIEWCOUNT) AS TotalPageViews
FROM CountryViews_Tumbling
GROUP BY REGIONNAME
ORDER BY TotalPageViews DESC
"""
curs.execute(query5a)
df_live_page_views = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

# Query for Average Session Length by Country
query5b = """
SELECT COUNTRY, AVG(SESSIONLENGTHSECONDS) AS AvgSessionLength
FROM Continent_Session_Analysis
GROUP BY COUNTRY
ORDER BY AvgSessionLength DESC
"""
curs.execute(query5b)
df_avg_session_length = pd.DataFrame(curs, columns=[item[0] for item in curs.description])

# Display the two datasets as separate charts to showcase real-time capabilities
col1, col2 = st.columns(2)

with col1:
    fig5a = px.bar(df_live_page_views, x="TotalPageViews", y="REGIONNAME", orientation='h',
                   title="Live Total Page Views by Region")
    fig5a.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', xaxis_title="Total Page Views", yaxis_title="Region")
    st.plotly_chart(fig5a)

with col2:
    fig5b = px.bar(df_avg_session_length, x="COUNTRY", y="AvgSessionLength",
                   title="Average Session Length by Country", text="AvgSessionLength")
    fig5b.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig5b.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', xaxis_title="Country", yaxis_title="Avg Session Length (seconds)")
    st.plotly_chart(fig5b)
