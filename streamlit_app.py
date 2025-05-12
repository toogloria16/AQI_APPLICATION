import streamlit as st
st.title("WELCOME TO THE AQI APP!")

import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")

st.title("Air Quality Index (AQI) and Pollutants EDA Dashboard")

# Load data
def load_data():
    df = pd.read_csv("combined_stations_with_AQI.csv")
    return df

# Load and preprocess data
df = load_data()
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
st.sidebar.header("Filter Options")
stations = df['station'].unique()
pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3']

selected_station = st.sidebar.selectbox("Select Station", stations)
selected_pollutant = st.sidebar.selectbox("Select Pollutant", pollutants)
date_range = st.sidebar.date_input("Select Date Range", [df['date'].min(), df['date'].max()])

# Apply filters
mask = (
    (df['station'] == selected_station) &
    (df['date'] >= pd.to_datetime(date_range[0])) &
    (df['date'] <= pd.to_datetime(date_range[1]))
)
df_filtered = df.loc[mask]

st.subheader(f"Trend of {selected_pollutant} at {selected_station}")
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=df_filtered, x='date', y=selected_pollutant, ax=ax)
ax.set_ylabel(f"{selected_pollutant} Concentration")
ax.set_xlabel("Date")
ax.set_title(f"{selected_pollutant} Over Time")
st.pyplot(fig)

# Show summary stats
st.subheader("Summary Statistics")
st.write(df_filtered[[selected_pollutant]].describe())

# Optional: Display AQI if available
if 'AQI' in df_filtered.columns:
    st.subheader("AQI Distribution")
    fig2, ax2 = plt.subplots()
    sns.histplot(df_filtered['AQI'], bins=20, kde=True, ax=ax2)
    ax2.set_title("AQI Distribution")
    st.pyplot(fig2)

st.markdown("---")
st.write("Data Source: Combined Air Quality Station Measurements")

